# PRD — PiG new object (reference)

Prototype reference document. Source: product notes for PIG extension and task clustering alignment.

---

## Main assumptions

### Clustering pipeline

AI task clustering organizes raw clickstream into **Tasks** and **Subtasks** — e.g. “handle customer invoices” (Task) composed of subtasks like “find customer invoice” and “communicate on Slack about invoice.” This usually reduces millions of raw events to tens of core Subtasks representing business activities people perform on their machines.

- **Task** = process-level goal.
- **Subtask** = smallest coherent unit of intent.

### Two pipeline goals

Clustering solves two independent problems:

1. Grouping raw events into Tasks/Subtasks.
2. Extracting Object IDs to link them to existing PIG Objects.

### PIG enrichment goal

Clustering output will enrich the PIG so users and agents can leverage structured task data for process intelligence use cases such as analyzing, designing, or orchestrating/improving a process. A strong example is building agentic solutions for manual, repetitive tasks, using organized data from high-level task intent down to low-level application details as context for agent development.

### PIG semantic

PIG currently structures data around **Objects** (Invoice, Sales Order) and the **Events** that occur on them. This is the right anchor for process intelligence.

**Goal:** Extend this model with clustered, task-mined events. **Position Subtask as the primary event type** due to its granular and actionable intent on objects, while maintaining the full hierarchy (**Task → Subtask → Raw event**) as related events to support both process analysis and automation use cases.

### Case ID coverage is structurally limited

From initial customer testing of the pipeline, **Case IDs are not extracted for 40–60% of events**, because they are not visible in the raw metadata. That makes PIG Object linkage impossible for that portion.

We will continue investing in systematic Case ID extraction, but it is **unlikely we can ever classify all work to objects**, as objects often do not fully represent real human work.

### Unlinked work cannot be ignored

Discarding unlinked events creates an incomplete picture of how work is executed. Especially in continuous workforce transformation, customers need **visibility into object-unrelated work** to identify elimination and improvement opportunities as part of agentic transformations.

### New “resource” type in PIG

To anchor the full dataset in the PIG—including unlinked events—introduce a **new resource/Object type** with a type attribute (human/agent), e.g. **“Worker,”** whose identity is consistently traceable, enabling **100% coverage** for events anchored to it.

### New PIG resource type should unify task and agent mining

The new resource (**Worker**) should be **executor-agnostic**—covering human clickstream, agent tool-call logs, and future IoT/non-SoR signals.

- A **common schema** covers shared attributes.
- **Executor-specific** attributes are modeled as **extensions**.
- Each source (task mining, agent mining) can introduce its own **ETL** to normalize data into the expected PIG schema.

---

## Appendix

_Add further PRD sections here as you refine scope (user stories, non-goals, open questions)._
