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
7. **Record.** Update `docs/PROCESS.md` (short). Write the memory note into `docs/memory/<task type>/` **before** the summary. It is required for every lane; the only exception is a trivial quick change with nothing worth keeping, shown as "Memory: none (trivial)" (`references/04-done-and-memory.md`). The summary's **Note** line must link the real path.
8. **Summary.** The developer opens the PR; the approver approves.

## Summary after every task

The summary is the whole final message of a finished task: nothing before the headline, nothing after **Action needed**, no closing recap. A plain question (not a finished task) gets a normal answer with no summary. Plain markdown, no table, no box, no emoji:

```
**<Outcome headline, 15 words at most; "Blocked: ..." when blocked>**

*<Lane> · <task type> · <used> used (<cached> cached) · <Low|Medium|High>*

---

**Issue:** the effect a user or the system felt, with a number.
**Fixed By:** the approach and the trade-off it made; one link, e.g. [app.py](app.py#L42).
**Test Result:** before -> after numbers (failing then passing for a fix); "Not run, <reason>" if untested.
**Skipped:** standards not applied, with the reason. Leave the line out when none were skipped.
**Note:** [name.md](docs/memory/<task type>/YYYY-MM-DD-name.md). Leave the line out when there is none.

**Insights**
- ...

**Action needed:** one concrete step for the developer.
```

- Task type is the memory folder: feature, fix, refactor, migration, decision or incident (`references/04-done-and-memory.md`).
- Concise but useful: every line is 12 words or fewer, one sentence, and holds something the diff does not show. **Issue** says how bad it was, not a restatement of the request. **Fixed By** gives the reason for the approach, not a list of files. **Test Result** gives numbers, never just "pass". Drop a line with nothing to say. Links are paths relative to the project root.
- Tokens: run `scripts/task-tokens.py` (python3 or python, from this plugin's `scripts/` folder) just before writing the summary and paste its output (`17k used (395k cached)`). If it prints nothing, show the level only. Never invent a number. Level definitions: `references/summary-resume.md`.
- **Insights** only when one changes the developer's next decision, shows a risk the diff does not, or is nearby debt that will cause trouble soon. Each bullet says what is wrong, what it causes and what to do, in 15 words or fewer, with a `file#Lnn` link when it points at code. Worst first, at most 2. A weak or general insight is dropped: none is better than a vague one. A pattern suggestion (`references/patterns.md`) goes here as a bold bullet: `**Pattern candidate:** ...`. Skip the section when there is none; never add general advice. Anything beyond two goes in the memory note.
- The short form is the default for a change under about 20 lines with no skipped standard and no insight: headline, meta line, **Fixed By** (with the test result), **Action needed**.
- Offer the PR title and description only when the next step is opening the PR.

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
8. Fix or build what was requested and apply the relevant standards to the affected area. Do not bring unrelated existing code up to standard. Mention nearby technical debt only when useful (under Insights). If the fix itself requires changing an area, the changed code follows the standard.

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
