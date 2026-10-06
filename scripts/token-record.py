#!/usr/bin/env python3
"""Record one run (or annotate one) in .devprocess/token-runs.jsonl.

Record from `claude -p ... --output-format json` output, or from numbers:
  claude -p "task" --output-format json | token-record.py --arm plugin --task csv-export --lane full --from-json -
  token-record.py --arm baseline --task csv-export --lane full --input 9000 --output 1200 --turns 4
Add what you learn later (rework rounds, review rounds) to an existing run:
  token-record.py --annotate <id> --rework 1 --review-rounds 2
Nothing is invented: a field you do not give is stored as unknown (null).
"""
import argparse, hashlib, json, os, sys, time

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

def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--file")
    a.add_argument("--arm", choices=["plugin", "baseline"])
    a.add_argument("--task", help="short id; the same task in both arms must use the same id")
    a.add_argument("--lane")
    a.add_argument("--kind", choices=["task", "init", "analyze"], default="task")
    a.add_argument("--version", help="plugin version label, for example v1.4.1")
    a.add_argument("--reviewer", choices=["yes", "no", "unknown"], default="unknown")
    a.add_argument("--from-json", help="claude --output-format json output; - for stdin")
    a.add_argument("--input", type=int)
    a.add_argument("--output", type=int)
    a.add_argument("--cache-write", type=int)
    a.add_argument("--cache-read", type=int)
    a.add_argument("--turns", type=int)
    a.add_argument("--cost", type=float, help="USD")
    a.add_argument("--rework", type=int, help="rework rounds after the first attempt")
    a.add_argument("--review-rounds", type=int)
    a.add_argument("--note")
    a.add_argument("--annotate", metavar="ID", help="update rework / review rounds / reviewer / note of an existing run")
    a.add_argument("--ts", help="ISO timestamp (default: now)")
    n = a.parse_args()
    path = n.file or default_file()

    if n.annotate:
        rows = load(path)
        hit = [r for r in rows if r.get("id") == n.annotate]
        if not hit:
            sys.exit("no run with id %s in %s" % (n.annotate, path))
        r = hit[0]
        if n.rework is not None: r["rework"] = n.rework
        if n.review_rounds is not None: r["review_rounds"] = n.review_rounds
        if n.reviewer != "unknown": r["reviewer"] = n.reviewer
        if n.note: r["note"] = n.note
        with open(path, "w", encoding="utf-8") as f:
            for x in rows:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
        print("updated", n.annotate)
        return

    if not (n.arm and n.task):
        sys.exit("--arm and --task are required")
    inp = out = cw = cr = turns = cost = None
    if n.from_json:
        raw = sys.stdin.read() if n.from_json == "-" else open(n.from_json, encoding="utf-8").read()
        try:
            j = json.loads(raw)
        except ValueError:
            sys.exit("could not read JSON from --from-json")
        u = j.get("usage") or {}
        inp, out = u.get("input_tokens"), u.get("output_tokens")
        cw, cr = u.get("cache_creation_input_tokens"), u.get("cache_read_input_tokens")
        turns, cost = j.get("num_turns"), j.get("total_cost_usd")
    for name, val in (("inp", n.input), ("out", n.output), ("cw", n.cache_write), ("cr", n.cache_read), ("turns", n.turns), ("cost", n.cost)):
        if val is not None:
            if name == "inp": inp = val
            elif name == "out": out = val
            elif name == "cw": cw = val
            elif name == "cr": cr = val
            elif name == "turns": turns = val
            else: cost = val
    if inp is None and out is None:
        sys.exit("no token numbers given (use --from-json or --input/--output)")
    parts = [x or 0 for x in (inp, out, cw, cr)]
    ts = n.ts or time.strftime("%Y-%m-%dT%H:%M:%S%z")
    rid = hashlib.sha1((ts + n.arm + n.task + str(parts) + str(time.time())).encode()).hexdigest()[:8]
    row = {"id": rid, "ts": ts, "version": n.version, "arm": n.arm, "task": n.task, "lane": n.lane, "kind": n.kind,
           "input": inp, "output": out, "cache_write": cw, "cache_read": cr, "total": sum(parts),
           "turns": turns, "cost_usd": cost, "reviewer": n.reviewer,
           "rework": n.rework, "review_rounds": n.review_rounds, "note": n.note}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("recorded %s (%s, %s, total %d)" % (rid, n.arm, n.task, row["total"]))

if __name__ == "__main__":
    main()
