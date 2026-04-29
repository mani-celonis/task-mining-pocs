# Knowledge layout gap analysis (reference)

PM content is **not** stored in the AhaAgent git tree by default. Agents compare **expected paths** to your **vault** at `KNOWLEDGE_ROOT` (all under `AhaAgent/`, `Tasks/`, `GOALS.md` at vault root). Use:

```bash
python scripts/knowledge_gap_check.py
# or
python scripts/knowledge_gap_check.py /path/to/vault
```

## Expected vs typical gaps (before migration)

| Expected for full PM workflows | Often missing in a strategy-only vault | Remediation |
|--------------------------------|----------------------------------------|-------------|
| `AhaAgent/product-glossary.md` with valid **Tags** | Portfolio table in `README.md` only | Add glossary; align tags with `.aha-config.yml` `products` |
| `AhaAgent/Products/<name>.md` hub pages | Only `products/<slug>.md` briefs | Thin hubs under `AhaAgent/Products/` linking to `../../products/...` |
| `AhaAgent/Meetings/`, `.../Transcripts/` | — | Create and start populating |
| `AhaAgent/jira-briefs/`, `intake/` | — | Empty dirs are fine; executors use them when `KNOWLEDGE_ROOT` is set |
| `incoming/feature-suggestions/` | — | Required for `knowledge_gap_check`; `aha_feature_suggestions` writes dated snapshots here |
| `Tasks/README.md`, `GOALS.md` (vault root) | — | For meeting-notes “Related” scans |
| `Tags:` on tagged files (per product-tagging rule) | — | Add `Tags: ...` matching the glossary |

See [knowledge_layout.md](knowledge_layout.md) for the full tree.

When `KNOWLEDGE_ROOT` is **unset**, the repo still uses `data/jira-briefs/`, `data/intake/`, `data/feature-suggestions/` as fallbacks.
