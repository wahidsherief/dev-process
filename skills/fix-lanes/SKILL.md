---
name: fix-lanes
description: 'Bug fix (failing test, root cause, minimal fix), hotfix (stabilise, approval, incident note) and data fix (dry run, backup, approval) lanes. Use when something is broken, a bug is reported, production is down or degraded, or production data must be corrected.'
---

# fix-lanes

Three lanes for things that are broken. Pick the lane, follow its steps, produce its documents. Hooks, CI and a named human approver apply in every lane: a hotfix may skip ceremony, never the approver or the checks.

Read the standard (Safe or Risk) from `docs/PROCESS.md` if it exists; risky tasks use Risk rules (see `dev-process`). Record the lane and task in `docs/PROCESS.md` (create the task entry if missing).

## Choose the lane

| Situation | Lane |
|---|---|
| A defect, not urgent (severity S3) | Bug fix |
| Production is down, losing data, insecure, or a major feature is broken for users (S1 or S2) | Hotfix |
| Production data must be corrected once | Data fix |
| The fix needs a schema, permission or large design change | Stop: say so and move to the normal flow (`dev-process` `start`) |

Severity: **S1** outage, data loss or security exposure. **S2** a major feature broken for many users. **S3** everything else.

## Lane 1: Bug fix

1. **Reproduce.** Exact steps, expected versus actual, environment, how often. If it cannot be reproduced or the report is too thin, ask for steps, logs (redacted) and the time it started. Do not guess.
2. **Failing test first.** Write a test that fails for the right reason. Show it failing.
3. **Root cause.** One or two sentences on why, not on the symptom. Search for the same pattern elsewhere.
4. **Minimal fix.** The smallest change. No refactoring or cleanup in the same PR. The changed lines follow the applicable standards; the code around them is left alone, and any existing non-compliance goes under "Noticed, not changed" in the handoff. Never "fix" by weakening or deleting a test, or by swallowing the error.
5. **Prove.** The new test passes, the whole suite passes, and a neighbouring behaviour is checked.
6. **Record.** `docs/memory/fix/YYYY-MM-DD-name.md` from `templates/fix-note.md`: symptom, root cause, fix, test, prevention.
7. **Done check (short).** Failing then passing test shown; root cause stated; no unrelated changes; suite green; memory note; approver named. If the fix touched a query, UI, auth code or code that calls an AI provider, also apply `db-check`, `ui-check`, `security-check` or `ai-check`.

Expected size under about 100 changed lines. Larger: say why, or split.

## Lane 2: Hotfix (production issue)

1. **Triage in five lines.** Impact, since when, who is affected, severity, last change deployed.
2. **Stabilise first.** Roll back the last release, switch off the feature flag, disable the job, or add a temporary guard. Prefer a rollback to a fix going forward. Write down what was done and when.
3. **Evidence.** Logs (Amber: redact), error-report links, recent commits, the scope of the damage. Never paste production data (Red).
4. **Fix on a short branch** `hotfix/<name>`. A failing test first if it takes minutes. The smallest change. Do not bundle other work. Do not change data by hand: use the data-fix lane.
5. **Expedited approval.** One named approver (the technical lead or the on-call approver) reviews now. The reviewer agent, CI and hooks still run.
6. **Release with a way back.** State the rollback step before deploying. The release owner signs off. Watch errors and latency for the agreed time afterwards.
7. **Within 24 hours.** Write the incident note from `templates/incident-note.md` into `docs/memory/incident/`: summary, impact, timeline, root cause, what stabilised it, the fix, why it was not caught, prevention actions with owners. Create follow-up tasks for the proper fix (a hotfix may be a stopgap) and for prevention.

Claude never deploys, rolls back or touches production itself. It prepares the steps and waits for a human.

## Lane 3: Data fix (one-off change to production data)

1. **Intent.** Which rows, why, how many, and the expected result.
2. **Script, not manual edits.** A reviewed script in `scripts/data-fixes/`, safe to run twice, with a dry-run mode that prints counts and a redacted sample and changes nothing.
3. **Backup and way back.** Snapshot the affected rows first. Write and test the rollback script.
4. **Dry run on a copy.** Reconcile the counts before and after.
5. **Approval.** The technical lead approves the script and the release owner approves the rollback. A human runs it in an agreed window and logs who ran it, when, and the counts.
6. **Record.** `templates/data-fix-runbook.md` plus a memory note in `docs/memory/fix/` (or `incident/` if an incident caused it).

Claude never runs a data fix against production.

## Summary

End with the short summary from `dev-process/references/summary-resume.md`, with the lane named first (bug fix, hotfix or data fix; add S1, S2 or S3):

```
Lane: <lane> (S1|S2|S3)
Checked:  Changed:  How: <include the root cause>
Proof: <the failing test output, then the passing output; suite result>
Standards applied:  Standards skipped (reason):  Noticed, not changed (only if useful):
Cost: Low | Medium | High     Next: <approver, rollback or deploy step, production items>
```

Proof shows the actual failing run first (paste the one-line failure), then the passing run. Do not stage or commit generated files such as `__pycache__`. A hotfix summary also lists the incident note due within 24 hours. A data fix summary lists the dry-run counts and the rollback script. Offer PR text only when the next step is opening the PR.

## Always stop for a human

Rollback or deploy, running anything against production, approval of the script or fix, and any change that widens beyond the lane.
