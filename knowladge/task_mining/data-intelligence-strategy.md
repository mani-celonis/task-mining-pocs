# Data Intelligence Layer — Strategy Overview

> **Version:** 1.0 | **Owner:** Task Mining PM | **Last updated:** April 2026

---

## 1. Vision & Executive Summary

### The North Star

The Data Intelligence layer is the **core differentiator of Task Mining**. Its primary job is to transform raw desktop activity streams into structured, meaningful tasks — automatically mapped to the Process Intelligence Graph (PiG) — to enrich the Digital Twin.

Its secondary job is to surface opportunities for optimization, automation, and agentic AI deployment.

To fulfill this role at platform scale, data intelligence must be:
- **Source-agnostic** — capable of ingesting clickstream data from any desktop client
- **Strategically aligned with data capture** — co-designed, not bolted on
- **AI-first in its intelligence layer** — LLM-powered clustering is the step-change, not incremental refinement

### Current State

The existing data intelligence layer is tightly coupled to a single capture client and the specific data model of the Workforce Productivity application. This creates three critical limitations:

1. **Pipeline fragility** — new features require changes across the entire transformation pipeline
2. **Data silos** — task mining data cannot be seamlessly joined with Process Mining event logs for end-to-end analysis
3. **Architecture lock-in** — the current model assumes a single source of truth, blocking future heterogeneous capture environments (VDI, browser-native, macOS)

A detailed architectural flow with core issues is documented separately in the appendix.

### The Big Leap

The next most impactful shift in this product area is **mature AI-task clustering** that:
- Radically simplifies how customers interpret Task Mining data
- Automatically augments the PiG with structured, business-level task context
- Unlocks entirely new cross-platform use cases that bridge desktop behavior with system-level process flows

This capability must guide all architectural decisions for the data intelligence layer going forward.

---

## 2. Role Within the Celonis Platform

Data Intelligence is the bridge between raw captured events and the Process Intelligence Graph. It sits at the center of what makes Task Mining a platform-native capability — not a standalone analytics product.

```
Desktop Activity (captured events)
         │
         ▼
┌─────────────────────────────────────────────────────┐
│              DATA INTELLIGENCE LAYER                 │
│                                                      │
│  Layer 1: Worker Productivity (out-of-the-box KPIs) │
│  Layer 2: Task Discovery (AI-powered clustering)     │
│  Layer 3: PiG Enrichment (per case ID mapping)      │
└─────────────────────────────────────────────────────┘
         │
         ▼
  Process Intelligence Graph → Digital Twin
         │
         ▼
  Analyze → Design → Operate
```

No digital twin is complete without the human layer. Data Intelligence is what makes that layer visible, structured, and actionable.

---

## 3. The Three Intelligence Layers

### Layer 1 — Worker Productivity

The entry point for most customers. The **Work Perspectivity app** delivers pre-built dashboards covering:
- Workforce capacity and productivity utilization
- Application usage patterns
- Time distribution across activities and user cohorts

This layer provides immediate time-to-value with zero configuration. It answers: *How are people spending their time, and where are the inefficiencies?*

### Layer 2 — Task Discovery (the core differentiator)

Raw clickstream data is inherently noisy. Millions of granular UI events do not tell a process story on their own. Task Discovery is the intelligence layer that converts noise into signal.

Using best-in-class LLM models, Task Discovery:
- **Clusters** raw UI events into meaningful, named business tasks (e.g. "process invoice," "reconcile discrepancy," "update customer record")
- **Denoises** the clickstream to surface process-relevant structure
- **Maps** discovered tasks to business context — objects, applications, process steps

This is the step-change from "we see what people click" to "we understand what people do and how they do it." Task Discovery is the foundation for everything that follows.

> **FY27 priority:** Reach production-grade clustering accuracy that allows auto-mapping to the PiG without manual SQL. This is the architectural precondition for both strategic initiatives.

### Layer 3 — Process Intelligence Graph Enrichment

The most strategically important layer: connecting task-level data into the Celonis PiG per **case ID** (invoice, service ticket, customer order).

Customers gain:
- A **complete digital twin** — system events + desktop tasks in a unified view
- **Root cause analysis** that spans automated and human behavior
- Identification of rework, workarounds, and off-system deviations
- A richer signal base for process simulation, redesign, and automation targeting

