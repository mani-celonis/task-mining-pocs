---
name: aha-bulk-update
description: Process task lists from AhaAgent/intake/ (under KNOWLEDGE_ROOT) or data/intake/ to bulk update Aha! Features or Epics. Use when the user says "run the task list", "execute intake", "bulk update features", or provides an intake file with field changes for named items.
---

# Aha! Bulk Update

Process structured task lists and execute bulk updates against the Aha! API. Intake files are **not** part of the shared repository.

## Where to put task files

- **Preferred:** With `KNOWLEDGE_ROOT` set in `AhaAgent/.env`, place files under **`$KNOWLEDGE_ROOT/AhaAgent/intake/`** in your Obsidian vault.
- **Fallback:** If `KNOWLEDGE_ROOT` is unset, use **`data/intake/`** in the repo. See `src/pm_data_paths.py` (`intake_dir()`).

## When to Use

- User has a task file in `AhaAgent/intake/` or `data/intake/`
- User asks to "execute", "run", or "process" an intake/task list
- User wants bulk PUT operations against Features or Epics

## Prerequisites

- `.env` with `AHA_API_KEY`
- Read [docs/celonis_aha_rules.md](../../docs/celonis_aha_rules.md) before generating payloads

## Workflow

1. **Interpret correctly**: Task says "feature" → Celonis Feature → `GET /epics`, `PUT /epics/{ref}`. Task says "epic" → Celonis Epic → `GET /features`, `PUT /features/{ref}`.

2. **Lookup first**: The API requires `reference_num`. Two options:
   - **Quick name → ref resolution** — use the read-only CLI and pipe through `jq`:
     ```bash
     python -m src.cli paginate /products/OPER/epics --collection epics \
       | jq '.[] | select(.name | test("migration"; "i")) | {ref: .reference_num, name}'
     ```
     No scratchpad write needed for simple resolution.
   - **Complex resolution or building payloads** — write a scratchpad that:
     - Imports `paginate` from [src/lib/aha_helpers.py](../../src/lib/aha_helpers.py) instead of re-implementing pagination
     - Filters by name (exact or partial)
     - Resolves name → `reference_num`
     - Builds payloads for the next step

3. **Custom fields**: Use `{"custom_fields": {"key": "value"}}` in the payload. See `docs/celonis_aha_rules.md` for valid keys.

4. **Safety check**: Before any bulk PUT/DELETE:
   - Print a summary (ref, field, old → new) to the console
   - Wait for user confirmation in chat or terminal
   - Never proceed without explicit approval

5. **Idempotency**: Track successes. If the script fails mid-way, re-running should not duplicate updates or throw errors on already-updated fields.

## Implementation

Write the logic into `src/executors/scratchpad.py` (overwrite per task). Use `AhaApiClient` from `src/api/client.py` and helpers from `src/lib/aha_helpers.py`.

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from dotenv import load_dotenv
from src.api.client import AhaApiClient
from src.lib.aha_helpers import paginate

load_dotenv()
client = AhaApiClient(os.getenv("AHA_API_KEY"))
# ... parse intake from intake_dir() (or data/intake/<file> fallback), resolve
# names via paginate(), build payloads, confirm, execute ...
```

## Guardrails

- Always generate a plan and wait for "yes" or "approved" before executing.
- If multiple records match a name, pause and ask which one to modify.
- Never hardcode the API key.
- After completion, move the processed file to an archive (e.g. under the vault or `data/archive/`) if the user wants — confirm with user.
