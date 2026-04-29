---
name: external-knowledge
description: Configure where PM knowledge lives outside the AhaAgent repo (Obsidian vault or any folder). Set KNOWLEDGE_ROOT in .env. Use when the user says configure knowledge, set obsidian path, external knowledge, KNOWLEDGE_ROOT, knowledge vault, or first-time knowledge setup.
allowed-tools: Bash Read Write Glob
---

# External knowledge (KNOWLEDGE_ROOT)

AhaAgent is for **Aha! API interaction and automation** (this repository). Long-form PM context—meeting notes, product hubs, glossaries, Jira briefs, bulk intake—should live in a **separate knowledge root** you control (often an Obsidian vault). This skill walks through **one-time configuration** so agents know where to read and write that content.

## Contract

- Set `KNOWLEDGE_ROOT` in `.env` to the **absolute path of the vault root** (or folder containing your portfolio).
- Most PM files use the **`AhaAgent/`** subtree: **`$KNOWLEDGE_ROOT/AhaAgent/...`** (glossary, Products, Meetings, jira-briefs, intake). Dated feature-suggestion exports: **`$KNOWLEDGE_ROOT/incoming/feature-suggestions/`** (from `aha_feature_suggestions`). **Legacy `Knowledge/` is not used.**
- **`Tasks/`** and **`GOALS.md`** live at the **vault root** (siblings of `AhaAgent/`). See [docs/knowledge_layout.md](../../../docs/knowledge_layout.md) and [docs/knowledge_multiroot.md](../../../docs/knowledge_multiroot.md).
- If `KNOWLEDGE_ROOT` is **unset**, executors fall back to `data/` under the repo; for normal PM use, set the vault path and run [scripts/knowledge_gap_check.py](../../../scripts/knowledge_gap_check.py).

**Never** require users to expose secrets. Only path configuration goes in `.env` alongside existing vars (or document that paths are user-specific).

## Ongoing use (agents)

When answering questions that depend on **saved** PM files (not only first-time setup), run `python scripts/print_knowledge_paths.py` from the repo root to print resolved absolute paths (no secrets), then read the latest files under those directories. Use `src/pm_data_paths.py` as the canonical source for how paths are derived.

If the vault is configured but files are not visible in the editor, the user may need **File → Add Folder to Workspace** (vault root) or a multi-root workspace; see [docs/knowledge_multiroot.md](../../../docs/knowledge_multiroot.md) and [AGENTS.md](../../../AGENTS.md) (Local knowledge first).

## Setup steps (agent)

1. **Explain the split** briefly: repo = code + API rules; `KNOWLEDGE_ROOT` = markdown and PM working files for the harness.
2. **Ask** whether the root is an **Obsidian vault** or a **plain folder** (same for agents: it is just a directory).
3. **Ask for the absolute path** to the directory that should be the knowledge root (e.g. `/path/to/obsidian-vault` or `/path/to/portfolio`).
4. **Optional:** Ask for 1–2 **entry file paths** relative to that root (MOCs), e.g. `README.md`, `AhaAgent/README.md`—so agents that do not resolve `[[wikilinks]]` have explicit targets.
5. **Write** to `AHA_ROOT/.env`:
   - Append or set: `KNOWLEDGE_ROOT=/absolute/path` (no quotes unless the path has spaces; prefer no trailing slash).
   - If `.env` does not exist, copy from `.env.example` first and remind the user to set `AHA_API_KEY` separately.
6. **Validate** without printing the path in unsafe logs:
   - `Path(KNOWLEDGE_ROOT).is_dir()` must be true.
   - Optionally list one file under the root to confirm read access.
7. **Point** the user to `python scripts/check_env.py` and `python scripts/knowledge_gap_check.py` to confirm layout.
8. **Do not** read or depend on `.obsidian/` for correctness; Obsidian config is local UI only.

## Reconfiguration

To change the vault, replace `KNOWLEDGE_ROOT` in `.env` and re-run validation. Move or sync markdown in the new location as needed.
