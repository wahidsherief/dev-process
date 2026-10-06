#!/usr/bin/env python3
"""Run the token-cost scenarios on the mini-app fixture, with and without the plugin.

  python3 tests/tokmeasure.py                      print the table (3 parallel runs)
  python3 tests/tokmeasure.py --record --version v1.4.1 --runs 2
                                                   also append every run to tests/token-runs.jsonl
Uses `claude -p` (costs tokens). One run per cell is noisy: use --runs for more samples.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile, concurrent.futures as cf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FX = os.path.join(ROOT, "tests", "fixtures", "mini-app")
REC = os.path.join(ROOT, "scripts", "token-record.py")
SUF = "\n\n(Non-interactive test run: nobody can answer questions and the plan is approved. Make reasonable choices, state them in one line, and complete the work.)"
TASKS = {
    "slow-page": ("bug fix", "The /orders page is slow. Find out why and fix it."),
    "tiny-ui": ("quick", "Change the 'New customer' button label to 'Add customer'."),
    "bug": ("bug fix", "Order totals show 10.99 when the real total is 11.00. Fix fmt_total in app.py."),
    "full-feature": ("full", "Add an orders CSV export with a date filter, only for admins, with a button on the page."),
    "small-feature": ("quick", "Add an endpoint /customers/count that returns the number of customers, with a test."),
}

PLUGIN_DIR = ROOT

def run(name, plugin):
    d = tempfile.mkdtemp()
    shutil.copytree(FX, d, dirs_exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=d)
    subprocess.run("git add -A && git -c user.name=t -c user.email=t@t commit -qm b", shell=True, cwd=d, capture_output=True)
    cmd = ["claude", "-p", TASKS[name][1] + SUF, "--output-format", "json", "--dangerously-skip-permissions"] + (["--plugin-dir", PLUGIN_DIR] if plugin else [])
    r = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=900)
    try:
        j = json.loads(r.stdout)
    except Exception:
        return name, plugin, None, (r.stdout[:200] + r.stderr[:200])
    return name, plugin, j, None

def main():
    a = argparse.ArgumentParser()
    a.add_argument("--record", action="store_true")
    a.add_argument("--version", default=None)
    a.add_argument("--runs", type=int, default=1)
    a.add_argument("--only", nargs="*", help="scenario names")
    a.add_argument("--plugin-dir", help="plugin folder to test (default: this repo), e.g. an older version")
    a.add_argument("--out", default=os.path.join(ROOT, "tests", "token-runs.jsonl"))
    n = a.parse_args()
    global PLUGIN_DIR
    if n.plugin_dir: PLUGIN_DIR = os.path.abspath(n.plugin_dir)
    names = n.only or list(TASKS)
    jobs = [(t, p) for t in names for p in (False, True) for _ in range(n.runs)]
    with cf.ThreadPoolExecutor(3) as ex:
        res = list(ex.map(lambda x: run(*x), jobs))
    for t, p, j, e in res:
        if j is None:
            print(t, "PLUGIN" if p else "plain ", "FAILED", e); continue
        u = j.get("usage", {})
        tot = sum((u.get(x) or 0) for x in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
        print(t, "PLUGIN" if p else "plain ", {"turns": j.get("num_turns"), "total": tot, "out": u.get("output_tokens"),
              "cost": round(j.get("total_cost_usd", 0), 3)})
        if n.record:
            cmd = [sys.executable, REC, "--file", n.out, "--arm", "plugin" if p else "baseline", "--task", t,
                   "--lane", TASKS[t][0], "--from-json", "-"]
            if n.version: cmd += ["--version", n.version]
            subprocess.run(cmd, input=json.dumps(j), text=True, capture_output=True)

if __name__ == "__main__":
    main()
