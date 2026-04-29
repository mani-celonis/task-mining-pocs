# Celonis Aha! Business & Taxonomy Rules

When creating or modifying data in Aha!, you must strictly adhere to the following Celonis company standards.

## 1. Glossary of Acronyms
For context, ensure you understand the following Celonis and Product Management acronyms:
- **GTM:** Go-To-Market (client-facing or commercial activities).
- **KTLO:** Keep The Lights On (maintenance, operational, or technical debt work).
- **PrP:** Private Preview (early access launch phase).
- **PuP:** Public Preview (beta launch phase).
- **GA:** General Availability (final, public launch phase).
- **PnE:** Product and Engineering.
- **PRD:** Product Requirements Document.

## 2. Features vs. Epics: The Core Distinction

### Business Meaning
- **Features are Client-Facing (GTM):** They must have GTM-oriented names and descriptions. The title should be understandable for external stakeholders to hook customers. The description should be a maximum of 2 sentences following a 'who-what-why' formula (e.g., "Find what you need faster...") rather than internal engineering specs.
- **Epics are Internal-Facing:** They are oriented for leadership and the PnE team execution. The description should contain the goal of the solution (2-3 sentences) and include links to designs or PRDs.

### Aha! API Mapping (Critical for Scripts)

Celonis uses the **opposite** of standard Aha! naming. When writing scripts or interpreting user requests:

| Celonis Term | `reference_num` Pattern | Aha! Resource | Endpoints |
|--------------|-------------------------|---------------|-----------|
| **Feature** (GTM) | Contains `-E-` (e.g. `AIMODULES-E-7`) | Epics | `GET/PUT/POST /epics`, `POST /releases/{id}/epics` |
| **Epic** (internal) | No `-E-` (e.g. `AIMODULES-10`) | Features | `GET/PUT/POST /features`, `POST /releases/{id}/features` |

**When the user says "my features"** → they mean Celonis Features (GTM) → use `GET /epics`.  
**When the user says "my epics"** → they mean Celonis Epics (internal) → use `GET /features`.

## 3. Multi-Phase Launches (PrP, PuP, GA)

- Do not create multiple Features for separate launch stages of the same item. 
- A Feature should ideally reflect the GA (General Availability) state.
- If a feature has multiple launch phases, it must be structured as **ONE Feature** assigned to the GA release date, with **MULTIPLE underlying Epics**—one Epic for each specific launch phase (e.g., Epic 1: PrP, Epic 2: GA) assigned to their respective release months.

## 4. Keep The Lights On (KTLO) Work
- KTLO work should be bundled into Features whenever logically possible to maintain a clean roadmap. 
- If bundling isn't practical, KTLO work can exist as Epics only (skipping the Feature level entirely).
- **Mandatory Linking:** All KTLO items (both Epics and Features) MUST be linked to the company-level "Operational Excellence" goal. 
- They must also align with one of the four supporting initiatives: Platform Health, Customer Responsiveness, Efficient Utilization, or PnE Productivity.

## 5. Required Feature Fields
When creating a Feature, the following fields must be properly configured:
- **Development Type:** Must be selected (Options: New Feature, Feature Enhancement, Technical Debt, Architecture Roadmap, or Customer Development).
- **Launch Type:** Must be explicitly set (Options: PrP, PuP, GA).
- **External Roadmap:** Explicitly mark the checkbox at the Feature level if it should be reflected on the external, customer-facing roadmap.

**Aha! API custom field keys** (use in `custom_fields` when creating/updating via REST API):
| UI Field | API Key | Example Values |
|----------|---------|----------------|
| Development Type | `development_type` | `New Feature`, `Feature Enhancement`, `Technical Debt`, `Architecture Roadmap`, `Customer Development` |
| Launch Type | `launch_type` | `PrP`, `PuP`, `GA` |
| For External Roadmap? | `for_external_roadmap` | `Yes`, `No` |

## 6. Now, Next, Later Roadmap Categorization
Celonis uses a rolling status and date-based logic to categorize items into Now, Next, or Later:
- **Now:** Status is "In Progress", "Ready to Release", or "Released". Release Month is Previous Month + Next 2 Months.
- **Next:** Status is "Plan & Design" or "In Progress". Release Month is Next 5 Months.
- **Later:** Status is "Plan & Design", "In Progress", or "Open". Release Month is Later than 6 Months or placed in the Parking Lot.
