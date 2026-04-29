---
name: jira-board-overview
description: Summarize Jira work (epics + issues) via JQL search or board; use when the user asks what an engineering team is doing in Jira, wants a TM / ML Infra snapshot, or to relate Jira epics to product context.
allowed-tools: Bash Read
---

# Jira board overview

Read-only pull of Jira issues, grouped by Epic Link. **Prefer `JIRA_JQL`** for PM-sized slices; `JIRA_BOARD_ID` only as fallback (full board can be huge). Uses `JIRA_*` in `.env`.

## Prerequisites

- `.env`: `JIRA_HOST`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
- One of: `JIRA_JQL`, `JIRA_JQL_PATH`, or `JIRA_BOARD_ID`

## Workflow

1. Run from repo root (venv active):
   ```bash
   python src/executors/jira_board_overview.py
   ```

2. For machine-readable output (e.g. PM brief):
   ```bash
   python src/executors/jira_board_overview.py --json
   ```

3. One-off JQL without editing `.env`:
   ```bash
   python src/executors/jira_board_overview.py --jql 'project = TM AND ...'
   ```

4. Narrate the Markdown: epics, status, owners, labels/components. Confirm scope (default ML Infra JQL or another filter) if unclear.

## Guardrails

- **Read-only** — no Jira writes.
- Never print `JIRA_API_TOKEN`; never commit `.env`.
- Require explicit confirm before any Jira mutations.
