---
name: aha-feature-suggestions-review
description: >-
  Fetch Aha! Feature Suggestions assigned to the current PM in "In Review"
  status, cross-reference against the PM's product backlog, and produce a
  recommendation report with suggested portal status, requestor-facing comment
  drafts, and optional clarification questions. Act as chief of staff: ask the
  PM when missing information blocks a sound recommendation. Use when the user
  says "review suggestions", "feature suggestions", "open suggestions",
  "suggestion inbox", or "suggestion review".
---

# Feature Suggestion Review

Fetch all Feature Suggestions assigned to the PM, cross-reference with the product backlog, and generate a recommendation report. Map each item to the **suggestion portal’s workflow statuses**, draft **concise requestor-facing comments** for every transition, and **ask the PM** whenever missing context would make the recommendation unreliable.

## Prerequisites

Check `.aha-config.yml` before running the executor. Three branches:

**No config file at all** — Point the user to the [onboarding skill](../onboarding/SKILL.md):
> You don't have a `.aha-config.yml` yet. Say "onboard" or "first-time setup" to create one.

**Config exists but missing fields** — If `user_email` or `suggestion_portal` is absent, run a micro-setup inline:

1. If `user_email` is missing, ask conversationally:
   - "What is your Aha! login email? (e.g. `your.name@celonis.com`)"
2. If `suggestion_portal` is missing, confirm defaults:
   - "Feature Suggestions typically live under product key `SUGGESTION` with status `In Review`. Is that correct for your workspace?"
3. Append the collected values to `.aha-config.yml` and confirm the update with the user.

**All fields present** — Proceed to the workflow.

Also verify `AHA_API_KEY` is set in `.env`. If not, instruct the user to edit `.env` locally (never ask for the key in chat).

## Suggestion portal statuses (workflow)

New requests arrive in **In Review**. From there, the PM may move a suggestion to one of the following (exact labels must match the Aha! workspace; treat this list as the canonical intent):

| Status | When to use |
|--------|-------------|
| **Need More Info** | The team needs additional detail from the requestor before the request can be understood, sized, or prioritized. |
| **Planned Next 3 Months** | Implementation is realistically planned within the next three months—typically because a linked **epic or feature** (or promoted idea) is already on the roadmap in that window. |
| **Not Planned Next 3 Months** | The idea is accepted and valued, but **no** delivery inside the next three months (e.g. a linked epic/feature exists but ships later, or work is not yet scheduled). |
| **Declined** | The request does not add enough value **for now** to pursue; use sparingly and with clear, respectful rationale. |
| **Delivered** | The capability requested has been shipped and matches what was asked. |

**Other actions (not necessarily a terminal “resolution” status):**

- Leave **In Review** while still deciding or doing internal follow-up.
- **Reassign** to another team when they are better suited to own the request (note in the report who/which area, if known).

When recommending a status, **name the status explicitly** and briefly justify it against this table.

## Quick lookups during review

While running this skill you'll often need to spot-check a single record (a backlog match's status, a linked epic's target dates, an Idea's full description). Use the read-only CLI instead of writing a scratchpad for one-off reads:

```bash
python -m src.cli get /ideas/SUGGESTION-I-2093
python -m src.cli get /epics/OPER-E-1234
python -m src.cli get /products/OPER/features --param q=migration --param per_page=10
```

JSON goes to stdout, so you can pipe through `jq` for filtering. Keep the scratchpad pattern for the comment-posting step (step 8) where deliberation is required.

## Chief of staff: query the PM when stuck

Act as the PM’s chief of staff. **Pause the “final” recommendation** and ask **specific, answerable questions** whenever the data from the executor is not enough to choose a status or message responsibly. Examples of when to query (not exhaustive):

- You cannot tell whether work is **inside vs. outside the next three months** without roadmap or epic dates the JSON does not contain.
- **Which OPER (or other) record** should be cited in the public comment (e.g. “already tracked as OPER-I-XXX”) is ambiguous between several backlog matches.
- **Ownership** is unclear (Phoenix vs. another team)—reassign vs. keep needs the PM’s call.
- **Decline vs. defer** hinges on product strategy or customer commitments you should not invent.
- **Delivered** would require confirmation that the shipped feature matches the suggestion.

Keep questions **short and grouped** (e.g. bullet list per suggestion ref). After the PM answers, **complete** the report with suggested status + drafts. If they prefer to defer some items, note what remains open.

## Workflow

1. **Run the executor** from the repo root (with `required_permissions: ["all"]`):
   ```bash
   python src/executors/suggestion_review.py
   ```
   Use `python3` if `python` is not on PATH. Progress messages go to stderr; the final JSON report goes to stdout.

2. **Handle errors** — If the executor exits non-zero, read stderr:
   - Missing config fields → trigger the micro-setup above, then re-run
   - API errors → help the user troubleshoot (wrong product key, expired token, etc.)
   - Zero results → suggest verifying `review_status` in `.aha-config.yml`

3. **Parse the JSON output** — The executor returns:
   ```json
   {
     "user_email": "...",
     "product_key": "...",
     "suggestion_portal": "...",
     "review_status": "...",
     "suggestions": [ ... ],
     "backlog_item_count": 0
   }
   ```
   Each suggestion has: `ref`, `name`, `description`, `url`, `status`, `created_by`, `votes`, `categories`, `linked_records`, `backlog_matches`, `category_overlap`, `has_enough_context`.

4. **Assess gaps** — Before writing final prose, decide if **chief-of-staff questions** to the PM are needed (see section above). If yes, ask them first (or interleave: show partial report + questions for blocked items only).

