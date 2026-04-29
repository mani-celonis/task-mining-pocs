# Aha! Management Agent Context (Celonis)

## Project Purpose
This repository acts as an AI-driven automation pipeline for managing Product Management data in Aha! for Celonis. 
Instead of manually clicking through the Aha! UI to fix discrepancies, the PM will export a list of required changes, write them in natural language under **`$KNOWLEDGE_ROOT/AhaAgent/intake/`** (with `KNOWLEDGE_ROOT` in `.env`), or in **`data/intake/`** as a fallback, and ask the AI agent to execute them via the Aha! REST API. See `src/pm_data_paths.py` and [docs/knowledge_layout.md](docs/knowledge_layout.md). Repo `data/*` is **gitignored** when used as fallback.

## Architecture & Workflow
1. **Intake:** Task lists are placed in **`$KNOWLEDGE_ROOT/AhaAgent/intake/`** (preferred) or `data/intake/` (not committed from repo when using the vault for PM data).
2. **Translation:** The agent parses the tasks and resolves entity names (Features/Epics) to their Aha! `reference_num` or `id`.
3. **Execution:** The agent uses the centralized API client (`src/api/client`) to execute `POST`, `PUT`, or `DELETE` requests.
4. **Archive:** Completed task lists are moved to `data/archive/` (not committed).

## Current State
- [x] Scaffolding created.
- [x] API documentation added to `docs/aha_api_notes.md`.
- [x] System prompts added to `.cursorrules`.
- [ ] Build the base API client (`src/api/client`) with authentication and rate-limiting.
- [ ] Create the first executor script to process natural language updates.

## Agent Instructions
When you are asked to work on this project, always read this `AGENT.md` file first to understand the current state and objectives. Update the "Current State" checklist as we complete tasks.

**Before making any Aha! API calls:** You MUST understand the Celonis taxonomy. Celonis uses the opposite of standard Aha! naming:
- **Celonis Features** (GTM, client-facing) = Aha! Epics → use `/epics` endpoints
- **Celonis Epics** (internal) = Aha! Features → use `/features` endpoints

When the user says "features", they typically mean Celonis Features → `GET /epics`. When they say "epics", they mean Celonis Epics → `GET /features`. Always consult `docs/aha_api_notes.md` and `docs/celonis_aha_rules.md` before writing scripts.
