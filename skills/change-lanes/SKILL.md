---
name: change-lanes
description: 'Quick change, refactor (no behavior change), upgrade or security patch, spike and release lanes. Use for small changes, tweaks, cleanups, dependency upgrades, "can we...?" questions and releases.'
---

# change-lanes

Five light lanes. Pick the lane, follow the steps, produce only the listed documents. Hooks, CI and the PR approver apply to all of them.

Read the standard (Safe or Risk) from `docs/PROCESS.md` if it exists; risky tasks use Risk rules (see `dev-process`). Keep every answer short: these lanes exist to be fast.

## Quick change

For: a small UI tweak, copy or style change, config change, or small enhancement in one area. About 50 changed lines or fewer. No database, permission, security or dependency change, no new endpoint.

1. One acceptance line ("the button says Add customer and is green"). No brief, no plan.
2. Make the change. Apply only the standard for the area touched (`ui-check` for UI: tokens not hard-coded values, both themes, 360 and 1280 px).
3. Add a test if there is logic.
4. Short check, in the summary: acceptance line met; tests pass; no hard-coded value or secret; for UI, the screenshots taken or the list of screenshots needed (light and dark at 360 and 1280 px).
5. Memory note only if there is a decision or gotcha worth keeping (eight lines at most). Otherwise none.

If it grows past the limits, say so and switch to the full flow.

## Refactor (no behavior change)

1. Run the tests on the untouched code first and state the result (the baseline). Make sure tests cover the area, including edge cases such as missing related rows and ordering. If not, add characterization tests first and show them green on the untouched code.
2. Change in small steps. Do not edit existing tests to make them pass: if a test must change, it is not a pure refactor.
3. No feature or fix mixed in.
4. Proof: the same tests green before and after; for queries, the count is the same or lower.
5. Memory note in `docs/memory/refactor/` (why, what changed, what did not change).

## Upgrade (dependency or security patch)

1. One dependency, or one family, per PR.
2. Read the release notes for breaking changes. For a security patch, note the advisory id and severity.
3. Upgrade in small version steps. Run the full tests after each step.
4. Proof: scan result before and after; tests green; lockfile committed.
5. Rollback is reverting the PR. Say so in the PR.
6. Memory note in `docs/memory/fix/` (security patch) or `refactor/` (other upgrade), five lines.

## Spike (investigation)

1. State the question and the time box (for example two hours).
2. Work on a throwaway branch `spike/<name>`. Never merge it. No production data.
3. Output: `templates/spike-note.md` saved to `docs/memory/decision/`: the question, options tried, findings, a recommendation, and what to build next.
4. Hand the decision to the technical lead. If it is a yes, the next step is a normal task.

## Release

1. Gather the merged PRs and memory notes since the last release.
2. Write the release notes from `templates/release-notes.md`: version, date, summary, added, changed, fixed, migrations, setting or config changes, known issues, rollback steps. Add the changelog entry.
3. Pre-release checklist, with proof: CI green on the main branch; migrations tested with rollback; feature flags in the intended state; backup taken; monitoring and alerts ready.
4. Stop: the release owner signs off. Claude never deploys.
5. After release: a watch period for errors and latency, then close the release.

## Summary

End with the summary in the format defined in `dev-process` SKILL.md ("Summary after every task"), with the lane named in the meta line (quick change, refactor, upgrade, spike or release). Task type: feature (quick change), refactor (refactor, upgrade), fix (security patch) or decision (spike, release). **Test Result** carries the proof: tests before -> after, scan before -> after.

Proof must show output, not a claim. For a refactor, run the tests first, state the result ("baseline: 1 passed") and run them again after. For an upgrade, run the dependency scan before and after, or say exactly which scanner is missing. For a release, include the checklist with a rollback line. Do not stage or commit generated files such as `__pycache__`.
