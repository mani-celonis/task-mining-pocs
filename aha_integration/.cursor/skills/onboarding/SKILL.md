---
name: onboarding
description: Guided first-time setup for Celonis PMs using AhaAgent — Python venv, .env credentials, optional Jira, meeting-notes and Aha! Ideas workflow, and domain safety. Use when the user says onboard, first-time setup, configure AhaAgent, new PM setup, get started with the harness, or similar.
---

# PM onboarding (AhaAgent harness)

Walk the user through **credentials and workspace configuration** in order. **Never ask for `AHA_API_KEY`, `JIRA_API_TOKEN`, or any secret in chat** — point them to edit `.env` locally.

Canonical business rules for payloads stay in [docs/celonis_aha_rules.md](../../../docs/celonis_aha_rules.md) (link only; do not paste long excerpts here).

---

## Step 0: Resolve paths

Use two roots:

| Variable | Meaning |
|----------|---------|
| **AHA_ROOT** | Directory that contains `src/api/client.py` (this repository clone). |
| **WORKSPACE_ROOT** | Cursor workspace root where `.aha-config.yml` and (for nested installs) `.cursor/` live. |
| **KNOWLEDGE_ROOT** | **Recommended:** absolute path in `AHA_ROOT/.env` to the vault root. PM content lives in **`$KNOWLEDGE_ROOT/AhaAgent/...`**, `Tasks/`, and `GOALS.md`. Not the old `Knowledge/` tree. Configure via [external-knowledge](../external-knowledge/SKILL.md). |

**Detect AHA_ROOT**

1. If `./src/api/client.py` exists from the current workspace root → `AHA_ROOT` = workspace root.
2. Else if `./tools/aha-agent/src/api/client.py` exists → `AHA_ROOT` = `./tools/aha-agent`.
3. Else ask: *Where did you clone AhaAgent?* and verify `src/api/client.py` exists there.

**Detect WORKSPACE_ROOT**

- If the user opened **only** the AhaAgent repo → `WORKSPACE_ROOT` = `AHA_ROOT`.
- If AhaAgent lives under `tools/aha-agent/` → `WORKSPACE_ROOT` is typically the **parent** folder (contains `tools/`, and will contain `.aha-config.yml`). Confirm with the user if unsure.

All `.env` and Python commands use **AHA_ROOT**. Glossary, meetings, and intake (under **`$KNOWLEDGE_ROOT/AhaAgent/`**) are **not** in the git tree; `.aha-config.yml` and optional `.cursor/` copies use **WORKSPACE_ROOT** unless it is the same as `AHA_ROOT`.

---

## Phase A — Python environment and Aha! API

1. **Dependencies** — From `AHA_ROOT`, with a venv activated:
   - Prefer venv names: `aha-agent-venv`, `ahaAgent`, `.venv`, `venv` (per [AGENTS.md](../../../AGENTS.md)).
   - `pip install -r requirements.txt`

2. **`.env`** — Path: `AHA_ROOT/.env`
   - If missing: instruct `cp .env.example .env` (from `AHA_ROOT`) and edit **locally** to set `AHA_API_KEY=...`.
   - Token: Aha! → Settings → Personal → Developer → API key.

3. **Sanity check** — After the user confirms `.env` is saved, run from `AHA_ROOT`:
   ```bash
   python scripts/check_env.py
   ```
   Optionally: `python src/executors/test_api.py` if they want a live API check (requires approval per session rules).

Wait for confirmation before moving on.

---

## Phase B — Optional: Jira (board overview, PM brief)

Ask whether they need **Jira board snapshot** or **Jira PM brief** skills.

If yes:

1. In **`AHA_ROOT/.env`**, they need (see [.env.example](../../../.env.example) and [docs/jira_api_notes.md](../../../docs/jira_api_notes.md)):
   - `JIRA_HOST` (e.g. `https://celonis.atlassian.net`)
   - `JIRA_EMAIL`
   - `JIRA_API_TOKEN` (Atlassian account API token; create in Atlassian profile security)
   - `JIRA_BOARD_ID`

2. Do **not** paste tokens in chat.

3. After values are set, run `python scripts/check_env.py` again from `AHA_ROOT`, then optionally:
   ```bash
   python src/executors/jira_board_overview.py
   ```
   (with user approval if required).

If no: skip; they can add Jira later.

---

## Phase C0 — External knowledge (Obsidian / vault)

Run [external-knowledge](../external-knowledge/SKILL.md) and set `KNOWLEDGE_ROOT` in `AHA_ROOT/.env` to the vault root. Most PM files go under **`$KNOWLEDGE_ROOT/AhaAgent/`** (glossary, Products, Meetings, jira-briefs, intake); dated feature-suggestion exports go to **`$KNOWLEDGE_ROOT/incoming/feature-suggestions/`**; plus **`$KNOWLEDGE_ROOT/Tasks/`** and **`$KNOWLEDGE_ROOT/GOALS.md`**. See [docs/knowledge_layout.md](../../../docs/knowledge_layout.md) and [docs/knowledge_multiroot.md](../../../docs/knowledge_multiroot.md). Confirm with `python scripts/check_env.py` and `python scripts/knowledge_gap_check.py`.

---

## Phase C — Optional: Meeting notes → Aha! Ideas workflow

Offer this only if they want meeting transcripts cross-referenced with Ideas.

**Prerequisites:** Phase A complete (`AHA_ROOT`, venv, `AHA_API_KEY`).