5. **Generate the report** — For each suggestion, produce:
   - A **recommendation paragraph** considering: description quality (`has_enough_context`), votes, `linked_records`, `backlog_matches`, `category_overlap`, and PM-supplied answers from step 4.
   - A **suggested status** from the portal status table (or **In Review** / **Reassign to …** with rationale).
   - A **draft requestor-facing comment** (see next section)—**always**, for the suggested status transition.

6. **Draft “Need More Info” detail (when applicable)** — If the suggested status is **Need More Info** (or the recommendation is “clarify first”), include a **concise** opening in the public comment (per below), and optionally a **follow-up HTML block** for structured questions (still do **not** post until approved):
   ```html
   <p>Thank you for this suggestion. To help us evaluate it, could you provide more detail on:</p>
   <ul>
     <li>How are you handling this today, and what's not working?</li>
     <li>What would a great solution look like to you?</li>
   </ul>
   ```

7. **Present the report** using the output template below.

8. **Post comments (only with approval)** — If the user approves drafts, write a scratchpad script to `src/executors/scratchpad.py` that posts them:
   ```python
   client.post(f"/ideas/{numeric_id}/comments", data={"comment": {"body": "<p>...</p>"}})
   ```
   Run with `required_permissions: ["all"]` after explicit user confirmation. Use `python -m src.cli get /ideas/{ref}` to verify state before and after if helpful. Status changes in Aha! remain **manual** unless the user asks for automation elsewhere.

## Requestor-facing comment on every status change

Whenever a suggestion moves **from In Review to any other status** (or when reassigning with a handoff note), the team **always** leaves a **concise** requestor-facing comment: warm, specific, and **non-defensive**. Length: roughly **two to four sentences**, unless **Need More Info** also includes the short HTML follow-up above.

**Tone:** Thank them; state the outcome (roadmap window, deferral, decline, shipped, more detail needed, or handoff); optionally offer a follow-up (e.g. ping when work starts).

**Examples (adapt names and refs; do not copy blindly):**

- **Planned Next 3 Months:**  
  *“Thanks for raising this — it’s already on our roadmap as part of OPER-I-XXX, and we expect to start work within the next few months. Happy to reach out when we kick off.”*

- **Not Planned Next 3 Months:**  
  *“Thanks for the clear write-up — we’re not planning this in the next three months, though we’ve captured it for a later cycle. I’ll update this idea if priorities shift.”*

- **Need More Info:**  
  *“Thanks — we’d like to take this seriously and need a bit more detail to size it. Could you share [one concrete ask]? I’ve listed a few prompts below.”*  
  *(then optional HTML list)*

- **Declined:**  
  *“Thanks for submitting this. We’re not planning to pursue this right now because [brief, respectful reason]. We really appreciate you taking the time to suggest improvements.”*

- **Delivered:**  
  *“Thanks for this suggestion — we’ve shipped [capability] in [release/product area]. Let us know if this covers what you had in mind.”*

- **Reassign / handoff:**  
  *“Thanks — this fits best with [team/product area]. I’m moving this to [owner/team] so they can respond directly.”*

Include these as **`Draft public comment (HTML-friendly)`** in the report (single `<p>…</p>` or `<p>` + `<ul>` as needed). Do **not** post without approval.

## Output template

Present the report in this format (use a real markdown report in chat; nested HTML lives in its own fenced block per field below):

````markdown
# Feature Suggestion Review — {date}

**Suggestions in review:** {count} | **Backlog items checked:** {backlog_item_count}

---

## {ref}: {name}
**Submitted by:** {created_by} | **Votes:** {votes} | **Categories:** {categories}
**Link:** {url}

**Description:**
> {description (truncated to ~200 words)}

**Already linked:**
- {linked_record.ref} — {linked_record.name} ({linked_record.link_type})  *(or "None")*

**Potential backlog matches:**
- {backlog_match.ref} — {backlog_match.name} (score: {match_score})

**Suggested status:** {Need More Info | Planned Next 3 Months | Not Planned Next 3 Months | Declined | Delivered | In Review | Reassign to …}
**Status rationale:** {1–3 sentences}

**Recommendation:**
{Agent-generated paragraph}

**Draft public comment (HTML-friendly):**
```html
<p>...</p>
```

{If chief-of-staff questions were needed for this item and are still open:}
**Open questions for PM:**
- ...

{If structured follow-up is useful (e.g. Need More Info):}
**Draft follow-up — structured questions (optional HTML):**
```html
<p>...</p><ul><li>...</li></ul>
```

---
(repeat for each suggestion)
````

If the entire run is **blocked** on PM input, lead with a short **“Questions before I finalize”** section, then partial bullets per `ref`.

## Guardrails

- **Read-only by default.** The executor only performs GET requests. No records are created or modified.
- **Comments require approval.** Never post comments to Aha! without the user explicitly approving each one. Present drafts, wait for confirmation, then execute via scratchpad.
- **No secrets in chat.** Never ask for or display `AHA_API_KEY`. Point the user to edit `.env`.
- **Config is the source of truth.** All identity and product context comes from `.aha-config.yml`. Never hardcode product keys, emails, or status names **except** where the PM has documented workspace conventions in this skill; if Aha! labels differ slightly, follow the workspace and adjust wording.
- **Do not invent roadmap dates or commitments.** Ask the PM when the three-month window or linked epic is unclear.

## Related

- [onboarding](../onboarding/SKILL.md) — first-time setup (creates `.aha-config.yml`)
- [aha-bulk-update](../aha-bulk-update/SKILL.md) — bulk update features/epics from task lists
- [meeting-notes](../meeting-notes/SKILL.md) — cross-reference meeting topics with Ideas
- [docs/aha_api_notes.md](../../../docs/aha_api_notes.md) — API reference
