# AhaAgent

AI-driven Aha! + Jira PM automation for Celonis. Manages backlog features/epics, Jira snapshots, meeting notes, and feature request prioritization via REST APIs.

## See also

- **External knowledge** — Most PM working files (meetings, hubs, glossary, Jira briefs, bulk intake) live under **`$KNOWLEDGE_ROOT/AhaAgent/...`**. Dated feature-suggestion API snapshots go to **`$KNOWLEDGE_ROOT/incoming/feature-suggestions/`** (`incoming_feature_suggestions_dir()` in `pm_data_paths.py`). **`Tasks/`** and **`GOALS.md`** sit at the vault root. Set **`KNOWLEDGE_ROOT`** in `.env`. See `.cursor/skills/external-knowledge` and `docs/knowledge_layout.md`. If `KNOWLEDGE_ROOT` is unset, executors fall back to `data/` in the repo.
- @docs/celonis_aha_rules.md — canonical Celonis taxonomy and business rules (read before API work)
- @ARCHITECTURE.md — module map and dependency rules
- @docs/aha_api_notes.md — Aha! API reference, pagination, rate limits
- @docs/jira_api_notes.md — Jira auth, JQL, ADF

## Bash commands

```bash
# Activate venv (prefer aha-agent-venv)
source aha-agent-venv/bin/activate

# Install deps
pip install -r requirements.txt

# Check env vars (never prints values)
python scripts/check_env.py

# Print resolved PM knowledge paths (KNOWLEDGE_ROOT + jira-briefs, intake, incoming feature-suggestions; no secrets)
python scripts/print_knowledge_paths.py

# Verify harness integrity (no API needed)
python scripts/verify_harness.py

# Quick API connectivity test
python src/executors/test_api.py

# Run daily debrief manually
bash scripts/run_debrief.sh
```

## Celonis taxonomy (CRITICAL — inverted vs standard Aha!)

| When user says | Celonis term | `reference_num` pattern | Aha! endpoint |
|---|---|---|---|
| "features" / "GTM features" | Feature (client-facing) | Contains `-E-` (e.g. `AIMODULES-E-7`) | `/epics` |
| "epics" / "internal epics" | Epic (internal) | No `-E-` (e.g. `AIMODULES-10`) | `/features` |

**Always check `reference_num` before choosing endpoint.** `-E-` → `/epics`. No `-E-` → `/features`.

## Scratchpad pattern

Write one-off scripts to `src/executors/scratchpad.py`. **Overwrite it per task — never accumulate logic.**

Template:
```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from dotenv import load_dotenv
from src.api.client import AhaApiClient

load_dotenv()
client = AhaApiClient(os.getenv("AHA_API_KEY"))
# ... your logic ...
```

## Safety rules

- **Always** present a plan and wait for explicit approval before bulk PUT/DELETE.
- **Never** hardcode API keys; always read from `.env` via `load_dotenv()`.
- **Never** commit `.env`, filled Jira briefs, or intake task lists (whether under the vault or `data/` when no vault is configured).
- **Disambiguate** when multiple records match a name — never guess.
- **Rate limits**: 300 req/min, 20/sec. `AhaApiClient` auto-retries 429s.

## Git workflow

- Branch off `main`; use `gh pr create` for PRs.
- Commit message trailer for AI-generated commits: `Includes-AI-Code: true`
- Never commit: `.env`, `data/intake/`, `data/archive/`, `data/jira-briefs/`, or PM content from the vault (e.g. `AhaAgent/Strategy/`, `AhaAgent/Research/`, `AhaAgent/Design/` if you ever copy those into the clone)

## Common gotchas

- **Jira descriptions** are Atlassian Document Format (ADF JSON) — use `src/api/jira_adf.py` to flatten to plain text.
- **Idea categories** are only returned by the detail endpoint (`GET /ideas/{ref}`), not the list endpoint.
- **Pagination**: always check `pagination.total_pages` and loop.
- **venv detection order**: `aha-agent-venv` > `ahaAgent` > `.venv` > `venv`. Ask before creating a new one.
- **Feature request prioritizer config** lives under `feature_requests:` key in `.aha-config.yml`.
