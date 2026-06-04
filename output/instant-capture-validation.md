# PRD: Instant Capture & Data-Quality Validation (Task Mining Onboarding)

**Status:** Draft
**Author:** Task Mining PM
**Last Updated:** 2026-06-04
**Target Release:** FY27 — onboarding redesign (controlled pilot first)

> **Purpose of this doc:** This is a prototype-ready spec. Sections 1–9 follow the standard PRD template; Section 10 contains the screen plan to feed directly into `/prototype`. Scope is intentionally framed for **low-fidelity mockups** — flows and states matter more than backend fidelity.

---

## 1. Executive Summary

Task Mining adoption stalls at the very first step: customers must install a client, configure capture, wait days for data to land, and only then discover whether the data is usable, compliant, and joinable to their processes. This is slow, opaque, and forces a privacy leap-of-faith before any value is seen.

This initiative **drastically simplifies data capturing into a self-serve, test-it-yourself moment**. A customer can validate capture in **two ways**: download the lightweight Task Mining client, **or** run capture instantly in the browser via a **browser extension** — no IT ticket, no waiting. As they record their own applications, the experience **scans live** for (a) **PII / GDPR exposure** (what will be masked and why), and (b) **case IDs and the business objects** they map to (which apps yield which IDs, which objects are covered, and which *could* be covered with additional context such as Process Mining data).

The outcome: a customer **sees and validates data quality, compliance, and process-joinability within minutes** of starting — turning onboarding from a blind setup task into a confidence-building, "aha" validation moment.

---

## 2. Problem Statement

**What problem are we solving?**
Onboarding is the highest-friction, lowest-confidence part of the Task Mining journey. Customers cannot answer three critical questions *before committing*: (1) Is this compliant — what PII gets captured/masked? (2) Is the data good — can it identify the case IDs and objects I care about? (3) Will it actually join to my processes? Today these answers arrive only after deployment, configuration, and a multi-day data-landing delay.

**Who has this problem?**
- **Primary — Carter (CoE Lead):** Owns Task Mining adoption; must prove, fast, that capture produces usable, joinable data before scaling to users.
- **Secondary — Ian (IT Lead / privacy gatekeeper):** Will not approve rollout without seeing exactly what PII is captured and how masking behaves.
- **Secondary — Andre (Data Analyst):** Needs early confidence that captured apps yield the case IDs/objects required for downstream Task Discovery and PiG enrichment.

**Why is it painful?**
- **Trust gap:** Privacy concerns block deployment; "trust us, we mask PII" is not enough for regulated buyers (GDPR/SOC/ISO).
- **Blind setup:** Customers configure capture scope without knowing what each app actually contributes.
- **Slow time-to-confidence:** Days between install and the first signal of whether data is good — and rework when it is not.
- **Joinability uncertainty:** No early visibility into whether captured IDs map to the objects (invoice, order, ticket) that make Task Mining valuable when joined to Process Mining.

**Evidence**
- **Strategy (Apr 2026):** "Radically simplifies how customers interpret Task Mining data" and "rapid setup & data validation" (invite 1–3 users, deploy in minutes, validate coverage) are named pillars — see `task-mining-strategy.md` §9 and `data-intelligence-strategy.md` §1.
- **Customer voice (IHG):** Customers want to **declare primary keys / case IDs up front** and get a **visual sample of the target data-pool structure** before clustering — validation must happen at onboarding, not after (`customer-insights.md`).
- **Customer voice (IHG):** Case-ID granularity gaps (brand/region vs. invoice-level) only surface late; early per-app object visibility would catch this sooner.
- **Positioning:** Trust (Pillar IV) is a cross-cutting, non-negotiable constraint — capture must be demonstrably privacy-first (`positioning.md` §5, §12).

---

## 3. Goals & Success Metrics

**Business Goals**
- Collapse **time-to-first-validated-capture** from days to minutes.
- Increase **onboarding completion / activation rate** by removing the privacy and data-quality leap-of-faith.
- Accelerate **IT/security sign-off** with transparent, demonstrable PII handling.
- Improve **downstream join readiness** (case ID → object → PiG) by catching gaps at onboarding.

**Metrics & Targets**

| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| Time from "start onboarding" to "first validated capture preview" | Days (post-install + data landing) | **< 10 minutes** | Pilot |
| Onboarding activation rate (started → reached validation screen) | [TO FILL — instrument] | **+30%** vs. baseline | 90 days post-pilot |
| % of pilot accounts completing capture test via **browser extension** (no client install) | 0% (new path) | **≥ 50%** | Pilot |
| IT/security approval cycle time for capture scope | [TO FILL — baseline in pilot] | **−40%** | 90 days |
| % of onboardings where ≥1 target case ID/object is confirmed before scaling | Not measured | **≥ 80%** | Pilot |

**Market Opportunity**
Differentiates against RPA-centric task mining (UiPath, Mimica) and SAP-locked alternatives (Signavio) on **trust + instant validation + PiG joinability** — a self-serve, "see it work before you commit" experience no competitor offers as a privacy-first onboarding.

**Competitive Landscape**
Competitors require install + admin setup before any signal. Browser-native instant capture + live PII scanning + case-ID/object mapping at onboarding is a defensible wedge tied to Celonis's platform (PiG) advantage.

**Why now?**
FY27 strategy makes "source-agnostic capture" and "radically simplified interpretation" architectural priorities; browser-native capture is an explicit expansion vector (`task-mining-strategy.md` §3). Trust-led onboarding directly de-risks the FY27 PiG-enrichment initiative.

---

## 4. Solution Overview

**High-Level Description**
A guided onboarding experience with one job: **let the customer test capture and validate its quality, compliance, and process-joinability in minutes.** Two entry paths — **download the client** or **run the browser extension** — converge into the same live validation experience. As the user records their own applications, three validation lenses run live:

1. **Privacy / GDPR scan** — every captured app/field is scanned; the UI shows what PII is detected and **what will be masked**, with a per-app compliance verdict (GDPR-compliant / needs attention).
2. **Case ID identification** — which **case IDs** are detected, and **through which applications** they were found.
3. **Object mapping** — which **business objects** (invoice, order, ticket, customer) those IDs map to: **covered**, **not covered**, or **could be covered with additional context** (e.g. a Process Mining data model the customer already has).

The customer ends onboarding with an explicit, trustworthy verdict: *here is what we capture, here is what we mask, here is the process data you'll get — and here is what you'd unlock with one more connection.*

**User Flows**
1. **Choose capture path:** Customer selects "Run in browser (extension)" or "Download client." Browser path requires no IT involvement.
2. **Record a sample:** Customer performs a normal task across a few apps (e.g. SAP, Excel, a web app). Capture runs locally; a live event/preview stream appears.
3. **Privacy scan (live):** As apps are recorded, the UI lists each detected app with PII findings and masking preview (masked vs. raw, side-by-side), and a compliance badge.
4. **Case-ID & object validation:** The UI shows detected case IDs, the apps they came from, and the objects they map to — with a "covered / not covered / unlockable with more context" state.
5. **Enrich (optional):** Customer connects/points to existing Process Mining context to convert "unlockable" objects into "covered."
6. **Confirm & scale:** Customer reviews the data-quality summary and confirms capture scope to roll out to representative users.

**Key Features**
- **Dual instant-capture entry:** browser extension (zero-install) + downloadable client, same validation UX.
- **Live PII / GDPR scanner:** per-app PII detection, masking preview (before/after), per-app and overall compliance verdict.
- **Case-ID detector:** detected IDs attributed to source applications, with confidence and sample values (masked).
- **Object-coverage map:** IDs → business objects with three states (covered / not covered / unlockable-with-context) and a path to enrich from Process Mining.
- **Data-quality summary:** a single onboarding verdict the customer can trust and an IT-shareable compliance view.

---

## 5. User Stories

**Story 1: CoE Lead — validate before committing (happy path)**
As **Carter (CoE Lead)**, I want to **test capture on my own apps in the browser and immediately see what data quality I'll get**, so that **I can decide to scale to users with confidence and without waiting days.**

*Acceptance Criteria:*
- [ ] Carter can start a capture test via **browser extension without installing the client**.
- [ ] Within the session, Carter sees a **live preview** of captured apps/events.
- [ ] Carter reaches a **data-quality summary** showing PII verdict, detected case IDs, and object coverage before any rollout.

*Edge Cases & Constraints:*
- If no recognizable case ID is detected, show a **guided empty state** ("no case IDs found yet — try recording the app where you enter/look up records"), not a dead end.

**Story 2: IT Lead — prove compliance**
As **Ian (IT Lead)**, I want to **see exactly what PII is detected and how it will be masked per application**, so that **I can approve capture scope against GDPR without a separate security project.**

