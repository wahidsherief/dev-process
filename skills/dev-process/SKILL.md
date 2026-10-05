---
name: dev-process
description: 'Runs the team development process behind the scenes for any development task: new feature, small change, bug, production issue, refactor, upgrade, migration or release. Use when a developer describes work to do in a project set up with this process (docs/PROCESS.md exists), or runs init, analyze, summary, status, resume or patterns.'
---

# dev-process

The developer describes the work in plain words. You do the rest: pick the lane, apply the standards, run the checks, gather the proof, write the notes and hand back one short summary. The developer should have to do as little as possible. The rules stay strict underneath.

## What the developer sees

- They type the task. No separate start step, no modes, and they are never asked to choose a lane.
- Optional commands (namespaced, for example `/dev-process:init`): `init` (once per project; prepares it and continues the current task), `analyze` (project and standards report, on request), `status`, `summary`, `resume` (after `/clear`), `patterns`. Use Claude Code's own `/clear`.
- You ask **at most one short question block**, only when a wrong guess is costly, each with your recommended answer. Never ask what the repo can answer.
- You stop for a human only at the points in "Stops".
- You finish every task with the short summary (below).

## The hidden flow

1. **Understand.** Read `docs/PROCESS.md` (tier, current task), `CLAUDE.md`, and search `docs/memory/` for related notes. Read code only for the area touched.
2. **Pick the lane and size.** Automatically, from the request and the code. Never ask the developer to choose. If unsure, take the lighter lane that fits, say so, and move up if the work grows. Say the lane in one line.

| Work | Lane | Details |
|---|---|---|
| New feature, large enhancement, new module | Full flow | below, and `references/02-start-and-plan.md` |
| Small change (about 50 lines or less, no database, permission or dependency change), small enhancement, copy or style tweak | Quick | skill `change-lanes` |
| Bug (not urgent) | Bug fix | skill `fix-lanes` |
| Production issue, outage, incident | Hotfix | skill `fix-lanes` |
| One-off production data correction | Data fix | skill `fix-lanes` |
| Internal cleanup, no behavior change | Refactor | skill `change-lanes` |
| Library upgrade or security patch | Upgrade | skill `change-lanes` |
| "Can we...?" investigation | Spike | skill `change-lanes` |
| Release | Release | skill `change-lanes` |
| Move or modernize an older system, redesign its UI | Migration | skill `legacy-migration` |

If a quick change grows past its limits, say so and switch to the full flow.

3. **Brief** (Full flow only). Goal, out of scope, numbered acceptance criteria. Always draft the criteria yourself with proposed answers. Skip the brief for the other lanes: one acceptance line is enough.
4. **Plan** (Full flow, hotfix actions, data fix). Short: tables and indexes, settings, log events, cache keys, tests, size. Show it and wait only for new or large work. Otherwise show a two-line summary and continue.
5. **Build.** Only what the plan says, with tests. If the task clearly matches an Approved or Active pattern in `docs/PATTERNS.md`, reuse it (`references/patterns.md`). Apply the standards for the areas touched, without asking (`references/autonomy.md`): call `security-check`, `db-check`, `ui-check`, `ai-check` as the work touches them.
6. **Verify.** Run lint, tests and scans (hooks already run them after edits). Run the `standards-reviewer` agent **only** when the tier is Full and the change is over about 80 lines or touches authentication, permissions, migrations or money. Otherwise review it yourself against the lane's short check. Gather the proof yourself.
7. **Record.** Update `docs/PROCESS.md` (short). Write the memory note when the lane calls for one (`references/04-done-and-memory.md`).
8. **Summary.** The short summary below. The developer opens the PR; the approver approves.

## Short summary after every task (always this shape)

```
Lane:  Checked:  Changed:  How:  Proof:
Standards applied:  Standards skipped (reason):  Noticed, not changed (only if useful):
Cost: Low | Medium | High     Next:
```

One line each, no repetition. Cost is a judgement of context used, never an exact token count. Details, and `summary`, `status` and `resume`: `references/summary-resume.md`.

## Stops (human decides)

- The plan, for new or large work
- Approval of a PR; hotfix approval; migration gates; release sign-off
- Anything destructive or hard to undo; anything against production
- Red-class data (see `references/01-init.md`)

## Hard rules

1. Plan before code on the full flow. One slice per PR.
2. Never put secrets, passwords or real customer data into a prompt, a log or a note.
3. Never hard-code colors, prices, URLs or settings.
4. Never query the database inside a loop. For every query you add or change: paginate lists, check indexes on foreign-key, filter and sort columns, and add a test that fails if the query count grows.
5. Log every critical action and report every error.
6. Never mark something done without proof. N/A only with a written reason.
7. Never write outside the plan without saying so.
8. Fix or build what was requested and apply the relevant standards to the affected area. Do not bring unrelated existing code up to standard. Mention nearby technical debt only when useful ("Noticed, not changed"). If the fix itself requires changing an area, the changed code follows the standard.

Tier: rules tagged [L] apply in the Light tier and the Full tier; the rest apply to Full only. Read it from `docs/PROCESS.md`.

## Keep it cheap

- Load only what the task needs: one lane skill, only the standards skills for the areas touched, only the reference for the step you are on.
- Do not re-read files you have read. Do not paste whole files into answers: summarize and use diffs.
- Keep `docs/PROCESS.md` under about 40 lines per task and update it at the end of a step, not after every edit.
- One reviewer pass at most, and only when the rule in step 6 says so. Agents do not call agents.
- Memory notes: eight lines for a quick change or a fix, twenty at most for anything else.

## Commands

- `init`: `references/01-init.md`. Prepares the project, then starts the current task. No project scan.
- `analyze`: `references/analyze.md`. The only place the whole project and its standards are scanned, and only on request. Reports ✓ Present / ⚠ Partial / ✗ Missing / — N/A. Fixes nothing.
- `summary`, `status`, `resume`: `references/summary-resume.md`.
- `patterns`: `references/patterns.md`.

Add a project skill, hook or agent: skill `extend-process`.
