#!/usr/bin/env python3
"""Print the tokens used by the current task, for the summary's meta line.

Reads the newest session transcript of this project (~/.claude/projects/<slug>/*.jsonl)
and sums the assistant usage since the last real user prompt:
  used   = input + cache-creation + output tokens (fresh work)
  cached = cache-read tokens (context re-read, cheap)
Prints e.g. "17k used (395k cached)". Prints nothing and exits 0 on any problem, so the
summary falls back to the level only. Nothing is ever invented.
Usage: task-tokens.py [--file transcript.jsonl]
"""
import glob, json, os, re, sys


def short(n):
    if n >= 1_000_000:
        return ("%.1fM" % (n / 1_000_000)).replace(".0M", "M")
    if n >= 1000:
        v = n / 1000
        return ("%.0fk" % v) if v >= 10 else ("%.1fk" % v).replace(".0k", "k")
    return str(n)


def transcript():
    if "--file" in sys.argv:
        return sys.argv[sys.argv.index("--file") + 1]
    base = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    slug = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(base))
    files = glob.glob(os.path.join(os.path.expanduser("~"), ".claude", "projects", slug, "*.jsonl"))
    return max(files, key=os.path.getmtime) if files else None


def is_prompt(row):
    """A real user prompt: a user row that is not just tool results or meta."""
    if row.get("type") != "user" or row.get("isMeta") or row.get("isSidechain"):
        return False
    c = (row.get("message") or {}).get("content")
    if isinstance(c, str):
        return bool(c.strip())
    if isinstance(c, list):
        return any(isinstance(b, dict) and b.get("type") == "text" for b in c)
    return False


def main():
    path = transcript()
    if not path or not os.path.exists(path):
        return
    msgs = {}  # message id -> usage (the last chunk of a message has the final counts)
    order = []
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if is_prompt(row):
            msgs, order = {}, []
        elif row.get("type") == "assistant" and not row.get("isSidechain"):
            m = row.get("message") or {}
            u = m.get("usage")
            if u:
                key = m.get("id") or row.get("uuid")
                if key not in msgs:
                    order.append(key)
                msgs[key] = u
    if not msgs:
        return
    g = lambda u, k: int(u.get(k) or 0)
    used = sum(g(u, "input_tokens") + g(u, "cache_creation_input_tokens") + g(u, "output_tokens") for u in msgs.values())
    cached = sum(g(u, "cache_read_input_tokens") for u in msgs.values())
    print("%s used (%s cached)" % (short(used), short(cached)))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
