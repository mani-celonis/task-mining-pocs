# Celonis Design System Reference

> This file is read by the `/prototype` command to produce UI that matches Celonis's visual language.
> It is derived from Figma analysis of the Celonis design system (Core Components, Iconography, and live product files).

---

## Logo Usage

- Always use the official Celonis logo image (`knowladge/assets/celonis-logo.png` relative to the workspace root).
- Display it at **28px height** in the top nav bar.
- **Never** accompany it with a "Celonis" wordmark text — the logo stands alone.
- **Never** substitute it with a generic SVG shape or circle placeholder.

---

## Design Principles

Celonis builds **enterprise-grade, data-dense interfaces** for expert users (IT admins, data engineers, process analysts, business analysts). The visual language prioritises:

- **Clarity over decoration** — every element earns its space; no decorative chrome
- **Data density without overwhelm** — compact rows, clear hierarchy, progressive disclosure
- **Confidence and trust** — precise labels, exact numbers, status always visible
- **Flow-first interaction** — complex operations broken into guided wizard steps with clear progress
- **Contextual depth** — side panels and drawers for detail without losing list context

---

## Color Tokens

### Light Theme (default)

```css
:root {
  /* Surfaces */
  --surface-app:        #F7F6FA;   /* app shell background */
  --surface-card:       #FFFFFF;   /* card, panel, modal background */
  --surface-raised:     #FFFFFF;   /* elevated elements */
  --surface-hover:      #F1F0F5;   /* row/item hover */
  --surface-selected:   #E8ECFF;   /* selected row/item */
  --surface-overlay:    rgba(26, 22, 37, 0.48); /* modal backdrop */

  /* Brand / Accent */
  --accent-primary:     #264AFF;   /* primary blue — buttons, links, active states */
  --accent-primary-hover: #1A3AE0; /* button hover */
  --accent-primary-subtle: #E8ECFF; /* tinted bg for badges, callouts */
  --accent-primary-text:  #1A3AE0; /* blue text on light bg */

  /* Semantic */
  --color-success:      #2AA87A;   /* teal-green — success, positive delta */
  --color-success-subtle: #E6F7F1;
  --color-warning:      #E8861A;   /* amber — warnings */
  --color-warning-subtle: #FEF3E2;
  --color-danger:       #D93025;   /* red — errors, destructive */
  --color-danger-subtle: #FDECEA;
  --color-info:         #1B76D4;   /* blue — informational */
  --color-info-subtle:  #E3F0FC;

  /* Text */
  --text-primary:       #1A1625;   /* headings, primary content */
  --text-secondary:     #6B6880;   /* labels, supporting text */
  --text-tertiary:      #9E9BAE;   /* placeholder, disabled, metadata */
  --text-inverse:       #FFFFFF;   /* text on dark/colored bg */
  --text-accent:        #264AFF;   /* interactive links */

  /* Borders */
  --border-default:     #E2E0EA;   /* standard divider / input border */
  --border-emphasized:  #C8C5D6;   /* focused or prominent border */
  --border-subtle:      #F0EFF6;   /* very light separator */

  /* Icons */
  --icon-primary:       #1A1625;
  --icon-secondary:     #6B6880;
  --icon-accent:        #264AFF;
  --icon-success:       #2AA87A;
  --icon-danger:        #D93025;
}
```

### Dark Theme (used for canvas / graph editors, dark panels)

```css
.dark-surface {
  --surface-app:        #1A1625;
  --surface-card:       #231F35;
  --surface-raised:     #2C2840;
  --surface-hover:      #342F4A;
  --surface-selected:   #3D3660;
  --border-default:     #3A3555;
  --border-emphasized:  #524C70;
  --text-primary:       #EAE8F4;
  --text-secondary:     #A09CBF;
  --text-tertiary:      #6B6880;
}
```

---

## Spacing Scale

```css
:root {
  --space-2:   2px;
  --space-4:   4px;   /* --space-xs */
  --space-8:   8px;   /* --space-sm */
  --space-12:  12px;
  --space-16:  16px;  /* --space-md */
  --space-20:  20px;
  --space-24:  24px;  /* --space-lg */
  --space-32:  32px;  /* --space-xl */
  --space-40:  40px;
  --space-48:  48px;
  --space-64:  64px;
}
```

---

## Border Radius

```css
:root {
  --radius-xs:   2px;
  --radius-sm:   4px;   /* inputs, small elements */
  --radius-md:   8px;   /* cards, dropdowns */
  --radius-lg:   12px;  /* modals, large panels */
  --radius-xl:   16px;  /* feature cards */
  --radius-full: 10000px; /* badges, pills, avatars, toggle */
}
```

