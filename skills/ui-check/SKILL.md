---
name: ui-check
description: 'Apply and check the frontend standards: design tokens, compact/standard/relaxed density, dark and light mode, responsive layout, validation, toasts and alerts, fallback pages, data states, accessibility, restrained visual style. Use when building or reviewing screens, components, forms or styles.'
---

# ui-check

Frontend standards. Apply them automatically while building UI and gather the screenshots as proof. [S] = Safe and Risk; no tag = Risk only.


[S] = Safe standard (always applies). No tag = Risk standard only (risky tasks). Apply these automatically when the task touches UI.

**Scope.** Rule 8 in `dev-process`: apply to the lines this task changes or adds; note nearby gaps as "Noticed, not changed".

## Before you finish (every time)
1. No hard-coded colors, including shadows and overlays: everything is a token.
2. Success = toast. Failure = inline alert. Destructive = confirm dialog that states the consequence. See "Feedback patterns".
3. Loading, empty and error states exist.
4. End with a `Screenshots needed:` list.

## Foundation
- [S] **Design tokens and components.** Color, spacing, radius, shadow and type as tokens. No hard-coded values. One shared component set: button, input, table, modal, nav, card, toast, alert.
- [S] **Layout density.** Compact, standard, relaxed. Saved per user. Applied through spacing tokens.
- [S] **Dark and light mode.** Both themes as tokens. System default plus a saved manual toggle. Verify contrast, focus rings, charts and images in both.
- [S] **Responsive.** Mobile-first. Verify at 360, 768 and 1280 px. Tap targets at least 44 px. No horizontal page scroll.

## UX and feedback
- [S] **Validation.** Client for speed, server for correctness. Message beside the field after the user leaves it; say what to fix. Keep entered data after a failed submit; disable submit while sending. Map server errors to the correct fields.
- [S] **Toasts and alerts.** Toast confirms: short, auto-dismiss after 4 to 5 seconds, maximum 3 stacked. Inline alert for warnings, failures and system notices; never auto-dismiss errors. Confirm dialog for destructive actions only: state the consequence, offer undo where possible. Announce through a live region. No toast for field validation.
- **Built-in guidance.** Empty states explain and offer the next action. Helper text and short tooltips for non-obvious fields; dismissible first-run hints. One term per action across the product; one clear primary action per screen.

## Visual quality
- **No clutter.** One primary action per view. Whitespace over borders. Group related items. Reveal secondary detail on demand (expand, drawer, more).
- **Restrained color.** Neutral base, one accent, muted status colors. At most three hues on a screen; no fully saturated colors. Color carries meaning, not decoration.
- **Typography.** One modern sans family plus one monospace. Variable font or system UI stack. Fixed type scale; line height 1.4 to 1.6; line length 65 to 75 characters.
- **Animation.** Small and purposeful: 150 to 250 ms, ease-out; up to 400 ms for page transitions. Animate only transform and opacity. Skeleton loaders for content. No looping motion on work screens. Respect reduced motion.

## Feedback patterns to apply every time
- Success of an action (create, save, delete): a **toast**. If the project has no toast component, add one small shared component instead of using an inline message.
- Failure of an action or a system problem: an **inline alert** (`role="alert"`, stays until dismissed or fixed), not a toast and not plain status text.
- Destructive action: a **confirm dialog** whose text states the consequence ("This permanently deletes Ada and cannot be undone"), with the safe choice as default. Prefer soft delete with an **undo** toast where it is possible; if undo is not possible, say so in the dialog.
- Field errors: beside the field after the user leaves it. Never a toast.

## Resilience
- [S] **Fallback pages.** Designed pages for 404, 500, 403, offline and maintenance. Each says what happened, offers a way out (home, retry, contact) and shows a reference id. A top-level error boundary shows a fallback and reports the error. Never show a stack trace.
- [S] **Data states.** Loading, empty and error states on every data view. Errors offer a retry.
- [S] **Error reporting.** Client errors reported (Sentry where decided) with source maps. Send the user id only, no personal data.

## Quality gates
- [S] **Accessibility.** WCAG 2.1 AA. Zero violations on the automated scan. Keyboard access, visible focus, labels, alt text, contrast.
- **Performance.** Bundle budget in CI. Lazy-load routes and heavy components. Paginated lists. Track Core Web Vitals: LCP, INP, CLS.
- **Data fetching.** One data layer with cache keys and invalidation. No duplicate or looping requests.
- **Testing.** Component tests for logic, end-to-end for critical flows, screenshot tests for key screens.

## Proof to gather
Always end the UI summary with a `Screenshots needed:` list (screen x theme x density x width: 360, 768, 1280 px) for anything not captured in this session, so the developer can capture them.

Screenshots at 360 / 768 / 1280 in light and dark and the three densities for key screens; accessibility scan output; test output; a forced error visible in the reporting tool.
