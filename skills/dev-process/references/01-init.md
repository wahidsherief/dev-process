# init: prepare the project, then start the task

Run once per project. It prepares the project and then immediately continues the developer's current task. There is no separate start step. It never scans the whole project (that is `analyze`) and never asks the developer to choose a lane.

If `init` runs in the middle of a task, or the developer wrote the task after it, keep that task: finish setup, then carry on with it from where it was. If there is no task, say the project is ready and stop.

## Questions (ask together, one message, skip any you can answer from the repo)

Defaults if nobody answers: Safe standard (the developer is not asked), existing system, detected stack and commands, the developer as approver, no error reporting.

1. Project type: new system, existing system, or legacy migration?
2. Stack: language, framework, ORM. (Detect from the repo, then confirm.)
3. Commands: lint, type check, unit tests, end-to-end tests, build. (Detect, then confirm.)
4. Named approver for PRs. Technical lead (default: the developer who ran init).
5. Error reporting: Sentry or another service, or none, where applicable or decided.

## Create

From `templates/`, adapt and write:

| File | Source |
|---|---|
| `CLAUDE.md` | `templates/CLAUDE.md.tpl`. Keep it short. Fill standard (Safe), stack, commands, approver. |
| `docs/PROCESS.md` | `templates/PROCESS.md.tpl`. Set `Standard: Safe` and type. |
| `docs/memory/{feature,fix,refactor,migration,decision,incident}/` | each with a `.gitkeep`; copy `templates/memory-note.md` to `docs/memory/_TEMPLATE.md` |
| `.github/pull_request_template.md` | `templates/pull_request_template.md` |
| `.claude/settings.json` | `templates/settings.json.tpl`: deny rules and permissions |
| `.devprocess/config.json` | commands for the hooks: `{"lint": "...", "test": "..."}` |
| `.github/workflows/standards.yml` | `templates/standards.yml.tpl`, only if the repo uses GitHub. Otherwise tell the developer what the CI must run. |
| `docs/PATTERNS.md` | `templates/PATTERNS.md.tpl` |
| `.gitignore` | add `.devprocess/summary.md` if it is not already ignored |

The standard starts as Safe. Risky tasks get the Risk rules for that task automatically (see `SKILL.md`). Nobody chooses a standard at setup.

Never overwrite an existing file. If one exists, show a diff and ask.

## Then

- Print one line on what was created. Then continue with the current task: pick its lane and run it as usual (see `SKILL.md`).
- Do not run the baseline or read the whole project. If the developer wants the project and its standards analysed, they run `analyze`.
- New system with a large first task: the full flow asks for a design page before the first slice.

## Plugins and tool servers (MCP)

- Keep a small allowlist in project settings. The reason for each goes in the PR.
- Read a plugin's commands and hooks before enabling it: they run code on the developer's machine.
- Prefer a skill in the repo over a plugin when a skill is enough. Pin versions.
- Tool servers get the same review. Start with read-only access.
- Suggested core set: skill-creator, Playwright, library docs, frontend-design.

## Prompt data classes

| Class | Examples | Rule |
|---|---|---|
| Green | Source code, public docs, error messages without personal data | Allowed |
| Amber | Logs, database samples, config files | Allowed after redaction: replace names, emails, ids and keys with fake values |
| Red | Secrets, credentials, personal or customer data, production dumps | Never |

- Use the company-approved AI account, not a personal one.
- Develop against seed or synthetic data.
- If Red data was pasted: rotate any exposed secret and tell the technical lead.

## Token discipline

- Explore once. Save the map in `docs/ARCHITECTURE.md` and reuse it.
- One slice per session. `/compact` keeps decisions. `/clear` between slices.
- Smaller model for search and formatting, larger for design and hard bugs.
- Ask for diffs, not whole files. Cap answer length.
- Use spec plugins only for large features. Brainstorm-and-plan plugins and sub-agent execution can use a very large number of tokens; plan the budget and split the work across sessions.
