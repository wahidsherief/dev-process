#!/usr/bin/env python3
"""Token efficiency report from .devprocess/token-runs.jsonl (see token-record.py).

Separates token OVERHEAD (extra tokens from using dev-process) from token EFFICIENCY
(is that cost justified by less rework or fewer review rounds). Invents nothing:
missing data is shown as N/A and the verdict says INSUFFICIENT DATA.
"""
import argparse, json, os, statistics as st, sys

MIN_TASKS = 5          # comparable tasks needed before a median comparison or a verdict
WORTH_IMPROVEMENT = 20.0   # percent fewer rework or review rounds needed for WORTH IT
MAX_WORSE = -10.0          # the other measure may not be worse than this percent
NA = "N/A — insufficient comparable data"

def default_file():
    base = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    return os.path.join(base, ".devprocess", "token-runs.jsonl")

def load(path):
    rows = []
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    pass
    return rows

def k(n):
    if n is None: return "n/a"
    n = float(n)
    if abs(n) >= 1000: return "%.1fk" % (n / 1000)
    return "%d" % round(n)

def sk(n):
    return ("+" if n >= 0 else "-") + k(abs(n))

def med(xs): return st.median(xs) if xs else None
def avg(xs): return sum(xs) / len(xs) if xs else None

def stats_line(rows, key):
    xs = [r[key] for r in rows if r.get(key) is not None]
    if not xs: return "n/a"
    if len(xs) >= MIN_TASKS:
        return "median %s, average %s" % (k(med(xs)), k(avg(xs)))
    return "average %s (%d runs: too few for a median)" % (k(avg(xs)), len(xs))

def pct(a, b):  # a relative to b
    return None if not b else (a - b) / b * 100.0

def improvement(plugin, base):
    """Percent reduction versus baseline (positive = better)."""
    if base is None or plugin is None: return None
    if base == 0: return 0.0 if plugin == 0 else -100.0
    return (base - plugin) / base * 100.0

