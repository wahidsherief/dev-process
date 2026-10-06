---
name: extend-process
description: 'Create a project skill, hook or subagent in the team format (name, trigger description, scope, evals or tests, registry entry). Use when a developer asks to add or change a skill, hook or agent, e.g. "add a skill that reviews our queries".'
---

# extend-process

Adds a project extension the same way every time, so the team can see what exists, nobody duplicates it, and each one has a test.

Extensions live in the repo (project scope), go through a PR with the reason written in it, and are listed in `docs/EXTENSIONS.md`.

## Before creating anything

1. Read `docs/EXTENSIONS.md` and the folders `.claude/skills/`, `.claude/agents/`, `.claude/hooks/`, plus the dev-process plugin's own skills. If something similar exists, extend it instead of adding a new one.
2. Decide the type:
   - **Skill**: a job repeated across tasks, where Claude needs instructions. If it happened once, it is a note in `docs/memory`, not a skill.
   - **Hook**: a rule that must never be broken, or an automatic action on a tool event. Use a hook, not a skill, when "must" matters.
   - **Agent**: work that needs its own context or restricted tools, such as a read-only reviewer or a long exploration. Not for steps the main session can do.
3. Ask only what is missing: the job in one sentence, when it should trigger, and who owns it.

## Naming (all types)

- Unique across the project and the plugin. Lowercase, hyphens, verb-noun or noun-noun: `review-queries`, `db-admin`.
- No stack names in the name or the body unless the extension is deliberately stack-specific. Stack-agnostic extensions survive migrations.
- Folder name = `name` field.

## Skill

Create `.claude/skills/<name>/SKILL.md` from `templates/SKILL.md.tpl`.

- `description` is the trigger. Claude reads only the name and description first and loads the rest on a match. Say what it does and when to use it, with the words a developer would use. Under 400 characters.
- Keep the body short (under 120 lines). Put detail in `references/` and say when to read each file.
- Write 4 to 6 evals in `evals/evals.json` (see below). A skill without evals is not accepted.
- If the plugin `skill-creator` is installed, use it to draft and improve the skill, then apply these rules.

## Hook

Create `.claude/hooks/<name>.sh` from `templates/hook.sh.tpl`, and register it in `.claude/settings.json` under `hooks`.

- State the event (PreToolUse, PostToolUse, UserPromptSubmit), the matcher, and the one thing it blocks or does.
- Exit code 2 blocks the action. The message on stderr must say what was blocked and what to do instead.
- Fail open on bad input (exit 0), never on a match.
- Add test cases to `tests/hooks.sh` (copy the pattern from the plugin's `tests/run.sh`): at least one that must block and one that must allow.
- Never put secrets in a hook. Read the project's commands from `.devprocess/config.json`.

## Agent

Create `.claude/agents/<name>.md` from `templates/agent.md.tpl`.

- `description` says when the main session should hand work to it.
- `tools`: the smallest set. Read-only (Read, Grep, Glob) by default. Add Edit or Write only when it must change files.
- `model`: a smaller model for search and formatting, a larger one for design and hard bugs.
- Put the current state and the target in its instructions, and what it returns.
- No nesting: an agent does not call other agents. Each one opens its own context and uses more tokens.

## Evals

`evals/evals.json` next to the skill:

```json
{
  "skill_name": "<name>",
  "evals": [
    {
      "id": 1,
      "prompt": "A realistic developer request that should trigger the skill",
      "expected_output": "One sentence describing a correct result",
      "assertions": ["A checkable statement about the output", "Another one"]
    }
  ]
}
```

Include: one prompt that should trigger the skill, one that should not (set `"should_trigger": false`), and one edge case. Assertions are checkable ("asks no question it could answer from the repo"), not vague ("is good").

## Register

Append a row to `docs/EXTENSIONS.md`: type, name, one-line description, owner, date, PR link. Create the file from `templates/EXTENSIONS.md.tpl` if it does not exist.

## Finish

1. Run the evals (or ask the developer to run them) and the hook tests.
2. Summarize in three lines: what was added, where, and what test proves it.
3. The change goes in a PR. The reviewer checks the new file against these rules.
