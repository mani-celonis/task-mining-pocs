---
name: meeting-notes
description: Process meeting notes and transcripts into structured summaries, extract tasks, and cross-reference Aha! Ideas. Use when the user says "log a meeting", "process this transcript", "meeting notes", pastes a transcript or notes blob, or references a file in AhaAgent/Meetings/Transcripts/ under KNOWLEDGE_ROOT.
---

# Meeting Notes

All paths below are under **`KNOWLEDGE_ROOT`** (set in `AhaAgent/.env`). If `KNOWLEDGE_ROOT` is unset, do not create repo-local `Knowledge/`; prompt the user to set the vault path (see [external-knowledge](../external-knowledge/SKILL.md)).

## Workspace layout

```
AhaAgent/Meetings/
├── <topic>-<date>.md                    # Structured meeting note
├── Transcripts/
│   └── <topic>-<date>.transcript.md     # Raw transcript (linked)
└── AI/                                  # Legacy subfolder (keep as-is)
```

- Meeting notes: `AhaAgent/Meetings/<topic>-<YYYY-MM-DD>.md`
- Transcripts: `AhaAgent/Meetings/Transcripts/<topic>-<YYYY-MM-DD>.transcript.md`
- **Tasks / goals:** `Tasks/README.md` and `GOALS.md` at the **vault root** (siblings of `AhaAgent/`), not inside `AhaAgent/`.
- Dates in filenames (unlike tasks) because meetings are inherently time-bound.

## Input handling

Two modes:

**Pasted in chat** — user pastes notes, a transcript, or both directly in the conversation. Extract the raw transcript and any structured notes from the message.

**File reference** — user drops a file into `AhaAgent/Meetings/Transcripts/` (under the vault) or points to one already in the workspace. Read the file to extract content.

## Processing workflow

1. **Save transcript**: if a raw transcript is provided, save it to `AhaAgent/Meetings/Transcripts/<topic>-<date>.transcript.md`.
2. **Generate meeting note**: create a structured note in `AhaAgent/Meetings/<topic>-<date>.md` using the template below.
3. **Find related items**: scan `Tasks/README.md`, `AhaAgent/Meetings/`, and `GOALS.md` (vault root) for overlapping topics (people, products, goals). Populate the "Related" section.
4. **Cross-reference Aha! Ideas**: use the Aha! agent (see `.cursor/rules/aha-agent.mdc`) to find backlog items related to the meeting. This helps the PM link customer insights and discussion topics to the right Ideas.

   **How to cross-reference:**

   a. Map the meeting's product tags to Aha! Idea categories using the `products[].category` mapping from `.aha-config.yml`.

   b. Write a scratchpad script that fetches Ideas from your product (read `product_key` from `.aha-config.yml`) filtered to matching categories, then does keyword matching against the meeting's key discussion points and action items. **Import helpers from [src/lib/aha_helpers.py](../../src/lib/aha_helpers.py) so the script stays short** — `fetch_all_ideas` for the list pass, `fetch_ideas_with_categories` for the throttled detail pass, and `build_idf` + `keyword_match` if you want IDF-weighted ranking. See `workflows/meeting-ideas-crossref/examples/crossref_ideas_example.py` for a reference implementation.

   For one-shot Aha! lookups along the way (e.g. "what's the status of OPER-I-321?"), use `python -m src.cli get /ideas/{ref}` instead of writing a scratchpad.

   c. Present the top matches (max 10) with ref, name, status, and a brief note on why it matched. Ask the user which ones to include in the "Related Aha! Ideas" section.

   d. If the meeting contains customer feedback, suggest adding the customer name and insight to those Ideas (the user can do this manually in Aha! or ask you to update via the API).

5. **Update product hubs**: for each product tag on the meeting note, update the corresponding `AhaAgent/Products/<product>.md` hub:
   - Add a link under "Meetings".
   - If the meeting contains customer feedback or notable product insights, also add a one-line summary under "Customer insights".
   - If the meeting references a file that isn't yet listed in the hub's "Knowledge" section, add it there too.
6. **Propose tasks**: extract action items from the notes. Use the task-management skill's guardrails to propose tasks — confirm before creating, check for duplicates, ask for due dates and tags.

## Meeting note template

```markdown
# <Topic> (<Mon DD, YYYY>)
Tags: <product tags>

## Participants
- <Name> (<role/team>)

## Transcript
→ [Full transcript](Transcripts/<topic>-<date>.transcript.md)

## Summary
<2-4 sentence overview>

## Key discussion points
- ...

## Decisions
- ...

## Action items
- [ ] <Person>: <action>

## Related
- [<Existing task or meeting>](relative-link)

## Related Aha! Ideas
- [{product_key}-I-XXX](https://celonis.aha.io/ideas/ideas/{product_key}-I-XXX) — <Idea name> (<status>)
```

Read `product_key` from `.aha-config.yml` when generating the Aha! Ideas links.

If no transcript was provided, omit the Transcript section entirely.

**Important:** When transcript filenames contain spaces, URL-encode them in the Markdown link (replace spaces with `%20`). Filenames with hyphens don't need encoding.

## Product tags

Valid tags from **`AhaAgent/product-glossary.md`** and `.aha-config.yml` (`products[].name`). Use `—` when no product applies.

**Multi-tag by default** — A meeting often touches multiple products. Tag all products discussed, not just the primary one.

## Guardrails — always confirm before acting

Use the `AskQuestion` tool (structured choices) when available. Otherwise ask conversationally. Batch related questions into a single ask.

### Before saving the meeting note

- Present a draft summary to the user and ask for confirmation before writing the file.
- If the transcript is very long (>500 lines), ask: *"The transcript is quite long. Should I store it as a separate file, or skip saving it?"*

### When proposing tasks

- List extracted action items and ask which should become tasks: *"I found these action items. Which should become tasks?"*
- For each confirmed task, follow the task-management skill's guardrails (duplicate check, ask for due date/priority/tags).

### When linking related items

- Suggest related links based on scanning the workspace, but confirm: *"This seems related to [existing item]. Should I link them?"*
- Don't silently add links the user hasn't seen.

### When cross-referencing Aha! Ideas

- Present matched Ideas as a numbered list with ref, name, status, and why it matched.
- Ask which ones to include in the meeting note: *"I found these Aha! Ideas that seem related. Which should I link in the meeting note?"*
- If the meeting contains customer feedback relevant to a matched Idea, flag it: *"This feedback from [customer] seems relevant to [Idea]. Want me to note this on the Idea or just link it in the meeting note?"*
- Don't update Ideas in Aha! without explicit confirmation.

### General principle

Never silently save a meeting note or create tasks from it. Always present, confirm, then act.
