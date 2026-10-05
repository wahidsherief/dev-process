# Task summary, status and resume

## Short summary after every task (automatic)

After each task, end with this, kept short. Say nothing that the code or diff already shows.

```
Lane: <lane>
Checked: <what you looked at>
Changed: <files or areas, one line>
How: <how it was fixed or built, one or two lines>
Proof: <tests run and result, screenshots, query numbers>
Standards applied: <list>
Standards skipped: <list with a one-line reason> or none
Noticed, not changed: <only if useful> 
Cost: <Low | Medium | High>
Next: <next step, or "none">
```

Cost is a judgement of how much context the task used, not a token count. Never state an exact number unless Claude Code shows one. Low: a small change, few files read. Medium: several files, tests run, one standards skill. High: the full flow, many files, a reviewer run, or an analysis.

Offer the PR title and description only when the next step is opening the PR.

## status

Five lines at most: task, lane, step, done so far, what needs the developer. Read from `docs/PROCESS.md`. Do not read code.

## summary: resume-friendly

Writes the full current-task state to `.devprocess/summary.md` (overwrite) and shows it. It must be enough to continue after `/clear` with nothing else. Use these headings; leave out any that are empty; no repetition.

```
# Task summary
Task:
Lane:
Scope:               what is in and out
Current state:
Decisions:           what was chosen and why, one line each
Changes:             files and what changed
Standards:           applied / skipped (reason)
Verification:        what was run and the result
Relevant files:      paths only
Relevant patterns:   names from docs/PATTERNS.md
Outstanding:
Next step:
```

Keep it under about 40 lines. Paths and names, not code. Tell the developer: `/clear`, then `resume`.

## resume

1. Read `.devprocess/summary.md` and `docs/PROCESS.md` only. If there is no summary, say so and ask for the task.
2. Do not rescan the project. Read only the files under "Relevant files" and only when the next step needs them.
3. Say in one line where the task stands, then continue from "Next step". Lane and scope stay as written.
