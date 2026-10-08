#!/usr/bin/env bash
# SessionStart hook: tell the developer when a newer dev-process is published, with the exact commands.
# It never updates anything. Checks at most once per 12 hours, 3 second timeout, and fails open
# (offline, no curl, odd version text, any error): then it prints nothing and exits 0.
# Plain bash, curl and sort only, so it also runs where python3 is missing.
# Test overrides: DEVPROCESS_LATEST_FILE (a local plugin.json instead of GitHub).
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)}"
ver() { sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([0-9][0-9.]*\)".*/\1/p' | head -1; }

local_v="$( { ver < "$root/.claude-plugin/plugin.json"; } 2>/dev/null )"
[ -n "$local_v" ] || exit 0

stamp="${TMPDIR:-/tmp}/dev-process-update-check"
if [ -z "$DEVPROCESS_LATEST_FILE" ] && [ -f "$stamp" ] && [ -z "$(find "$stamp" -mmin +720 2>/dev/null)" ]; then
  exit 0
fi

if [ -n "$DEVPROCESS_LATEST_FILE" ]; then
  latest="$( { ver < "$DEVPROCESS_LATEST_FILE"; } 2>/dev/null )"
else
  command -v curl >/dev/null 2>&1 || exit 0
  latest="$(curl -fsS --max-time 3 https://raw.githubusercontent.com/wahidsherief/dev-process/main/.claude-plugin/plugin.json 2>/dev/null | ver)"
  : > "$stamp" 2>/dev/null
fi
[ -n "$latest" ] && [ "$latest" != "$local_v" ] || exit 0

# Notify only when latest is strictly newer.
newest="$(printf '%s\n%s\n' "$local_v" "$latest" | sort -V | tail -1)"
[ "$newest" = "$latest" ] || exit 0

msg="dev-process $latest is available (you have $local_v). To get the new summary format and fixes, run: /plugin marketplace update dev-process, then /plugin update dev-process@dev-process, then /reload-plugins."
printf '{"systemMessage":"%s"}\n' "$msg"
exit 0
