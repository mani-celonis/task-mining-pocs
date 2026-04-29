---
description: Jira Cloud API usage — auth, JQL search, ADF flattening, read-only constraint. Loads when working on Jira executors or Jira docs.
paths:
  - "src/api/jira_client.py"
  - "src/executors/jira_*.py"
  - "docs/jira_api_notes.md"
---

# Jira API — rules

## Auth

HTTP Basic: `JIRA_EMAIL` + `JIRA_API_TOKEN` from `.env`. Base URL: `JIRA_HOST` (e.g. `https://celonis.atlassian.net`).

## Read-only

`JiraApiClient` supports GET only. No writes to Jira from this project.

## Endpoints

- `GET /rest/api/3/search/jql` — search issues by JQL (paginate via `nextPageToken`)
- `GET /rest/api/3/field` — fetch field metadata (Epic Link field ID)
- `GET /rest/agile/1.0/board/{id}/issue` — fallback board fetch (can be huge; prefer JQL)

## JQL scope

Prefer `JIRA_JQL` in `.env` for PM-sized slices. `JIRA_JQL_PATH` for file-based multiline JQL. `JIRA_BOARD_ID` only as last resort.

## ADF descriptions

Jira descriptions are Atlassian Document Format (ADF JSON). Use `src/api/jira_adf.py` → `flatten_adf(node, max_chars=400)` to get plain text snippets.

## Guardrails

- Never print `JIRA_API_TOKEN`.
- Never commit `.env` or files under `data/jira-briefs/`.
- Rate-limit: auto-retry on 429 with `Retry-After` header.
