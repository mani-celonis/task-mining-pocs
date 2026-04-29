# Task mining — competitive landscape

<!--
AGENT BRIEF
doc_id: task_mining.competition | v0.2 | 2026-04-29
Purpose: Reference when analyzing new initiatives or features against task mining competitors.
How to use:
  1. Start with "Initiative analysis framework" to run a structured comparison.
  2. Pull competitor facts from "Competitor profiles".
  3. Use "Feature matrix" for capability-level parity checks.
  4. Check "Win / loss signals" for deal-level heuristics.
Sources (internal — do not distribute):
  - Celonis_vs_Skan.AI_Battlecard_WIP.pdf
  - 251025_Internal_Battlecard_TaskMining_EN.pdf
  - Product Feature Comparison_ Mimica, Skan, Soroco, Celonis.xlsx
Mark claims from above sources [bc] = battlecard / internal.
-->

---

## 1. Market snapshot

| Dimension | Note |
| --------- | ---- |
| Category names | **Task Mining** (Gartner) · **Digital Interaction Intelligence / DII** (Everest) |
| Market size | ~$600M by end-2025E, CAGR 65–75%; BFSI, health/pharma, tech/telco lead [bc] |
| Analyst lists | Gartner Market Guide · Everest PEAK DII · QKS SPARK Q3 2025 |
| Key agentic driver | Accurate work capture is prerequisite for *designing and monitoring* AI agents on tasks (Gartner, cited [bc]) |

**Celonis positioning in this category:** Task Mining is not a standalone product. It bridges system-level process mining with desktop reality to build a complete digital twin and ground Agentic AI. See `positioning.md`.

---

## 2. Competitor register

| Slug | Vendor | Tier | Capture angle (one line) | Analyst presence |
| ---- | ------ | ---- | ------------------------ | ---------------- |
| `skan` | Skan.AI | **direct** | CV-first, "invisible work," zero-integration passive observation | Gartner · Everest · QKS [bc] |
| `mimica` | Mimica | **direct** | AI-first process mapping; fast discovery for automation pipeline [bc] | Gartner · Everest |
| `soroco` | Soroco | **direct** | Work graph; people–technology & collaboration patterns [bc] | Everest |
| `uipath` | UiPath | platform_adjacent | Task mining inside UiPath Discovery; strong RPA pipeline | QKS leader |
| `abbyy` | ABBYY | adjacent | IDP + process / task capture [bc] | Everest |
| `automation_anywhere` | Automation Anywhere | adjacent | Embedded task capture in AA360 [bc] | QKS leader |
| `edgeverve` | Edgeverve | adjacent | Finacle-linked; enterprise process capture [bc] | — |
| `kyp_ai` | KYP.AI | adjacent | Lightweight desktop analytics [bc] | — |
| `nintex` | Nintex | adjacent | Process documentation + workflow automation [bc] | — |
| `servicenow` | ServiceNow | platform_adjacent | Process discovery inside Now Platform [bc] | — |
| `stereologic` | Stereologic | niche | Specialist desktop observation [bc] | — |

---

## 3. Initiative analysis framework

> Use this when a new feature or product initiative is being evaluated against the market.  
> Run each dimension; record your output in the initiative's PRD or opportunity brief.

### 3.1 Dimensions

| # | Dimension | Question to answer | Primary source |
| - | --------- | ------------------ | -------------- |
| 1 | **Feature parity** | Do competitors already have this? At what maturity? | Feature matrix (§4) |
| 2 | **Differentiation angle** | Is the initiative a catch-up move, parity play, or genuine wedge? | Competitor profiles (§5) |
| 3 | **ICP fit** | Which buyer / use-case archetype is the initiative targeting — and who else targets them? | Competitor profiles → `icp` field |
| 4 | **Agentic / AI story** | How does this initiative strengthen or weaken the "ground AI agents with task data" narrative vs. competitors? | §5 → *Agentic angle* |
| 5 | **Integration depth** | Does the initiative require / exploit PM ↔ Task fusion? Can stand-alone players replicate it? | §5 → *Architecture* |
| 6 | **Privacy & compliance** | Is this relevant in regulated sectors (FSI, health)? Who has the strongest trust story? | §4 → `security_and_compliance` |
| 7 | **Time to value** | How does deployment speed compare? Where do competitors claim "zero integration"? | §5 → *Win/loss signals* |
| 8 | **Commercial model** | Pricing structure / packaging implications vs. competitors | §4 → `commercial_model` |

### 3.2 Scoring guide

Rate each dimension **per relevant competitor** using:

| Score | Meaning |
| ----- | ------- |
| `ahead` | Initiative gives Celonis a clear, defensible lead |
| `parity` | Competitors match; bet on execution or adjacent strengths |
| `behind` | Competitor ahead; initiative is catch-up |
| `n/a` | Dimension not applicable for this initiative |

### 3.3 Output template (copy into PRD / opportunity brief)

```
Initiative: [name]
Date: [YYYY-MM-DD]

| Dimension           | skan | mimica | soroco | uipath | key insight |
|---------------------|------|--------|--------|--------|-------------|
| Feature parity      |      |        |        |        |             |
| Differentiation     |      |        |        |        |             |
| ICP fit             |      |        |        |        |             |
| Agentic / AI story  |      |        |        |        |             |
| Integration depth   |      |        |        |        |             |
| Privacy/compliance  |      |        |        |        |             |
| Time to value       |      |        |        |        |             |
| Commercial model    |      |        |        |        |             |

Recommended positioning angle:
Key risks:
Gaps to close before launch:
```

---

## 4. Feature matrix

> Capability groups sourced from internal Excel comparison (Mimica · Skan · Soroco · Celonis).  
> Status values: `✓ available` · `~ partial` · `⏳ roadmap` · `P partner` · `✗ not available` · `? unknown`

### 4.1 Data collection & preparation

| Feature | skan | mimica | soroco | celonis |
| ------- | ---- | ------ | ------ | ------- |
| DOM/COM-based recorder (legacy + mainframe) | ✓ | ✓ | ? | ✓ |
| Image-based / CV recorder | ✓ | ~ | ? | P |
| Green screen / Citrix / VDI capture | ✓ | ? | ? | P |
| Silent background recording | ✓ | ✓ | ✓ | ✓ |
| Screenshot per action | ✓ | ✓ | ? | ✓ |
| Browser extension for web capture | ✓ | ✓ | ? | ✓ |
| OCR / IDP field extraction from screenshots | ✓ | ~ | ? | ~ |
| Allowlist / blocklist URLs and apps | ✓ | ? | ? | ✓ |
| Semantic clustering for context | ✓ | ✓ | ✓ | ✓ |
| Export raw UI log (csv/xls) | ✓ | ? | ? | ✓ |
| Automated PII masking at edge/source | ✓ | ~ | ? | ✓ |
| Hybrid / on-premises data gateway | ~ | ? | ? | ✓ |

### 4.2 AI-powered process discovery

| Feature | skan | mimica | soroco | celonis |
| ------- | ---- | ------ | ------ | ------- |
| Unsupervised task classification | ✓ | ✓ | ✓ | ✓ |
| Supervised / labeled classification | ~ | ✓ | ? | ~ |
| AI-driven start/end point detection | ✓ | ✓ | ? | ✓ |
| Process hierarchy discovery (cross-BU) | ~ | ? | ✓ | ✓ |
| BPMN 2.0 export | ? | ? | ? | ✓ |
| Correlation of desktop + system event logs | ✗ | ? | ? | ✓ |
| Video playback of discovered tasks | ✓ | ✓ | ? | ✓ |
| Rework / loop percentage detection | ? | ? | ? | ✓ |

### 4.3 Process conformance

| Feature | skan | mimica | soroco | celonis |
| ------- | ---- | ------ | ------ | ------- |
| Compliance rate at activity + task level | ~ | ? | ? | ✓ |
| Conformance check vs. benchmark model | ~ | ? | ? | ✓ |
| Variant analysis / optimal path ID | ✓ | ? | ? | ✓ |
| Root-cause analysis for deviations | ~ | ? | ? | ✓ |
| NL-defined compliance rules | ? | ? | ? | ⏳ |
| To-be model via task capture | ✓ | ✓ | ? | ✓ |
| To-be model via process modeler | ✗ | ✗ | ? | ✓ |

### 4.4 Process monitoring & insights

| Feature | skan | mimica | soroco | celonis |
| ------- | ---- | ------ | ------ | ------- |
| Custom dashboards | ✓ | ~ | ✓ | ✓ |
| Automation potential score | ✓ | ✓ | ? | ✓ |
| Application switching time | ✓ | ? | ✓ | ✓ |
| Idle time per user | ✓ | ? | ✓ | ✓ |
| Business KPI impact of human–machine interaction | ~ | ? | ? | ✓ |
| Cost-saving potential display | ~ | ✓ | ? | ✓ |
| Task variance rate | ✓ | ? | ? | ✓ |
| Conversational / NL query interface | ~ | ? | ? | ~ |
| PDD (Process Design Document) generation | ✓ | ✓ | ? | ✓ |
| On-screen pop-up for process deviations | ? | ? | ? | ✓ |