**Config file:** `WORKSPACE_ROOT/.aha-config.yml` — schema in [.aha-config.example.yml](../../../.aha-config.example.yml).

**Scenarios** (mirror [workflows/meeting-ideas-crossref/skill-setup-wizard.md](../../../workflows/meeting-ideas-crossref/skill-setup-wizard.md)):

- **A — Fresh:** No `.aha-config.yml` (and no legacy baked-in rule-only setup) → collect product key, team, products, categories; write YAML.
- **B — Legacy migration:** `.cursor/rules/aha-agent.mdc` with baked-in `**Product key:**` etc., no `.aha-config.yml` → extract values per wizard, confirm, then write `.aha-config.yml`.
- **C — Update:** `.aha-config.yml` exists → offer regenerate templates vs reconfigure.

**Collect configuration** (conversational, free text):

1. Aha! **product key** (from URL `https://celonis.aha.io/products/<KEY>/...`).
2. **Team** custom field value for filtering, or empty.
3. **Products** (name + short description) and **Idea category** mapping (or “same as products”).

**Generate files** (after user confirms summary):

- Copy templates from **`AHA_ROOT/workflows/meeting-ideas-crossref/`** (paths below are source → destination under `WORKSPACE_ROOT`):

| Source | Destination |
|--------|-------------|
| `cursor-rule-product-tagging.mdc` | `.cursor/rules/product-tagging.mdc` |
| `skill-meeting-notes.md` | `.cursor/skills/meeting-notes/SKILL.md` |

**`aha-agent.mdc` rule**

- If **`WORKSPACE_ROOT` == `AHA_ROOT`**: **Do not** overwrite the repo’s `.cursor/rules/aha-agent.mdc` with `cursor-rule-aha-agent.mdc` (the workflow template hardcodes `tools/aha-agent/` for nested workspaces). The committed rule already matches repo-root layout.
- If **nested** (`AHA_ROOT` is `.../tools/aha-agent`): copy `cursor-rule-aha-agent.mdc` → `WORKSPACE_ROOT/.cursor/rules/aha-agent.mdc` so paths match.

**Directories** (idempotent) under the vault (with `KNOWLEDGE_ROOT` set):

```bash
ROOT="$KNOWLEDGE_ROOT"
mkdir -p "$ROOT"/AhaAgent/Meetings/Transcripts "$ROOT"/AhaAgent/Products \
  "$ROOT"/AhaAgent/jira-briefs "$ROOT"/AhaAgent/intake \
  "$ROOT"/incoming/feature-suggestions \
  "$ROOT"/Tasks
touch "$ROOT"/GOALS.md  # if missing
```

If `KNOWLEDGE_ROOT` is **unset** (not recommended for PM use), the repo can still use `data/` for intake and Jira briefs via `src/pm_data_paths.py`.

**Glossary and hubs:** Create `AhaAgent/product-glossary.md` and `AhaAgent/Products/<product>.md` per wizard (see skill-setup-wizard Phase 4–5) under the vault; on update, only add missing hub pages.

**Validate Ideas API** — Scratchpad under `AHA_ROOT` with `load_dotenv()` from `AHA_ROOT/.env`, read **`WORKSPACE_ROOT/.aha-config.yml`** for `product_key`, then `GET /products/{product_key}/ideas` with `per_page=1` and report pagination total. Fix product key or auth if it fails.

**Deeper reference:** [workflows/meeting-ideas-crossref/README.md](../../../workflows/meeting-ideas-crossref/README.md)

---

## Phase D — Domain safety (before bulk Aha! changes)

Tell the user:

- Celonis **naming is inverted** vs Aha! API: “features” (GTM) → `/epics`; internal “epics” → `/features`. See [AGENTS.md](../../../AGENTS.md) and [docs/celonis_aha_rules.md](../../../docs/celonis_aha_rules.md).
- Bulk **PUT/DELETE** always needs a written plan, name→reference resolution, and **explicit approval** before execution.

Optional: one check question, e.g. *If a task says “update the Celonis feature X”, which API collection do you use?* (Answer: epics.)

---

## Completion checklist

Summarize what is ready:

| Capability | Ready when |
|------------|------------|
| Aha! API scripts / bulk update | venv, `AHA_ROOT/.env` with `AHA_API_KEY`, `check_env.py` OK |
| Jira board / PM brief | All `JIRA_*` set in `.env`, `jira_board_overview` runs |
| Meeting → Ideas | `.aha-config.yml`, templates copied, glossary/hubs, Ideas validation OK |
| Suggestion review | `user_email` and `suggestion_portal` set in `.aha-config.yml` |

**Example next prompts**

- *Run the task list* → [aha-bulk-update](../aha-bulk-update/SKILL.md)
- *Log a meeting* → [meeting-notes](../meeting-notes/SKILL.md)
- *Jira PM brief* → [jira-pm-brief](../jira-pm-brief/SKILL.md)
- *Review suggestions* → [aha-feature-suggestions-review](../aha-feature-suggestions-review/SKILL.md)

---

## Related

- [README.md](../../../README.md) — clone, venv, Quick Start
- [workflows/meeting-ideas-crossref/skill-setup-wizard.md](../../../workflows/meeting-ideas-crossref/skill-setup-wizard.md) — meeting-only wizard (still valid; onboarding supersedes for full harness setup)
- Dedicated meeting trigger phrases can still run that wizard for template refresh: “update my meeting workflow”