def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument("--file")
    a.add_argument("--version", help="only runs recorded for this plugin version label")
    n = a.parse_args()
    path = n.file or default_file()
    rows = load(path)
    if n.version:
        rows = [r for r in rows if r.get("version") == n.version]
    out = ["TOKEN EFFICIENCY REPORT", "─" * 24, ""]
    if not rows:
        out += ["Recorded runs: 0", "No runs recorded in %s." % path,
                "Record runs with scripts/token-record.py (plugin and without-plugin runs of the same task).", "",
                "VERDICT: INSUFFICIENT DATA — no runs recorded."]
        print("\n".join(out)); return

    tasks = [r for r in rows if r.get("kind", "task") == "task"]
    P = [r for r in tasks if r.get("arm") == "plugin"]
    B = [r for r in tasks if r.get("arm") == "baseline"]
    others = [r for r in rows if r.get("kind", "task") != "task"]
    out.append("Recorded runs: %d  (with plugin %d, without plugin %d%s)" % (
        len(rows), len(P), len(B),
        "; init/analyze %d" % len(others) if others else ""))
    if others:
        ia = {}
        for r in others: ia[r["kind"]] = ia.get(r["kind"], 0) + 1
        out.append("Init / analyze runs: " + ", ".join("%s %d" % (x, y) for x, y in sorted(ia.items())) + " (not used in the comparison)")
    rv = {"yes": 0, "no": 0, "unknown": 0}
    for r in P: rv[r.get("reviewer") or "unknown"] = rv.get(r.get("reviewer") or "unknown", 0) + 1
    out.append("Reviewer (plugin runs): yes %d, no %d, unknown %d" % (rv["yes"], rv["no"], rv["unknown"]))
    vers = sorted({r.get("version") for r in rows if r.get("version")})
    if vers: out.append("Versions: " + ", ".join(vers))
    out.append("")

    out.append("RECORDED USAGE (all runs, tokens per run)")
    for label, rs in (("With plugin", P), ("Without plugin", B)):
        if not rs:
            out.append("  %-15s no runs" % (label + ":")); continue
        out.append("  %-15s %d runs" % (label + ":", len(rs)))
        out.append("    total %s | input %s | output %s | turns %s" % (
            stats_line(rs, "total"), stats_line(rs, "input"), stats_line(rs, "output"), stats_line(rs, "turns")))
    out.append("  (input = uncached input; total also counts cache writes and cache reads)")
    out.append("")

    # comparable = same task id recorded in both arms
    by = {}
    for r in P: by.setdefault(r.get("task"), {"p": [], "b": []})["p"].append(r)
    for r in B: by.setdefault(r.get("task"), {"p": [], "b": []})["b"].append(r)
    comp = {t: v for t, v in by.items() if t and v["p"] and v["b"]}
    nc = len(comp)

    out.append("TOKEN OVERHEAD  (extra tokens from using dev-process)")
    out.append("  Comparable tasks (same task in both arms): %d" % nc)
    oh_pct = oh_abs = None
    if nc < MIN_TASKS:
        out.append("  Overhead: " + NA + " (need %d tasks, have %d)" % (MIN_TASKS, nc))
        if nc:
            out.append("  Per task (single results, not a median):")
            for t, v in sorted(comp.items()):
                pm, bm = med([x["total"] for x in v["p"]]), med([x["total"] for x in v["b"]])
                out.append("    %-22s plugin %s vs without %s (%s%%)" % (t[:22], k(pm), k(bm), "%+.0f" % pct(pm, bm) if bm else "n/a"))
    else:
        pm_all, bm_all, pcts, diffs = [], [], [], []
        for t, v in comp.items():
            pm, bm = med([x["total"] for x in v["p"]]), med([x["total"] for x in v["b"]])
            pm_all.append(pm); bm_all.append(bm); diffs.append(pm - bm)
            if bm: pcts.append(pct(pm, bm))
        oh_abs, oh_pct = med(diffs), med(pcts)
        out.append("  Plugin median:        %s" % k(med(pm_all)))
        out.append("  Without-plugin:       %s" % k(med(bm_all)))
        out.append("  Token overhead:       %s (%+.1f%%)   [median of per-task overhead]" % (sk(oh_abs), oh_pct))
        out.append("  Average overhead:     %s (%+.1f%%)" % (sk(avg(diffs)), avg(pcts)))
        lanes = {}
        for t, v in comp.items():
            ln = (v["p"][0].get("lane") or "unknown")
            bm = med([x["total"] for x in v["b"]])
            if bm: lanes.setdefault(ln, []).append(pct(med([x["total"] for x in v["p"]]), bm))
        if lanes:
            out.append("  By lane (median overhead): " + "; ".join("%s %+.0f%% (%d)" % (ln, med(x), len(x)) for ln, x in sorted(lanes.items())))
    out.append("")

    out.append("TOKEN EFFICIENCY  (is the extra cost justified by less waste?)")
    imps = {}
    for key, label in (("rework", "Rework"), ("review_rounds", "Review rounds")):
        pr, br = [], []
        for t, v in comp.items():
            px = [x[key] for x in v["p"] if x.get(key) is not None]
            bx = [x[key] for x in v["b"] if x.get(key) is not None]
            if px and bx:
                pr.append(avg(px)); br.append(avg(bx))
        if len(pr) < MIN_TASKS:
            out.append("  %s: %s (%d tasks with data, need %d)" % (label, NA, len(pr), MIN_TASKS))
            continue
        imp = improvement(avg(pr), avg(br))
        imps[key] = (imp, len(pr))
        out.append("  %s:" % label)
        out.append("    Plugin:           %.1f/task" % avg(pr))
        out.append("    Without-plugin:   %.1f/task" % avg(br))
        out.append("    Improvement:      %+.1f%%" % (imp if imp is not None else 0.0))
    out.append("  Not recorded by this report: repeated investigation and failed attempts (add them to rework if you count them).")
    out.append("")

    out.append("VERDICT")
    out.append("─" * 7)
    if nc < MIN_TASKS:
        v = "VERDICT: INSUFFICIENT DATA — only %d comparable task%s recorded (need %d)." % (nc, "" if nc == 1 else "s", MIN_TASKS)
    elif not imps:
        v = ("VERDICT: INSUFFICIENT DATA — %d comparable tasks, overhead %+.0f%%, but no rework or review-round data to judge efficiency." % (nc, oh_pct))
    else:
        vals = [x[0] for x in imps.values() if x[0] is not None]
        best, worst = max(vals), min(vals)
        names = {"rework": "rework rounds", "review_rounds": "review rounds"}
        if best >= WORTH_IMPROVEMENT and worst >= MAX_WORSE:
            key = max(imps, key=lambda z: imps[z][0] if imps[z][0] is not None else -1e9)
            v = "VERDICT: WORTH IT — %+.0f%% token overhead, but %.0f%% fewer %s across %d comparable tasks." % (oh_pct, best, names[key], imps[key][1])
        else:
            parts = ", ".join("%s %+.0f%%" % (names[x], imps[x][0]) for x in imps)
            v = "VERDICT: NOT YET WORTH IT — %+.0f%% token overhead with no measurable reduction (%s) across %d comparable tasks." % (oh_pct, parts, nc)
    out.append(v)
    out.append("")
    out.append("Rules: needs %d comparable tasks; WORTH IT needs at least %d%% fewer rework or review rounds and neither worse than %d%%. Lower tokens alone never counts as efficiency." % (MIN_TASKS, WORTH_IMPROVEMENT, -MAX_WORSE))
    print("\n".join(out))

if __name__ == "__main__":
    main()
