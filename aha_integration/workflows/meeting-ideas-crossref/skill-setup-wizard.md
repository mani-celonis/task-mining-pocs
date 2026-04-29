---
name: setup-aha-meeting-workflow
description: Interactive guided setup for the Meeting Notes to Aha! Ideas cross-reference workflow. Use when the user says "set up meeting ideas workflow", "configure Aha! integration", "set up meeting notes", "update my meeting workflow", or wants to connect their workspace to Aha! Ideas.
---

# Setup Wizard: Meeting Notes → Aha! Ideas

This skill walks a PM through configuring their Cursor workspace so that meeting transcripts are automatically cross-referenced with Aha! Ideas.

All user-specific values are stored in `.aha-config.yml`. Templates reference this config file and are copied as-is — no placeholder substitution is needed.

## Trigger

Run this setup when the user asks to set up, configure, or update the meeting-ideas workflow, or when you detect that `tools/aha-agent/` exists but `.aha-config.yml` does not.

## Setup workflow

### Phase 1: Check prerequisites

Before collecting any config, verify the environment:

1. **Aha! agent repo**: check that `tools/aha-agent/src/api/client.py` exists. If not, tell the user:
   > The Aha! agent isn't set up yet. Clone it into your workspace:
   > ```
   > git clone <repo-url> tools/aha-agent
   > cd tools/aha-agent && python3 -m venv aha-agent-venv
   > source aha-agent-venv/bin/activate && pip install -r requirements.txt
   > ```
   > Let me know when done.

   Wait for the user to confirm before continuing.

2. **Python venv**: check that `tools/aha-agent/aha-agent-venv/bin/activate` exists. If not, guide the user to create it.

3. **API key**: check that `tools/aha-agent/.env` exists and contains `AHA_API_KEY`. Do NOT ask the user to paste the key in chat. If `.env` is missing:
   > Create `tools/aha-agent/.env` with your Aha! API key:
   > ```
   > cp tools/aha-agent/.env.example tools/aha-agent/.env
   > ```
   > Then edit `.env` and set `AHA_API_KEY=<your-token>`.
   > You can find your token at: Aha! → Settings → Personal → Developer → API key.
   > Let me know when done.

   Wait for the user to confirm before continuing.

### Phase 2: Detect existing setup

Check for three scenarios and branch accordingly:

**Scenario A — Fresh install:**
Neither `.aha-config.yml` nor `.cursor/rules/aha-agent.mdc` exists. Proceed to Phase 3 (collect config).

**Scenario B — Legacy install (migration):**
`.cursor/rules/aha-agent.mdc` exists with baked-in values (contains a line like `**Product key:** \`OPER\`` rather than a reference to `.aha-config.yml`) but `.aha-config.yml` does not exist.

Migrate automatically:

1. Parse the existing `.cursor/rules/aha-agent.mdc`:
   - Extract `product_key` from the `**Product key:**` line
   - Extract `team` from the `**Team:**` line
   - Extract category names from the `**Idea categories:**` line

2. Parse `AhaAgent/product-glossary.md` if it exists:
   - Extract product names and descriptions from the "Current products" section
   - Extract legacy products from the "Legacy products" section if present

3. Parse `.cursor/skills/meeting-notes/SKILL.md` if it exists:
   - Extract the tag-to-category mapping table to determine which product tag maps to which Aha! Idea category

4. Build the `.aha-config.yml` from extracted values. If product descriptions or tag-to-category mappings cannot be found, ask the user to fill in the gaps.

5. Show the user what was extracted:
   > I found an existing setup and extracted your config:
   > - Product key: `{product_key}`
   > - Team: `{team}`
   > - Products: {list of product names}
   > - Categories: {list of categories}
   >
   > I'll save this to `.aha-config.yml` and update your rules/skills to use the new config-file approach. OK?

6. After confirmation, write `.aha-config.yml` and proceed to Phase 4 (generate files).

**Scenario C — Existing config (update mode):**
`.aha-config.yml` already exists. Read it and ask:

> I found your existing config ({product_key} / {team} / {N} products). What would you like to do?

Use `AskQuestion` with options:
- **Regenerate from latest templates** — keeps your config, re-copies the latest template files
- **Reconfigure from scratch** — re-enter all values and overwrite config

If regenerate: skip Phase 3, proceed to Phase 4.
If reconfigure: proceed to Phase 3.

### Phase 3: Collect configuration

Ask conversationally (not AskQuestion, since these are free-text):

**Batch 1 — Aha! workspace details:**
- "What is your Aha! **product key**? (e.g. `OPER`, `AIMODULES` — you can find it in your Aha! product URL: `https://celonis.aha.io/products/<KEY>/...`)"
- "What is your **team name** in Aha!? (e.g. `074_Phoenix` — this is the custom field value used to filter. Leave blank if not applicable.)"
- "What is your **Aha! login email**? (e.g. `j.moelich@celonis.com` — used to filter Feature Suggestions assigned to you)"

