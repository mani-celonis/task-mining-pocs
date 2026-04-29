---
name: meeting-notes
description: Process meeting notes and transcripts into structured summaries, extract tasks, and cross-reference Aha! Ideas. Use when the user says "log a meeting", "process this transcript", "meeting notes", pastes a transcript or notes blob, or references a file in AhaAgent/Meetings/Transcripts/ under KNOWLEDGE_ROOT.
allowed-tools: Bash Read Write Glob
---

# Meeting Notes

The canonical instructions match **[`.cursor/skills/meeting-notes/SKILL.md`](../../../.cursor/skills/meeting-notes/SKILL.md)** (same content). Summary:

- All paths are under **`KNOWLEDGE_ROOT`**: `AhaAgent/Meetings/`, `AhaAgent/Products/`, `AhaAgent/product-glossary.md`; `Tasks/`, `GOALS.md` at vault root.
- No repo-local `Knowledge/` folder.

Read the Cursor skill file above for the full template, product tagging, and guardrails.
