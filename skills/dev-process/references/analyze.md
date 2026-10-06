# analyze: project and standards analysis (on request only)

Run only when the developer asks. Never run it automatically. It reports; it fixes nothing and starts no refactor. Say the mode and what it will read in one line first.

## Modes

| Command | Reads | Use |
|---|---|---|
| `analyze` (light, default) | `docs/ARCHITECTURE.md` if present, config and dependency files, a small sample per area | Quick view, cheap |
| `analyze deep` | First time: maps the project once into `docs/ARCHITECTURE.md`, then samples each area. Later: only files changed since the last deep report's commit (`git diff --name-only <commit>..HEAD`) | Proper review; repeats are cheap |
| `analyze deep --full` | Re-maps everything, ignoring the previous report | After a big restructure |

An area can be added: `analyze backend`, `analyze deep frontend` (areas: `frontend`, `backend`, `ai`, `security`).

Before a first deep map of a large project (roughly over 300 source files), say so and ask once. Light mode never maps the whole project.

## Steps

1. Read the project standard from `docs/PROCESS.md` (Safe if missing). Judge `[S]` rules in a Safe project, all rules in a Risk project. List untagged gaps in a Safe project only as "Risk-only" rows, not as failures.
2. Find the latest report in `docs/analysis/`. For `deep`, if one exists and has a commit, compare against it; only changed areas are re-checked, unchanged rows are carried over and marked "(carried)".
3. Detect which areas exist (UI, API and data, AI provider calls, jobs, email). Load only the matching standards skills (`ui-check`, `db-check`, `ai-check`, `security-check`), or only the one asked for.
4. For each standard, look at a sample of real code and settings, not every file. Give one mark:

| Mark | Meaning |
|---|---|
| ✓ Present | Found and used consistently |
| ⚠ Partial | Found in some places or incomplete |
| ✗ Missing | Not found |
| — N/A | Does not apply here (give the reason) |

5. Give each row one scope: **Current task** (matters to the task in progress), **Project gap** (a real gap overall), or **Unrelated** (code the task does not touch; also for N/A rows). With no current task, no row is "Current task".

## Report

Save a new file, never overwrite: `docs/analysis/YYYY-MM-DD-HHMM-<mode>.md`. First line:

```
Analyzed: 2026-10-06 14:20 | commit a1b2c3d | mode: deep | standard: Safe | previous: 2026-09-01-1010-deep.md (or: first)
```

Then the table `Standard | Status | Scope | Evidence (file or one line)`, for example:

```
Error monitoring   ✗ Missing   Project gap    no reporting client found
UI tokens          ⚠ Partial   Current task   tokens in theme.css; 14 hard-coded colors in forms/
Database indexing  ✓ Present   Unrelated      migrations index all foreign keys (carried)
```

Then at most three lines: changes since the previous report (if any), gaps that matter to the current task, and the three most important project gaps. The files are committed with the project, so the team shares them and the history shows the trend.

## Rules

- Visibility, not scope. A gap is never fixed because of this report. Work on it only when the developer asks for a task on it.
- Standards still apply only to the code a task changes (rule 8).
- Say that the result is sample-based.
