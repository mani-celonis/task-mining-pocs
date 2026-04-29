---
name: jira-board-overview
description: Summarize Jira work (epics + issues) via JQL search or board; use when the user asks what an engineering team is doing in Jira, wants a TM / ML Infra snapshot, or to relate Jira epics to product context.
---

# Jira board overview

Read-only pull of Jira issues, grouped by **Epic Link** + Epic-type issues in the result set. **Prefer `JIRA_JQL`** (or `JIRA_JQL_PATH`) for PM-sized slices; **`JIRA_BOARD_ID`** only as fallback (full board can be huge). Uses `JIRA_*` in `.env` (not MCP).

## Prerequisites

- `.env`: `JIRA_HOST`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
- **One of:** `JIRA_JQL`, `JIRA_JQL_PATH` (file), or `JIRA_BOARD_ID` — see [docs/jira_api_notes.md](../../docs/jira_api_notes.md) and `.env.example`

## Workflow

1. Run from repo root (venv active if needed):

   ```bash
   python src/executors/jira_board_overview.py
   ```

2. For machine-readable output (e.g. PM brief or filtering in chat):

   ```bash
   python src/executors/jira_board_overview.py --json
   ```

3. One-off JQL without editing `.env`:

   ```bash
   python src/executors/jira_board_overview.py --jql 'project = TM AND ...'
   ```

4. Narrate the Markdown: epics, status, owners, **labels/components**. If the user’s scope is unclear, confirm whether they use the **default ML Infra JQL** or another filter.

5. **Aha! crosswalk (manual for now):** compare Jira keys to Aha! `integration_fields` / `check_missing_jira.py` when mapping to roadmap.

## Guardrails

- **Read-only** — no Jira writes from this skill.
- **Secrets** — never print `JIRA_API_TOKEN`; do not commit `.env`.
- **Approval** — if the user later asks for Jira mutations, require explicit confirm per [AGENTS.md](../../AGENTS.md).
