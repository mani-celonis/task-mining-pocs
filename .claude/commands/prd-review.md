You are facilitating a multi-perspective PRD review. The PRD will be evaluated by four reviewers — an Expert Product Manager, a CEO, an Engineering Lead, and a UX Designer — each bringing their own priorities and blind spots. Your job is to voice each perspective authentically, produce a structured report, and then synthesise the findings into a consolidated, prioritised list of improvements.

---

## Step 1 — Identify the PRD to review

If a filename or path was provided in the arguments below, use that. Otherwise, list the files in the `output/` directory using the Bash tool and ask the user which PRD they want to review.

$ARGUMENTS

---

## Step 2 — Read the PRD

Read the specified file using the Read tool. If the file does not exist, tell the user and stop.

---

## Step 3 — Run all four perspective reviews

Evaluate the PRD from each perspective in sequence using the criteria files below. For each check, assign ✅ / ⚠️ / ❌ with a brief inline note for any non-✅ result.

@.claude/config/strategy.md
@.claude/evals/prd-evals.md
@.claude/evals/prd-evals-ceo.md
@.claude/evals/prd-evals-eng.md
@.claude/evals/prd-evals-ux.md

---

## Step 4 — Produce the full review report

Output the report in the following structure. Use a distinct voice for each reviewer — the CEO is commercially blunt, the Engineering Lead is precise and risk-focused, the UX Designer is user-advocate and detail-oriented, the PM is holistic and process-oriented.

---

# PRD Review — `<filename>`
**Reviewed:** [today's date]

---

## 🗂 Product Manager Review

Show the full rubric table for each of the 5 PM categories (Completeness, Specificity, Consistency, Risk Coverage, Actionability) with ✅ / ⚠️ / ❌ and inline notes.

**PM Score:** [n]/21 — [Rating]

**PM Strengths:** 2–3 things done well from a PM perspective.

**PM Issues:**
List every ❌ and ⚠️ with a specific, one-line actionable note.

---

## 💼 CEO Review

Show the full rubric table for each of the 3 CEO categories (Business Case, Strategic Alignment, Executive Readability) with ✅ / ⚠️ / ❌ and inline notes.

**CEO Score:** [n]/10 — [Rating]

**CEO Perspective — key concern:** Write 2–4 sentences in the voice of the CEO summarising the single biggest concern and what would need to change for this PRD to earn executive buy-in.

**CEO Issues:**
List every ❌ and ⚠️ with a specific, one-line actionable note.

---

## ⚙️ Engineering Lead Review

Show the full rubric table for each of the 4 Engineering categories (Buildability, Technical Risk, Dependencies & Integration, Edge Cases) with ✅ / ⚠️ / ❌ and inline notes.

**Engineering Score:** [n]/13 — [Rating]

**Engineering Lead Perspective — key concern:** Write 2–4 sentences in the voice of the Engineering Lead summarising what would block or significantly slow implementation and what needs to be resolved before sprint planning.

**Engineering Issues:**
List every ❌ and ⚠️ with a specific, one-line actionable note.

---

## 🎨 UX Designer Review

Show the full rubric table for each of the 4 UX categories (Persona & User Understanding, User Flow Coverage, UI States, Design Constraints & Context) with ✅ / ⚠️ / ❌ and inline notes.

**UX Score:** [n]/13 — [Rating]

**UX Designer Perspective — key concern:** Write 2–4 sentences in the voice of the UX Designer summarising what would prevent them from starting design and what questions need answering first.

**UX Issues:**
List every ❌ and ⚠️ with a specific, one-line actionable note.

---

## 📊 Consolidated Summary

**Score overview:**

| Reviewer | Score | Rating |
|----------|-------|--------|
| Product Manager | [n]/21 | [rating] |
| CEO | [n]/10 | [rating] |
| Engineering Lead | [n]/13 | [rating] |
| UX Designer | [n]/13 | [rating] |

**Top issues across all perspectives** (ranked by impact — address these first):

List the most critical issues, ordered by how many reviewers flagged the same underlying gap and how much it would affect the PRD's usefulness. Where multiple reviewers flagged the same root cause (e.g. vague persona affects both UX and CEO sections), consolidate into a single issue and note which reviewers it affects.

| # | Issue | Affects | Priority |
|---|-------|---------|----------|
| 1 | [specific issue] | PM, CEO | High |
| 2 | [specific issue] | Eng | High |
| ... | | | |

---

## Step 5 — Offer to apply improvements

After delivering the report, ask:

"Would you like me to apply any of these improvements to the PRD directly? You can say 'apply all', name specific issue numbers (e.g. 'apply 1, 3, 5'), or describe what you want changed."

If the user asks for fixes:
1. Make all requested changes to the PRD content.
2. Re-run the full four-perspective evaluation on the updated draft.
3. Show only the delta — which checks moved from ❌/⚠️ to ✅, and if any new issues were introduced.
4. Ask the user to confirm before saving the updated file with the Write tool.
