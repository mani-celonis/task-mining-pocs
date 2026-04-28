---
name: emotion-ui
description: Build consistent, production-grade dashboard and data UIs with the Celonis Emotion design system. Use when building Angular interfaces with @celonis/emotion, selecting components, applying tokens, or prototyping Celonis-style UIs.
---

# Emotion UI

This skill guides creation of consistent, production-grade dashboard and data interfaces using the Celonis Emotion design system. Emotion powers enterprise dashboards, configuration screens, data tables, and operational UIs — not marketing sites or creative web design.

## Design Thinking

Before writing code, understand the context and commit to intentional choices:

- **Task flow**: What is the user trying to accomplish? What data are they reading, comparing, or acting on?
- **Information hierarchy**: What is primary content vs. supporting detail? Lead with the data the user came for.
- **Interaction model**: Read-heavy views need tables, KPIs, and status indicators. Write-heavy views need forms, validation, and confirmation patterns. Pick the right components for the intent.
- **Consistency over novelty**: Every screen in the app should feel like it belongs to the same product. Reuse the same overlay type for the same intent. Reuse the same button hierarchy. Reuse the same empty-state pattern.

**CRITICAL**: Dashboards succeed through clarity, scannability, and predictability — not through visual surprise. Every layout, spacing, and component choice should reduce cognitive load.

## Dashboard UI Guidelines

### Layout and Structure

- Use `ce-layout` or `ce-main-layout` for page structure. Do not invent custom shells.
- Keep page headers consistent: title left, actions right, one primary button max.
- Use `ce-section` to group related content blocks. Use `ce-tabs` for alternate views of the same dataset.
- Prefer single-column forms. Use multi-column grids only for card/tile dashboards.
- Use `ce-panel` / `ce-frame` for content cards. Apply `cePanelContent` for standard padding.

### Data Presentation

- Tables (`ce-table-grid`) for structured, comparable data. Always include sticky headers.
- KPIs (`ce-kpi`) for headline metrics. Place them prominently at the top of dashboards.
- Status indicators (`ce-status-indicator`) for state-at-a-glance. Be consistent with variant-to-meaning mapping across the app.
- Lists (`ce-list`) for simple enumerations. Tiles (`ce-tile`) for card-based browsing.

### Actions and Feedback

- One primary action per view. Secondary actions use `variant="secondary"`. Destructive actions always use `variant="danger"` with a confirmation dialog.
- Button order: Cancel -> Secondary -> Primary (left to right, highest priority rightmost).
- Use `CeDialogService` for simple confirmations. Use `CeModal` only when custom content is needed.
- Toast notifications (`CeNotificationsService`) for async operation results. Inline banners (`ce-info`) for persistent warnings.

### Empty and Loading States

- Every data view must handle: loading, empty (first use), empty (no results), and error states.
- Use `ce-skeleton` during data load to prevent layout shift.
- Use `ce-placeholder` for first-use empty states with a clear call-to-action.
- Use `ce-no-results` for search/filter misses.

### Spacing and Typography

- Use semantic spacing tokens for all padding, margins, and gaps. Never hardcode pixel values.
- Use `@include typeset('...')` for all text. Never set font properties directly.
- Maintain heading hierarchy: one `h1` per page, then `h2` > `h3` > `h4`. Never skip levels.

## Anti-Patterns

NEVER do the following in Emotion UIs:

- **Custom components that duplicate Emotion**: Check the component catalog before building anything custom.
- **Hardcoded values**: No hex colors, pixel spacing, or direct font properties. Always use semantic tokens.
- **Primitive tokens in styles**: `$_palette-*`, `$size-*`, `$space-*` are internal. Use semantic tokens (`$surface-*`, `$content-*`, `$border-*`, etc.).
- **Inconsistent overlays**: Do not use a modal where a dialog suffices, or a popover where a tooltip works.
- **Centered buttons**: Buttons are left- or right-aligned, never centered.
- **Missing states**: Every async view needs loading, empty, and error handling.
- **Styling Emotion host selectors**: Use content directives (`cePanelContent`, `ceLayoutBody`) and their classes instead.

## Core Workflow

1. Read `llms.txt` from the canonical docs directory first.
2. Pick components from `component-catalog.md` before suggesting custom components.
3. Use import and integration rules from `consumer-guide.md`.
4. Use token decisions from `token-quick-reference.md`, then exact token details from `token-api-reference.md`.
5. Validate interaction and layout choices with `ux-guidelines.md`.
6. Return code that is accessibility-safe, token-compliant, and consistent with the patterns above.

## Output Requirements

For implementation requests, provide:

- Component choice and why it matches the use case
- Required Angular module imports from `@celonis/emotion`
- Template structure using Emotion components/directives
- SCSS using semantic tokens and `typeset` mixin only
- Icon registration from `@celonis/icons` when needed
- State handling: loading, empty, and error states for data views

## New Prototype Checklist

If Emotion is not yet installed, include:

- Package installation: `@celonis/emotion` and `@celonis/icons`
- Minimal standalone component setup with `Ce*Module` imports
- SCSS imports:
  - `@use '@celonis/emotion/styles/tokens' as t;`
  - `@import '@celonis/emotion/styles/core';`
- Icon registration example with `CeIconRegistryService`

## Full Documentation

For detailed reference, read these files from `node_modules/@celonis/emotion/ai-docs/`:

- `component-catalog.md` - All components with APIs and usage examples
- `consumer-guide.md` - Import patterns, theming, common patterns
- `token-api-reference.md` - Complete token, mixin, and utility class reference
- `ux-guidelines.md` - UX patterns and best practices
- `token-quick-reference.md` - Quick token decision trees and usage checks
- `llms.txt` - High-level package overview and quick-start guidance