*Acceptance Criteria:*
- [ ] Each detected application shows **PII findings** and a **before/after masking preview**.
- [ ] Each app shows a **compliance verdict** (compliant / needs attention) with the reason.
- [ ] Ian can export/share a **compliance summary** of the scanned scope.

*Edge Cases & Constraints:*
- An app with **un-maskable / high-risk fields** must surface a clear **"needs attention"** warning rather than a silent pass.

**Story 3: Analyst — confirm joinability to objects**
As **Andre (Data Analyst)**, I want to **see which case IDs map to which business objects and which objects are not yet covered**, so that **I know the captured data will join to our processes before I build anything.**

*Acceptance Criteria:*
- [ ] Detected case IDs are shown with the **applications they were identified in**.
- [ ] Each candidate **object** is labeled **covered**, **not covered**, or **unlockable with additional context**.
- [ ] For "unlockable" objects, the UI explains **what context would unlock it** (e.g. a Process Mining data model) and offers a connect action.

*Edge Cases & Constraints:*
- Sub-document IDs (e.g. invoice-level inside an Excel file) should be representable; if granularity is only brand/region, mark the finer object as "not covered / unlockable" (per IHG insight).

**Story 4: Failure / low-signal state**
As **Carter**, I want **clear feedback when capture produces too little signal or the extension can't read an app**, so that **I can correct it instead of trusting a misleading "all good."**

*Acceptance Criteria:*
- [ ] If a sample is too short/sparse, show an **insufficient-data state** with guidance to record more.
- [ ] If the extension cannot access an app (e.g. native desktop app in browser path), show a **"capture this with the client"** prompt — no false success.

*Edge Cases & Constraints:*
- Never display a confident compliance "pass" when scanning was incomplete; show **partial / in-progress** scan status.

---

## 6. Out of Scope

- **Production-grade capture engine changes** — this initiative is the **onboarding + validation experience**; the underlying capture/masking engine is consumed, not rebuilt.
- **Full Task Discovery clustering** — onboarding validates *capture quality and joinability*, not the full LLM clustering output (covered by `ai-task-discovery.md`).
- **Cross-OS / VDI client parity** — browser extension + Windows client only for first cut; macOS/VDI deferred.
- **Automatic PiG writes** — "unlockable with context" demonstrates the path and connects context, but committing enrichment to the PiG stays in the existing enrichment flow.
- **Real backend scanning accuracy** — for the prototype, PII/case-ID/object detection is represented with realistic mock results, not a live model.

---

## 7. Platform & Integration Context

**Platform layer(s) affected**
- [x] Data Core — capture entry (client + browser extension), local PII masking, sample event stream
- [x] Process Intelligence Graph — case ID → object mapping; "unlockable with PM context" preview
- [x] Build Experience — the onboarding/validation UI itself

**Source systems in scope**
Representative captured apps for mockups: SAP (GUI/Fiori), Excel, a browser-based web app (e.g. ServiceNow/Salesforce), Outlook. Optional connect-point: existing **Process Mining data model** for object enrichment.

**Process Intelligence Graph impact**
No schema change in this initiative. It **previews** how captured IDs would join to PiG objects and surfaces coverage gaps; actual enrichment uses existing paths.

**AI / agentic implications**
PII detection, case-ID extraction, and object inference are AI-assisted in production; for the prototype they are mocked. Validated capture scope improves the operational-memory quality that grounds downstream agents.

**Strategic priority alignment**
- [x] AI context layer
- [x] Visibility → action → orchestration
- [x] Agentic AI readiness
- [x] Open ecosystem (source-agnostic capture, browser-native path)
- [x] Operational readiness gap (removes onboarding friction / expertise barrier)

---

## 8. Dependencies & Risks

**Technical Dependencies**
- Browser extension capture runtime + local masking on the client.
- PII detection, case-ID extraction, and object-inference services (mocked for prototype).
- Read access to an existing Process Mining data model for the enrichment/"unlock" path.

**External Dependencies**
- Browser vendor extension review/distribution (Chrome/Edge) for the browser path.

**Internal Team Dependencies**
- Task Mining engineering (capture, masking, onboarding UI).
- PI Graph / platform data (object mapping contract).
- Security & privacy (PII taxonomy, masking rules, compliance verdict logic, DPIA).
- Design / UX (validation patterns, accessibility WCAG 2.1).

