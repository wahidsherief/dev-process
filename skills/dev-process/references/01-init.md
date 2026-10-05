# init: one-time project setup

Run once per project. Ask as few questions as possible. Answer from the repo where you can.

## Questions (ask together, one message)

1. Tier: Light (internal tools, prototypes, small fixes) or Full (customer-facing, user data, AI features)?
2. Project type: new system, existing system, or legacy migration?
3. Stack: language, framework, ORM. (Detect from the repo, then confirm.)
4. Commands: lint, type check, unit tests, end-to-end tests, build. (Detect, then confirm.)
5. Named approver for PRs. Technical lead (default: the developer who ran init).
6. Error reporting: Sentry or another service, or none, where applicable or decided.

## Create

From `templates/`, adapt and write:

| File | Source |
|---|---|
| `CLAUDE.md` | `templates/CLAUDE.md.tpl`. Keep it short. Fill tier, stack, commands, approver. |
| `docs/PROCESS.md` | `templates/PROCESS.md.tpl`. Set tier and type. |
| `docs/memory/{feature,fix,refactor,migration,decision,incident}/` | each with a `.gitkeep`; copy `templates/memory-note.md` to `docs/memory/_TEMPLATE.md` |
| `.github/pull_request_template.md` | `templates/pull_request_template.md` |
| `.claude/settings.json` | `templates/settings.json.tpl`: deny rules and permissions |
| `.devprocess/config.json` | commands for the hooks: `{"lint": "...", "test": "..."}` |
| `.github/workflows/standards.yml` | `templates/standards.yml.tpl`, only if the repo uses GitHub. Otherwise tell the developer what the CI must run. |
| `docs/BASELINE.md` | `templates/BASELINE.md` |

Never overwrite an existing file. If one exists, show a diff and ask.

## Then

- Existing or legacy project: run the baseline now (see the `legacy-migration` skill, stage 1). Do not change code.
- New system: offer `design` before any slice.
- Print a three-line summary of what was created and the next command.

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
