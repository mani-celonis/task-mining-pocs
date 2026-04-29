---
name: aha-feature-suggestions
description: Pull and summarize Aha feature suggestions (Feature Suggestions workspace). Use when the user asks about assigned suggestions, exports, or counts. If the request is ambiguous, confirm whether to sync from Aha! into the knowledge root or use existing files only—see Operating modes.
allowed-tools: Bash Read Write Glob
---

# Aha Feature Suggestions

Use this skill to pull Aha feature suggestions from the Feature Suggestions workspace, save a dated local snapshot, and generate a readable summary—or to read and process the latest saved export without calling the API.

## Operating modes

| Mode | Name | Behavior |
|------|------|----------|
| **A** | **Sync from Aha!** | Run `aha_feature_suggestions.py`. Writes a new dated folder under `incoming/feature-suggestions/`. Use for **live** state, a **new** export, or when no snapshot exists. Requires `AHA_API_KEY`. |
| **B** | **Vault / local only** | Resolve paths (`python scripts/print_knowledge_paths.py`), read the **latest** `feature-suggestions-*.md` under the newest `YYYY-MM-DD` in `incoming_feature_suggestions_dir()`. **No** Aha API call unless the user switches to Mode A. Use for “what’s in my last export”, summarize/process saved data, offline, or “don’t hit Aha”. |

**Disambiguation:** If the user does **not** clearly choose a mode, **ask once** and wait:

> Do you want to **sync fresh from Aha!** into your knowledge root (new dated export), or **work from the latest saved export** in `KNOWLEDGE_ROOT` (no API call)?

**Skip the question** when intent is explicit:

- **Mode A cues:** “pull from Aha”, “refresh”, “sync”, “run the executor”, “new export”, “up-to-the-minute”, “live”
- **Mode B cues:** “from the vault”, “last export”, “what we saved”, “the file I have”, “don’t sync”, “offline”, “process my snapshot”

If they ask for a **specific** `SUGGESTION-I-*` and only Mode B can answer from files, use Mode B unless they asked for live verification.

## Defaults

- Assignee: `Frederik Chettouh`
- Output directory: **`$KNOWLEDGE_ROOT/incoming/feature-suggestions/`** when `KNOWLEDGE_ROOT` is set, else `data/feature-suggestions` (`incoming_feature_suggestions_dir()` in `src/pm_data_paths.py`)
- Workspace key: `SUGGESTION`

Read overrides from `.aha-config.yml` under `feature_requests:` when present.

## When to use

- User wants a count of assigned feature suggestions (confirm mode if ambiguous)
- User wants a saved snapshot of assigned feature suggestions (usually Mode A)
- User wants a readable summary (Mode B if last export is enough; Mode A if they need fresh data—confirm if unclear)
- User wants to inspect whether a specific `SUGGESTION-I-*` ref appears in **live** results (Mode A) or in the **last export** (Mode B)

## Workflow

0. **Choose mode** using Operating modes and Disambiguation above.
1. **Mode B:** Run `python scripts/print_knowledge_paths.py`, open the latest `feature-suggestions-*.md` under the newest date folder. Summarize or process from that file. Stop unless the user then asks to sync.
2. **Mode A:** Ensure `.env` contains `AHA_API_KEY`. Run:

```bash
python src/executors/aha_feature_suggestions.py
```

3. Optional filters:

```bash
python src/executors/aha_feature_suggestions.py --assignee "Frederik Chettouh" --status "In Review" --limit 20
```

4. After a Mode A run, summarize from the new markdown if the user wants a narrative summary.

The **local file** reflects the **last** API export; the **Aha API** is the source of truth for **live** state.

## Outputs

Each run saves (paths depend on `KNOWLEDGE_ROOT` and assignee slug):

- `$KNOWLEDGE_ROOT/incoming/feature-suggestions/YYYY-MM-DD/feature-suggestions-<assignee>.md` (and `.json`), or
- `data/feature-suggestions/YYYY-MM-DD/...` when the vault is unset

These files are local only; paths under the repo are gitignored. Vault paths are not committed from this repo.

## Guardrails

- Source of truth is the Aha API, not email notifications.
- Do not hardcode suggestion references into the implementation.
- This workflow is read-only. Never update Aha statuses, comments, or assignments.