---

## Elevation / Shadows

```css
:root {
  --shadow-sm:   0 1px 2px rgba(0,0,0,0.06);
  --shadow-card: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md:   0 4px 8px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
  --shadow-lg:   0 8px 24px rgba(0,0,0,0.12), 0 4px 8px rgba(0,0,0,0.06);
  --shadow-modal: 0 20px 60px rgba(0,0,0,0.20);
}
```

---

## Typography

Font family: `Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`

| Role | Size | Weight | Line-height | Usage |
|------|------|--------|-------------|-------|
| Display | 32px | 600 | 1.2 | Page titles, hero headings |
| Heading 1 | 24px | 600 | 1.3 | Section headings |
| Heading 2 | 20px | 600 | 1.3 | Card headings, dialog titles |
| Heading 3 | 16px | 600 | 1.4 | Sub-section headings |
| Body large | 16px | 400 | 1.5 | Main body copy |
| Body | 14px | 400 | 1.5 | Default text, form labels |
| Body small | 12px | 400 | 1.4 | Metadata, captions |
| Label | 12px | 500 | 1.3 | Column headers, form labels |
| Code | 13px | 400 | 1.6 | Mono: `'JetBrains Mono', 'Fira Code', monospace` |
| Micro | 11px | 500 | 1.2 | Badges, status chips |

---

## Layout Patterns

### App Shell

There is **no top navigation bar**. All navigation is on the left. The shell uses a two-level left navigation:

```
┌──────┬──────────────────────────────────────────────┐
│ Rail │  Data › Breadcrumb path here                 │ ← 36px context bar
│ 40px ├──────────┬───────────────────────────────────┤
│      │ Sidebar  │  Main content area                │
│ Logo │  240px   │  padding: 24px                    │
│      │          │                                   │
│ [D]  │ SECTION  │                                   │
│ [S]  │ Nav item │                                   │
│ [A]  │ Nav item │                                   │
│ ──── │          │                                   │
│ [⚙]  │          │                                   │
│ [?]  │          │                                   │
│  NC  │          │                                   │
└──────┴──────────┴───────────────────────────────────┘
```

**Left rail** (`.left-rail`, always visible):
- Width: `40px`, `background: var(--surface-card)`, `border-right: 1px solid var(--border-default)`
- Celonis logo image at top (`height: 20px`)
- Platform section icons in `.rail-nav`: **Data**, **Studio**, **Apps** (no divider, no Settings in nav group)
- `.rail-bottom` (pinned to bottom) contains, top to bottom: **Settings** (sliders icon), **Help** (? circle icon), **user avatar**
- Icons: 32×32px buttons, icon centered; active item uses `--accent-primary-subtle` background and `--accent-primary` icon color
- Labels shown as CSS tooltips (`:after` pseudo-element) on hover — no text visible in resting state
- Settings icon: horizontal sliders (3 lines with offset handle circles) — represents settings/preferences controls

**Context bar** (`.context-bar`, `.app-right` child):
- Height: `36px`, `background: var(--surface-card)`, `border-bottom: 1px solid var(--border-default)`
- Left side uses `.context-bar-left` (flex row, gap 8px): shows the active section title followed by `›` separator and the page breadcrumb when applicable
- Section title: `font-size: 13px`, `font-weight: 600`, `color: var(--text-secondary)`
- Breadcrumb: inline inside `.context-bar-left`, `margin-bottom: 0` (overrides default content-area style)
- No utility icons on the right — Help and Settings are in the rail bottom

**Section sidebar** (`.sidebar`, always visible when in a section):
- Width: `240px`, `background: var(--surface-app)`, `border-right: 1px solid var(--border-default)`
- Contains grouped nav using `.nav-group-label` and `.nav-item`
- The sidebar is the "extended" view of the active rail section

**HTML structure:**
```html
<div class="app-shell">
  <nav class="left-rail">
    <img src="celonis-logo.png" class="rail-logo" alt="Celonis" height="20">
    <div class="rail-nav">
      <button class="rail-item active" data-label="Data"><!-- icon --></button>
      <button class="rail-item" data-label="Studio"><!-- icon --></button>
      <button class="rail-item" data-label="Apps"><!-- icon --></button>
    </div>
    <div class="rail-bottom">
      <button class="rail-item" data-label="Settings"><!-- sliders icon --></button>
      <button class="rail-item" data-label="Help"><!-- ? circle icon --></button>
      <div class="avatar">DL</div>
    </div>
  </nav>
  <div class="app-right">
    <div class="context-bar">
      <div class="context-bar-left">
        <span class="context-bar-title">Data</span>
        <!-- on pages with breadcrumb: -->
        <span class="breadcrumb-sep">›</span>
        <div class="breadcrumb">
          <a href="01-ingestion-history.html">Ingestion History</a>
          <span class="breadcrumb-sep">›</span>
          <span style="color:var(--text-primary);">Page Title</span>
        </div>
      </div>
    </div>
    <div class="body-layout">
      <aside class="sidebar"><!-- section nav --></aside>
      <main class="main-content"><!-- page content --></main>
    </div>
  </div>
</div>
```

