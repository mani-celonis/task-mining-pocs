---
name: planning-to-ideas
description: Draft and create Aha! Ideas from quarterly or strategic planning markdown under KNOWLEDGE_ROOT, confirm the target Aha product, list near-duplicate existing Ideas, then POST only after user approval. Use when the user says "planning doc to Ideas", "quarter plan to Aha", "create Ideas from my planning file", or points to a planning document in the knowledge vault.
allowed-tools: Bash Read Write Glob
---

# Planning documents → Aha! Ideas

The canonical instructions match **[`.cursor/skills/planning-to-ideas/SKILL.md`](../../../.cursor/skills/planning-to-ideas/SKILL.md)**. Summary:

- Anchor paths on **`KNOWLEDGE_ROOT`** via `knowledge_root()` and `python scripts/print_knowledge_paths.py` from the AhaAgent repo; optional default folders `portfolio/products/planning/` or `products/planning/` (see `planning_docs_dir_candidates()` in `pm_data_paths.py`) when present.
- Read `.aha-config.yml` for `product_key` and `products[]`; user **must** confirm the Aha product before any write.
- **Extract** candidate Ideas from planning markdown, run a **mandatory** near-duplicate check (`GET /products/{product_key}/ideas`, then compare titles with `difflib` or similar; see planning-to-ideas skill and `crossref_ideas_example.py`).
- **Preview** and get **explicit approval** before `POST` to create Ideas. Use `AhaApiClient` and the payload in `docs/aha_api_notes.md` (Ideas section).

Read the Cursor skill file for the full workflow, guardrails, and links.