**Risks & Mitigations**

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Browser extension can't capture native desktop apps | High | Med | Clear path-routing to client; set expectations per app type |
| False "compliant" verdict erodes trust | Low | High | Show partial/in-progress scan states; never pass on incomplete scan |
| Over-promising object coverage | Med | High | Explicit three-state model (covered / not / unlockable) with required context named |
| Privacy concerns about the test itself | Med | High | Local processing, masking-before-display, opt-in, no raw PII leaves device |
| Onboarding feels like surveillance | Low | High | Self-record only, user-initiated, transparent capture indicator |

---

## 9. Open Questions

- [ ] **Browser scope** — Which app classes are realistically capturable via extension vs. must route to client? — Owner: Eng — Due: design review
- [ ] **PII taxonomy depth** — Which PII categories shown at onboarding (names, emails, IDs, financial)? — Owner: Privacy — Due: pilot kickoff
- [ ] **Object inference source** — Do we infer objects from captured IDs alone, or require a declared key list (per IHG insight)? — Owner: PM + Andre persona research — Due: design review
- [ ] **Enrichment connect UX** — How lightweight can the "connect Process Mining context" step be at onboarding? — Owner: PM + PI Graph — Due: phase 2
- [ ] **Compliance export format** — What does Ian need to share for sign-off? — Owner: PM + Security — Due: pilot

---

## 10. Prototype Screen Plan (for `/prototype`)

**Feature name:** `instant-capture-validation`

**Primary persona:** Carter (CoE Lead) — wants to test capture and validate data quality, compliance, and joinability in minutes before scaling to users. Ian (IT) and Andre (Analyst) are secondary viewers of the same screens.

**Platform layer:** Data Core (capture) → Build Experience (validation UI), previewing Process Intelligence Graph joins.

**User journeys covered:**
1. **Instant capture test** — choose browser extension or client, record a sample, see live capture.
2. **Privacy validation** — scan recorded apps, preview PII masking, get per-app GDPR verdict.
3. **Joinability validation** — see case IDs per app, map to objects, identify covered / not / unlockable.
4. **Enrich & confirm** — connect Process Mining context to unlock objects, confirm scope, scale to users.

**Screens:**

| # | Screen name | Purpose | Links to |
|---|-------------|---------|----------|
| 1 | Choose capture path | Select **Browser extension** (zero-install) or **Download client**; explain privacy-first, self-record | 2 |
| 2 | Record a sample | Live capture view: detected apps + event stream as the user works; capture indicator; "I'm done" CTA | 1, 3 |
| 3 | Privacy & GDPR scan | Per-app PII findings, before/after masking preview, per-app + overall compliance verdict; export for IT | 2, 4 |
| 4 | Case IDs & object coverage | Detected case IDs attributed to apps; object map with covered / not covered / unlockable-with-context states | 3, 5 |
| 5 | Enrich from process context | Connect existing Process Mining data model to convert "unlockable" objects to "covered"; before/after coverage | 4, 6 |
| 6 | Data-quality summary & scale | Single verdict (compliance + IDs + coverage); confirm capture scope; invite representative users | 4, 5 |

**Special states included:**
- Empty state on: Screen 4 (no case IDs detected yet — guidance to record the right app)
- Error/validation on: Screen 2 (extension can't read a native app → route to client); Screen 3 ("needs attention" on un-maskable fields)
- Confirmation modal on: Screen 6 (confirm capture scope before scaling to users)
- Loading state on: Screen 3 (scan in progress — partial results, never a premature "pass")

**Files to be created:**
```
output/instant-capture-validation-prototype/
├── index.html          ← redirects to 01
├── style.css           ← Celonis design tokens + shared styles
├── nav.js              ← cross-screen navigation
├── 01-choose-capture-path.html
├── 02-record-sample.html
├── 03-privacy-gdpr-scan.html
├── 04-case-ids-object-coverage.html
├── 05-enrich-process-context.html
└── 06-data-quality-summary.html
```

---

## Appendix — Alignment References

- `knowladge/task_mining/task-mining-strategy.md` — Pillar I (Data Capturing), browser-native expansion, "rapid setup & data validation."
- `knowladge/task_mining/data-intelligence-strategy.md` — source-agnostic capture, case-ID → PiG mapping.
- `knowladge/task_mining/positioning.md` — Trust (Pillar IV), privacy-first guardrails, "not surveillance."
- `knowladge/task_mining/customer-insights.md` — IHG: declare primary keys up front, visual sample of target schema, invoice-level case-ID gaps.
- `knowladge/celonis_strategy/personas.md` — Carter, Ian, Andre.
