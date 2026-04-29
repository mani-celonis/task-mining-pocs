# Celonis — Customer Personas

> This file is read by the `/prd` command during brainstorming to suggest realistic personas and sharpen user stories.
> Each entry covers: the official Celonis archetype name, role, seniority, what they care about, how they interact with Celonis, and their key frustrations.

---

## Persona categories

Celonis groups stakeholders by how they interact with the platform:

| Category | Who | Relationship to Celonis |
|----------|-----|-------------------------|
| **Executives** | Economic buyers and sponsors | Strategic direction, budget, expansion; light direct product use |
| **Activators** | CoE, IT, data, value roles | Implementation, governance, modeling, scaling adoption |
| **Users** | Process leads and front-line operators | Consume insights, validate process truth, act on recommendations |

When a feature touches both configuration and consumption, specify **builder** (Activator) and **consumer** (User or Executive) stories separately.

---

## Executives

### Erin — Economic Buyer

**Also known as:** SVP Operations, Director IT, CFO, Head of Transformation
**Seniority:** C-Suite / VP / Director
**Company context:** Budget owner and ultimate approver; engaged at steering moments (business case, renewal, expansion)

**What they care about:**
- Proof of significant ROI tied to cost reduction, risk, or competitive efficiency
- Total cost of ownership — platform, integrations, services, and change management
- Renewal narrative: is the program delivering on what was promised?
- Involvement limited to key decision points (QBRs, stage gates)

**How they use Celonis:**
- Receives executive summaries and program-level value dashboards
- Reviews business case outputs framed by the Value Architect (Vince)
- Does not typically build or configure; relies on CoE and sponsors to surface findings

**Key frustrations:**
- Perceived premium price without clear "plug and play" readiness
- Difficulty attributing measurable outcomes to the platform investment
- Slow procurement and implementation cycles

**Key question for PRDs:** "What is the measurable operational or financial outcome, and what does it cost to achieve it?"

---

### Sachie — Executive Sponsor

**Also known as:** CFO, VP / Head of GBS, VP Operations
**Seniority:** C-Suite / VP
**Company context:** Senior leader championing Celonis internally; bridges the platform to enterprise OKRs

**What they care about:**
- Linking Celonis outcomes to company-level priorities (cost, growth, resilience)
- Getting peer buy-in from other senior leaders for cross-functional expansion
- Fast, credible root-cause answers — where bottlenecks are hurting revenue or working capital
- Clarity on where to prioritize across a growing use-case portfolio

**How they use Celonis:**
- Consumes high-level process performance narratives and KPI summaries
- Advocates internally based on results framed by Carter (CoE Lead) and Vince (Value Architect)
- Asks direct questions at QBRs; expects clear "so what" without needing to dig

**Key frustrations:**
- Organization cannot execute change at scale even when insights are clear
- Unclear which use cases to fund first across competing business units
- Lack of visibility into program health without relying on manual updates

**Key question for PRDs:** "Does this help us move a strategic metric, and can I explain it to my peers in one sentence?"

---

## Activators

### Carter — CoE Lead

**Also known as:** Celonis CoE Lead, Process Excellence Lead, Internal Product Manager (Celonis), Business Process Lead
**Seniority:** Manager / Senior Manager
**Company context:** Centre of Excellence team; day-to-day owner of Celonis across the organisation

**What they care about:**
- Understanding where processes are breaking down and why
- Proving ROI from process improvement initiatives to leadership
- Scaling Celonis adoption across business units
- Building a repeatable, data-driven improvement culture

**How they use Celonis:**
- Primary power user — builds analyses, monitors KPIs, investigates root causes in **Studio**
- Central point of contact for Celonis; prioritises use cases and manages governance/reporting
- Manages budget, licensing, and vendor relationship
- Creates dashboards and apps for business stakeholders to self-serve

**Key frustrations:**
- Slow internal adoption despite clear insights
- Frequent UI or workflow changes without migration support
- Business stakeholders don't act on findings without a clear "so what"
- Long ticket resolution cycles for minor platform fixes
- Difficulty showing year-over-year value to justify renewal

