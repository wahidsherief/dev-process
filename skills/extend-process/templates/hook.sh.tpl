#!/usr/bin/env bash
# Hook: <unique-name>
# Event: <PreToolUse | PostToolUse | UserPromptSubmit>   Matcher: <tool names>
# Purpose: <the one thing it blocks or does>
# Exit 2 blocks the action and shows the stderr message to Claude. Any other exit lets it through.
input="$(cat)"

python3 - "$input" <<'PY'
import json, sys
try:
    data = json.loads(sys.argv[1])
except Exception:
    sys.exit(0)   # bad input: fail open

# ti = data.get("tool_input", {})   # PreToolUse / PostToolUse
# prompt = data.get("prompt", "")   # UserPromptSubmit

def block(msg):
    sys.stderr.write("<unique-name>: " + msg + "\n")
    sys.exit(2)

# if <condition>:
#     block("<what was blocked>. <what to do instead>.")
sys.exit(0)
PY
