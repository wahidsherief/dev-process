# <Project name>

Process: dev-process v1.4 · Standard: <Safe|Risk> · Type: <new|existing|legacy migration>
Approver: <name> · Technical lead: <name>

## Stack and commands
- Stack: <language, framework, ORM>
- Lint: `<cmd>`  · Types: `<cmd>`  · Unit tests: `<cmd>`  · E2E: `<cmd>`  · Build: `<cmd>`
- Error reporting: <Sentry | other | none, where applicable or decided>

## How we work
Describe the task in plain words. The dev-process skill picks the lane (feature, bug fix, hotfix, data fix, quick change, refactor, upgrade, spike, release), applies the standards and ends with a short summary. Commands: `/dev-process:init`, `analyze`, `summary`, `resume`, `status`, `patterns`. Patterns live in `docs/PATTERNS.md`. State lives in `docs/PROCESS.md`. Plan before code on new features. One slice per PR (max 400 changed lines). Search `docs/memory/` before planning.

## Hard rules
1. Never put secrets, passwords or real customer data into a prompt, log or note.
2. Never hard-code colors, prices, URLs or settings: use tokens and the settings page.
3. Never query the database inside a loop. No N+1. Index filter, sort and foreign-key columns.
4. Log every critical action. Report every error.
5. Every change has a test. Every PR carries the done check with proof.
6. If unclear and a wrong guess is costly, ask. Otherwise decide and record it.

## Apply automatically
Caching with invalidation, validation, loading / empty / error states, dark and light, density, responsive, audit entries, settings entries, mocks and seed data. Report what was applied.

## Prompt data
Green (code, public docs): allowed. Amber (logs, DB samples, config): redact first. Red (secrets, personal data, production dumps): never.

## Notes
Keep this file short. Detail lives in the dev-process skill.
