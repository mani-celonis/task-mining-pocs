---
name: jira-pm-brief
description: Produce a local PM brief from Jira data—categorized themes, user-facing outcomes, Celonis product mapping, priority, value/delivery risks. Use when the user wants an engineering team overview without reading dozens of tickets, a roadmap-sync brief, or a PM-facing Jira summary.
---

# Jira PM brief (local, not committed)

Compress scoped Jira issues into a **scannable brief** for PMs. **Use `JIRA_JQL`** (e.g. TM + ML Infra + sprint/backlog slice in `.env.example`) so the brief reflects **hundreds** of relevant tickets, not an entire board history. Output files **must not** be committed.

## Prerequisites

- `.env` with `JIRA_*` set; **`KNOWLEDGE_ROOT` recommended** so briefs land in the vault; **`JIRA_JQL` recommended** for Frederik / ML Infra default scope.
- Read [docs/templates/jira_pm_brief.md](../../docs/templates/jira_pm_brief.md) for the section structure.
- Run data through [jira-board-overview](../jira-board-overview/SKILL.md) first.

## Output path

With **`KNOWLEDGE_ROOT` set** (see [external-knowledge](../external-knowledge/SKILL.md)), write under:

`$KNOWLEDGE_ROOT/AhaAgent/jira-briefs/YYYY-MM-DD_tm-ml-infra-brief.md`

when using the **default ML Infra JQL** from `.env.example`. If `KNOWLEDGE_ROOT` is **unset**, the generator uses **`data/jira-briefs/`** in the repo (see `src/pm_data_paths.py`). `jira_pm_brief_generate.py` defaults to the correct directory. **Gitignored** from the repo when under `data/`; vault files are outside the clone — see [AGENTS.md](../../AGENTS.md).

## Workflow

### Option A — Detailed themes (every issue listed)

Use when the PM wants **full traceability** across all issues in the JQL result (no hand-pasted ticket lists).

1. **Fetch JSON with extra fields** (description + sprint; larger payloads). Use a path under the same jira-briefs directory you will use for output, e.g.:

   With vault (`KNOWLEDGE_ROOT` set; replace with your vault path as needed):

   ```bash
   OUT="$KNOWLEDGE_ROOT/AhaAgent/jira-briefs"
   python src/executors/jira_board_overview.py --json --extra-fields 2>/dev/null > "$OUT/_snap.json"
   ```

   Or from repo only (no `KNOWLEDGE_ROOT`):

   ```bash
   python src/executors/jira_board_overview.py --json --extra-fields 2>/dev/null > data/jira-briefs/_snap.json
   ```

   Or set `JIRA_EXTRA_FIELDS=true` in `.env` so `--extra-fields` is implicit for that run. Ensure JSON `source` is `jql` when expecting the PM slice.

2. **Generate the Markdown brief** (deterministic grouping, epic subsections, per-issue tables). Omit `--output` to use the default directory (vault or `data/`):

   ```bash
   python src/executors/jira_pm_brief_generate.py --input /path/to/_snap.json
   ```

   Or pass an explicit `--output` path. Flags: `--group-by component|epic`, `--max-desc-chars`, `--redact-assignees`, `--max-issues-per-theme` (overflow → Appendix). See [docs/jira_api_notes.md](../../docs/jira_api_notes.md).

3. **Optional polish:** Tighten prose or user-facing framing **without dropping issue rows** unless the PM explicitly approves.

### Option B — Executive brief (aggregated)

1. **Fetch data (JSON):**

   ```bash
   python src/executors/jira_board_overview.py --json
   ```

   Optionally add `--also-markdown` for human-readable output in the terminal.

2. **Disambiguate before heavy inference:** If the PM’s product area, glossary, or Aha! focus is unclear, ask **1–2 targeted questions**. Do not guess cross-product dependencies.

3. **Categorize:** Cluster issues into **roughly 5–10 themes** using epic titles, summaries, labels, components.

4. **User-facing lens:** Describe themes as **customer/user outcome** where possible; mark **Inferred — confirm with eng** vs **Explicit in tickets** when Jira text is internal-only.

5. **Celonis product map:** Use PM input, labels/components, or a glossary pattern ([product-glossary.example.md](../../workflows/meeting-ideas-crossref/product-glossary.example.md)). **Confidence: high | medium | low**. **Never** invent Aha! links.

6. **Priority & risks:** Per template; evidence-only.

7. **Length:** Aim for **under two pages** of Markdown unless the user asks for depth.

8. **Write** the file under `AhaAgent/jira-briefs/` (vault) or `data/jira-briefs/` (fallback) using the template sections.

## Guardrails

- **Never** `git add`, commit, or push files under `data/jira-briefs/`. Never paste `JIRA_API_TOKEN`.
- **Read-only Jira** — `jira_board_overview.py` only.
- **No invented facts** — no fake blockers or roadmap links.
- Offer to **redact** assignee names if the brief may leave the team.

## Related docs

- [docs/jira_api_notes.md](../../docs/jira_api_notes.md) — JQL vs board, ML Infra default.