- Content area: `padding: 24px`, `background: var(--surface-app)`
- Breadcrumb is placed in the context bar, **not** in the content area — do not render a standalone `.breadcrumb` div inside `.main-content` or `.panel-main`

### Page Header (inside content area)

```
[Page title H1]                    [Primary action button]
[Breadcrumb or subtitle]
──────────────────────────────────────────────────
[Content below]
```

- Page title: 24px 600
- Divider: `border-bottom: 1px solid var(--border-default)`, `padding-bottom: 16px`, `margin-bottom: 24px`

### Wizard / Step Flow

```
┌─────────────────────────────────────────────┐
│  Step 1   →   Step 2   →   Step 3   (header)│
├─────────────────────────────────────────────┤
│                                             │
│  [Step content card]                        │
│                                             │
├─────────────────────────────────────────────┤
│  [Back]                     [Next / Finish] │
└─────────────────────────────────────────────┘
```

- Step indicator: horizontal, numbered circles (`32px`, `--accent-primary` for active, `--border-emphasized` for inactive), connected by a line
- Content: centered card, `max-width: 720px`, `padding: 32px`, `border-radius: var(--radius-lg)`
- Footer actions: `height: 64px`, `border-top: 1px solid var(--border-default)`, right-aligned with Back left

### Side Panel (detail/config without leaving list)

```
[List / Main content]         │  [Side panel: 384px]
                              │  [Panel header + close]
                              │  [Panel content]
                              │  [Panel footer actions]
```

- Panel: `width: 384px`, `border-left: 1px solid var(--border-default)`, slides in from right
- Header: `height: 56px`, title + close icon
- Footer: `height: 64px`, action buttons

### Graph / Canvas Editor

- Background: dark `var(--surface-app)` in dark theme (`#1A1625`)
- Node cards: `background: var(--surface-card)` in dark (`#231F35`), `border-radius: var(--radius-md)`, colored left border (4px) indicating type
- Connections: SVG lines, `stroke: var(--border-emphasized)` in dark
- Mini-map: bottom-right corner, 160×120px
- Toolbar: dark floating bar at top-center, icon buttons with tooltip

---

## Component Patterns

### Buttons

```css
/* Primary */
.btn-primary {
  background: var(--accent-primary);
  color: var(--text-inverse);
  height: 32px;
  padding: 0 16px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  border: none;
}
.btn-primary:hover { background: var(--accent-primary-hover); }

/* Secondary / outline */
.btn-secondary {
  background: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-emphasized);
  height: 32px; padding: 0 16px;
  border-radius: var(--radius-sm);
}

/* Ghost */
.btn-ghost {
  background: transparent;
  color: var(--text-accent);
  border: none;
  height: 32px; padding: 0 12px;
  border-radius: var(--radius-sm);
}

/* Danger */
.btn-danger {
  background: var(--color-danger);
  color: var(--text-inverse);
  height: 32px; padding: 0 16px;
  border-radius: var(--radius-sm);
}

/* Sizes: sm = 24px height, md = 32px (default), lg = 40px */
```

### Cards

```css
.card {
  background: var(--surface-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  padding: 24px;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: 16px;
}
```

### Data Table

- Row height: 40px
- Header: 36px, `font-size: 12px`, `font-weight: 500`, `color: var(--text-secondary)`, `letter-spacing: 0.04em`, uppercase
- Row hover: `background: var(--surface-hover)`
- Selected row: `background: var(--surface-selected)`
- Column dividers: vertical `1px solid var(--border-subtle)`
- Pagination: 32px buttons, right-aligned, shows "1–25 of 143"
- Sortable columns: caret icon on hover/active
- Checkboxes: 16px, `--accent-primary` check color

### Form Inputs

```css
.input {
  height: 36px;
  padding: 0 12px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  font-size: 14px;
  color: var(--text-primary);
  background: var(--surface-card);
}
.input:focus {
  border-color: var(--accent-primary);
  outline: 2px solid var(--accent-primary-subtle);
}
.input:invalid, .input.error {
  border-color: var(--color-danger);
}
/* Label above input */
.form-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 4px;
}
/* Helper text below */
.form-helper {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 4px;
}
```

