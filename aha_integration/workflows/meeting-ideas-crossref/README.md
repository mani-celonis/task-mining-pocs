# Workflow: Meeting Notes → Aha! Ideas Cross-Reference

Automatically surface relevant Aha! Ideas when processing meeting transcripts in Cursor, so customer feedback and discussion topics get linked to your backlog.

## What it does

When you paste a meeting transcript (or point to a transcript file), the AI assistant:

1. Generates a structured meeting note with summary, decisions, and action items
2. Extracts keywords from the discussion points
3. Queries the Aha! API to find Ideas matching those keywords in your product
4. Filters results by your Aha! Idea categories
5. Presents matched Ideas and asks which to link in the meeting note
6. Saves the note with a "Related Aha! Ideas" section containing clickable links

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Paste transcript │────▶│ AI generates     │────▶│ AI extracts     │
│ or reference     │     │ meeting note     │     │ keywords        │
│ a file           │     │ (summary, tags)  │     │ from discussion │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Meeting note     │◀────│ PM picks which   │◀────│ AI runs Aha!    │
│ saved with       │     │ Ideas to link    │     │ Ideas query via │
│ Aha! Idea links  │     │                  │     │ scratchpad      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## Prerequisites

- [AhaAgent](../../README.md) set up and working (venv, `.env` with API key)
- A Cursor workspace for your PM work
- Your Aha! product key and Idea categories

## How configuration works

All user-specific values (product key, team, products, categories) live in a single `.aha-config.yml` file at your workspace root. The Cursor rules and skills reference this config file at runtime — they are copied as-is from the templates in this directory and never need placeholder substitution.

```
.aha-config.yml          ← Your config (gitignored)
.cursor/rules/           ← Copies of templates (gitignored)
.cursor/skills/          ← Copies of templates (gitignored)
$KNOWLEDGE_ROOT/AhaAgent/ …  ← Your PM content in the vault (not in this repo)

workflows/meeting-ideas-crossref/   ← Shared templates (tracked in git)
.aha-config.example.yml             ← Reference schema (tracked in git)
```

## Quick Setup (recommended)

The setup wizard walks you through configuration interactively. It collects your Aha! product details, writes `.aha-config.yml`, copies all template files, and validates the API connection.

**Step 1:** Copy the setup skill into your workspace:

```bash
mkdir -p .cursor/skills/setup-aha-workflow
cp workflows/meeting-ideas-crossref/skill-setup-wizard.md .cursor/skills/setup-aha-workflow/SKILL.md
```

**Step 2:** Open Cursor and say:

> Set up my meeting ideas workflow

The AI will guide you through entering your product key, team, products, and Aha! categories, then generate all configured files automatically.

## Updating after a template change

When someone improves the templates (e.g. after a `git pull`), you don't need to re-enter your config. Just say:

> Update my meeting workflow

The wizard detects your existing `.aha-config.yml`, re-copies the latest templates, and only creates hub pages for any newly added products — your existing meeting notes and customer insights are preserved.

## Manual Setup (alternative)

If you prefer to configure files by hand, follow these steps.

### 1. Create your config file

Copy the example and fill in your values:

```bash
cp .aha-config.example.yml .aha-config.yml
```

Edit `.aha-config.yml` with your product key, team, products, and categories. See the example file for the schema.

### 2. Copy template files into your workspace

From this directory, copy the following files into your Cursor workspace:

| Source file | Copy to | Purpose |
|---|---|---|
| `cursor-rule-aha-agent.mdc` | `.cursor/rules/aha-agent.mdc` | Teaches the AI how to use the Aha! agent |
| `cursor-rule-product-tagging.mdc` | `.cursor/rules/product-tagging.mdc` | Ensures all content is product-tagged |
| `skill-meeting-notes.md` | `.cursor/skills/meeting-notes/SKILL.md` | The meeting-notes processing workflow |

These templates reference `.aha-config.yml` at runtime — no placeholder editing needed.

### 3. Set up the AhaAgent tool in your workspace

Clone or copy AhaAgent into your workspace at `tools/aha-agent/`:

```bash
# From your workspace root
git clone <this-repo-url> tools/aha-agent
cd tools/aha-agent
python3 -m venv aha-agent-venv
source aha-agent-venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set AHA_API_KEY=your_token
```

### 4. Create your vault folder structure and content files

Set `KNOWLEDGE_ROOT` in `tools/aha-agent/.env` to your Obsidian vault root, then:

```bash
ROOT="$KNOWLEDGE_ROOT"
mkdir -p "$ROOT"/AhaAgent/Meetings/Transcripts
mkdir -p "$ROOT"/AhaAgent/Products
mkdir -p "$ROOT"/Tasks
```

Create `AhaAgent/product-glossary.md` from your config values, and a hub page for each product at `AhaAgent/Products/<product>.md` (under the vault):

```markdown
# <Product Name>

## Meetings
- (links added automatically when meeting notes are processed)

## Customer insights
- (one-liners added when meetings contain customer feedback)

## Open tasks
- (links added when tasks are created)

## Completed tasks

## Knowledge
- (links to relevant knowledge files)
```

## Usage

Once set up, just paste a meeting transcript into Cursor chat or say "process this transcript" while referencing a file. The AI handles the rest, asking for confirmation at each step.

**Example prompt:**
> Log a meeting — here are the notes from today's customer feedback call: [paste transcript]

**What you'll get:**

```markdown
# Customer Feedback Call (Mar 3, 2026)
Tags: Product A, Product B

## Summary
...

## Related Aha! Ideas
- [PROD-I-42](https://celonis.aha.io/ideas/ideas/PROD-I-42) — Improve onboarding flow (In Review)
- [PROD-I-87](https://celonis.aha.io/ideas/ideas/PROD-I-87) — Bulk export feature (Planned)
```

## How the Ideas cross-reference works

The AI doesn't call a fixed script. Instead, it writes a tailored Python script to `src/executors/scratchpad.py` each time, using:

1. **Keywords** extracted from the meeting's discussion points and action items
2. **Your product key** from `.aha-config.yml`
3. **Your Idea categories** to filter results to your domain

The script imports helpers from `src/lib/aha_helpers.py` (`fetch_all_ideas`, `fetch_ideas_with_categories`, `build_idf`, `keyword_match`) so the per-meeting script stays short — it only contains the keywords and category filter, not pagination or matching boilerplate.

For one-off lookups during the conversation (e.g. "what's the status of OPER-I-321?"), the AI uses the read-only CLI instead: `python -m src.cli get /ideas/OPER-I-321`. No scratchpad write needed.

See `examples/crossref_ideas_example.py` for the reference implementation the AI adapts from.

## Customization tips

- **Add or remove products:** Edit `.aha-config.yml` directly, then say "update my meeting workflow" to regenerate. New products get hub pages automatically.
- **Add more keywords:** The AI extracts keywords from each meeting, but you can also ask it to include specific terms: *"Also look for Ideas about onboarding and data quality."*
- **Adjust categories:** Edit the `category` field for each product in `.aha-config.yml` to control which Aha! Idea categories are matched.
- **Skip cross-referencing:** If a meeting isn't relevant to your backlog, just tell the AI: *"Skip the Aha! Ideas step."*
- **Bulk cross-reference:** You can also ask the AI to cross-reference an existing meeting note after the fact: *"Find Aha! Ideas related to [meeting note file]."*
