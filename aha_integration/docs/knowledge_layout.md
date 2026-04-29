# External knowledge layout (KNOWLEDGE_ROOT)

Set `KNOWLEDGE_ROOT` in `AHA_ROOT/.env` to the root of your Obsidian vault or any folder. Most **PM-facing files** (glossary, meetings, hubs, Jira briefs, bulk-update intake) live under **`${KNOWLEDGE_ROOT}/AhaAgent/...`**. **Dated feature-suggestion API exports** from `aha_feature_suggestions` go under **`${KNOWLEDGE_ROOT}/incoming/feature-suggestions/`** (see `incoming_feature_suggestions_dir()` in `src/pm_data_paths.py`). **`${KNOWLEDGE_ROOT}/Tasks/`** and **`${KNOWLEDGE_ROOT}/GOALS.md`** sit at the vault root. The legacy `Knowledge/` path is **not** used.

If `KNOWLEDGE_ROOT` is **unset**, executors fall back to `data/` under the repo (local-only / CI).

## Recommended tree

```text
${KNOWLEDGE_ROOT}/
  README.md                    # Your portfolio MOC (optional; may pre-exist)
  products/                    # Deep product briefs (optional; may pre-exist)
  incoming/
    feature-suggestions/        # Dated snapshots from aha_feature_suggestions (default export root)
  AhaAgent/                    # Agent workflow root
    README.md                  # Entry: links to glossary, Meetings, MOCs
    product-glossary.md        # Canonical product Tags (see .cursor/rules/product-tagging)
    Products/                  # Hub pages: meetings, customer insights, links to products/...
    Meetings/
      Transcripts/
    jira-briefs/               # Generated Jira PM briefs (.md)
    intake/                    # Bulk Aha! update task lists (local; not committed from repo)
    Strategy/                  # optional
    Research/                  # optional
    Design/                    # optional
  Tasks/
    README.md                  # For meeting-notes “Related” scan
  GOALS.md                     # For meeting-notes “Related” scan
```

## Conventions

- **Feature-suggestion exports:** `incoming/feature-suggestions/<YYYY-MM-DD>/` from `aha_feature_suggestions` (or `data/feature-suggestions/` when `KNOWLEDGE_ROOT` is unset). Do not expect dated pulls under `AhaAgent/feature-suggestions/` by default.
- **Glossary:** `AhaAgent/product-glossary.md` defines valid `Tags:` values. Align names with `products[]` in `.aha-config.yml` and link to full briefs under `products/<slug>.md` instead of duplicating long content.
- **Hubs:** `AhaAgent/Products/<ProductName>.md` can be **thin** pages (meetings list, customer insight lines) with links to `../../products/...` for strategy and capabilities.
- **Meetings:** `AhaAgent/Meetings/<topic>-<YYYY-MM-DD>.md` and raw files under `AhaAgent/Meetings/Transcripts/`.
- **Wikilinks:** Obsidian `[[...]]` is fine; add plain relative links in `AhaAgent/README.md` for tools that do not resolve wikilinks.

## Cursor / workspace

Add the **vault folder** to the same workspace as the AhaAgent repo (or open a parent folder on disk) so rules and tools can read `AhaAgent/**/*.md` under the vault. See [knowledge_multiroot.md](knowledge_multiroot.md).

## Verification

```bash
python scripts/knowledge_gap_check.py
```

With `KNOWLEDGE_ROOT` set, the script reports missing paths without printing the vault path value.