### Badges / Status Chips

```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 20px;
  padding: 0 8px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 500;
}
/* Variants */
.badge-success  { background: var(--color-success-subtle); color: var(--color-success); }
.badge-warning  { background: var(--color-warning-subtle); color: var(--color-warning); }
.badge-danger   { background: var(--color-danger-subtle);  color: var(--color-danger); }
.badge-accent   { background: var(--accent-primary-subtle); color: var(--accent-primary-text); }
.badge-neutral  { background: var(--surface-hover);        color: var(--text-secondary); }
```

### Navigation

Navigation is split into two tiers: the **left rail** (platform level) and the **section sidebar** (feature level).

#### Left Rail (`.left-rail`)

```css
.left-rail {
  width: 40px;
  background: var(--surface-card);
  border-right: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 0;
  flex-shrink: 0;
  z-index: 200;
}
.rail-logo { display: block; margin-bottom: 16px; }
.rail-nav  { display: flex; flex-direction: column; align-items: center; gap: 2px; flex: 1; }
.rail-item {
  width: 32px; height: 32px;
  border-radius: var(--radius-sm);
  border: none; background: none;
  color: var(--icon-secondary);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; position: relative;
}
.rail-item:hover  { background: var(--surface-hover); color: var(--icon-primary); }
.rail-item.active { background: var(--accent-primary-subtle); color: var(--accent-primary); }
/* Tooltip */
.rail-item::after {
  content: attr(data-label);
  position: absolute; left: calc(100% + 10px); top: 50%; transform: translateY(-50%);
  background: var(--text-primary); color: var(--text-inverse);
  font-size: 12px; font-weight: 500; white-space: nowrap;
  padding: 4px 8px; border-radius: var(--radius-sm);
  opacity: 0; pointer-events: none; transition: opacity 0.15s; z-index: 300;
}
.rail-item:hover::after { opacity: 1; }
.rail-bottom  { display: flex; flex-direction: column; align-items: center; gap: var(--space-8); margin-top: auto; }
```

#### Section Sidebar (`.sidebar`)

```css
/* Nav group label */
.nav-group-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 16px 8px 4px;
}
/* Nav item */
.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 36px;
  padding: 0 8px;
  font-size: 14px;
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  cursor: pointer;
  text-decoration: none;
}
.nav-item:hover  { background: var(--surface-hover); color: var(--text-primary); }
.nav-item.active { background: var(--accent-primary-subtle); color: var(--accent-primary-text); font-weight: 500; }
```

### Skeleton Loading

```css
.skeleton {
  background: var(--surface-hover);   /* #F1F0F5 */
  border-radius: var(--radius-full);
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}
@keyframes skeleton-pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}
/* Bar variants */
.skeleton-text  { height: 8px;  width: 100%; }
.skeleton-title { height: 16px; width: 60%; }
.skeleton-avatar { height: 40px; width: 40px; border-radius: 50%; }
```

### Empty State

```html
<!-- Center vertically and horizontally in content area -->
<div class="empty-state">
  <div class="empty-state-icon"><!-- SVG icon, 48px, --icon-secondary color --></div>
  <h3 class="empty-state-title">No [items] yet</h3>
  <p class="empty-state-desc">Short description of why and what to do.</p>
  <button class="btn-primary">Create your first [item]</button>
</div>
```

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 64px 32px;
  gap: 12px;
}
.empty-state-title { font-size: 16px; font-weight: 600; color: var(--text-primary); }
.empty-state-desc  { font-size: 14px; color: var(--text-secondary); max-width: 360px; }
```

### Confirmation Modal

```html
<div class="modal-backdrop">
  <div class="modal" style="max-width: 480px">
    <div class="modal-header">
      <h2>Delete "[Item name]"?</h2>
      <button class="btn-ghost icon-only">✕</button>
    </div>
    <div class="modal-body">
      <p>This action cannot be undone. [N] dependent [items] will also be affected.</p>
    </div>
    <div class="modal-footer">
      <button class="btn-secondary">Cancel</button>
      <button class="btn-danger">Delete</button>
    </div>
  </div>
