#!/usr/bin/env python3
"""Tests for scripts/task-tokens.py: sums since the last real prompt, de-duplicates streamed chunks, fails silent."""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "task-tokens.py")


def run(rows):
    d = tempfile.mkdtemp()
    p = os.path.join(d, "t.jsonl")
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    out = subprocess.run([sys.executable, SCRIPT, "--file", p], capture_output=True, text=True)
    return out.returncode, out.stdout.strip()


def prompt(text):
    return {"type": "user", "message": {"role": "user", "content": text}}


def tool_result():
    return {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": "x"}]}}


def asst(mid, i, o, cw=0, cr=0):
    return {"type": "assistant", "message": {"id": mid, "usage": {
        "input_tokens": i, "output_tokens": o,
        "cache_creation_input_tokens": cw, "cache_read_input_tokens": cr}}}


fails = []


def check(name, got, want):
    if got != want:
        fails.append("%s: got %r want %r" % (name, got, want))


# only the last prompt counts; tool results do not start a new task; streamed chunks of one message count once
rc, out = run([
    prompt("old task"), asst("m0", 100000, 5000, 0, 900000),
    prompt("new task"),
    asst("m1", 1000, 100, 2000, 100000),
    asst("m1", 1000, 500, 2000, 100000),  # same message id, final counts win
    tool_result(),
    asst("m2", 4000, 1500, 0, 300000),
])
check("sum", (rc, out), (0, "9k used (400k cached)"))

# no usage at all: silent
rc, out = run([prompt("hello")])
check("no usage", (rc, out), (0, ""))

# missing file: silent, exit 0
out = subprocess.run([sys.executable, SCRIPT, "--file", os.path.join(tempfile.gettempdir(), "nope-%d.jsonl" % os.getpid())],
                     capture_output=True, text=True)
check("missing file", (out.returncode, out.stdout.strip()), (0, ""))

# garbage lines are skipped
d = tempfile.mkdtemp()
p = os.path.join(d, "g.jsonl")
open(p, "w").write("not json\n" + json.dumps(prompt("x")) + "\n" + json.dumps(asst("a", 1500, 500, 0, 2500000)) + "\n")
out = subprocess.run([sys.executable, SCRIPT, "--file", p], capture_output=True, text=True)
check("garbage", (out.returncode, out.stdout.strip()), (0, "2k used (2.5M cached)"))

if fails:
    print("\n".join(fails))
    sys.exit(1)
print("ok")
