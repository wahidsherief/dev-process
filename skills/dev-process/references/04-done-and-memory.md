# Done check and memory note

You run the check and gather the proof. Ask the developer only for what you cannot do (for example screenshots in a browser). N/A needs a written reason the developer can confirm in one word.

Proof is a screenshot, query plan, test output or log line. Save it under `docs/proof/<task>/` or link it in the PR. No proof, no tick.

## Short checks by lane

- **Quick change:** acceptance line met; tests pass; no hard-coded value or secret; UI: screenshots taken or listed.
- **Bug fix:** failing test shown, then passing; root cause stated; no unrelated changes; suite green.
- **Hotfix:** stabilised first; failing test if feasible; named approver; rollback step stated; incident note within 24 hours.
- **Data fix:** script with dry run; backup and rollback tested; counts reconciled; approvals; run log.
- **Refactor:** same tests green before and after; no test edited to pass; no feature mixed in.
- **Upgrade:** scan before and after; tests green at each step; rollback is a revert.
- **Spike:** note with recommendation; branch not merged.
- **Release:** pre-release checklist with proof; release owner sign-off.

## Full flow: the 12 items

Tags: **[S]** applies in Safe and Risk. No tag: Risk only.

**UI**
- [S] Density modes, dark and light, 360 / 768 / 1280 px verified with screenshots
- [S] Validation, toasts and alerts, loading, empty and error states
- [S] Fallback pages (404, 500, 403, offline) and the error boundary
- Restrained colors, one font family, uncluttered, short animations, reduced motion
- [S] Accessibility scan clean, no hard-coded colors

**Platform**
- [S] Critical actions logged; a test error visible in the error-reporting tool (where applicable or decided)
- Settings page for configurable values; caching with invalidation
- Email in Mailpit; test mode, seed and reset

**Data**
- [S] No N+1, indexes in place, query plans checked, migration and rollback tested

**AI**
- Settings, usage log, cost in GBP and USD, budget alert, mock mode

**Security**
- [S] Auth and roles enforced, scans clean, rollback noted

**Process**
- [S] Tests pass, reviewer report attached when required, approver named, memory note saved
- [S] Every acceptance criterion in the brief is met, with proof

Only the items for the areas touched need proof. Write the result in the summary and the PR description, for example `9 of 12: 7 proven, 2 N/A (reasons)`. If an item is open, list exactly what would close it.

## Memory note

Draft it in the same PR. Location: `docs/memory/<category>/YYYY-MM-DD-short-name.md`.

| Folder | Use |
|---|---|
| feature | A new capability delivered |
| fix | A bug or issue resolved. Record the root cause, not only the patch. |
| refactor | An internal change with no behavior change; non-security upgrades |
| migration | A legacy slice or data moved |
| decision | Design records and spike results |
| incident | A production problem, with cause and prevention |

Length: eight lines for a quick change or a fix, twenty at most otherwise. Content: what and why; what changed; decisions and trade-offs; how verified; gotchas; PR link. Skip it for a trivial quick change with nothing worth keeping.

Before planning any task, search `docs/memory/` for related notes.
