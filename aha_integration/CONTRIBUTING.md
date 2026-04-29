# Contributing to AhaAgent

How to add rules, skills, run validations, and contribute to the agentic harness.

## Prerequisites

- Python 3.9+
- Virtual environment (prefer `aha-agent-venv`, `.venv`, or `venv`)
- Aha! API token in `.env` for API-related work

## Before You Start

1. **Read the docs**
   - [AGENTS.md](AGENTS.md) — conventions, landmines, three-tier boundaries
   - [ARCHITECTURE.md](ARCHITECTURE.md) — module map and dependency rules
   - [docs/celonis_aha_rules.md](docs/celonis_aha_rules.md) — payload conventions for Features/Epics

2. **Run the harness verification**
   ```bash
   python scripts/verify_harness.py
   ```
   Fix any reported issues before opening a PR.

## Branch and PR Flow

1. Create a branch off `main`:
   ```bash
   git checkout -b feature/your-change
   ```

2. Make your changes:
   - For ad-hoc Aha! reads, prefer `python -m src.cli get <path>` (no scratchpad write needed).
   - For multi-step or write flows, use the scratchpad pattern: overwrite `src/executors/scratchpad.py` per task and import shared helpers from [src/lib/aha_helpers.py](src/lib/aha_helpers.py).

3. Run `verify_harness`:
   ```bash
   python scripts/verify_harness.py
   ```

4. Commit with a Conventional Commit message. Add the trailer for AI-generated commits:
   ```
   feat: add aha-bulk-update skill

   Includes-AI-Code: true
   ```

5. Push and open a PR:
   ```bash
   git push -u origin feature/your-change
   gh pr create --title "..." --body "..."
   ```

## Adding or Updating Rules

Rules live in `.cursor/rules/` as `.mdc` files with YAML frontmatter.

- **description**: Explains what the rule does; used for "Apply Intelligently"
- **globs**: File patterns for scoped rules (e.g. `["**/*.py"]`)
- **alwaysApply**: Use sparingly; prefer `false` with `globs` or `description` for relevance

**Guidelines:**
- Keep rules under 500 lines
- Reference files instead of copying content (e.g. link to `docs/aha_api_notes.md`)
- Use `globs` for file-specific rules instead of `alwaysApply: true`

## Adding or Updating Skills

Skills live in `.cursor/skills/<skill-name>/` with a `SKILL.md` file.

- **name**: Must match the folder name (lowercase, hyphens)
- **description**: When to use; the agent uses this for auto-activation

**Guidelines:**
- Put workflow steps and domain logic in skills, not rules
- Use guardrails (confirm before acting, ask for clarification)
- Optionally add `scripts/`, `references/`, `assets/` subfolders

## Running Validations

| Command | Purpose |
|---------|---------|
| `python scripts/verify_harness.py` | Check paths, rules parse, executor + CLI + helpers syntax |
| `python src/executors/test_api.py` | Test Aha! API connection (requires `.env`) |
| `python -m src.cli get <path>` | Ad-hoc read against the Aha! API (e.g. `/features/OPER-E-1234`) |
| `python -m src.cli paginate <path> --collection <key>` | Auto-page a list endpoint into one JSON array |

## Payload Conventions

When creating or updating Aha! Features/Epics, follow [docs/celonis_aha_rules.md](docs/celonis_aha_rules.md):

- Celonis taxonomy (Features vs Epics mapping)
- Custom field keys (`development_type`, `launch_type`, `for_external_roadmap`)
- Description formats (who-what-why for GTM, goal + links for internal)
