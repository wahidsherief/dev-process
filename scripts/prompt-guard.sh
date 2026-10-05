#!/usr/bin/env bash
# UserPromptSubmit hook: block a prompt that contains a secret (Red-class data).
# Exit 2 blocks the prompt and shows the message. Bad input fails open.
input="$(cat)"

python3 - "$input" <<'PY'
import json, re, sys
try:
    data = json.loads(sys.argv[1])
except Exception:
    sys.exit(0)
p = data.get("prompt", "") or ""

PATTERNS = [
    (r'-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----', 'a private key'),
    (r'\bAKIA[0-9A-Z]{16}\b', 'an AWS access key'),
    (r'\bgh[pousr]_[A-Za-z0-9]{30,}\b', 'a GitHub token'),
    (r'\bsk-[A-Za-z0-9_-]{20,}\b', 'an API key'),
    (r'\bxox[baprs]-[A-Za-z0-9-]{10,}\b', 'a Slack token'),
    (r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b', 'a JWT'),
    (r'(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp)://[^\s:/@]+:[^\s@]+@', 'a connection string with a password'),
    # Quoted literal assigned to a credential-like name, unless it is obviously a placeholder
    (r'(?i)\b(?:password|passwd|secret|api[_-]?key|auth[_-]?token|access[_-]?token|token)\w*\s*[:=]\s*(["\'])(?!(?:your|example|change|placeholder|dummy|test|fake|xxx|\*\*\*|<|\$\{|%\())[^"\'\s]{8,}\1', 'a credential assignment'),
    # Unquoted value that looks like a literal secret (letters and digits, no code punctuation)
    (r'(?i)\b(?:password|passwd|secret|api[_-]?key|auth[_-]?token|access[_-]?token|token)\w*\s*[:=]\s*(?=[^\s"\'.(\[${}]*\d)(?=[^\s"\'.(\[${}]*[A-Za-z])[^\s"\'.(\[${}]{8,}(?=\s|$)', 'a credential assignment'),
]
for rx, what in PATTERNS:
    if re.search(rx, p):
        sys.stderr.write("dev-process prompt guard: your prompt looks like it contains %s (Red-class data). "
                         "Remove it or replace it with a fake value, then send again. If it was real, rotate it and tell the technical lead.\n" % what)
        sys.exit(2)
sys.exit(0)
PY
