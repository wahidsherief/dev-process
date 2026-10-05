# analyze: project and standards analysis (on request only)

Run only when the developer asks (`analyze`, optionally with an area: `frontend`, `backend`, `ai`, `security`). Never run it automatically. It reads the project, so say that in one line first. It reports; it fixes nothing and starts no refactor.

## Steps

1. If `docs/ARCHITECTURE.md` exists, use it. Otherwise map the code once (stage 1 of `legacy-migration`) and save it there. Use `docs/BASELINE.md` the same way, creating it from `templates/BASELINE.md` only if missing. Do not re-read what is already mapped.
2. Detect which areas exist (UI, API and data, AI provider calls, jobs, email). Load only the standards skills for those areas (`ui-check`, `db-check`, `ai-check`, `security-check`), or only the one asked for.
3. For each standard, look at a sample of the real code and settings, not every file. Give one status:

| Mark | Meaning |
|---|---|
| ✓ Present | Found and used consistently |
| ⚠ Partial | Found in some places or incomplete |
| ✗ Missing | Not found |
| — N/A | Does not apply here (give the reason) |

4. Give each row a scope:
   - **Current task**: matters to the task in progress
   - **Project gap**: a real gap in the project overall
   - **Unrelated**: a gap in code the task does not touch (also use this for N/A rows)

   Every row gets exactly one of these three. If there is no current task, no row is "Current task".

## Output (short)

A table: `Standard | Status | Scope | Evidence (file or one line)`, for example:

```
Error monitoring   ✗ Missing   Project gap    no reporting client found
UI tokens          ⚠ Partial   Current task   tokens in theme.css; 14 hard-coded colors in forms/
Database indexing  ✓ Present   Unrelated      migrations index all foreign keys
```

Then two lines: the gaps that matter to the current task, and the three most important project gaps. Save the table to `docs/ANALYSIS.md` (overwrite) so it is not repeated.

## Rules

- Visibility, not scope. A missing or partial standard is never fixed or refactored because of this report. Work on a gap only when the developer asks for a task on it.
- The standards apply to the code a task changes (see `autonomy.md`). The analysis does not change that.
- Say that the result is sample-based.
