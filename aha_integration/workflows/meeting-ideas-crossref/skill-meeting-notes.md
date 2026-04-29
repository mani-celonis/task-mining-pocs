---
name: meeting-notes
description: Process meeting notes and transcripts into structured summaries, extract tasks, and cross-reference Aha! Ideas. Use when the user says "log a meeting", "process this transcript", "meeting notes", pastes a transcript or notes blob, or references a file in AhaAgent/Meetings/Transcripts/ under KNOWLEDGE_ROOT.
---

# Meeting Notes

All paths below are under **`KNOWLEDGE_ROOT`** (set in `AhaAgent/.env`). If `KNOWLEDGE_ROOT` is unset, do not create repo-local `Knowledge/`; prompt the user to set the vault path (see external-knowledge skill in `.cursor/skills/`).

## Workspace layout

```
AhaAgent/Meetings/
├── <topic>-<date>.md
├── Transcripts/
│   └── <topic>-<date>.transcript.md
└── AI/
```

- Meeting notes: `AhaAgent/Meetings/<topic>-<YYYY-MM-DD>.md`
- Transcripts: `AhaAgent/Meetings/Transcripts/<topic>-<YYYY-MM-DD>.transcript.md`
- **Tasks / goals:** `Tasks/README.md` and `GOALS.md` at the **vault root** (siblings of `AhaAgent/`).

## Input handling

**Pasted in chat** or **file reference** under `AhaAgent/Meetings/Transcripts/`.

## Processing workflow

1. **Save transcript** to `AhaAgent/Meetings/Transcripts/<topic>-<date>.transcript.md`.
2. **Generate meeting note** in `AhaAgent/Meetings/<topic>-<date>.md`.
3. **Find related items:** scan `Tasks/README.md`, `AhaAgent/Meetings/`, and `GOALS.md` (vault root).
4. **Cross-reference Aha! Ideas** (see `.cursor/rules/aha-agent.mdc` and `examples/crossref_ideas_example.py`).
5. **Update product hubs** at `AhaAgent/Products/<product>.md`.
6. **Propose tasks** with confirmation.

(See the committed copy in [`.cursor/skills/meeting-notes/SKILL.md`](../../.cursor/skills/meeting-notes/SKILL.md) for the full template and guardrails.)
