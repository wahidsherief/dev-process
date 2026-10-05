#!/usr/bin/env bash
# PreToolUse guard. Reads the hook JSON from stdin.
# Exit 2 blocks the action and shows the message to Claude.
# Blocks: reading .env files, force-push, deleting branches (local or remote), recursive delete of wide paths.
input="$(cat)"

python3 - "$input" <<'PY'
import json, re, sys

try:
    data = json.loads(sys.argv[1])
except Exception:
    sys.exit(0)

tool = data.get("tool_name", "")
ti = data.get("tool_input", {}) or {}

def block(msg):
    sys.stderr.write("dev-process guard: " + msg + "\n")
    sys.exit(2)

ENV = re.compile(r'(^|[\s/"\'=])\.env(\.[A-Za-z0-9_-]+)?($|[\s"\';|&])')
ENV_OK = re.compile(r'\.env\.(example|sample|template)$')

if tool == "Read":
    p = ti.get("file_path", "")
    base = p.rsplit("/", 1)[-1]
    if re.match(r'^\.env(\..+)?$', base) and not ENV_OK.search(base):
        block("reading %s is blocked. Secrets must not enter the session. Use .env.example." % base)
    sys.exit(0)

if tool == "Bash":
    cmd = ti.get("command", "")
    if re.search(r'\bgit\s+push\b[^;&|]*(\s--force(-with-lease)?\b|\s-f\b)', cmd):
        block("force-push is blocked. Open a PR instead.")
    if re.search(r'\bgit\s+branch\b[^;&|]*\s(-D|-d|--delete)\b', cmd) or re.search(r'\bgit\s+push\b[^;&|]*(\s--delete\b|\s-d\b|\s:[A-Za-z0-9._/-]+)', cmd):
        block("deleting a branch is blocked. Ask the technical lead, or delete it in the repo host after merge.")
    if re.search(r'\brm\s+(-[a-zA-Z]*r[a-zA-Z]*\s+|--recursive\s+)', cmd) and re.search(r'(\s/(\s|$)|\s~(/|\s|$)|\s\$HOME|\s\*(\s|$)|\s\.\s*$|\s\.\./)', cmd):
        block("recursive delete of a wide path is blocked. Name the exact folder.")
    if re.search(r'\b(cat|less|more|head|tail|grep|sed|awk|cp|scp|curl|base64)\b', cmd):
        for m in re.finditer(r'(?:^|[\s"\'=/])(\.env(?:\.[A-Za-z0-9_-]+)?)(?=$|[\s"\';|&])', cmd):
            if not ENV_OK.search(m.group(1)):
                block("reading %s is blocked. Secrets must not enter the session." % m.group(1))
sys.exit(0)
PY
