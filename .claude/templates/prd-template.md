# PRD: [Feature/Initiative Title]

**Status:** Draft
**Author:** [Author]
**Last Updated:** [Today's date]
**Target Release:** [TO FILL]

---

## 1. Executive Summary

Write 3–5 sentences covering:
- The problem being solved
- The proposed solution at a high level
- The expected business and user impact

---

## 2. Problem Statement

**What problem are we solving?**
[Clear, specific description of the problem]

**Who has this problem?**
[Primary persona — role, company size, industry if relevant]

**Why is it painful?**
[Describe the friction, cost, or risk the problem creates today]

**Evidence**
[Customer quotes, support ticket themes, usage data, research findings. If not provided in input, write: "[TO FILL — add customer quotes or data here]"]

---

## 3. Goals & Success Metrics

**Business Goals**
[What business outcome does this drive? e.g., retention, expansion, acquisition]

**Metrics & Targets**

| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| [metric] | [baseline] | [goal] | [e.g., 90 days post-launch] |

**Market Opportunity**
[TAM/SAM/SOM if relevant, or a qualitative statement about the opportunity size. Mark [TO FILL] if unknown.]

**Competitive Landscape**
[How do competitors handle this? What's our differentiation? Mark [TO FILL] if unknown.]

**Why now?**
[What makes this the right time to build this — market signal, contract at risk, strategic priority, etc.]

---

## 4. Solution Overview

**High-Level Description**
[What are we building? Describe the solution in plain language, as if explaining to a customer.]

**User Flows**
[Describe the key flows step by step. If wireframes exist, note where they'd be attached. Otherwise describe the expected UI/UX behavior.]

**Key Features**
- [Feature 1 — brief description]
- [Feature 2 — brief description]
- [Feature 3 — brief description]

---

## 5. User Stories

For each user story, follow this format:

**Story [N]: [Short title]**
As a [persona], I want to [action] so that [outcome].

*Acceptance Criteria:*
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

*Edge Cases & Constraints:*
- [Edge case or constraint]

Write at least 3 user stories covering the primary happy path, a secondary persona or use case, and one edge/error case.

---

## 6. Out of Scope

List what is explicitly NOT being built in this iteration, with a brief rationale for each:

- **[Thing not being built]** — [Why: deferred to v2 / separate initiative / out of product scope / etc.]

---

## 7. Platform & Integration Context

**Platform layer(s) affected**
- [ ] Data Core — extraction, connectors, event log schema
- [ ] Process Intelligence Graph — business context, KPIs, rules, ML models, digital twin
- [ ] Build Experience — analysis views, apps, action flows, UI components

**Source systems in scope**
[List the enterprise systems this feature reads from or writes to, e.g. SAP ECC/S4, Salesforce, ServiceNow, Oracle, Workday. If none, write "N/A".]

**Process Intelligence Graph impact**
[Does this feature change the data model, extend the graph schema, or affect how business context (rules, KPIs, benchmarks) is represented? If yes, describe the change. If no, write "None".]

**AI / agentic implications**
[Does this feature enable, depend on, or interact with AI agents or multi-agent orchestration? If yes, describe the surface area. If no, write "None".]

**Strategic priority alignment**
Check all that apply:
- [ ] AI context layer — reinforces Celonis as the operational foundation for enterprise AI
- [ ] Visibility → action → orchestration — moves customers along the maturity curve
- [ ] Agentic AI readiness — supports AI agents using the Process Intelligence Graph
- [ ] Open ecosystem — works across any source system stack
- [ ] Operational readiness gap — reduces time-to-value or expertise barrier

---

## 8. Dependencies & Risks

**Technical Dependencies**
- [System, service, or API this relies on]

**External Dependencies**
- [Third-party integrations, partner commitments, data requirements]

**Internal Team Dependencies**
- [Other teams whose work is required: eng, design, data, legal, etc.]

**Risks & Mitigations**

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk description] | High/Med/Low | High/Med/Low | [Mitigation plan] |

---

## 9. Open Questions

List unresolved decisions or areas requiring further discovery before or during development:

- [ ] **[Question]** — Owner: [TO FILL] — Due: [TO FILL]
