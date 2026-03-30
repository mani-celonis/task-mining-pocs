# Work IQ × Celonis Task Mining — Proof of Concept

Demonstrates how **Microsoft Work IQ** agent signals (Copilot invocations, tool calls, completions) can be ingested alongside **Celonis Task Mining** desktop/browser captures, clustered into semantic tasks via AI, and visualized as a unified **Process Intelligence Graph (PiG)**.

## Quick Start

```bash
cd work-iq-poc
pip install -r requirements.txt
python run.py
```

Open **http://localhost:5050** — the dashboard launches automatically.

## Architecture

```
Task Mining (Desktop/Browser)  ──┐
                                 ├──→  Unified Schema  ──→  AI Clustering  ──→  PiG
Work IQ (Copilot/M365 Graph)   ──┘     (ETL Adapters)     (TF-IDF+KMeans)    (Dashboard)
```

## What's Inside

| Module | Purpose |
|--------|---------|
| `pipeline/models.py` | Unified activity event schema, task instances, process variants |
| `pipeline/adapters.py` | Source-agnostic normalizers (Task Mining adapter, Work IQ adapter) |
| `pipeline/clustering.py` | AI-based task clustering (TF-IDF vectorization + KMeans) |
| `pipeline/analytics.py` | Process Intelligence Graph builder (variants, KPIs, adoption) |
| `data/generator.py` | Dummy data generator — Contoso Financial, 8 loan cases, 4 analysts |
| `web/server.py` | Flask API server |
| `web/templates/dashboard.html` | Interactive visualization dashboard |

## Dummy Customer Data

**Contoso Financial Services** — Loan Origination Process:
- 8 loan cases (LOAN-4872 through LOAN-4879)
- 4 analysts (Sarah Chen, James Miller, Priya Patel, Marcus Johnson)
- 2 process variants: with Copilot (~62%) and manual-only (~38%)
- Applications: SAP GUI, Outlook, SharePoint, Word, Excel

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/raw` | Raw events from both sources (Task Mining + Work IQ) |
| `GET /api/unified` | Normalized events in the unified schema |
| `GET /api/pig` | Process Intelligence Graph (tasks, variants, KPIs) |
| `GET /api/pipeline` | Complete pipeline output |
