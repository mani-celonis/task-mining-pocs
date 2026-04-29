---
description: Celonis-specific Aha! taxonomy rules — inverted Features/Epics naming, multi-phase launches, KTLO, custom fields. Always apply when working with src/ or data/.
paths:
  - "src/**"
  - "data/**"
---

# Celonis taxonomy — rules

Full rules: @docs/celonis_aha_rules.md

## The inversion (critical)

Celonis naming is **opposite** of standard Aha!:

| Celonis term | `reference_num` | Aha! endpoint | Meaning |
|---|---|---|---|
| **Feature** (GTM) | Contains `-E-` e.g. `AIMODULES-E-7` | `/epics` | Client-facing, external roadmap |
| **Epic** (internal) | No `-E-` e.g. `AIMODULES-10` | `/features` | Internal engineering work |

**Check `reference_num` before choosing endpoint.** `-E-` → `/epics`. No `-E-` → `/features`.

## Multi-phase launches

One Feature (GA release) + multiple Epics (one per phase: PrP, PuP, GA).

## Required custom fields

Pass via `{"custom_fields": {"key": "value"}}`:
- `development_type`: "New Feature" | "Feature Enhancement" | "Technical Debt" | "Architecture Roadmap" | "Customer Development"
- `launch_type`: "PrP" | "PuP" | "GA"
- `for_external_roadmap`: "Yes" | "No"

## KTLO

Bundle into Features where possible. Must link to "Operational Excellence" goal + supporting initiative.

## Descriptions

- Feature (GTM): max 2 sentences, who-what-why (e.g. "Find what you need faster...")
- Epic (internal): 2–3 sentences with goal + links to designs/PRDs
