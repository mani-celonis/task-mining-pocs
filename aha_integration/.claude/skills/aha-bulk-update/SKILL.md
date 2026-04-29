---
name: aha-bulk-update
description: Process task lists from AhaAgent/intake/ (under KNOWLEDGE_ROOT) or data/intake/ to bulk update Aha! Features or Epics. Use when the user says "run the task list", "execute intake", "bulk update features", or provides an intake file with field changes for named items.
allowed-tools: Bash Read Write Glob
---

# Aha! Bulk Update

The canonical instructions match **[`.cursor/skills/aha-bulk-update/SKILL.md`](../../../.cursor/skills/aha-bulk-update/SKILL.md)**. Summary:

- **Preferred location:** `$KNOWLEDGE_ROOT/AhaAgent/intake/` when `KNOWLEDGE_ROOT` is set in `.env`.
- **Fallback:** `data/intake/` in the repo. See `src/pm_data_paths.py` (`intake_dir()`).

## Implementation snippet

```python
from src.pm_data_paths import intake_dir
# ... read tasks from intake_dir() ...
```

Follow full workflow and guardrails in the Cursor skill file linked above.
