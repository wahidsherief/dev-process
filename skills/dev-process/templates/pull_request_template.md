## Lane
<!-- full | quick | bug fix | hotfix | data fix | refactor | upgrade | spike | release | migration -->

## What and why
<!-- Goal in one or two lines. Link the task or ticket. -->

## Acceptance criteria
<!-- Each criterion from the brief, with proof (screenshot, query plan, test output or log line). -->
- [ ] 

## Done check (attach proof, or N/A with a reason)
**UI**
- [ ] Density modes, dark and light, 360 / 768 / 1280 px
- [ ] Validation, toasts and alerts, loading / empty / error states
- [ ] Fallback pages and error boundary
- [ ] Restrained colors, one font, uncluttered, short animations, reduced motion
- [ ] Accessibility scan clean, no hard-coded colors

**Platform**
- [ ] Critical actions logged; a test error visible in the error-reporting tool
- [ ] Settings page for configurable values; caching with invalidation
- [ ] Email in Mailpit; test mode, seed and reset

**Data**
- [ ] No N+1, indexes in place, query plans checked, migration and rollback tested

**AI**
- [ ] Settings, usage log, cost in GBP and USD, budget alert, mock mode

**Security**
- [ ] Auth and roles enforced, scans clean, rollback noted

**Process**
- [ ] Tests pass
- [ ] Reviewer report attached (or: not required)
- [ ] Memory note saved in docs/memory/<category>/ (or: none needed)
- [ ] Approver named

## Applied automatically
<!-- What Claude applied without asking, one line each, so the approver can spot-check. -->

## Reviewer report
<!-- Paste the standards-reviewer output. -->

## Notes for the approver
<!-- N/A items with reasons, trade-offs, follow-ups. -->
