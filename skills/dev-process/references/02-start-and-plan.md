# Full flow: brief, design and plan

Only for new features, large enhancements and new modules. Other work uses its own lane (see the lane table in `SKILL.md`). No code is written in this step.

## Brief

1. Read the task, any pasted ticket or link, `CLAUDE.md`, `docs/ARCHITECTURE.md` if it exists, and search `docs/memory/` for related notes.
2. Ask what is missing, once, in one block: who uses it, what exactly changes, formats, who is allowed, expected data size. Give a recommended answer with each question. If nothing is missing, ask nothing.
3. Write the brief into `docs/PROCESS.md` under the task:
   - Goal (one or two lines)
   - Out of scope
   - Acceptance criteria: numbered, each testable. Always draft them yourself from your recommended answers, marked "(proposed)" where a question is still open. Never leave them empty.
   - Open questions
4. Classify: areas touched (UI, database, API, AI, email, jobs, settings). From that, the standards skills to use and any rule that is N/A with a one-line reason.
5. Save the brief to `docs/PROCESS.md` before you reply, even when questions are open. Your reply then shows: the lane, the areas touched, the standards that apply, any N/A rule with a one-line reason, the numbered acceptance criteria and the open questions.
6. If the requirement was unclear or had several readings, wait for the developer. Otherwise show a three-line summary and continue.

Never invent a requirement. A title alone is not enough: ask, or stop at "open questions".

## Design (new systems and large modules only)

Write one page to `docs/design/<name>.md` from `templates/design-page.md`: scope, data model, boundaries, targets, threat check, decision record. Stop: the technical lead approves it before the first slice.

## Plan

One slice per plan (one screen or one module). Short. Name:

- Tables and indexes touched or added
- Settings added, with defaults
- Log events and audit entries
- Cache keys and invalidation
- Tests, each mapped to an acceptance criterion
- Expected size (maximum 400 changed lines per PR; split if larger)

New or large work: show the plan and wait. Small slice: show a two-line summary and continue unless the developer objects. Record the plan in `docs/PROCESS.md` in a few lines.
