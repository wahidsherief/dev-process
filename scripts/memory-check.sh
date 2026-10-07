#!/usr/bin/env bash
# Stop hook: when a task changed project files but left no memory note, ask Claude once to write it.
# Exit 2 sends the message back to Claude. Fails open (non-git project, no docs/memory, any error).
# Plain bash and git only, so it also runs where python3 is missing.
input="$(cat)"

# Already asked once in this stop cycle: never loop.
case "$input" in *'"stop_hook_active":true'*|*'"stop_hook_active": true'*) exit 0 ;; esac

cwd="$(printf '%s' "$input" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | sed 's#\\\\#/#g')"
[ -n "$cwd" ] || cwd="$PWD"

# Only projects set up by /dev-process:init have docs/memory.
[ -d "$cwd/docs/memory" ] || exit 0
status="$(git -C "$cwd" status --porcelain -uall 2>/dev/null)" || exit 0
[ -n "$status" ] || exit 0

paths="$(printf '%s\n' "$status" | cut -c4- | tr -d '"')"
notes="$(printf '%s\n' "$paths" | grep '^docs/memory/' | grep -v -e '\.gitkeep$' -e '_TEMPLATE\.md$')"
code="$(printf '%s\n' "$paths" | grep -v -e '^docs/' -e '^\.devprocess/' -e '\.bak')"

if [ -n "$code" ] && [ -z "$notes" ]; then
  echo "dev-process: files changed but no memory note was written. Add docs/memory/<task type>/YYYY-MM-DD-name.md (feature, fix, refactor, migration, decision or incident; use the matching template) and link it on the summary's 'Note saved to' line. If this was a trivial quick change with nothing worth keeping, write 'Note saved to: none (trivial change)' in the summary instead." >&2
  exit 2
fi
exit 0
