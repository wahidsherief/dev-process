# Build and verify

## Build

1. Implement only the approved plan. If something outside it is needed, say so first.
2. Write tests with the code, one or more per acceptance criterion.
3. Apply the standards for the areas touched, silently (`autonomy.md`). Use only the standards skills the task touches.
4. Hooks run lint and tests after edits. Fix failures before moving on.
5. If the diff approaches 400 changed lines, stop and propose a split.
6. Clear the session between slices.

## Verify

1. Run lint, type checks, tests and scans with the commands in `.devprocess/config.json`.
2. Run the `standards-reviewer` agent **only** when both are true: the task's standard is Risk (project Risk, or task risk as in `SKILL.md`), and the diff is over about 80 lines or touches authentication, permissions, migrations or money. For everything else, check the diff yourself against the lane's short check.
3. Fix every blocker and major finding. For each one that stays, say why.
4. Re-run until clean. One reviewer pass; do not loop the agent.
5. Put the reviewer verdict in the summary, one line, with the report path if there is one.

Do not nest agents.
