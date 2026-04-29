# Aha! Management Agent

An AI-driven automation pipeline for managing Aha! Features and Epics at Celonis via the Aha! REST API. **Set `KNOWLEDGE_ROOT` in `.env`** to your Obsidian vault (or PM folder): bulk task lists, Jira PM briefs, meeting notes, and related files go under **`$KNOWLEDGE_ROOT/AhaAgent/...`** (see [docs/knowledge_layout.md](docs/knowledge_layout.md)). If `KNOWLEDGE_ROOT` is unset, the repo uses **`data/intake/`**, **`data/jira-briefs/`**, etc. (gitignored local fallbacks).

## Features

- **Python-based** — Uses `requests` and `python-dotenv` for API calls and configuration
- **Read-only CLI** — `python -m src.cli get <path>` for ad-hoc Aha! lookups, no scratchpad needed
- **Shared helpers** — `src/lib/aha_helpers.py` covers pagination, backlog fetch, and IDF-weighted matching
- **Scratchpad pattern** — Multi-step or write flows run from `src/executors/scratchpad.py` (overwritten per task)
- **Celonis taxonomy** — Follows company standards for Features, Epics, KTLO, and multi-phase launches (see `docs/celonis_aha_rules.md`)

## Quick Start

### 1. Clone the repository

```bash
git clone <repo-url>
cd AhaAgent
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv aha-agent-venv
source aha-agent-venv/bin/activate   # macOS/Linux
# or: aha-agent-venv\Scripts\activate   # Windows
```

### 3. Install dependencies (with venv activated)

Ensure the virtual environment is active (your prompt should show `(aha-agent-venv)`), then:

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Copy the example env file and add your Aha! API token:

```bash
cp .env.example .env
# Edit .env and set AHA_API_KEY=your_token_here
```

### 5. Verify the harness (optional)

```bash
python scripts/verify_harness.py
```

This checks required paths, rule files, and scratchpad syntax. See [AGENTS.md](AGENTS.md) for agentic use.

### 6. Quick reads via CLI

For one-shot lookups, use the read-only CLI — no scratchpad write needed:

```bash
python -m src.cli get /features/OPER-E-1234
python -m src.cli get /products/OPER/ideas --param per_page=5
python -m src.cli paginate /products/OPER/epics --collection epics
```

JSON goes to stdout, so it composes with `jq`, `>`, `| less`.

### 7. Run the scratchpad (multi-step or writes)

```bash
python src/executors/scratchpad.py
```

Use this for analytical loops (e.g. meeting cross-reference) and any write (`POST`/`PUT`/`DELETE`). Import shared helpers from `src/lib/aha_helpers.py` instead of re-implementing pagination or matching.

## PM onboarding (Cursor)

If you are new to the harness, use the **onboarding** skill so the agent can walk you through venv, `.env` (without pasting secrets in chat), optional Jira variables, the meeting-notes → Aha! Ideas workflow, and Celonis taxonomy guardrails.

**Example prompt in Cursor:**

> Onboard me to AhaAgent

Skill file: [.cursor/skills/onboarding/SKILL.md](.cursor/skills/onboarding/SKILL.md). For the meeting → Ideas templates, folder layout, and manual setup, see [workflows/meeting-ideas-crossref/README.md](workflows/meeting-ideas-crossref/README.md).

After you edit `.env`, you can confirm variables are present (values are never printed):

```bash
python scripts/check_env.py
```

## Agentic use

This repo is set up for AI agents (e.g. Cursor Agent):

- **[AGENTS.md](AGENTS.md)** — Map of conventions, landmines, and three-tier boundaries
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — Module map and dependency rules
- **`.cursor/rules/`** — Project rules (Aha! backlog access, product tagging)
- **`.cursor/skills/`** — Skills including **onboarding** (first-time PM setup), meeting notes, bulk updates, Jira board overview, Jira PM briefs (default output: vault `AhaAgent/jira-briefs/` or `data/jira-briefs/` — not committed)
- **`scripts/verify_harness.py`** — Run before commits to validate harness integrity

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add rules, skills, and run validations.

## Project Structure

```
AhaAgent/
├── AGENTS.md             # Agent map (conventions, landmines, boundaries)
├── ARCHITECTURE.md       # Module map and dependency rules
├── .cursorrules          # Core agent rules (links to docs)
├── .cursor/rules/        # Cursor rules (Aha! access, product tagging)
├── .cursor/skills/       # Skills (meeting-notes, aha-bulk-update, jira, jira-pm-brief)
├── .env.example          # Template for AHA_API_KEY
├── docs/
│   ├── README.md         # Docs index
│   ├── aha_api_notes.md  # API reference
│   └── celonis_aha_rules.md  # Celonis business taxonomy
├── scripts/
│   └── verify_harness.py # Harness validation
├── data/
│   ├── intake/           # Task lists to process (local; gitignored except .gitkeep)
│   └── archive/          # Completed task lists (local; gitignored except .gitkeep)
└── src/
    ├── cli.py            # Read-only CLI: `python -m src.cli get|paginate`
    ├── api/
    │   └── client.py     # Base Aha! API client
    ├── lib/
    │   └── aha_helpers.py # Shared helpers (pagination, IDF matching, backlog fetch)
    └── executors/
        ├── scratchpad.py # Multi-step / write tasks (overwrite per task)
        └── test_api.py   # API connection test
```

## Workflow

1. **Intake** — Place task lists in **`$KNOWLEDGE_ROOT/AhaAgent/intake/`** (preferred) or `data/intake/` (not committed)
2. **Translation** — The agent parses tasks and resolves names to Aha! `reference_num` or `id`
3. **Execution** — Uses `src/api/client.py` to run `GET`, `POST`, `PUT`, or `DELETE` requests
4. **Archive** — Completed task lists move to `data/archive/` (not committed)

## Workflows

Reusable workflow recipes that extend AhaAgent for common PM tasks:

| Workflow | Description |
|---|---|
| [Meeting → Aha! Ideas Cross-Reference](workflows/meeting-ideas-crossref/) | Automatically surface relevant Aha! Ideas when processing meeting transcripts in Cursor. Includes Cursor rules, a meeting-notes skill, and an example script. |

## Requirements

- Python 3.9+
- Aha! API token (from your Aha! account settings)

## License

Internal use — Celonis Product Management.
