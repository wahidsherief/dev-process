---
name: legacy-migration
description: 'Run the legacy migration track: choose an approach, then seven stages with four human gates, legacy risks, and UI redesign. Use when migrating, modernizing or redesigning an existing system, when asked to skip tests or the safety net during a migration, or when the project type in docs/PROCESS.md is legacy migration.'
---

# legacy-migration

Migration track. State lives in `docs/PROCESS.md` (migration table). Each slice goes through the normal work loop in the `dev-process` skill.


Migrate in slices. Do not rewrite everything at once. Each gate needs a named human approval before work continues. Record progress in `docs/PROCESS.md`.

## Hold the line

- Never skip the safety net (stage 4) because of time pressure or because "the old app has no tests". Say so plainly, then offer the smallest set of characterization tests that covers the one critical flow, and start there.
- Never change code before Gate 1 (baseline and guardrails) is approved and Gate 2 (decision record and critical-flow coverage) is approved. Name each gate and who approves it.
- If `docs/PROCESS.md` does not exist, start at stage 1 (discover and baseline). Do not start with code.

- For a UI redesign, never roll a new look across pages before the technical lead approves the golden page.

## Choose an approach (record it in the decision record)

| Approach | Use |
|---|---|
| Piece by piece beside the old system (preferred) | Each slice goes live behind a feature flag, then the old slice is switched off |
| Parallel run | Risky logic: old and new process the same input and the results are compared |
| In-place upgrade | Small version steps with strong tests |
| Full rewrite (avoid) | Only if the old system cannot be understood or run |

## Seven stages

1. **Discover and baseline.** Map the code once with an explore agent; save `docs/ARCHITECTURE.md`. Record build time, tests, coverage, bundle size, query times, known bugs in `docs/BASELINE.md`. Frontend: list screens and components. Backend: list modules, endpoints, tables, jobs. Also list scheduled jobs, emails, integrations and manual processes (hidden behavior).
2. **Guardrails.** CLAUDE.md, hooks, deny rules and CI in place before any change. **Gate 1: technical lead approves baseline and guardrails.**
3. **Decision record.** One page: options, chosen target and reason, slice order, rollback path, tier.
4. **Safety net.** Characterization tests lock current behavior. Backend: golden API responses and data fixtures. Frontend: end-to-end tests and screenshots. CI green on untouched code. **Gate 2: technical lead approves the decision record and coverage of critical flows.**
5. **Migrate in slices.** One module or screen per session, behind a feature flag, using the normal work loop (`start`, `plan`, `build`, `review`, `done`). Data: backup, dry run on a copy, reconcile counts afterwards. Old tests stay green. **Gate 3: approver reviews every slice PR.**
6. **Verify and release.** End-to-end, security and performance checks against the baseline. Staged rollout, tested rollback, monitoring and alerts live. **Gate 4: release owner signs off.**
7. **Retrospective.** Compare metrics with the baseline. Update CLAUDE.md, skills and this procedure.

At each gate: stop, summarize the evidence, name the approver, and wait. Record who approved and when.

## Legacy risks

| Risk | Response |
|---|---|
| Missing documentation | Claude maps the code and writes it down. A human corrects it. |
| Missing tests | Write characterization tests before any change. |
| Hidden behavior | List scheduled jobs, emails, integrations and manual processes in the baseline. |
| Data | Back up, dry run on a copy, reconcile counts afterwards, plan the rollback. |
| Dependencies | Upgrade in small steps and run the tests after each. |
| Dead code | Remove only after tests and usage logs show it is unused. |

## UI redesign (logic does not change)

1. **Freeze logic.** Tag the current release. Keep tests green. Change only markup and styles.
2. **Audit and design system.** Audit every screen and component. Build tokens and a small component set of 15 to 20.
3. **Golden page.** Build one page first and stop. The technical lead approves it before the look is applied to other pages. Apply it page by page.
4. **Visual QA.** Screenshots against the golden page, accessibility scan, three widths, light and dark, three densities.
5. **Keep structure.** Keep the legacy structure and navigation. One design owner.

## Role agents (optional)

For a large migration, create role agents with `extend-process` (for example a read-only `migration-planner`, a `frontend-migration` and a `backend-migration` agent). Put the current state and the target in the agent's instructions. Keep them flat: agents do not call other agents, because each one opens its own context and uses more tokens.