### 4.5 Process enhancement & agentic action

| Feature | skan | mimica | soroco | celonis |
| ------- | ---- | ------ | ------ | ------- |
| On-screen guidance / next-best action | ~ | ✓ | ? | ✓ |
| RPA script generation from discovered tasks | ✓ | ✓ | ? | ✓ |
| What-if / scenario simulation | ✗ | ? | ? | ✓ |
| AI/ML KPI breach prediction & alerts | ~ | ? | ? | ✓ |
| AI-based simulation (ML-generated scenarios) | ~ | ? | ? | ⏳ |
| Guided learning / training video generation | ✓ | ? | ? | ? |
| Agent training from observed patterns | ✓ | ~ | ? | ✓ |

### 4.6 Integration with complementary capabilities

| Feature | skan | mimica | soroco | celonis |
| ------- | ---- | ------ | ------ | ------- |
| Native process mining integration | ✗ | ✗ | ✗ | ✓ |
| IDP integration | P | P | ? | ~ |
| RPA platform connectors | ~ | ✓ | ? | ✓ |
| ERP / CRM native extractors (100+) | ✗ | ✗ | ? | ✓ |
| Orchestration / action engine | ~ | ✗ | ? | ✓ |
| Open API / data export | ~ | ? | ? | ✓ |
| Enterprise app marketplace | ✗ | ✗ | ? | ✓ |

### 4.7 Security & compliance

| Feature | skan | mimica | soroco | celonis |
| ------- | ---- | ------ | ------ | ------- |
| GDPR compliance | ✓ | ✓ | ? | ✓ |
| SOC 2 certification | ✓ | ? | ? | ✓ |
| ISO 27001 | ? | ? | ? | ✓ |
| Edge / at-source PII masking | ✓ | ? | ? | ✓ |
| Role-based access controls | ✓ | ? | ? | ✓ |
| On-premises / hybrid data residency | ~ | ? | ? | ✓ |
| Audit trail for captured data | ✓ | ? | ? | ✓ |

### 4.8 Commercial model

| Feature | skan | mimica | soroco | celonis |
| ------- | ---- | ------ | ------ | ------- |
| Per-user pricing | ✓ | ✓ | ? | ✓ |
| Consumption / usage-based pricing | ? | ? | ? | ✓ |
| Free trial / pilot offering | ✓ | ✓ | ? | ✓ |
| Partner / reseller program | ✓ | ? | ? | ✓ |
| Land-and-expand motion | ✓ | ✓ | ? | ✓ |

> **Note:** Matrix rows marked `?` need verification. Cells without public evidence should not be used in external-facing materials.

---

## 5. Competitor profiles

### skan — Skan.AI

| Field | Detail |
| ----- | ------ |
| **Website** | skan.ai |
| **ICP / buyer** | Head of Ops, COO, Transformation/Automation lead; FSI (BofA, Wells Fargo, Citi) accounts [bc] |
| **GTM** | Land-and-expand; solution-focused; rapid time-to-value framing [bc] |
| **Capture model** | Pure CV + deep learning; lightweight desktop sensor or browser extension; "passive observation / zero integration" narrative [bc] |
| **Architecture** | No process intelligence graph; CV-centric "UI layer ground truth"; probabilistic/behavioral AI agents [bc] |
| **Privacy** | Cognitive masking: automated PII/PCI redaction at edge before leaving machine; FSI compliance narrative [bc] |

**Their frame:** "Invisible work," 360° human–system visibility, digital twin of operations, context-aware AI agents trained on human execution patterns.

**Strengths (customer feedback [bc]):**
- Edge PII redaction — strong in regulated industries
- App-agnostic (legacy, SaaS, Citrix, custom apps) without API connectors
- Surfaces dark processes and shadow IT usage

**Weaknesses / gaps (customer feedback [bc]):**
- Insight-to-action gap: generates visualizations but lacks automated write-backs
- Struggles to standardize data in highly variable, unstructured workflows at enterprise scale
- Limited customization and deep backend integration ("WYSIWYG")
- Delivery expectations sometimes oversold in sales cycle

**Agentic angle:** Trains AI agents on observed human execution patterns (behavioral). PDD generation. No deterministic grounding in system-of-record event data.

**Win conditions for Celonis:** PM already in house; need E2E conformance + system linkage; regulated sector with process audit requirement; large-scale ERP landscape.