**Batch 2 — Products and categories:**
- "List your **products** (the things you own as a PM), one per line, with a short description. These become your product tags and glossary entries. Example:
  ```
  Tasks: Operational tasks for approvals, manual input, or decisions
  Triggers: Auto-detect items meeting criteria to execute automations
  ```"
- "List the **Aha! Idea categories** that map to your products. These are used to filter Ideas during cross-referencing. If your category names match your product names exactly, just say 'same as products'. Otherwise list the mapping:
  ```
  Tasks → Tasks
  Triggers → Triggers
  Comments → Commenting
  ```"

**Batch 3 — Feature Suggestions (optional):**
- "Feature Suggestions typically live under the `SUGGESTION` product key with workflow status `In Review`. Does that match your workspace? (If different, provide your product key and status name.)"

If the user confirms defaults, use `product_key: SUGGESTION` and `review_status: "In Review"`. If they provide custom values, use those instead.

**Write `.aha-config.yml`** from the collected values:

```yaml
product_key: {PRODUCT_KEY}
team: "{TEAM}"
user_email: "{USER_EMAIL}"

products:
  - name: {product1.name}
    description: "{product1.description}"
    category: {product1.category}
  # ... one entry per product

legacy_products:
  - name: {legacy1.name}
    description: "{legacy1.description}"
  # ... only if user mentioned legacy products

suggestion_portal:
  product_key: SUGGESTION
  review_status: "In Review"
```

### Phase 4: Generate files

Present a summary of what will be created/updated and ask for confirmation before writing.

**1. `.cursor/rules/aha-agent.mdc`**

Copy the template from `workflows/meeting-ideas-crossref/cursor-rule-aha-agent.mdc` as-is (it references `.aha-config.yml` — no placeholder substitution needed).

**2. `.cursor/rules/product-tagging.mdc`**

Copy the template from `workflows/meeting-ideas-crossref/cursor-rule-product-tagging.mdc` as-is.

**3. `.cursor/skills/meeting-notes/SKILL.md`**

Copy the template from `workflows/meeting-ideas-crossref/skill-meeting-notes.md` as-is.

**4. `AhaAgent/product-glossary.md`** (first setup only)

Only generate if the file does not already exist:

```markdown
# Product glossary ({TEAM or domain name})

## Current products

{for each product in config.products}
{product.name}: {product.description}
{end for}
```

Add a "## Legacy products" section only if `legacy_products` is present in the config.

**5. `AhaAgent/Products/{product.name}.md`** (incremental)

On first setup, create a hub page for each product. On update, only create pages for products that don't already have one (compare `products[].name` in config against existing files in `AhaAgent/Products/`). Never overwrite an existing hub page.

```markdown
# {product.name}

## Meetings

## Customer insights

## Open tasks

## Completed tasks

## Knowledge
```

### Phase 5: Create directory structure

Paths are under **`$KNOWLEDGE_ROOT`** (the vault). If `KNOWLEDGE_ROOT` is unset, stop and have the user set it (see `docs/knowledge_layout.md`).

```bash
ROOT="${KNOWLEDGE_ROOT:?set KNOWLEDGE_ROOT in .env}"
mkdir -p "$ROOT"/AhaAgent/Meetings/Transcripts
mkdir -p "$ROOT"/AhaAgent/Products
mkdir -p "$ROOT"/Tasks
```

### Phase 6: Validate API connection

Use the read-only CLI to verify the connection — no scratchpad needed. Read `product_key` from `.aha-config.yml` and run:

```bash
python -m src.cli get /products/{product_key}/ideas --param per_page=1 --param page=1
```

Confirm the response includes `pagination.total_records` and at least one Idea (or zero if the product is genuinely empty). If the call fails, help the user troubleshoot (wrong product key, invalid API key, network issues).

### Phase 7: Confirm completion

Summarize what was created:

> Setup complete. Here's what I configured:
>
> - `.aha-config.yml` — your workspace config (product: {product_key}, {N} products, user: {user_email})
> - `.cursor/rules/aha-agent.mdc` — Aha! agent integration
> - `.cursor/rules/product-tagging.mdc` — product tagging
> - `.cursor/skills/meeting-notes/SKILL.md` — meeting notes workflow
> - `AhaAgent/product-glossary.md` — product definitions
> - `AhaAgent/Products/` — {N} product hub pages
> - Validated API connection: {total} ideas found
>
> Try it out:
> - Paste a recent meeting transcript and say "log a meeting"
> - Say "review suggestions" to see Feature Suggestions assigned to you

## Updating after a template change

When templates in `workflows/meeting-ideas-crossref/` are updated (e.g. after a `git pull`), the user can say "update my meeting workflow" to trigger this wizard. It detects `.aha-config.yml` (Scenario C), offers to regenerate, and re-copies the latest templates without re-entering any config values.

## Reconfiguring products

If the user wants to add or remove products, they can either:
- Edit `.aha-config.yml` directly and say "update my meeting workflow" to regenerate
- Say "reconfigure meeting workflow" to re-enter all values from scratch
