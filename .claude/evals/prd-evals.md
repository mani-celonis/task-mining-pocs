# PRD Evaluation Criteria

Use this rubric to evaluate a PRD. For each check, assign a status:
- ✅ Pass — criterion is clearly met
- ⚠️ Partial — criterion is partially met or could be stronger
- ❌ Fail — criterion is missing or not met

---

## 1. Completeness

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1.1 | All 8 sections are present | | |
| 1.2 | No unexplained `[TO FILL]` placeholders remain | | |
| 1.3 | At least 3 user stories are written | | |
| 1.4 | At least one metric has a baseline and a target | | |
| 1.5 | At least one item is listed in Out of Scope | | |
| 1.6 | At least one open question is listed | | |

---

## 2. Specificity

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 2.1 | Problem statement names a specific persona (role, context) — not "users" generically | | |
| 2.2 | Evidence section includes at least one concrete data point or customer quote | | |
| 2.3 | Success metrics are measurable — each has a number, not just a direction (e.g. "reduce churn by 10%", not "reduce churn") | | |
| 2.4 | "Why now?" provides a concrete business reason — not a generic statement | | |
| 2.5 | Key features describe behaviour, not just names (e.g. "users can filter by date range" not "date filter") | | |
| 2.6 | Each acceptance criterion is testable — a QA engineer could verify it | | |

---

## 3. Consistency

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 3.1 | The solution directly addresses the problem stated in Section 2 | | |
| 3.2 | User stories cover all key features listed in Section 4 | | |
| 3.3 | Out of Scope items do not contradict features listed as in scope | | |
| 3.4 | Risks table addresses at least the dependencies listed in Section 7 | | |
| 3.5 | Success metrics in Section 3 align with the business goals stated | | |

---

## 4. Risk Coverage

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 4.1 | At least one technical risk is identified | | |
| 4.2 | Each risk has a mitigation (not just acknowledged) | | |
| 4.3 | Edge cases in user stories include at least one error or failure scenario | | |
| 4.4 | Key assumptions that could invalidate the approach are surfaced | | |

---

## 5. Actionability

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 5.1 | Open questions identify what decision is needed, not just what is unknown | | |
| 5.2 | Dependencies name specific teams, systems, or partners — not generic references | | |
| 5.3 | The Executive Summary is understandable to a non-technical stakeholder | | |
| 5.4 | A new engineer joining the team could understand what to build from this document | | |

---

## Scoring

Count the results across all 21 checks:

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 19–21 ✅ | Excellent | Ready to share with stakeholders |
| 15–18 ✅ | Good | Minor gaps — address ⚠️ items before sharing |
| 10–14 ✅ | Needs work | Significant gaps — resolve ❌ items before proceeding |
| < 10 ✅ | Insufficient | Major revision required |

List all ❌ and ⚠️ items with specific, actionable improvement notes.
