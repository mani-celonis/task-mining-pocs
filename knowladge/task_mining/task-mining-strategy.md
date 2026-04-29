# Task Mining — Product Strategy

> **Version:** 1.0 | **Owner:** Task Mining PM | **Last updated:** April 2026

---

## 1. Origin & Strategic Rationale

Task Mining was created to solve a fundamental blind spot in process intelligence: **work that happens outside systems of record**.

Process mining reconstructs how processes flow across ERP, CRM, and other enterprise systems. But a substantial share of real work — the coordination, the data wrangling, the exception handling — happens in spreadsheets, desktop applications, and productivity tools. That is where process inefficiencies actually live, and where no system of record writes an event log.

Task Mining was purpose-built to capture that layer. Not as a standalone click-recording tool, but as a **platform-native capability** that enriches the Celonis Process Intelligence Graph with desktop-level reality. When customers want a true digital twin of their operations, they need both dimensions: what the systems say happened, and what people actually did in between.

This platform embeddedness is the primary differentiator. Task Mining is not a point solution for RPA discovery. It is the mechanism by which Celonis delivers **end-to-end process observability** — connecting system-level flows with the human work that spans and bridges them.

---

## 2. Strategic Position Within the Celonis Platform

The Celonis platform is organized in three layers: Data Core, Process Intelligence Graph, and the Build Experience (Analyze → Design → Operate). Task Mining contributes to all three.

```
Celonis Platform
├── Data Core
│   └── Task Mining: Data Capturing (desktop agents → dedicated data pool)
├── Process Intelligence Graph
│   └── Task Mining: enriches case IDs with desktop-level task context
└── Build Experience (Analyze / Design / Operate)
    └── Task Mining: enables workforce productivity analysis, task discovery,
        automation opportunity identification, and agentic AI grounding
```

The strategic intent is straightforward: **no digital twin is complete without the human layer**. Task Mining makes that layer visible, structured, and actionable.

---

## 3. Two Core Pillars + One Cross-Cutting Principle

> **Positioning note:** Externally, Task Mining is communicated via four pillars — **(I) Capture hidden workflows at scale, (II) Contextualize & discover task reality, (III) Fuel action & Agentic AI, (IV) Trust: security & privacy**. Internally, Pillars I–III map to the two product pillars below; Pillar IV (Trust) is a cross-cutting principle embedded in both.

### Pillar I — Data Capturing

Everything from the moment a user's activity is recorded on their machine to the point data lands in the platform.

**How it works today:**
- A lightweight client is installed on **Windows machines** — deployable via central IT (MDM/GPO) or by individual users via a self-service download link.
- The client captures granular desktop interactions using **UI metadata and DOM elements as the primary data source**: click coordinates, active application window, URLs visited, page titles, and application-level context.
- **Screenshots are supported** as an optional, supplementary signal — they are not the primary extraction mechanism. Privacy and compliance requirements are the governing constraint here.
- Captured events are processed locally (extraction, masking) and pushed to a **dedicated data pool** in the Celonis platform.

**Key design principles:**
- Privacy-first by design: automated PII masking, configurable capture scope, and support for hybrid/on-premises data gateways for customers in regulated industries.
- Enterprise scale: architecture supports deployments across thousands of users generating millions of events per day.
- Lightweight footprint: the client is a silent background agent, not disruptive to end-user workflows.

**Strategic direction:**
The capturing layer must scale to heterogeneous environments — additional OS support, cloud desktop (VDI), and browser-native capture are the natural expansion vectors. The goal is to eliminate deployment friction so that coverage becomes a non-issue.

---

### Pillar II — Data Intelligence

Everything from the moment raw event data arrives in the platform to the point customers derive actionable insight.

This pillar has three progressive layers:

#### Layer 1 — Worker Productivity (out-of-the-box insights)

The **Work Perspectivity app** is the entry point for most customers. It provides pre-built dashboards and KPIs covering:
- Workforce productivity and capacity utilization
- Application usage patterns
- Time distribution across activities and user cohorts

This layer delivers immediate time-to-value without requiring customers to build anything. It answers the question: *How are people spending their time, and where are the inefficiencies?*

#### Layer 2 — Task Discovery (AI-powered structuring)

