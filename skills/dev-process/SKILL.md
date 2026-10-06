---
name: dev-process
description: 'Runs the team development process behind the scenes for any development task (feature, change, bug, production issue, refactor, upgrade, migration, release). Use when a developer describes work in a project with docs/PROCESS.md, or runs init, analyze, summary, status, resume, patterns or token-report.'
---

# dev-process

The developer describes the work in plain words. You pick the lane, apply the standards, run the checks, gather the proof, write the notes and hand back one short summary. Keep the developer's effort low and the rules strict.

## What the developer sees

- They type the task. No modes, and they are never asked to choose a lane or a standard.
- Optional commands (`/dev-process:<name>`): `init`, `analyze`, `status`, `summary`, `resume` (after `/clear`), `patterns`, `token-report`. Details under "Commands".
- You ask at most **one short question block**, only when a wrong guess is costly, each with your recommended answer. Never ask what the repo can answer.
- You stop for a human only at "Stops". Every task ends with the short summary.

## Flow

1. **Understand.** Read `docs/PROCESS.md` (standard, current task) and `CLAUDE.md`; search `docs/memory/` for related notes. Read code only for the area touched.
2. **Pick the lane.** Automatically, from the request and the code. If unsure, take the lighter lane that fits, say so, and move up if the work grows. Say the lane and the areas touched (UI, API, data, AI, jobs) in one line.

| Work | Lane | Details |
|---|---|---|
| New feature, large enhancement, new module | Full flow | below; `references/02-start-and-plan.md` |
| Small change (about 50 lines or less, no database, permission or dependency change), copy or style tweak | Quick | `change-lanes` |
| Bug (not urgent) | Bug fix | `fix-lanes` |
| Production issue, outage, incident | Hotfix | `fix-lanes` |
| One-off production data correction | Data fix | `fix-lanes` |
| Internal cleanup, no behavior change | Refactor | `change-lanes` |
| Library upgrade or security patch | Upgrade | `change-lanes` |
| "Can we...?" investigation | Spike | `change-lanes` |
| Release | Release | `change-lanes` |
| Move or modernize an older system, redesign its UI | Migration | `legacy-migration` |

A quick change that grows past its limits switches to the full flow; say so.

3. **Brief** (full flow only). Goal, out of scope, numbered acceptance criteria. Draft the criteria yourself with proposed answers. Save it to `docs/PROCESS.md` and show it with the lane, areas touched, the standards that apply and any N/A rule with a one-line reason (`references/02-start-and-plan.md`). Other lanes need one acceptance line.
4. **Plan** (full flow, hotfix actions, data fix). Short: tables and indexes, settings, log events, cache keys, tests, size. Wait for approval only for new or large work; otherwise show two lines and continue.
5. **Build.** Only what the plan says, with tests. Reuse an Approved or Active pattern from `docs/PATTERNS.md` when the task clearly matches (`references/patterns.md`). Apply the standards for the areas touched without asking (`references/autonomy.md`): `security-check`, `db-check`, `ui-check`, `ai-check`.
6. **Verify.** Run lint, tests and scans (hooks run them after edits). Check that every critical action you added has a log or audit line (`security-check`). Run the `standards-reviewer` agent **only** when the task's standard is Risk and the change is over about 80 lines or touches authentication, permissions, migrations or money; otherwise review against the lane's short check yourself. Gather the proof yourself.
7. **Record.** Update `docs/PROCESS.md` (short). Write the memory note when the lane calls for one (`references/04-done-and-memory.md`).
8. **Summary.** The developer opens the PR; the approver approves.

## Summary after every task

```
Lane:  Checked:  Changed:  How:  Proof:
Standards applied:  Standards skipped (reason):  Noticed, not changed (if useful):
Cost: Low | Medium | High     Next:
```

One line each, nothing the diff already shows. Cost is a judgement of context used, never an exact token count (definitions: `references/summary-resume.md`).

## Stops (human decides)

- The plan, for new or large work
- Approval of a PR; hotfix approval; migration gates; release sign-off
- Anything destructive or hard to undo; anything against production
- Red-class data (`references/01-init.md`)

## Hard rules

1. Plan before code on the full flow. One slice per PR.
2. Never put secrets, passwords or real customer data into a prompt, a log or a note.
3. Never hard-code colors, prices, URLs or settings.
4. Never query the database inside a loop. For every query you add or change: paginate lists, check indexes on foreign-key, filter and sort columns, and add a test that fails if the query count grows.
5. Log every critical action and report every error.
6. Never mark something done without proof. N/A only with a written reason.
7. Never write outside the plan without saying so.
8. Fix or build what was requested and apply the relevant standards to the affected area. Do not bring unrelated existing code up to standard. Mention nearby technical debt only when useful ("Noticed, not changed"). If the fix itself requires changing an area, the changed code follows the standard.

## Standard: Safe or Risk (never asked)

- **Safe** (default) applies rules tagged `[S]`. **Risk** applies every rule (`[S]` plus untagged). Stored once in `docs/PROCESS.md` (`Standard:`); `init` sets Safe. The developer can say "set this project to Risk" at any time.
- **Task risk is temporary.** A task touching payments or money, customer or personal data, authentication or permissions, or migrations is treated as Risk for that task: apply the untagged rules to the changed code and allow the reviewer. The project standard does not change. Say so in the summary; suggest "set the project to Risk?" at most once.
- AI provider calls in a Safe project apply the `[S]` AI rules (data rules, spend cap, usage log). The rest of `ai-check` applies in Risk.

## Keep it cheap

- Load one lane skill, only the standards skills for the areas touched, and only the reference for the current step.
- Do not re-read files or paste whole files: summarize, use diffs.
- `docs/PROCESS.md` stays under about 40 lines per task, updated at the end of a step. Memory notes: 8 lines for a quick change or fix, 20 at most otherwise.
- One reviewer pass at most. Agents do not call agents.

## Commands

- `init`: `references/01-init.md`. Prepares the project, then starts the current task. No project scan.
- `analyze`: `references/analyze.md`. Light by default; `deep` and `deep --full` map more. Only on request. Fixes nothing.
- `summary`, `status`, `resume`: `references/summary-resume.md`.
- `patterns`: `references/patterns.md`.
- `token-report`: `references/token-report.md`. Reads recorded runs; builds nothing.

Add a project skill, hook or agent: skill `extend-process`.
