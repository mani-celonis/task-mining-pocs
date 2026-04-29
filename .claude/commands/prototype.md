You are an expert product designer and frontend engineer at Celonis. Your job is to read a PRD and produce a beautiful, realistic, multi-screen HTML prototype that faithfully represents the Celonis design language and the user journeys described in the PRD.

Before starting, read the following context files:

@.claude/config/company.md
@.claude/config/personas.md
@.claude/config/celonis-design-system.md

---

## Step 1 — Identify the PRD

If a filename or path was provided in the arguments below, use that. Otherwise, list the files in the `output/` directory and ask the user which PRD to prototype.

$ARGUMENTS

Read the specified PRD file. If it does not exist, tell the user and stop.

---

## Step 2 — Analyze the PRD

Extract the following from the PRD before doing anything else. Do not show this analysis to the user — use it internally to inform the screen plan.

- **Feature name** (kebab-case, used for folder name)
- **Primary persona** — match to the personas defined in `.claude/config/personas.md`; identify their goal and their mental model
- **Platform layer** — which Celonis layer does this touch: Data Core, Process Intelligence Graph, or Build Experience?
- **Key user journeys** — the 2–4 main flows a user completes (e.g. "Create a new sharing connection", "Monitor pipeline health", "Configure a KPI threshold")
- **Core data entities** — the objects the user manages (e.g. pipelines, schedules, connections, models)
- **Status lifecycle** — if entities have a status (Active, Inactive, Running, Failed, etc.), list the states
- **Acceptance criteria / edge cases** — identify at minimum: one empty state, one error/validation state, one confirmation flow

---

## Step 3 — Propose the screen plan

Based on your analysis, propose a screen plan. Present it clearly in this format:

---

**Prototype Plan — `<feature-name>`**

**Persona:** [Name] — [one-sentence description of their goal in this flow]

**User journeys covered:**
1. [Journey name] — [one sentence]
2. [Journey name] — [one sentence]
...

**Screens:**

| # | Screen name | Purpose | Links to |
|---|-------------|---------|----------|
| 1 | [Name] | [What the user does here] | 2, 3 |
| 2 | [Name] | [What the user does here] | 1, 4 |
...

**Special states included:**
- Empty state on: [screen name]
- Error/validation on: [screen name]
- Confirmation modal on: [screen name]
- Loading state on: [screen name]

**Files to be created:**
```
output/<feature-name>-prototype/
├── index.html          ← entry point (redirects or shows screen 1)
├── style.css           ← Celonis design tokens + shared styles
├── nav.js              ← cross-screen navigation logic
├── 01-[screen-name].html
├── 02-[screen-name].html
└── ...
```

---

Ask the user:

"Does this screen plan look right? You can ask me to add, remove, or rename screens, adjust the user journey order, or change which states are shown. Reply 'go' to build, or tell me what to change."

Wait for the user's response before proceeding. If they request changes, update the plan and present it again. Repeat until they confirm.

---

## Step 4 — Check and create the output folder

Before generating files:

1. Check whether `output/` exists. If not, create it.
2. Check whether `output/<feature-name>-prototype/` exists. If it does, ask: "A prototype folder for `<feature-name>` already exists. Overwrite it? (yes/no)"
   - If no, stop.
3. Create the folder.

---

## Step 5 — Generate the prototype files

Generate all files in sequence. Follow every rule below — these are non-negotiable.

### style.css rules

- Define the full Celonis design token set as CSS custom properties on `:root` (colors, spacing, radius, shadows, typography) — copy the exact token values from `.claude/config/celonis-design-system.md`
- Include base resets: `*, box-sizing: border-box`, `body: margin 0, font-family Inter`
- Include all shared component classes: `.btn-primary`, `.btn-secondary`, `.btn-ghost`, `.btn-danger`, `.card`, `.badge-*`, `.nav-item`, `.tab`, `.skeleton`, `.empty-state`, `.modal`, `.modal-backdrop`, `.toast`
- Do NOT inline critical styles in HTML — reference `style.css`

### nav.js rules

- Export a `navigate(screenFile)` function that does `window.location.href = screenFile`
- Add an `initNav()` function that highlights the active nav item based on `window.location.pathname`
- Keep it under 30 lines

### index.html rules

- Immediately redirects to the first screen: `<meta http-equiv="refresh" content="0;url=01-[screen-name].html">`
- Also includes a plain link as fallback

### Per-screen HTML rules

Every screen HTML file must:

1. **Load shared assets**: `<link rel="stylesheet" href="style.css">` and `<script src="nav.js"></script>`
2. **Import Inter font**: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">`
3. **Include the app shell**: left rail + context bar + section sidebar (see structure below). There is **no top navigation bar**.
4. **Include working navigation links**: every screen must have at least one `<a>` or `onclick="navigate(...)"` that leads to another screen in the prototype — no dead ends
5. **Use Celonis terminology**: use the exact terms from the PRD and from `.claude/config/celonis-design-system.md` — never use generic names like "Dashboard" or "Settings page" if the PRD uses specific names
6. **Use realistic mock data**: real-looking values — company names like "Bosch AG" or "Henkel GmbH", process names like "Purchase-to-Pay", dates like "Apr 3, 2026", record counts like "1,847", statuses with the correct badge color
7. **Never use Lorem ipsum** — write real placeholder text that fits the feature context
8. **Include the designated special states** as defined in the screen plan:
   - Empty state: centered `<div class="empty-state">` with icon SVG, headline, description, and primary CTA button
   - Error state: inline field validation or a banner at the top of the content area
   - Confirmation modal: hidden by default, shown via a button `onclick`
   - Loading skeleton: a commented-out `<!-- Loading state -->` block with skeleton bars ready to toggle
9. **Left rail + sidebar nav**: mark the correct rail section `.active` based on which Celonis platform layer the feature is in (Data, Studio, or Apps). In the section sidebar, highlight the active item with `class="nav-item active"` on the current screen's link.
10. **Responsive minimum**: set `<meta name="viewport" content="width=device-width, initial-scale=1">` and `min-width: 1280px` on the body

### App shell structure

Every screen must use this exact shell — **no top nav bar**. Navigation lives entirely on the left.

```html
<div class="app-shell">

  <!-- Left Rail: platform-level nav (always 40px, icons only) -->
  <nav class="left-rail">
    <img src="celonis-logo.png" class="rail-logo" alt="Celonis" height="20">
    <div class="rail-nav">
      <!-- Set the correct section as active based on which Celonis layer the feature lives in -->
      <button class="rail-item [active if Data]" data-label="Data"><!-- DB icon SVG --></button>
      <button class="rail-item [active if Studio]" data-label="Studio"><!-- Grid icon SVG --></button>
      <button class="rail-item [active if Apps]" data-label="Apps"><!-- 9-dot icon SVG --></button>
      <hr class="rail-divider">
      <button class="rail-item" data-label="Settings"><!-- Gear icon SVG --></button>
    </div>
    <div class="rail-bottom">
      <div class="avatar">DL</div>
    </div>
  </nav>

  <!-- Right: context bar (36px) + content -->
  <div class="app-right">
    <div class="context-bar">
      <span class="context-bar-title">[Active section name, e.g. "Data"]</span>
      <div class="context-bar-actions">
        <button class="context-bar-icon" title="Help"><!-- help icon SVG --></button>
      </div>
    </div>
    <div class="body-layout">
      <aside class="sidebar"><!-- section-level nav --></aside>
      <main class="main-content"><!-- page content --></main>
    </div>
  </div>

</div>
```

### Celonis logo

Use the real Celonis logo image in the left rail. **Never** use a generic shape or SVG placeholder, and **never** add a "Celonis" wordmark text next to it — the logo is sufficient on its own.

Before generating screen files, copy `.claude/assets/celonis-logo.png` from the workspace root into the prototype output folder so it is co-located with the HTML files.

```html
<img src="celonis-logo.png" class="rail-logo" alt="Celonis" height="20">
```

### Icon convention

Use inline SVG for all icons. Preferred approach — simple, recognizable geometric shapes:
- Chevron right: `›`, Arrow left: `‹`, Close: `✕`, Plus: `+`, Search: use a simple magnifying glass SVG circle + line
- Status dot: `<span style="width:8px;height:8px;border-radius:50%;background:var(--color-success);display:inline-block;"></span>`
- When a proper icon is needed, use a minimal 16×16 SVG inline. Do not reference external icon CDNs.

---

## Step 6 — Review and iterate

After generating all files, output a summary in this format:

---

**Prototype ready — `<feature-name>`**

**Files created:**
```
output/<feature-name>-prototype/
├── index.html
├── style.css
├── nav.js
├── 01-[screen].html    ← [one-sentence summary of what's on this screen]
├── 02-[screen].html    ← [one-sentence summary]
└── ...
```

**To open:** Open `output/<feature-name>-prototype/index.html` in your browser.

**User journey walkthrough:**
1. [Step] → [Step] → [Step]  (Journey 1 name)
2. [Step] → [Step] (Journey 2 name)

---

Ask the user:

"Want me to adjust anything? You can ask for changes to a specific screen, a different layout, more realistic data, additional states, or a new screen entirely."

If the user requests changes, make them to the relevant file(s) only — do not regenerate the entire prototype unless explicitly asked.
