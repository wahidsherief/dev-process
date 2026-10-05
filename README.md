# dev-process (v1.2)

AI-assisted development standard procedure as a Claude Code plugin. Stack-agnostic. The developer types the task; the standards, proof and notes happen behind the scenes.

## Install

```
claude --plugin-dir /path/to/dev-process      # try it
```

For the team, publish this folder in a git repo and add it to the team's plugin marketplace.

## Use

Describe the work in plain words, in the project repo:

```
"Add an invoice export for finance"           -> full flow (brief, plan, build, verify)
"The order total shows 10.99, should be 11"   -> bug fix: failing test first, then fix
"Production orders page is down"              -> hotfix: stabilise, rollback, incident note
"Change the heading to Order Desk"            -> quick change: do it, run tests, short summary
```

Only two optional commands exist: `/dev-process:dev-process init` (once per project) and `/dev-process:dev-process status`.

Claude picks the lane, applies the standards itself, asks only when it must, and ends every task with a short summary: lane, what was checked, what changed, how, proof, standards applied and skipped, a Low/Medium/High cost, and the next step.

## Lanes

| Lane | When | What the developer sees |
|---|---|---|
| Full | New feature, large enhancement, new module | Brief, plan (confirm), build, verify, summary |
| Quick change | Small UI or copy change, under about 50 lines | Do it, tests, summary |
| Bug fix | Something behaves wrongly | Failing test, fix, root cause, summary |
| Hotfix | Production issue (S1 to S3) | Stabilise, rollback step, named approver, incident note |
| Data fix | Correct data in a live database | Script with dry run, backup, rollback, reconciled counts, approvals |
| Refactor | Change structure, not behaviour | Tests green before and after |
| Upgrade | Dependency or framework | Scan before and after, tests, rollback is a revert |
| Spike | Find out if something is worth it | Short note and recommendation; nothing merged |
| Release | Cut a version | Release notes, checklist, release owner sign-off |
| Migration | Legacy system | Seven stages, four gates |

Claude never deploys and never touches production.

## What is in it

| Skill | Job |
|---|---|
| `dev-process` | Entry point: picks the lane, runs the flow, summary. Orchestrates the others. |
| `fix-lanes` | Bug fix, hotfix, data fix |
| `change-lanes` | Quick change, refactor, upgrade, spike, release |
| `security-check` | Auth, secrets, logging, audit, error reporting, prompt data |
| `db-check` | API, database, ORM, migrations, cache, jobs, email |
| `ui-check` | Tokens, density, dark/light, responsive, validation, toasts, fallback pages, accessibility |
| `ai-check` | Settings, service layer, usage log, GBP/USD pricing, budgets, mock mode |
| `legacy-migration` | Seven stages, four gates, risks, UI redesign |
| `extend-process` | Add a project skill, hook or agent in a fixed format and register it |

Each skill has a trigger-style `description` (Claude loads the rest only on a match) and an `evals/evals.json` test suite. The plugin also has the `standards-reviewer` agent (read-only, runs only for larger or risky full-flow changes), three hooks and templates for CLAUDE.md, PR, memory, incident, fix, release, spike notes, data-fix runbook, design page, baseline and CI.

## Hooks (enforced, whatever the developer does)

- Before a tool runs: block `.env` reads, force-push, branch deletion (local and remote), wide recursive deletes
- Before a prompt is sent: block prompts that contain a secret
- After an edit: run the project's lint and test commands (`.devprocess/config.json`)

CI (`templates/standards.yml.tpl`): PR size, scans, checklist, and `fix-has-test` (a bug-fix PR must change a test).

## Guided vs enforced

- Enforced: hooks, deny rules, CI
- Guided: the flow and the standards. A developer can still ignore Claude, which is why CI and the PR approver exist.

## Token cost

Skills load only when needed; the reviewer agent runs only for the full flow on larger or risky diffs; state and notes are short; no nested agents. See `tests/TOKEN-COST.md` for measured numbers.

## Tests

```
bash tests/run.sh               files, frontmatter, evals structure, coverage map, hook behaviour (fast, no network)
claude plugin validate .        official manifest check
python3 tests/run-evals.py      runs every eval with the claude CLI and grades the assertions (slow, uses tokens)
```

`run-evals.py` copies a small fixture app (`tests/fixtures/mini-app`) into a temp folder for each eval, runs the prompt with this plugin, then grades each assertion with a second call. Results go to `tests/eval-results/`. LLM grading is noisy; see `tests/EVAL-RESULTS.md`.

## Repo host setup

Mark the `standards` CI jobs as required in branch protection. Require one approving review.

## Known limitations

- The standards are guidance to Claude, not enforced code. Hooks and CI enforce only a small set (secrets, risky git commands, lint and tests, PR size, scans, a test with every fix).
- Standards are intended to apply to the code a task changes. They do not audit or fix existing code.
- Defaults you may want to change: quick-change limit (about 50 lines), 400-line PR limit, hotfix approver.
- Eval scores come from an LLM grader and vary between runs. See `tests/EVAL-RESULTS.md` and `tests/TOKEN-COST.md`.

## Install from this repo

```
/plugin marketplace add wahidsherief/dev-process
/plugin install dev-process@dev-process
```

## Contributing

Issues and pull requests are welcome. Run `bash tests/run.sh` and `claude plugin validate .` before opening a PR. A new skill needs an `evals/evals.json` (see the `extend-process` skill).

## License

MIT. See `LICENSE`.
