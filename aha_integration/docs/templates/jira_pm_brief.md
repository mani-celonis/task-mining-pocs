# Jira PM brief — template

**Instructions:** Copy structure when writing a filled brief. Replace angle-bracket placeholders. **Filled briefs** go under **`$KNOWLEDGE_ROOT/AhaAgent/jira-briefs/`** when `KNOWLEDGE_ROOT` is set, else `data/jira-briefs/` (gitignored from the repo—do not commit).

**Two modes:**

| Mode | How | Themes section |
|------|-----|----------------|
| **Executive** | Agent-written summary from aggregates | 5–10 themes; do not list every ticket—use “+N related issues” |
| **Detailed** | Run `jira_pm_brief_generate.py` on `jira_board_overview.py --json --extra-fields` | Every issue listed in tables under component or epic themes; see below |

---

## Context

| Field | Value |
|-------|-------|
| Date | `<YYYY-MM-DD>` |
| Jira board ID | `<from JIRA_BOARD_ID>` *(or “JQL” if search-only)* |
| Engineering team / board name | `<user-supplied>` |
| PM product focus | `<what the PM cares about mapping to>` |
| Data source | `jira_board_overview.py` (+ optional `jira_pm_brief_generate.py`) |

---

## Executive summary

*(5–8 bullets: user/customer-facing outcomes; reference theme names from next section.)*

- …
- …

---

## Themes (categorized work)

### Executive style (aggregated)

*(Target roughly 5–10 themes. Do not list every ticket—use “+N related issues” where needed.)*

### Theme 1: `<short name>`

- **User-facing outcome:** *(1–2 sentences; label **Explicit in tickets** vs **Inferred — confirm with eng**.)*
- **Evidence:** `<KEY-1, KEY-2, …>` (+N related issues if applicable)
- **Status snapshot:** e.g. mostly In Progress / Done / Backlog

### Theme 2: `<short name>`

- **User-facing outcome:** …
- **Evidence:** …
- **Status snapshot:** …

*(Add themes as needed.)*

### Detailed style (machine-generated baseline)

Use when you need **full traceability** across all issues in scope:

1. `python src/executors/jira_board_overview.py --json --extra-fields > data/jira-briefs/_snap.json`
2. `python src/executors/jira_pm_brief_generate.py --input data/jira-briefs/_snap.json --output data/jira-briefs/YYYY-MM-DD_<slug>.md`

**Structure produced:**

- **Theme:** primary **component** (or **epic** if `--group-by epic`).
- **Narrative:** recurring words + title-prefix hints from all summaries in that theme.
- **Epic quick list** when the theme is large (≥40 issues by default).
- **Per epic:** `#### Epic TM-xxx — title` then a **Markdown table** with every issue: Key, Summary, Status, Priority, Sprint, Assignee, Description snippet (ADF flattened, truncated).

Optional flags: `--redact-assignees`, `--max-desc-chars`, `--max-issues-per-theme` (overflow → Appendix).

The agent may **edit** the generated file for user-facing tone but should **not drop issue rows** without explicit PM approval.

---

## Map to Celonis product context

*(Theme → product area; state **Confidence: high | medium | low** for inferred rows. Do not invent Aha! or roadmap links—only if PM supplied or IDs referenced in session.)*

| Theme | Product area / capability | Confidence | Related roadmap / Aha! *(optional)* |
|-------|---------------------------|------------|-------------------------------------|
| … | … | … | … |

---

## Priority view

*(Tier or rank; cite Jira signals: priority field, status, labels. Use **Unclear / needs triage** bucket when data is weak.)*

| Tier | Themes / work | Rationale (from Jira) |
|------|---------------|------------------------|
| P0 / High | … | … |
| P1 / Med | … | … |
| Unclear / needs triage | … | … |

---

## Risks

### Value risks

*(Wrong bet, weak customer outcome, unclear value—only if supported by summaries/labels/status or PM context.)*

| Description | Signal *(tickets / fields)* | Severity (H/M/L) | Suggested PM action |
|-------------|------------------------------|------------------|---------------------|
| … | … | … | … |

*If none: **None visible in Jira data.***

### Delivery risks

*(Blocked, dependencies, drag, long-running In Progress, churn—evidence-based only.)*

| Description | Signal *(tickets / fields)* | Severity (H/M/L) | Suggested PM action |
|-------------|------------------------------|------------------|---------------------|
| … | … | … | … |

*If none: **None visible in Jira data.***

---

## Open questions

*(Crisp list for eng lead / GPM.)*

1. …
2. …
