# AhaAgent Documentation

Index of design documents, execution plans, and reference materials.

## Reference (API & Taxonomy)

| Document | Purpose |
|----------|---------|
| [aha_api_notes.md](aha_api_notes.md) | Aha! REST API usage, auth, endpoints, pagination |
| [celonis_aha_rules.md](celonis_aha_rules.md) | Celonis taxonomy (Features vs Epics), KTLO, multi-phase launches |
| [jira_api_notes.md](jira_api_notes.md) | Jira Cloud read-only board overview (`JIRA_*` env, Agile REST) |

## Templates

Committed skeletons for agent outputs (filled content goes to **`$KNOWLEDGE_ROOT/AhaAgent/jira-briefs/`** or gitignored `data/jira-briefs/` as fallback).

| Document | Purpose |
|----------|---------|
| [templates/jira_pm_brief.md](templates/jira_pm_brief.md) | PM brief structure for Jira board synthesis; filled copies → vault or `data/` (not committed) |
| [knowledge_layout.md](knowledge_layout.md) | Vault tree: `AhaAgent/`, `Tasks/`, `GOALS.md` |
| [knowledge_multiroot.md](knowledge_multiroot.md) | Opening the vault + repo in Cursor |
| [knowledge_gap_analysis.md](knowledge_gap_analysis.md) | Migration / gap checklist |

## Design Docs

Place design documents, architecture decisions, and product specs in [design-docs/](design-docs/).

## Execution Plans

Place step-by-step execution plans and runbooks in [exec-plans/](exec-plans/).

## References

Place external references, Aha! API docs links, and supplementary material in [references/](references/).