**Threat in deals:** Speed of deployment ("weeks not months"); CV approach persuasive when IT access is limited; strong FSI narrative.

---

### mimica — Mimica

| Field | Detail |
| ----- | ------ |
| **Website** | mimica.ai |
| **ICP / buyer** | Automation CoE, RPA teams, process analysts [bc] |
| **GTM** | (fill from live research) |
| **Capture model** | AI-first manual task recording; supervised labeling for automation discovery |
| **Architecture** | Focused on automation pipeline; Mimica Mapper → task map → RPA blueprint |
| **Privacy** | (fill) |

**Their frame:** AI-first, fastest path from observation to automation blueprint.

**Strengths:** Fast discovery for targeted RPA use cases; strong labeling UX; fits CoE workflow.

**Weaknesses / gaps:** Point-solution positioning; limited PM depth; no enterprise digital twin story; dependent on automation platform for execution.

**Agentic angle:** Generates automation blueprints / PDDs; agent training capability unclear — verify.

**Win conditions for Celonis:** Need cross-system E2E visibility; buyer is CIO / transformation leader not CoE; PM already anchors the platform deal.

**Threat in deals:** Fast time-to-first-insight; CoE-friendly; strong RPA community ties.

---

### soroco — Soroco (Scout)

| Field | Detail |
| ----- | ------ |
| **Website** | soroco.com |
| **ICP / buyer** | HR / workforce analytics, operations leaders [bc] |
| **GTM** | (fill from live research) |
| **Capture model** | Work graph: people–technology–collaboration patterns; desktop + collaboration tool capture |
| **Architecture** | Workforce optimization angle; cross-BU process hierarchy; less focus on ERP log fusion |
| **Privacy** | (fill) |

**Their frame:** "Work graph" — how people and technology interact across the enterprise; workforce productivity and collaboration lens.

**Strengths:** People-centric analytics; collaboration pattern discovery; cross-BU hierarchy detection.

**Weaknesses / gaps:** Less PM depth; limited action/automation layer; backend system integration shallow [bc].

**Agentic angle:** Unclear — verify on current product site.

**Win conditions for Celonis:** Need ERP-linked outcome metrics; buyer is finance/operations not HR; agentic execution required.

**Threat in deals:** Workforce analytics framing resonates in CHRO-led initiatives; collaboration data angle differentiated.

---

### uipath — UiPath (Task Mining / Process Mining)

| Field | Detail |
| ----- | ------ |
| **Website** | uipath.com/product/task-mining |
| **ICP / buyer** | RPA/automation CoE; UiPath-incumbent accounts |
| **GTM** | Bundled in UiPath platform; automation-first buyer |
| **Capture model** | Desktop recorder inside UiPath Discovery; tightly coupled to UiPath Studio / Autopilot |
| **Architecture** | Strong if already on UiPath; weaker cross-platform; limited system-of-record PM depth |

**Agentic angle:** Autopilot / agentic automation pipeline built on observed task data; strong RPA-to-agent story within UiPath ecosystem.

**Win conditions for Celonis:** Multi-vendor automation landscape; need ERP / object-centric PM; buyer prefers vendor-neutral digital twin.

**Threat in deals:** Incumbent automation platform; bundled pricing; rapid cross-sell in existing accounts.

---

## 6. Head-to-head heuristics

| Initiative archetype | Best competitor to benchmark | Why it matters |
| -------------------- | ---------------------------- | -------------- |
| CV / zero-integration capture | skan | Their core narrative; strongest objection in IT-constrained accounts |
| Agentic AI grounding (PDD / blueprints) | skan, mimica, uipath | All three have some PDD or agent-training story |
| Workforce / productivity analytics | soroco | Work graph is their differentiated angle |
| RPA pipeline acceleration | mimica, uipath | Fast discovery → automation is their primary motion |
| FSI / regulated industry | skan | Edge masking + compliance narrative is their FSI playbook |
| E2E process + task fusion | none (Celonis unique) | No direct competitor fuses PM PI graph + Task at this depth [bc] |

---

## 7. Open gaps & maintenance

- [ ] Verify Mimica and Soroco current product pages; fill empty cells in §5.
- [ ] Import full 103-row xlsx matrix into §4 with stable `feature_id` slugs.
- [ ] Add Stereologic, KYP.AI, Edgeverve one-pagers when they enter deals.
- [ ] Refresh Skan.AI claims against public product site (battlecard is WIP).
- [ ] Mark cells with source + date when filled to enable staleness tracking.

---

*Internal use only. Claims marked [bc] derive from Celonis internal battlecard materials; verify against public sources before external use.*
