# Coverage map

Every section of the Standard Procedure (V1) and where the plugin handles it. "Guides" = the skill instructs Claude. "Enforced" = a hook or CI blocks it regardless.

| # | Procedure section | Plugin file | How |
|---|---|---|---|
| 1 | Purpose, principles, standards (Safe, Risk) | `SKILL.md` (Standard section, Hard rules); `templates/CLAUDE.md.tpl`; `references/01-init.md` (defaults to Safe, no question) | Guides. [S] tags in every standards file; task risk escalates per task |
| 2 | Definitions and roles | `templates/PROCESS.md.tpl` (approver, technical lead, release owner); skill `legacy-migration` (gates) | Guides |
| 3 | AI environment: CLAUDE.md, skills, reviewer agent, hooks, permissions | `references/01-init.md`; `agents/standards-reviewer.md`; `hooks/hooks.json`; `scripts/*.sh`; `templates/settings.json.tpl` | Guides + enforced |
| 3 | Plugins allowlist and review | `references/01-init.md` | Guides |
| 3 | Prompt-data classes (Green / Amber / Red) | `references/01-init.md`; `security-check`; `templates/CLAUDE.md.tpl`; `scripts/guard.sh` (blocks .env reads); `scripts/prompt-guard.sh` (blocks secrets in prompts) | Guides + enforced |
| 3 | Token discipline | `references/01-init.md` | Guides |
| 4 | Design step | `references/02-start-and-plan.md`; `templates/design-page.md` | Guides; technical lead approves |
| 4 | Work loop (kick off, plan, build, review, done check, record) | `SKILL.md` modes; `references/02`, `03`, `04` | Guides; state in `docs/PROCESS.md` |
| 4 | Six rules | `SKILL.md` (Hard rules); `templates/CLAUDE.md.tpl`; reviewer agent | Guides + reviewed |
| 4 | Memory notes | `references/04-done-and-memory.md`; `templates/memory-note.md`; init creates folders | Guides; CI checks the PR box |
| 5 | Git and PR | `standards-core.md`; `templates/pull_request_template.md`; `templates/standards.yml.tpl` (400-line limit) | Enforced in CI |
| 5 | Security | `security-check`; CI secret and dependency scans; `guard.sh`; `prompt-guard.sh`; deny rules | Guides + enforced |
| 5 | Logging and error reporting | `security-check`; reviewer agent | Guides + reviewed |
| 5 | Settings page | `standards-core.md`; `autonomy.md` | Guides + reviewed |
| 5 | Test environment | `standards-core.md` | Guides |
| 6 | Frontend standards (all 17 points) | skill `ui-check` | Guides + reviewed |
| 7 | Backend standards (all points) | skill `db-check` | Guides + reviewed |
| 8 | AI-integrated systems | skill `ai-check` | Guides + reviewed |
| 9 | Legacy migration: approaches, 7 stages, 4 gates, risks, UI redesign | skill `legacy-migration`; `templates/PROCESS.md.tpl` (migration table) | Guides; human gates |
| 10 | Done check (12 items) | `references/04-done-and-memory.md`; `templates/pull_request_template.md` | Guides + CI checks the PR box |
| 11 | Metrics and review | `templates/BASELINE.md`; skill `legacy-migration` stage 7 | Guides |
| 12 | Decisions and open items | `README.md` (open items) | n/a |
| new | Structured skills, hooks and agents added by developers | skill `extend-process` and its templates; `docs/EXTENSIONS.md` registry | Guides; evals required for a skill, tests for a hook |
| new | Skill evals | `skills/*/evals/evals.json`; `tests/run-evals.py` | Test suite for each skill |
| new | Lanes for non-feature work: bug fix, hotfix (S1 to S3), data fix | skill `fix-lanes`; `skills/fix-lanes/templates/`; CI job `fix-has-test` in `templates/standards.yml.tpl` | Guides; Claude never deploys or touches production |
| new | Lanes for quick change, refactor, upgrade, spike, release | skill `change-lanes`; `skills/change-lanes/templates/` | Guides; release owner signs off |
| new | Simple developer interface: type the task, lane picked automatically, short summary after every task | `SKILL.md` (lane table, handoff); `references/04-done-and-memory.md` (short checks by lane) | Guides |
| new | Commands: init (then start the task), analyze, summary, status, resume | `commands/*.md`; `references/01-init.md`; `references/analyze.md`; `references/summary-resume.md` | Guides; analyze only on request |
| new | Reusable approved patterns (Candidate, Approved, Active, Deprecated) | `references/patterns.md`; `templates/PATTERNS.md.tpl`; `docs/PATTERNS.md` | Guides; a human approves |
| new | Token cost controls | `SKILL.md` (Keep it cheap); `references/03-build-and-review.md` (conditional reviewer) | Guides |
| new | Requirement intake and acceptance criteria | `references/02-start-and-plan.md` | Guides. Not yet in the V1 document |
| new | Autonomy: apply silently, ask only when needed, always stop for a human | `references/autonomy.md` | Guides. Not yet in the V1 document |

## Not covered by the plugin (needs the project)

- Required status checks in branch protection (set once in the repo host)
- Sentry or other error-reporting project and keys
- Mailpit service in dev environments
- Playwright or accessibility tooling in the project's toolchain
- Removing a human approval: nothing in the plugin does this, by design
