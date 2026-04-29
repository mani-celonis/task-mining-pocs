# Agent Instructions for AhaAgent

Operating manual for AI agents working on this codebase. Link to canonical docs; do not duplicate content.

---

## Conventions

- **Stack:** Python 3.9+, `requests`, `python-dotenv`. All scripts in Python.
- **Execution:**
  - **Quick reads:** `python -m src.cli get <path>` and `python -m src.cli paginate <path> --collection <key>` for one-shot lookups. Read-only by design.
  - **Multi-step / writes:** `src/executors/scratchpad.py` — **overwrite per task**, do not accumulate logic. Import helpers from [src/lib/aha_helpers.py](src/lib/aha_helpers.py) (`paginate`, `fetch_backlog`, `fetch_all_ideas`, `fetch_ideas_with_categories`, `build_idf`, `keyword_match`).
- **Venv:** Prefer `ahaAgent`, `.venv`, `venv`, or `aha-agent-venv`. Ask before creating a new venv.
- **API:** Aha! base URL `https://celonis.aha.io/api/v1`. Auth via `AHA_API_KEY` in `.env`. Jira Cloud read-only helpers use `JIRA_*` in `.env` (see [docs/jira_api_notes.md](docs/jira_api_notes.md)). Never hardcode keys.

## Local knowledge first

When the user’s question depends on **saved** PM content (dated feature-suggestion exports, Jira PM briefs, intake task lists, meetings/glossary under the vault), resolve paths and **read those files** before claiming nothing exists.

1. Run `python scripts/print_knowledge_paths.py` (or use `src/pm_data_paths.py`) to get absolute directories for the current machine.
2. Open or read the latest relevant files there (e.g. newest `YYYY-MM-DD` under `incoming/feature-suggestions/` from that output).
3. Do **not** treat an empty `data/` tree in the repo as authoritative when `KNOWLEDGE_ROOT` is set: exports usually live under the vault. See [docs/knowledge_multiroot.md](docs/knowledge_multiroot.md) if the vault is not in the workspace.
4. **Feature suggestions** are a special case: work can mean **syncing from Aha!** (new export under `incoming/feature-suggestions/`) or **reading/processing the latest saved export only** (no API). If the user does not say which, follow [aha-feature-suggestions](.cursor/skills/aha-feature-suggestions/SKILL.md) and **ask once** to disambiguate.

---

## Landmines

1. **Celonis taxonomy is inverted:** "Features" (GTM) → Aha! Epics (`/epics`). "Epics" (internal) → Aha! Features (`/features`). `-E-` in `reference_num` = Celonis Feature.
2. **Planning before execution:** Always present a plan and wait for explicit approval before running API calls or bulk updates.
3. **Name → reference resolution:** Task lists often use names. Resolve to `reference_num` via query/filter before `PUT`/`DELETE`.
4. **Custom fields:** Pass via `custom_fields: {"key": "value"}` in payloads.
5. **Rate limits:** 300/min, 20/sec. Implement retry on 429.
6. **Jira PM briefs are out-of-repo:** With `KNOWLEDGE_ROOT` set, default output is **`$KNOWLEDGE_ROOT/AhaAgent/jira-briefs/`**; otherwise `data/jira-briefs/` (gitignored). See [jira-pm-brief](.cursor/skills/jira-pm-brief/SKILL.md) and [docs/templates/jira_pm_brief.md](docs/templates/jira_pm_brief.md). **Never commit** generated briefs.

---

## Pointers

| Topic | Location |
|-------|----------|
| External knowledge root (`KNOWLEDGE_ROOT` in `.env`) | [.cursor/skills/external-knowledge/SKILL.md](.cursor/skills/external-knowledge/SKILL.md), [docs/knowledge_layout.md](docs/knowledge_layout.md), [docs/knowledge_multiroot.md](docs/knowledge_multiroot.md), [docs/knowledge_gap_analysis.md](docs/knowledge_gap_analysis.md), `src/pm_data_paths.py`, `python scripts/knowledge_gap_check.py` |
| Resolved PM paths (read-only; prints absolute paths, never secrets) | `python scripts/print_knowledge_paths.py` |
| API reference, taxonomy, Celonis rules | [docs/aha_api_notes.md](docs/aha_api_notes.md), [docs/celonis_aha_rules.md](docs/celonis_aha_rules.md) |
| Quick reads (CLI) | [src/cli.py](src/cli.py) — `python -m src.cli get`, `python -m src.cli paginate` |
| Reusable helpers (pagination, IDF matching, backlog fetch) | [src/lib/aha_helpers.py](src/lib/aha_helpers.py) |
| Aha! backlog access, scratchpad template | [.cursor/rules/aha-agent.mdc](.cursor/rules/aha-agent.mdc) |
| Product tagging, hub maintenance | [.cursor/rules/product-tagging.mdc](.cursor/rules/product-tagging.mdc) |
| Meeting notes workflow | [.cursor/skills/meeting-notes/SKILL.md](.cursor/skills/meeting-notes/SKILL.md) |
| Planning documents → Aha! Ideas (vault, dedupe, confirm, then POST) | [.cursor/skills/planning-to-ideas/SKILL.md](.cursor/skills/planning-to-ideas/SKILL.md) |
| Aha feature suggestions (sync vs. local export) | [.cursor/skills/aha-feature-suggestions/SKILL.md](.cursor/skills/aha-feature-suggestions/SKILL.md) |
| Bulk Aha! updates from task lists | [.cursor/skills/aha-bulk-update/SKILL.md](.cursor/skills/aha-bulk-update/SKILL.md) |
| Jira snapshot (JQL or board; PM slice = `JIRA_JQL` in `.env`) | [.cursor/skills/jira-board-overview/SKILL.md](.cursor/skills/jira-board-overview/SKILL.md) |
| Jira → PM brief (themes, risks; vault or `data/`) | [.cursor/skills/jira-pm-brief/SKILL.md](.cursor/skills/jira-pm-brief/SKILL.md) |
| Feature Suggestion review and triage | [.cursor/skills/aha-feature-suggestions-review/SKILL.md](.cursor/skills/aha-feature-suggestions-review/SKILL.md) |
| Architecture, modules, entry points | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Contributing, validation | [CONTRIBUTING.md](CONTRIBUTING.md) |

---

## Three-Tier Boundaries

### Always
- Read `docs/celonis_aha_rules.md` before creating/updating Features or Epics.
- For tasks involving **local** PM exports or vault files: follow [Local knowledge first](#local-knowledge-first) and prefer reading the latest files under the paths from `print_knowledge_paths` / `pm_data_paths` before inferring missing data.
- Use `AhaApiClient` from `src/api/client.py` for API calls.
- Load API key from `.env` via `load_dotenv()`.
- Prefer `python -m src.cli get` for ad-hoc reads — no scratchpad write needed.
- Use helpers from `src.lib.aha_helpers` (e.g. `paginate`, `fetch_backlog`, `keyword_match`) instead of re-implementing pagination or matching in scratchpads.

### Ask First
- Bulk `PUT` or `DELETE` — print summary, wait for confirmation.
- Creating or modifying records when multiple matches exist — disambiguate.
- Running scripts that hit the Aha! API — ensure user approves.

### Never
- Hardcode `AHA_API_KEY` or any secret.
- Guess which record to modify when ambiguous.
- Proceed with execution without explicit user approval.
- Commit `.env`, API keys, or user-specific config.
- Commit generated Jira PM briefs (they belong in the vault or `data/`, not git).
- Accumulate logic in `scratchpad.py` — overwrite per task.

---

## Validation

Run harness check before committing:

```bash
python scripts/verify_harness.py
```