Raw clickstream data is inherently noisy. Millions of granular events do not, by themselves, tell a process story. Task Discovery is the intelligence layer that turns that noise into signal.

Using **best-in-class LLM models**, Task Discovery:
- Clusters raw UI events into **meaningful, named business tasks** (e.g. "process invoice," "update customer record," "reconcile discrepancy")
- Denoise the clickstream and surfaces the **process-relevant structure** within it
- Maps discovered tasks to **business context** — objects, applications, process steps

This is what moves customers from "we see what people click" to "we understand what people do and how they do it." Task Discovery is the core differentiation of the data intelligence layer and the foundation for everything that follows.

#### Layer 3 — Process Intelligence Graph Enrichment

The final and most strategic layer: connecting task-level data back into the broader Celonis Process Intelligence Graph.

For a given **case ID** (an invoice, a service ticket, a customer order), customers can now see not just the system-level events but also the **desktop-level tasks** that occurred in parallel or in between. This creates true end-to-end process observability — a complete digital twin that reflects both the automated and the human dimensions of how work gets done.

This enrichment enables:
- Root cause analysis that spans system and human behavior
- Identification of rework, workarounds, and process deviations happening "off-system"
- A richer signal base for process simulation, redesign, and automation targeting

---

### Cross-cutting: Trust, Security & Privacy (Pillar IV in positioning)

Trust is not a feature — it is a foundational constraint that governs every decision in both pillars above.

**Key commitments:**
- **Privacy-first capture:** Automated PII masking, configurable capture scope, and explicit user consent flows. Users are not surveilled; data capture is governed.
- **Enterprise-grade compliance:** GDPR, SOC 2, ISO 27001 alignment. Hybrid/on-premises data gateway for regulated industries.
- **Transparency:** Customers retain full control over what is captured, who is included, and how data is used.

This principle must be reflected in all positioning, sales, and customer-facing materials. See the positioning file (Section 12) for the hard negation: Task Mining is **not** a surveillance or monitoring platform.

---

## 4. The Full Value Loop: Analyze → Design → Operate

Task Mining feeds directly into the three modes of value creation that define the Celonis Build Experience:

| Phase | What Task Mining enables |
|-------|--------------------------|
| **Analyze** | Understand how processes actually run today — including the human work invisible to process mining alone. Surface inefficiencies, bottlenecks, and deviation patterns. |
| **Design** | Model the target process state with full visibility into current-state behavior. Identify which manual tasks are candidates for automation, standardization, or elimination. |
| **Operate** | Deploy improvements via process orchestration, RPA, or agentic solutions — grounded in operational reality, not assumptions. Task data provides the operational memory that makes AI agents reliable. |

This loop closes the gap between insight and action, and it is only possible when the process intelligence picture is complete. Task Mining is what makes it complete.

---

## 5. Differentiation Summary

| Dimension | Task Mining (Celonis) |
|-----------|----------------------|
| **Strategic fit** | Platform-native; not a standalone product |
| **Primary signal** | UI metadata / DOM elements (not screenshot-dependent) |
| **Intelligence layer** | LLM-powered task discovery, not just event replay |
| **Process connection** | Direct enrichment of the Process Intelligence Graph per case ID |
| **End state** | Complete digital twin enabling Analyze → Design → Operate |
| **AI readiness** | Provides operational memory and task context for agentic AI systems |
| **Trust & privacy** | Privacy-first by design; not a surveillance tool; enterprise-grade compliance built in |

---

## 6. What Task Mining Is Not

- Not a **standalone RPA discovery** tool whose primary output is automation scripts
- Not a **surveillance or monitoring** platform — privacy and user trust are non-negotiable constraints
- Not a **replacement for process mining** — it is an additive, complementary data layer

---

## 7. Open Strategic Questions

1. **OS and environment expansion** — When does Windows-only become a strategic constraint? What is the prioritization logic for macOS, VDI, and browser-native capture?
2. **Task Discovery accuracy benchmarks** — What are the thresholds that define "production-ready" task clustering for different industries?
3. **Data pool architecture evolution** — As task data volumes grow, what is the long-term data model for efficient Process Intelligence Graph joins?
4. **Agentic AI integration depth** — How should task execution history be exposed as structured context for Celonis agents and third-party LLM-based orchestrators?