The architectural direction here is a **platform-native model** — moving from isolated, case-centric data pools toward a shared, cost-efficient infrastructure (e.g. Rubberband) that removes data silos between Task Mining and Process Mining.

---

## 4. FY27 Strategic Initiatives

All data intelligence work in FY27 concentrates on two pillars. Work outside these pillars is paused.

---

### Initiative 1 — PiG Enrichment from Task Mining Data

**Strategic intent:** Transform Task Mining from a productivity analysis tool into a platform-native intelligence layer. Evolve the architecture to ingest, standardize, and analyze clickstream data from any source using AI-driven clustering. Break down data silos by migrating to platform-native architecture that enables seamless PiG enrichment.

| | |
|---|---|
| **North Star Metric** | % of raw task mining events auto-clustered into PiG |
| **Definition** | % of ingested events automatically clustered into business-level tasks and successfully mapped to the PiG |
| **Why it matters** | Measures how effectively raw desktop activity converts into reusable process intelligence. If this metric is weak, downstream use cases (SOPs, BPMN, automation, agentic AI) collapse. |
| **Current baseline** | Not measured — measurement infrastructure to be established |
| **FY27 Target** | ≥ …% of ingested events clustered and enriched in PiG; ≥ …% of clustered tasks mapped to PiG without manual SQL |

---

### Initiative 2 — Actionable Insights from Task Mining

**Strategic intent:** Move beyond productivity analysis. By connecting Task and Process data, empower customers to actively fix their processes — generating high-fidelity documentation (BPMN-compatible), Standard Operating Procedures (SOPs), and actionable improvement recommendations grounded in operational reality.

| | |
|---|---|
| **North Star Metric** | % of Task Mining analyses that result in at least one downstream action |
| **Definition** | % of analyses that lead to a concrete downstream action: SOP/BPMN generation, automation/agent/orchestration recommendation, or a process change validated by the customer |
| **Why it matters** | Clearest proof that Task Mining is moving from "Analyze" to "Operate" — closing the loop between insight and execution |
| **Current baseline** | Not measured — measurement infrastructure to be established |
| **FY27 Target** | ≥ …% of analyses trigger at least one concrete action |

---

## 5. Architectural Direction

The current architecture is tightly coupled and client-specific. The target state is:

| Dimension | Current | Target |
|---|---|---|
| **Data ingestion** | Single client, proprietary format | Source-agnostic; any clickstream client via standardized schema |
| **Data model** | Coupled to Workforce Productivity app | Platform-native; shared data layer (e.g. Rubberband) |
| **Task structuring** | Manual SQL + rule-based | AI-driven clustering (LLM-powered Task Discovery) |
| **PiG integration** | Custom per-case join logic | Native enrichment via case ID — zero manual SQL |
| **Scalability** | Scales with single pipeline | Pipeline-agnostic; supports new sources without refactoring |

This evolution is the architectural precondition for both FY27 initiatives to succeed.

---

## 6. Connection to the Full Value Loop

Data Intelligence directly enables all three phases of value creation on the Celonis platform:

| Phase | What Data Intelligence enables |
|---|---|
| **Analyze** | Complete picture of process reality — system events + desktop tasks. Surface inefficiencies invisible to Process Mining alone. |
| **Design** | High-fidelity documentation of current-state behavior. BPMN-compatible task maps and SOPs grounded in observed reality, not assumptions. |
| **Operate** | Automation and agentic AI grounded in real task patterns. Task history provides the operational memory that makes AI agents reliable and auditable. |

---

## 7. What Data Intelligence Is Not

- Not a **monitoring or surveillance layer** — privacy-first design is non-negotiable
- Not a **standalone analytics product** — it exists to enrich the PiG, not to replace Process Mining
- Not a **fixed pipeline** — the target architecture is source-agnostic and extensible by design

---

## 8. Open Questions

1. **Clustering accuracy benchmarks** — What thresholds define "production-ready" for auto-PiG mapping across industries?
2. **Measurement infrastructure** — What telemetry needs to be built to start tracking the two North Star metrics?
3. **Architecture migration sequencing** — What is the phased path from current coupled model to platform-native without disrupting active customers?
4. **Agentic AI integration** — How should clustered task history be exposed as structured context for Celonis agents and third-party LLM orchestrators?
