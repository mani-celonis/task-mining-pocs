---
name: planning-to-ideas
description: Draft and create Aha! Ideas from quarterly or strategic planning markdown under KNOWLEDGE_ROOT, confirm the target Aha product, list near-duplicate existing Ideas, then POST only after user approval. Use when the user says "planning doc to Ideas", "quarter plan to Aha", "create Ideas from my planning file", or points to a planning document in the knowledge vault.
---

# Planning documents → Aha! Ideas

Turn planning notes (quarterly plans, OKR docs, product strategy markdown) into **Aha! Ideas** for the right **product** (`product_key`), without duplicating work already in the Ideas portal.

## When to use

- User has a **planning document** (e.g. quarter plan) and wants **new Ideas** in Aha!.
- Triggers: *"planning doc to Ideas"*, *"promote this plan to Ideas"*, *"create Ideas from [file] under the vault"*.

## Prerequisites

- `AHA_API_KEY` in `.env` (never commit, never print).
- [`.aha-config.yml`](../../../.aha-config.yml) at the **workspace root** with at least `product_key` and `products[]` (each with `name`, `category` for Idea category mapping). See [`.aha-config.example.yml`](../../../.aha-config.example.yml).
- `KNOWLEDGE_ROOT` set in `.env` for normal use (so paths resolve to the Obsidian / portfolio root). If unset, the user can still pass an **absolute** path to a file.
- Python venv: `source aha-agent-venv/bin/activate` (or your project venv), then `python scripts/print_knowledge_paths.py` to print resolved `KNOWLEDGE_ROOT` and other dirs.

## Path resolution (KNOWLEDGE_ROOT)

- **Never** assume a repo-specific prefix. Anchor on [`knowledge_root()`](../../../src/pm_data_paths.py) and [`scripts/print_knowledge_paths.py`](../../../scripts/print_knowledge_paths.py).
- **Default folder hints** (see `planning_docs_dir_candidates()` in `pm_data_paths.py`): under `KNOWLEDGE_ROOT`, use the first path that exists: `portfolio/products/planning/`, or `products/planning/` when the knowledge root is already the inner `portfolio` directory. The user may place planning files anywhere under the vault; these are only **conventions** to suggest candidate paths.
- The user must pick a **concrete** `.md` file: path **relative to the vault root** or an **absolute** path.

## Workflow (must follow in order)

### 1. Resolve where files live

- Run from repo root: `python scripts/print_knowledge_paths.py`.
- If a default planning directory exists, mention it. Otherwise ask the user which file to use.

### 2. Choose the planning document

- Read the chosen file from disk.
- If the doc is long or poorly structured, ask for a section to focus on or use clear headings (initiatives, goals, epics) for extraction.

### 3. Map to Aha! product and category

- Open `.aha-config.yml` at the workspace root.
- **`product_key`**: the Aha! product for Ideas in this flow (one product per run unless the user explicitly splits work across products).
- **`products[]`**: the user says which **named product** from this list they are planning for. Use the matching `category` value as the **Idea category** in Aha! when the API allows it; if the create payload does not accept a category by name, note it for a follow-up edit in the UI (see [docs/aha_api_notes.md](../../../docs/aha_api_notes.md)).

### 4. Confirm the Aha! target (mandatory before any write)

- Show clearly:
  - `product_key`
  - The chosen `products[]` name and `category`
  - Link pattern: `https://celonis.aha.io/products/{product_key}/ideas` (or your account base URL from config if different)
- Ask: *"Confirm this is the product/line where new Ideas should be created."* Do not POST until the user agrees.

### 5. Propose candidate Ideas (from the doc only)

- From the planning markdown, propose a table of **candidate** Ideas: **title**, **short description** (plain text; user can later refine HTML in Aha!), **target category** (from step 3).
- Prefer one Idea per distinct initiative/OKR/bullet, not one giant Idea.
- This step is **local reasoning** only; no API writes yet.

### 6. Near-duplicate check against existing Ideas (mandatory)

Before creating anything, reduce duplicate or overlapping Ideas in Aha!:

1. Use [`AhaApiClient`](../../../src/api/client.py) and the same pagination pattern as [`workflows/meeting-ideas-crossref/examples/crossref_ideas_example.py`](../../../workflows/meeting-ideas-crossref/examples/crossref_ideas_example.py): `GET /products/{product_key}/ideas` with `per_page=100` (or 200) and loop `pagination.total_pages`.
2. For each **proposed title** (and optionally a one-line description), compare to each existing Idea **name** using a **simple, dependency-free** match:
   - Normalize: lowercase, strip extra whitespace, collapse punctuation.
   - Use `difflib.SequenceMatcher` (or token overlap) and flag **possible duplicates** when similarity is high (e.g. ratio ≥ 0.6 or strong substring match). Tune so obvious paraphrases surface without flooding the list.
3. `GET /ideas/{ref}` for **detail** only when needed to confirm **category** (categories are not on the list endpoint; see [`.cursor/rules/aha-agent.mdc`](../../../.cursor/rules/aha-agent.mdc)). Rate-limit detail fetches: `time.sleep(1.1)` every 15 requests.
4. Present a **single table** for the user:

| Proposed title | Suggested body (snippet) | Possible existing match (ref, name) | Note |
|----------------|-----------------------------|--------------------------------------|------|
| ... | ... | ... or — | e.g. "High similarity" / "No close match" |

- Ask the user, per row: **Create new** / **Skip (duplicate)** / **Link only in planning doc to existing** (and which ref).
- If they skip, do not POST that row.

### 7. Final preview and explicit approval

- After dedupe decisions, show the **final** list: title, description, category, create vs skip.
- State: *"I will POST N Ideas to product `{product_key}`."* Wait for **explicit approval** in chat (same bar as [aha-bulk-update](../aha-bulk-update/SKILL.md)).

### 8. Create Ideas (only after approval)

- Implement in `src/executors/scratchpad.py` (or a one-off under `src/executors/`) with:

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from dotenv import load_dotenv
from src.api.client import AhaApiClient
load_dotenv()
client = AhaApiClient(os.getenv("AHA_API_KEY"))
# client.post(f"/products/{product_key}/ideas", data={...})
```

- Use `client.post` per [docs/aha_api_notes.md](../../../docs/aha_api_notes.md) (**Ideas** section). One POST per approved Idea.
- On success, print `reference_num` and URL for each. On partial failure, report which succeeded and which failed; do not retry without user consent.

## Guardrails

- **No** POST/PUT/DELETE in Aha! without the confirmation steps above.
- **No** hardcoded API key; use `.env` + `load_dotenv()`.
- If `.aha-config.yml` is missing or `product_key` is wrong, stop and ask the user to fix config.
- This skill targets **product Ideas** (`/products/{product_key}/ideas`), not the Feature Suggestions workspace (`SUGGESTION` / [aha_feature_suggestions](../../../src/executors/aha_feature_suggestions.py)) unless the user explicitly asks to use that system.

## Documentation pointers

- Ideas list/detail: [`.cursor/rules/aha-agent.mdc`](../../../.cursor/rules/aha-agent.mdc)
- API notes (create Idea): [docs/aha_api_notes.md](../../../docs/aha_api_notes.md)
- Path helpers: [src/pm_data_paths.py](../../../src/pm_data_paths.py) (`knowledge_root`, `default_planning_docs_dir`, `planning_docs_dir_candidates`)
