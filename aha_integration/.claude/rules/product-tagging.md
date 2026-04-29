---
description: Product tagging and hub maintenance — AhaAgent and Tasks files under KNOWLEDGE_ROOT must have product tags and cross-references in product hubs.
paths:
  - "**/AhaAgent/**/*.md"
  - "**/Tasks/**/*.md"
---

# Product tagging and hub maintenance

Content lives under **`KNOWLEDGE_ROOT`** (see `AhaAgent` `.env`). Resolve **`AhaAgent/...`** and **`Tasks/...`** relative to the vault root. Read **`GOALS.md`** at the vault root for goals.

Every meeting note, task file, and knowledge file MUST have a `Tags:` line with valid product tags from **`AhaAgent/product-glossary.md`**.

Valid tags: read product names from `.aha-config.yml` (`products[].name`). Use `—` only when no product applies.

## Multi-tagging

Most content touches 2–3 products. Tag all products discussed, not just the primary one.

## Product hubs

Each product has a hub page at **`AhaAgent/Products/<product>.md`**. When saving tagged content, update the corresponding hub(s):

- **Meeting notes**: add link under "Meetings"; add one-line summary under "Customer insights" if the meeting contains customer feedback.
- **Tasks (create)**: add link under "Open tasks".
- **Tasks (complete)**: move link from "Open tasks" to "Completed tasks".
- **Knowledge files**: add link under "Knowledge" if not already listed.

## Querying by product

When the user asks "what do we know about [product]?", read the product hub first (`AhaAgent/Products/<product>.md`) before scanning further.