**Key question for PRDs:** "Does this help me scale adoption, govern the platform, or prove value to leadership?"

---

### Ian — IT Lead

**Also known as:** Enterprise Architect, Solution Architect, Integration Lead, Platform Engineer, CIO / IT Director (mid-market)
**Seniority:** Senior IC to Director
**Company context:** IT or Digital Transformation team; gatekeeper for data access and system integrations

**What they care about:**
- Secure, governed, scalable data extraction from source systems
- Minimising integration complexity and ongoing maintenance burden
- Ensuring Celonis fits within the broader data and AI architecture
- Compliance with data residency, access control, and audit requirements

**How they use Celonis:**
- Sets up and operates **extractors**, agents, and connectivity to source systems (SAP, Salesforce, etc.)
- Manages user access, data governance policies, and environment configuration
- Monitors API thresholds and operational health
- Evaluates Celonis against the enterprise data/AI platform landscape

**Key frustrations:**
- Connector setup is complex and brittle when source system versions change
- Limited transparency into what data is extracted and how it is stored
- Difficult to integrate Celonis outputs into the broader data stack (BI tools, data lakes)
- Security reviews are slow because technical documentation is insufficient

**Key question for PRDs:** "Does this integrate cleanly with our architecture, and does it meet our security and compliance requirements?"

---

### Andre — Data Analyst

**Also known as:** Celonis Analyst, BI Analyst (Celonis), Process Analyst (builder), App Builder
**Seniority:** Individual contributor to Senior IC
**Company context:** May sit in the CoE, a business unit, or a partner/SI; builds the analyses and apps others consume

**What they care about:**
- Translating business requirements into analyses, KPIs, and **Action Flows** in Celonis
- Fast iteration from hypothesis to published insight — "fast first insights" after data lands
- Ability to pull data from multiple source systems into one unified process view
- Reusable components to accelerate delivery across use cases

**How they use Celonis:**
- Power user of **Studio**, **PQL**, and the visualization layer
- Investigates root causes and frames value through process data
- Builds dashboards and apps for process leads, executives, and business users

**Key frustrations:**
- Custom or legacy source systems that don't fit standard extractors
- Limits of out-of-the-box visuals for complex analytical storytelling
- Undocumented edge cases in PQL or the app builder
- Long feedback loops when debugging data extraction issues

**Key question for PRDs:** "Does this reduce the time from data to insight, or give me more expressive power to answer complex process questions?"

---

### Vince — Value Architect

**Also known as:** Value Manager, Transformation Manager, Senior Process Analyst, Program Manager
**Seniority:** Senior IC to Manager
**Company context:** Often sits in the CoE or a Strategy/Transformation function; bridges analytics and business outcomes

**What they care about:**
- Developing credible business cases and benefit hypotheses before and during deployment
- Tracking and reporting value realization with defensible baselines and before/after narratives
- Connecting Celonis capabilities (automation, Action Flows, EMS) to measurable KPIs
- Driving user adoption so identified benefits actually materialize

**How they use Celonis:**
- Consumes process and KPI data to build value dashboards and executive reporting
- Partners with Carter (CoE Lead) on use-case prioritization based on expected impact
- Supports change management planning and adoption tracking

**Key frustrations:**
- Hard to establish clean baselines before go-live, making attribution difficult
- Value dashboards require custom build effort rather than being available out of the box
- Adoption data is fragmented, making it difficult to link usage to outcomes

**Key question for PRDs:** "Does this make it easier to measure, attribute, and communicate the business impact of Celonis?"

---

### Davina — Data Engineer

**Also known as:** Analytics Engineer, Integration Developer (Celonis), Celonis Consultant (technical)
**Seniority:** Individual contributor to Senior IC
**Company context:** May be a customer employee or a partner/SI resource; owns data pipeline health

**What they care about:**
- Reliable ETL/ELT from source systems into Celonis-ready data models
- Stable platform surface area — breaking changes in **PQL** or extractors are costly
- Smooth environment lifecycle (dev → test → prod) with proper versioning and promotion
- Performance at scale: large event logs, complex transformations

