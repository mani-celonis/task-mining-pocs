---
name: onboarding
description: Guided first-time setup for Celonis PMs using AhaAgent — Python venv, .env credentials, optional Jira, meeting-notes and Aha! Ideas workflow, and domain safety. Use when the user says onboard, first-time setup, configure AhaAgent, new PM setup, get started with the harness, or similar.
allowed-tools: Bash Read Write Glob
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
| **WORKSPACE_ROOT** | Workspace root where `.aha-config.yml` lives. |
| **KNOWLEDGE_ROOT** | **Recommended:** absolute path in `AHA_ROOT/.env` to the vault root. PM content in **`$KNOWLEDGE_ROOT/AhaAgent/...`**, `Tasks/`, `GOALS.md`. Configure via [.cursor/skills/external-knowledge/SKILL.md](../../../.cursor/skills/external-knowledge/SKILL.md). |

**Detect AHA_ROOT**

1. If `./src/api/client.py` exists → `AHA_ROOT` = current dir.
2. Else if `./tools/aha-agent/src/api/client.py` exists → `AHA_ROOT` = `./tools/aha-agent`.
3. Else ask: *Where did you clone AhaAgent?*

**Detect WORKSPACE_ROOT**

- If user opened only AhaAgent repo → `WORKSPACE_ROOT` = `AHA_ROOT`.
- If AhaAgent lives under `tools/aha-agent/` → `WORKSPACE_ROOT` is the parent folder.

---

## Phase A — Python environment and Aha! API

1. **Dependencies** — From `AHA_ROOT`, venv active (prefer `aha-agent-venv`):
   ```bash
   pip install -r requirements.txt
   ```

2. **`.env`** — If missing: `cp .env.example .env` and edit locally to set `AHA_API_KEY`.

3. **Sanity check:**
   ```bash
   python scripts/check_env.py
   ```

Wait for confirmation before moving on.

---

## Phase B — Optional: Jira

Ask if they need Jira board snapshot or PM brief skills.

If yes, add to `AHA_ROOT/.env`:
- `JIRA_HOST`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_BOARD_ID`

After values are set, run `python scripts/check_env.py` again, then optionally:
```bash
python src/executors/jira_board_overview.py
```

---

## Phase C0 — External knowledge (Obsidian / vault)

Run the **external knowledge** skill and set `KNOWLEDGE_ROOT` in `AHA_ROOT/.env` to the vault root. Most PM files go under **`$KNOWLEDGE_ROOT/AhaAgent/`** (glossary, Products, Meetings, jira-briefs, intake); dated feature-suggestion exports go to **`$KNOWLEDGE_ROOT/incoming/feature-suggestions/`**; plus **`Tasks/`** and **`GOALS.md`**. See [docs/knowledge_layout.md](../../../docs/knowledge_layout.md), [docs/knowledge_multiroot.md](../../../docs/knowledge_multiroot.md). Run `python scripts/check_env.py` and `python scripts/knowledge_gap_check.py`.

---

## Phase C — Optional: Meeting notes → Aha! Ideas workflow

Offer if they want meeting transcripts cross-referenced with Ideas.

**Config file:** `WORKSPACE_ROOT/.aha-config.yml` — schema in [.aha-config.example.yml](../../../.aha-config.example.yml).

Collect: product key, team, products (name + description), Idea category mapping.

Generate files after user confirms (under the vault when `KNOWLEDGE_ROOT` is set):
- `.cursor/rules/product-tagging.mdc` (from `workflows/meeting-ideas-crossref/cursor-rule-product-tagging.mdc`)
- `.cursor/skills/meeting-notes/SKILL.md` (if missing)
- `AhaAgent/product-glossary.md` and `AhaAgent/Products/<product>.md` in the vault

```bash
ROOT="${KNOWLEDGE_ROOT:?set KNOWLEDGE_ROOT first}"
mkdir -p "$ROOT"/AhaAgent/Meetings/Transcripts "$ROOT"/AhaAgent/Products \
  "$ROOT"/AhaAgent/jira-briefs "$ROOT"/AhaAgent/intake \
  "$ROOT"/incoming/feature-suggestions \
  "$ROOT"/Tasks
```

Validate Ideas API: `GET /products/{product_key}/ideas?per_page=1`.

---

## Phase D — Optional: Feature request prioritization

Ask if they want the daily feature request debrief.

If yes, run the setup wizard:
```
/aha-feature-setup-wizard
```

---

## Phase E — Domain safety

Remind:
- Celonis naming is inverted: "features" (GTM) → `/epics`; "epics" (internal) → `/features`.
- Bulk PUT/DELETE always needs a written plan and **explicit approval**.

---

## Completion checklist

| Capability | Ready when |
|------------|------------|
| Aha! API scripts / bulk update | venv, `.env` with `AHA_API_KEY`, `check_env.py` OK |
| Jira board / PM brief | All `JIRA_*` set, `jira_board_overview` runs |
| Meeting → Ideas | `.aha-config.yml`, templates copied, Ideas validation OK |
| Feature request debrief | `feature_requests:` in `.aha-config.yml`, SMTP in `.env`, launchd loaded |

**Example next prompts**
- *Run the task list* → `/aha-bulk-update`
- *Log a meeting* → `/meeting-notes`
- *Jira PM brief* → `/jira-pm-brief`
- *Prioritize feature requests* → `/aha-feature-prioritizer`