</div>
```

```css
.modal-backdrop {
  position: fixed; inset: 0;
  background: var(--surface-overlay);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.modal {
  background: var(--surface-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-modal);
  width: 100%; max-height: 80vh;
  display: flex; flex-direction: column;
}
.modal-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-default);
}
.modal-body   { padding: 24px; overflow-y: auto; flex: 1; }
.modal-footer {
  display: flex; justify-content: flex-end; gap: 8px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-default);
}
```

### Tabs

```css
.tabs { display: flex; border-bottom: 1px solid var(--border-default); gap: 0; }
.tab {
  height: 40px;
  padding: 0 16px;
  font-size: 14px;
  color: var(--text-secondary);
  border-bottom: 2px solid transparent;
  cursor: pointer;
  white-space: nowrap;
}
.tab:hover  { color: var(--text-primary); }
.tab.active { color: var(--accent-primary-text); border-bottom-color: var(--accent-primary); font-weight: 500; }
```

### Toast / Notification

```css
.toast {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 16px;
  background: var(--surface-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  border-left: 4px solid var(--color-success);
  min-width: 320px; max-width: 480px;
  font-size: 14px;
}
/* Position: fixed bottom-right, z-index 2000 */
```

---

## UX Patterns and Rules

### Navigation Flow Rules
- Every screen must have at least one visible path to another screen — no dead ends
- Wizard flows: always show which step you're on and how many remain (e.g., "Step 2 of 4")
- After a destructive action, return the user to the list view, never to an empty state

### Data and Content Rules
- Use realistic mock data: real-looking company names, real process names, real column names
- Numbers should be plausible (not round: `142`, not `1,000,000`)
- Dates: use relative dates ("3 days ago", "Today at 14:23") where context allows
- Status badges: always show for objects that have a lifecycle (Active, Inactive, Pending, Failed, Running)

### Celonis-Specific Terminology
Use these terms consistently — never invent synonyms:

| Concept | Correct term | Not |
|---------|-------------|-----|
| Data loading jobs | **Data Job** | pipeline, ETL job |
| Data model elements | **Data Model** | schema, dataset |
| Process view | **Process Explorer** | process map |
| Scheduled run | **Schedule** | cron, job |
| Data extraction | **Extractor** | connector |
| Transformation | **Transformation** | transform step |
| User-defined metric | **KPI** | metric, measure |
| Process deviation | **Variant** | case, flow |
| Action trigger | **Action Flow** | automation, webhook |
| Platform layer configs | **Studio** | admin panel, settings |

### Empty States
Always provide an empty state for every list/table view. Include:
1. A descriptive icon (SVG, `--icon-secondary` color, 48px)
2. A headline: "No [items] yet" or "No [items] match your filters"
3. A supporting sentence explaining what [items] are and why the list is empty
4. A primary CTA if the user can create/add items from this view

### Error and Validation States
- Inline validation: show error below the field, `--color-danger` text, 12px
- Page-level errors: banner at top of content area, `--color-danger-subtle` background
- Network/API errors: toast notification + retry option
- Permission errors: full-page state with explanation and contact-admin link

### Loading States
- Skeleton screens for initial page load (not spinners)
- Spinner (`--accent-primary`, 24px) for in-place loading (button clicks, filter changes)
- Progress bar for long-running async operations (file upload, large data jobs)

### Responsiveness
Prototypes are desktop-first (1280px minimum width). Side panels and tables may collapse at narrower viewports but this is not required.

---

## Figma Design System References

The full component library is documented at **[designsystem.celonis.com](https://designsystem.celonis.com)**.

Key Figma files (internal):
- [Core Components](https://www.figma.com/design/gmVXi2VaagRZHneOpvgNAQ/) — `ce-` prefixed components, Emotion framework
- [Iconography 2.0](https://www.figma.com/design/xn8vL0zESk8T4uCGRc5doo/) — icon set
- [DS Documentation](https://www.figma.com/design/1WEKZUkYyN78qqDCpYyxCY/) — usage guidelines

Product reference files:
- [Pipeline Builder](https://www.figma.com/design/AMEoIIcqBfCS3cU9TpUY0W/) — node/graph editor patterns, dark canvas
- [Delta Sharing](https://www.figma.com/design/xfRzCsdOxAtyNDWVBmB7I3/) — dark wizard flow, step indicators
- [Annotation Builder](https://www.figma.com/design/3zYwEnItrJie1Sm7mFMhWD/) — form-heavy configuration flows
- [Knowledge Model](https://www.figma.com/design/ESwGC71nJwz5wRVD9BxhNq/) — graph-based data model editing
- [SQL/PQL Editors](https://www.figma.com/design/COBGGS5ApD14wSMq4D378g/) — code editor, split-panel layouts
- [Process Explorer](https://www.figma.com/design/GqC7aykE47TKtW3PxZzWob/) — process flow visualization
- [Orchestration / Action Engine](https://www.figma.com/design/8jj1HeQ48XqigDN204Lh7b/) — agentic/automation builder
