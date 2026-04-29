# Jira Cloud API notes (AhaAgent)

Read-only integration for PM visibility. Secrets live in `.env` only; never commit tokens.

## Auth

- **Jira Cloud:** HTTP Basic with **Atlassian account email** + **API token** ([create token](https://id.atlassian.com/manage-profile/security/api-tokens)).
- Env vars: `JIRA_HOST`, `JIRA_EMAIL`, `JIRA_API_TOKEN`.

## How issues are fetched (PM default vs full board)

| Mode | Env | API | Typical size |
|------|-----|-----|----------------|
| **JQL search (recommended)** | `JIRA_JQL` or `JIRA_JQL_PATH` | `GET /rest/api/3/search/jql` (token pagination; legacy `GET /search` returns **410**) | Hundreds of issues when scoped (e.g. TM + not Done + sprint/backlog + component) |
| **Board fallback** | `JIRA_BOARD_ID` (only if no JQL) | `GET /rest/agile/1.0/board/{id}/issue` | Often thousands including Done history |

**Precedence:** `JIRA_JQL` → `JIRA_JQL_PATH` (file must exist and be non-empty) → `JIRA_BOARD_ID`.

**Frederik / ML Infra default** (in `.env.example`): TM project, exclude Epic and Sub-task, `statusCategory != Done`, open sprint **or** empty sprint (backlog), **`component = "ML Infra"`**, `ORDER BY Rank ASC`. That matches a realistic “what the team is working on now + ranked backlog” slice instead of the whole board.

**`.env` tip:** JQL contains `=` — put the whole query in **single quotes** (see `.env.example`) or use **`JIRA_JQL_PATH`** pointing to a `.jql` file under `data/jira-jql/` (gitignored).

## Endpoints used

| Purpose | Method | Path |
|--------|--------|------|
| Site field metadata (Epic Link id) | GET | `/rest/api/3/field` |
| Issues matching JQL | GET | `/rest/api/3/search/jql` |
| Issues on a board | GET | `/rest/agile/1.0/board/{boardId}/issue` |

JQL search: paginate with `nextPageToken` + `maxResults` (max 100 per page). Board fetch still uses `startAt`.

## Epic grouping

- **Company-managed** projects usually expose **Epic Link**; we resolve its `customfield_*` id from `/field` by name. Jira may return Epic Link as a **string** key or object — both are handled.
- Issues with issuetype **Epic** in the result set are listed as epics; others are grouped under Epic Link / parent Epic.
- JQL that **excludes Epic** (like the ML Infra default) still groups children by Epic Link to parent epics not in the result.

## Rate limits

Jira Cloud may return **429**. [`JiraApiClient`](../src/api/jira_client.py) retries using `Retry-After`, similar to `AhaApiClient`.

## Script

```bash
python src/executors/jira_board_overview.py              # Markdown
python src/executors/jira_board_overview.py --json       # JSON
python src/executors/jira_board_overview.py --json --extra-fields   # + description (ADF) + sprint (larger)
python src/executors/jira_board_overview.py --jql 'project = TM AND ...'   # one-off override
```

### Extra fields (`--extra-fields` / `JIRA_EXTRA_FIELDS`)

When enabled, the issue `fields` list also requests **`description`** and **`sprint`**.

- **Description** on Jira Cloud is **Atlassian Document Format (ADF)** JSON, not plain text. [`adf_to_plain_text`](../src/api/jira_adf.py) flattens it for briefs; snippets are **truncated** per issue (default 400 chars in the generator; configurable via `jira_pm_brief_generate.py --max-desc-chars`).
- **Sprint** helps split “in sprint” vs backlog within a theme.

Tradeoff: **larger responses and slower fetches** — use only when generating a detailed brief.

## PM brief workflow

**Two-step pipeline (detailed themes):**

1. `jira_board_overview.py --json --extra-fields` → save snapshot JSON (stderr to `/dev/null` if redirecting stdout to a file).
2. `jira_pm_brief_generate.py --input <snap.json> --output data/jira-briefs/...` → Markdown with every issue under component- or epic-grouped themes.

For an **executive** (aggregated) brief, skip step 2 and follow the skill’s Option B.

Use [.cursor/skills/jira-pm-brief/SKILL.md](../.cursor/skills/jira-pm-brief/SKILL.md) with **`JIRA_JQL`** set so the brief reflects the scoped set. Filled briefs: **`data/jira-briefs/`** (gitignored). Template: [docs/templates/jira_pm_brief.md](templates/jira_pm_brief.md).