**How they use Celonis:**
- Builds and maintains data extraction pipelines and **data models**
- Debugs transformation logic and monitors pipeline health
- Manages environment configuration and artifact promotion

**Key frustrations:**
- Debugging PQL scripts or transformation logic with limited tooling
- Friction moving artifacts between environments (transportability, versioning)
- Limited ability to version-control or collaborate on analyses and models
- Connector behaviour changes between source system versions

**Key question for PRDs:** "Does this reduce the operational burden of keeping data pipelines healthy and environments in sync?"

---

## Users

### Ben — Business User

**Also known as:** Accounts Payable Clerk, Procurement Specialist, Order Manager, Customer Service Agent
**Seniority:** Individual contributor
**Company context:** Front-line operational role in Finance, Supply Chain, or Customer Operations

**What they care about:**
- Getting work done efficiently without context-switching between systems
- Knowing what to prioritise and why — clear, trusted recommendations
- Avoiding errors and rework that affect their personal SLAs and KPIs
- Confidence that the tool is helping them, not monitoring them

**How they use Celonis:**
- Receives task recommendations or alerts via **EMS**, **Action Flows**, email, or embedded in SAP / Salesforce
- Acts on prioritised work queues; may not know they are using Celonis if intelligence is embedded
- Provides feedback when recommendations don't match their reality

**Key frustrations:**
- Alert fatigue — too many exceptions with unclear prioritisation
- Having to leave their primary system to take action
- Unclear instructions: knowing *what* to do but not *how*
- Lack of feedback on whether their action had the intended outcome
- Anxiety that process transparency could be used to reduce headcount

**Key question for PRDs:** "Does this make my daily work faster, clearer, or less error-prone without adding new systems to learn?"

---

### Petra — Process Lead

**Also known as:** Global Process Owner (GPO), Business Process Owner (BPO), Director Sales Ops, Director Supply Chain Ops
**Seniority:** Manager to Director
**Company context:** Accountable for an end-to-end process (O2C, P2P, R2R) and its KPIs; sits between executives and front-line operators

**What they care about:**
- Setting strategic direction and KPIs for use cases in their domain
- Validating that data models and metrics reflect the real process
- Identifying execution gaps and sponsoring cross-functional remediation
- Running change management for new process initiatives

**How they use Celonis:**
- Consumes process performance dashboards and exception views
- Validates analyses built by Andre or Carter against domain knowledge
- Drives follow-up actions (approvals, escalations) and tracks outcome

**Key frustrations:**
- Data models that don't match how the process actually runs in their business unit
- Insights without clear ownership or action path across functions
- Inability to see whether interventions led to sustained improvement

**Key question for PRDs:** "Does this give me an accurate, actionable view of my process — and can I drive change from it without needing a data team for every question?"

> **Finance Operations Lead sub-type:** AP/AR Manager, Shared Services Lead, Finance Transformation Lead. Primarily consumes pre-built finance apps; key concerns are DPO/DSO metrics, audit compliance, and alert fatigue from unactionable exceptions.

---

## Notes for PRDs

- Most Celonis features have **two user types**: the *builder* (Carter, Andre, Davina — who configure the feature) and the *consumer* (Ben, Petra, Sachie — who act on it). Address both in user stories.
- **Carter** is the most common primary persona for platform-level and governance features.
- For **finance use cases**, the Finance Operations Lead sub-type of Petra is the primary end-user persona.
- For **integration or data pipeline features**, Ian and Davina are the primary personas.
- **Erin and Sachie** are typically secondary personas — they sponsor and judge outcomes but rarely use the product directly.
- **Vince** is relevant whenever a feature touches value measurement, baselines, or adoption tracking.
- Prefer Celonis-native terms where accurate: **use case**, **value realization**, **Studio**, **EMS**, **Action Flow**, **process mining**, **PQL**, **extractors**, **CoE**, **GPO/BPO**.
