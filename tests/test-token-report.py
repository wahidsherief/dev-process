#!/usr/bin/env python3
"""Tests for scripts/token-record.py and scripts/token-report.py. Test data is synthetic and
lives only in a temp folder; it is never written to a project or to tests/token-runs.jsonl."""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(ROOT, "scripts", "token-record.py")
REP = os.path.join(ROOT, "scripts", "token-report.py")
fails = 0

def check(name, cond, detail=""):
    global fails
    print(("  ok  " if cond else "  FAIL ") + name + ("" if cond else "  " + detail))
    if not cond: fails += 1

def rec(f, arm, task, total, **kw):
    cmd = [sys.executable, REC, "--file", f, "--arm", arm, "--task", task, "--lane", kw.pop("lane", "bug fix"),
           "--input", str(total), "--output", "0", "--turns", str(kw.pop("turns", 4))]
    for k, v in kw.items(): cmd += ["--" + k.replace("_", "-"), str(v)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr

def report(f, *extra):
    r = subprocess.run([sys.executable, REP, "--file", f, *extra], capture_output=True, text=True)
    return r.stdout

d = tempfile.mkdtemp()

# 1. no data at all
out = report(os.path.join(d, "none.jsonl"))
check("no data: verdict INSUFFICIENT DATA", "VERDICT: INSUFFICIENT DATA" in out and "Recorded runs: 0" in out, out)

# 2. insufficient comparable data: 3 comparable tasks, plugin-only extras
f = os.path.join(d, "few.jsonl")
for t in ("a", "b", "c"):
    rec(f, "baseline", t, 10000); rec(f, "plugin", t, 11000)
rec(f, "plugin", "only-plugin", 12000)
out = report(f)
check("insufficient: overhead is N/A", "Overhead: N/A — insufficient comparable data" in out, out)
check("insufficient: verdict names the count", "VERDICT: INSUFFICIENT DATA — only 3 comparable tasks" in out, out)
check("insufficient: no WORTH IT claim", "WORTH IT" not in out.split("VERDICT:")[-1].split("\n")[0].replace("NOT YET WORTH IT", ""), out)

# 3. enough comparable tasks but no rework data -> still INSUFFICIENT (lower tokens alone is not proof)
f = os.path.join(d, "norework.jsonl")
for i in range(6):
    rec(f, "baseline", "t%d" % i, 10000); rec(f, "plugin", "t%d" % i, 11000)
out = report(f)
check("no rework data: median overhead shown (+1.0k, +10%)", "+1.0k (+10.0%)" in out, out)
check("no rework data: verdict INSUFFICIENT DATA", "VERDICT: INSUFFICIENT DATA" in out and "no rework or review-round data" in out, out)

# 4. multiple comparable runs with rework improvement -> WORTH IT
f = os.path.join(d, "worth.jsonl")
for i in range(6):
    rec(f, "baseline", "t%d" % i, 10000, rework=2, review_rounds=2)
    rec(f, "plugin", "t%d" % i, 11500, rework=1, review_rounds=1, reviewer="yes" if i == 0 else "no")
out = report(f)
check("worth: overhead +15%", "+15.0%" in out, out)
check("worth: rework improvement +50%", "Improvement:      +50.0%" in out, out)
check("worth: verdict WORTH IT", "VERDICT: WORTH IT" in out and "fewer" in out, out)
check("worth: reviewer counts", "yes 1, no 5, unknown 0" in out, out)

# 5. enough data, no improvement -> NOT YET WORTH IT
f = os.path.join(d, "notyet.jsonl")
for i in range(6):
    rec(f, "baseline", "t%d" % i, 10000, rework=1, review_rounds=1)
    rec(f, "plugin", "t%d" % i, 13100, rework=1, review_rounds=1)
out = report(f)
check("not yet: verdict NOT YET WORTH IT", "VERDICT: NOT YET WORTH IT" in out and "+31%" in out, out)

# 6. init/analyze runs are listed but excluded from the comparison
f = os.path.join(d, "kinds.jsonl")
for i in range(5):
    rec(f, "baseline", "t%d" % i, 10000); rec(f, "plugin", "t%d" % i, 10500)
rec(f, "plugin", "init-1", 3000, kind="init"); rec(f, "plugin", "an-1", 9000, kind="analyze")
out = report(f)
check("kinds: init/analyze counted separately", "Init / analyze runs: analyze 1, init 1" in out and "Comparable tasks (same task in both arms): 5" in out, out)

# 7. annotate adds rework later; version filter
f = os.path.join(d, "ann.jsonl")
rec(f, "plugin", "x", 5000, version="v1.4.1")
rid = json.loads(open(f).readline())["id"]
r = subprocess.run([sys.executable, REC, "--file", f, "--annotate", rid, "--rework", "2"], capture_output=True, text=True)
check("annotate: rework stored", r.returncode == 0 and json.loads(open(f).readline())["rework"] == 2, r.stdout + r.stderr)
check("version filter: other version gives no runs", "Recorded runs: 0" in report(f, "--version", "v0"), "")

# 8. from-json input (claude -p shape)
f = os.path.join(d, "json.jsonl")
j = {"usage": {"input_tokens": 10, "output_tokens": 300, "cache_creation_input_tokens": 1000, "cache_read_input_tokens": 5000},
     "num_turns": 3, "total_cost_usd": 0.07}
r = subprocess.run([sys.executable, REC, "--file", f, "--arm", "plugin", "--task", "j", "--from-json", "-"], input=json.dumps(j), text=True, capture_output=True)
row = json.loads(open(f).readline())
check("from-json: totals and turns", r.returncode == 0 and row["total"] == 6310 and row["turns"] == 3, r.stdout + r.stderr)

sys.exit(1 if fails else 0)
