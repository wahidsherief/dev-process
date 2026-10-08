# Task summary, status and resume

## Cost wording (the shape is in `SKILL.md`)

The meta line shows the real tokens from `scripts/task-tokens.py`: **used** = fresh input + cache-creation + output tokens (the work), **cached** = cache-read tokens (context re-read at a fraction of the price). Never state a number the script did not print; if it prints nothing, show the level only. The summary itself is not counted.

The level is judged from **used**. Low: a small change, few files read. Medium: several files, tests run, one standards skill. High: the full flow, many files, a reviewer run, or an analysis. Indicative cut-offs, to be tuned from real runs: Low under about 30k used, Medium 30k to 150k, High above 150k. Offer the PR title and description only when the next step is opening the PR.

## status

Five lines at most: task, lane, step, done so far, what needs the developer. Read from `docs/PROCESS.md`. Do not read code.

## summary: resume-friendly

Writes the full current-task state to `.devprocess/summary.md` (overwrite) and shows it. It must be enough to continue after `/clear` with nothing else. Write it in a professional tone, as a short report a reviewer could read cold. Use the same plain style as the end-of-task summary (`SKILL.md`): no table, no box, no emoji, and nothing before the headline or after **Action needed**. Leave out any line that is empty; no repetition.

```
**<Headline: where the task stands, 15 words at most>**

*<Lane (S1/S2/S3 for fixes)> · <task type> · <used> used (<cached> cached) · <Low|Medium|High>*

---

**Task:** one line.
**Issue:** what was wrong or requested, and the impact; for bugs, the root cause.
**Fixed By:** how it was resolved and why this approach (key decisions, one line each).
**Changes:**
- [file](path): one short phrase each. This is the list `resume` reads.
**Test Result:** what was run and the result (before -> after).
**Skipped:** standards not applied, with the reason (leave out when none).
**Patterns:** names from docs/PATTERNS.md (only if used).
**Note:** [name.md](docs/memory/<task type>/YYYY-MM-DD-name.md). Leave the line out when there is none.

**Outstanding**
- what is left, including anything not changed on purpose.

**Action needed:** the next step, concrete enough to continue after `/clear`; end with: run `/clear`, then `resume`.
```

The labels are fixed because `resume` reads them. Task type is the memory folder: feature, fix, refactor, migration, decision or incident (`references/04-done-and-memory.md`). Keep it under about 40 lines. Paths and names, not code.

## resume

1. Read `.devprocess/summary.md` and `docs/PROCESS.md` only. If there is no summary, say so and ask for the task.
2. Do not rescan the project. Read only the files under "Changes" and only when the next step needs them.
3. Say in one line where the task stands, then continue from "Action needed". Lane stays as written.
