# Task summary, status and resume

## Cost wording (the shape is in `SKILL.md`)

Token cost is a judgement of context used, not a token count. Never state a number unless Claude Code shows one. Low: a small change, few files read. Medium: several files, tests run, one standards skill. High: the full flow, many files, a reviewer run, or an analysis. Offer the PR title and description only when the next step is opening the PR.

## status

Five lines at most: task, lane, step, done so far, what needs the developer. Read from `docs/PROCESS.md`. Do not read code.

## summary: resume-friendly

Writes the full current-task state to `.devprocess/summary.md` (overwrite) and shows it. It must be enough to continue after `/clear` with nothing else. Write it in a professional tone, as a short report a reviewer could read cold. Show it as a two-column markdown table (Item | Detail), never a code block. Leave out any row that is empty; no repetition.

| Item | Detail |
|---|---|
| Task | one line |
| Lane | lane (and S1/S2/S3 for fixes) |
| Task type | memory folder: feature, fix, refactor, migration, decision or incident (`references/04-done-and-memory.md`) |
| Issue | what was wrong or requested, and the impact; for bugs, the root cause |
| Fix | how it was resolved and why this approach (key decisions, one line each) |
| Changes | files, one short phrase each; this is also the list `resume` reads |
| Standards | applied; skipped (reason) |
| Verification | what was run and the result (before -> after) |
| Patterns | names from docs/PATTERNS.md (only if used) |
| Memory | path of the note: docs/memory/<task type>/YYYY-MM-DD-name.md, or "none" |
| Outstanding | what is left, including anything not changed on purpose |
| Token cost | Low / Medium / High |
| Guide | the next step, concrete enough to continue after `/clear` |

Keep it under about 40 lines; each cell is a short sentence or phrase. Paths and names, not code. Tell the developer: `/clear`, then `resume`.

## resume

1. Read `.devprocess/summary.md` and `docs/PROCESS.md` only. If there is no summary, say so and ask for the task.
2. Do not rescan the project. Read only the files under "Changes" and only when the next step needs them.
3. Say in one line where the task stands, then continue from "Guide". Lane stays as written.
