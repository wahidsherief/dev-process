#!/usr/bin/env bash
# PostToolUse hook: run the project's lint and test commands after an edit.
# Commands come from .devprocess/config.json: {"lint": "...", "test": "..."}.
# Missing file or empty command = skipped. A failure exits 2 so Claude sees the output and fixes it.
root="${CLAUDE_PROJECT_DIR:-$PWD}"
cfg="$root/.devprocess/config.json"
[ -f "$cfg" ] || exit 0

get() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get(sys.argv[2],"") or "")' "$cfg" "$1" 2>/dev/null; }

cd "$root" || exit 0
for key in lint test; do
  cmd="$(get "$key")"
  [ -n "$cmd" ] || continue
  out="$(bash -c "$cmd" 2>&1)"; rc=$?
  if [ $rc -ne 0 ]; then
    echo "dev-process: '$key' failed after your edit. Fix before continuing." >&2
    echo "$out" | tail -n 40 >&2
    exit 2
  fi
done
exit 0
