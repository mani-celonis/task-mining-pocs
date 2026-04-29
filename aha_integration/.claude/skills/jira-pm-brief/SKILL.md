---
name: jira-pm-brief
description: Produce a local PM brief from Jira data—categorized themes, user-facing outcomes, Celonis product mapping, priority, value/delivery risks. Use when the user wants an engineering team overview without reading dozens of tickets, a roadmap-sync brief, or a PM-facing Jira summary.
allowed-tools: Bash Read Write Glob
---

# Jira PM brief (local, not committed)

The canonical instructions match **[`.cursor/skills/jira-pm-brief/SKILL.md`](../../../.cursor/skills/jira-pm-brief/SKILL.md)**. Default Markdown output: **`$KNOWLEDGE_ROOT/AhaAgent/jira-briefs/`** when `KNOWLEDGE_ROOT` is set; else `data/jira-briefs/` via `jira_pm_brief_generate.py` and `src/pm_data_paths.py`.
