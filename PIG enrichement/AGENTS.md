# AGENTS.md — Emotion Playground

## Project Overview

This is the Celonis Emotion design system playground — a sandbox Angular app where designers, product managers, and developers prototype Celonis-style applications using the [Emotion design system](https://github.com/celonis/emotion).

**Target audience**: Anyone, especially non-technical users working with AI coding agents (Cursor, GitHub Copilot, Kiro, etc.).

**Workflow**:

1. Clone the repo and create a branch
2. Build your prototype with the help of an AI agent
3. Open a pull request
4. A preview URL is automatically deployed (like Vercel)
5. Share the preview link with your team

Prototypes live in branches only — never merge into `main`. The `main` branch stays clean as a starting point.

**Key commands**:

```bash
bash scripts/bootstrap.sh   # First-time setup from scratch (installs all prerequisites)
yarn install                 # Install dependencies (requires GITHUB_TOKEN for @celonis packages)
ng serve                     # Run locally at http://localhost:4200
ng build                     # Production build
```

**First-time users without developer tools**: If the user has no Homebrew, Git, Node.js, or Yarn, point them to `scripts/bootstrap.sh`. If they don't have the repo yet, they can download the script from the [landing page](https://supreme-chainsaw-4q5oznn.pages.github.io/) and run `bash ~/Downloads/bootstrap.sh`.

**App shell**: The root `AppComponent` wraps everything in `ce-main-layout`, giving every prototype the Celonis look and feel automatically. Build your content inside it — customize the sidebar, header, and content area in your branch however you like.

## Agent output style (readability)

Users skim; lead with **state emojis** on bullets, headings, or short labels so outcomes are obvious at a glance.

- **🟢** — Success, done, safe to proceed, recommendation, no blockers
- **🔴** — Error, failed, blocked, must fix, risk, or “do not”
- **🟡** — Warning, caution, needs attention soon, or fragile area
- **🔵** — Neutral info, context, or FYI (not good or bad)
- **⏳** — In progress, waiting, or pending
- **✅** — Checklist item completed or requirement satisfied
- **❌** — Rejected, invalid, or requirement not met

Use these consistently; add others when they clarify (for example **⚠️** for breaking changes, **📝** for follow-ups). Do not replace precise wording with emojis alone — pair a short emoji cue with the actual detail.

## Emotion Component Rules

### Mandatory usage

- MUST use `@celonis/emotion` components for all UI elements — buttons, inputs, tables, modals, dialogs, panels, etc.
- NEVER create custom components that duplicate what Emotion already provides. Check the component catalog first.
- MUST register icons via `CeIconRegistryService` from `@celonis/icons`.

### Tokens and styling

- MUST use semantic design tokens for colors, spacing, and typography — no hardcoded hex, rgb, or px values.
- Required SCSS imports in every component stylesheet:

```scss
@use '@celonis/emotion/styles/tokens' as t;
@import '@celonis/emotion/styles/core';
```

- Use `@include typeset('...')` for all text styling. Never set font properties directly.
- Use semantic tokens (`$surface-*`, `$content-*`, `$border-*`) — never primitive tokens (`$_palette-*`, `$size-*`, `$space-*`).

### States

- Every data view must handle: loading (`ce-skeleton`), empty (`ce-placeholder`), and error states.
- Use `ce-no-results` for search/filter misses.

### No tests

This is a prototyping playground — do NOT write, generate, or suggest unit tests, integration tests, e2e tests, or any other kind of test. Focus entirely on building the prototype.

### Anti-patterns (never do these)

- Hardcoded colors (hex, rgb), pixel spacing, or direct font properties
- Custom buttons, inputs, modals, tables, or dialogs — use Emotion's
- Primitive tokens in styles
- Custom overlays when a dialog or tooltip suffices
- Centered buttons (always left- or right-aligned)
- Missing loading/empty/error states on data views
- Writing tests of any kind

### Full component documentation

For detailed component APIs, usage examples, and patterns, read:
`node_modules/@celonis/emotion/ai-docs/component-catalog.md`

## How to Build a Prototype

This section is for non-technical users working with an AI coding agent. You don't need to know Angular — just describe what you want and let the agent build it.

### Step 0: Branch guard (agents MUST follow this)

**Before making any code changes**, the agent MUST check the current git branch:

```bash
git branch --show-current
```

- **If on `main`**: Create and switch to a new prototype branch automatically before making changes. Use a short, descriptive branch name derived from the request when possible, for example:
  ```bash
  git checkout -b dashboard-prototype
  ```
  Then proceed with the request on that branch.

- **If on any other branch**: This is an existing prototype. Continue normally — the user is iterating on an in-progress prototype.

**Never write code or modify files while staying on the `main` branch.** The agent must switch to a new branch first so `main` stays clean as the starting point for all prototypes.

### Step 1: Set up your branch

If the agent didn't already create a branch for you in Step 0, tell it:

> "Create a new branch called `my-prototype` and switch to it."

Or do it yourself in the terminal:

```bash
git checkout -b my-prototype
```

### Step 2: Describe what you want

Give your AI agent a prompt like one of these examples:

> "Build a dashboard with a KPI bar at the top showing 4 metrics, and a data table below with sortable columns."

> "Create a settings page with a form that has text inputs, dropdowns, and a save button. Use Emotion components."

> "Build a task list view with a sidebar for categories and a main content area showing tasks in a table with status indicators."

> "Add a sidebar navigation to the app shell with links for Dashboard, Settings, and Reports."

The agent will read this file and the Emotion component catalog to pick the right components.

### Step 3: Preview locally (optional)

Ask your agent to run the app, or run it yourself:

```bash
ng serve
```

Then open http://localhost:4200 in your browser.

### Step 4: Push and open a pull request

Tell your AI agent:

> "Commit all changes and push to the remote branch."

Then open a pull request on GitHub. A preview URL will be automatically deployed and posted as a comment on your PR. Share that link with your team.

### Step 5: Iterate

Keep telling your agent what to change. Every push to your branch updates the preview automatically.

## Component Quick Reference

| Need | Component | Module Import |
|------|-----------|---------------|
| Button | `<button ceButton>` | `CeButtonModule` |
| Table | `<ce-table-grid>` | `CeTableGridModule` |
| Panel / Card | `<ce-panel>` | `CePanelModule` |
| Dialog | `CeDialogService` | `CeDialogModule` |
| KPI | `<ce-kpi>` | `CeKpiModule` |
| Icons | `<ce-icon>` | `CeIconModule` |
| Loading skeleton | `<ce-skeleton>` | `CeSkeletonModule` |
| Empty state | `<ce-placeholder>` | `CePlaceholderModule` |
| Tabs | `<ce-tabs>` | `CeTabsModule` |
| Input | `<input ceInput>` | `CeInputGroupModule` |
| Dropdown | `<ce-input-dropdown>` | `CeInputDropdownModule` |
| Status indicator | `<ce-status-indicator>` | `CeStatusIndicatorModule` |
| Toast notifications | `CeNotificationsService` | `CeNotificationsModule` |
| Info banner | `<ce-info>` | `CeInfoModule` |
| Layout | `<ce-main-layout>` | `CeMainLayoutModule` |
| Section | `<ce-section>` | `CeSectionModule` |
| List | `<ce-list>` | `CeListModule` |

All imports come from `@celonis/emotion`. Icons come from `@celonis/icons`.
