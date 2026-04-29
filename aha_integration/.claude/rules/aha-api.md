---
description: Aha! API usage, scratchpad pattern, pagination, and Ideas cross-referencing. Loads when working on executors, intake files, or API docs.
paths:
  - "src/**/*.py"
  - "**/AhaAgent/intake/**"
  - "data/intake/**"
  - "docs/aha_api_notes.md"
  - "docs/celonis_aha_rules.md"
---

# Aha! API — rules

See [CLAUDE.md](../../CLAUDE.md) for the Celonis taxonomy cheat sheet and scratchpad template.

**Intake:** With `KNOWLEDGE_ROOT` in `.env`, bulk task files go under **`AhaAgent/intake/`** in the vault; otherwise `data/intake/` in the repo (`intake_dir()` in `src/pm_data_paths.py`).

## API client

`AhaApiClient` from `src/api/client.py`. Methods: `get(path, params=)`, `put(path, data=)`, `post(path, data=)`, `delete(path)`. All auto-retry on 429.

## Scratchpad template

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from dotenv import load_dotenv
from src.api.client import AhaApiClient

load_dotenv()
client = AhaApiClient(os.getenv("AHA_API_KEY"))
# ... your logic ...
```

## Ideas endpoint

- List: `GET /products/{product_key}/ideas` — returns refs only; no category detail
- Detail: `GET /ideas/{ref}` — returns categories, custom fields, endorsements
- When filtering by category: fetch all refs from list, then detail each (~15/sec max; `time.sleep(1.1)` every 15 requests)
- Read `product_key` and `products[].category` from `.aha-config.yml`

## Pagination

Always check `pagination.total_pages` and loop over pages. Use `?fields=` to limit response size.

## Safety

- Never hardcode `AHA_API_KEY`. Always `load_dotenv()` from `.env`.
- Before bulk PUT/DELETE: print summary (ref, field, old→new), wait for explicit "yes".
- Rate limits: 300 req/min, 20/sec.
