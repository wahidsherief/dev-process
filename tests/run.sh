#!/usr/bin/env bash
# Checks the plugin files and the hook scripts. Exit 1 on any failure.
cd "$(dirname "$0")/.." || exit 1
fail=0
ok()  { echo "  ok   $1"; }
bad() { echo "  FAIL $1"; fail=1; }

echo "JSON"
for f in .claude-plugin/plugin.json hooks/hooks.json skills/dev-process/templates/settings.json.tpl skills/*/evals/evals.json; do
  python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$f" 2>/dev/null && ok "$f" || bad "$f"
done

echo "Skills and agents: frontmatter, unique names, trigger descriptions"
names=""
for f in skills/*/SKILL.md agents/*.md; do
  python3 - "$f" <<'PY' && ok "$f" || bad "$f"
import re, sys
t = open(sys.argv[1]).read()
m = re.match(r"---\n(.*?)\n---\n", t, re.S)
assert m, "no frontmatter"
fm = m.group(1)
name = re.search(r"^name: (\S+)$", fm, re.M); desc = re.search(r"^description: '(.*)'$", fm, re.M)
assert name and desc, "name or quoted description missing"
d = desc.group(1).replace("''", "'")
assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name.group(1)), "name must be lowercase-hyphen"
assert 60 <= len(d) <= 500, "description length %d" % len(d)
assert re.search(r"\b(Use when|Use for|Use during|Use before)\b", d), "description must say when to use it"
if sys.argv[1].startswith("skills/"):
    assert sys.argv[1].split("/")[1] == name.group(1), "folder name must equal name"
PY
  names="$names $(grep -m1 '^name: ' "$f" | cut -d' ' -f2)"
done
dups=$(echo $names | tr ' ' '\n' | sort | uniq -d); [ -z "$dups" ] && ok "names are unique" || bad "duplicate names: $dups"

echo "Evals"
for d in skills/*/; do
  s=$(basename "$d")
  python3 - "$d/evals/evals.json" "$s" <<'PY' && ok "$s evals" || bad "$s evals"
import json, sys
d = json.load(open(sys.argv[1]))
assert d["skill_name"] == sys.argv[2]
ev = d["evals"]
assert 3 <= len(ev) <= 10, "need 3 to 10 evals, have %d" % len(ev)
assert any(e.get("should_trigger") is False for e in ev), "need a non-trigger eval"
assert any(e.get("should_trigger", True) for e in ev), "need a trigger eval"
ids = [e["id"] for e in ev]; assert len(set(ids)) == len(ids), "duplicate ids"
for e in ev:
    assert e["prompt"] and e["expected_output"] and len(e["assertions"]) >= 1
PY
done

echo "Files referenced exist"
for ref in $(grep -oh 'references/[A-Za-z0-9._-]*\.md' skills/dev-process/SKILL.md skills/dev-process/references/*.md | sort -u); do
  [ -f "skills/dev-process/$ref" ] && ok "$ref" || bad "missing $ref"
done
for t in $(grep -oh 'templates/[A-Za-z0-9_-]*\.[A-Za-z0-9.]*[A-Za-z0-9]' skills/dev-process/references/*.md skills/dev-process/SKILL.md | sort -u); do
  [ -f "skills/dev-process/$t" ] && ok "dev-process/$t" || bad "missing $t"
done
for t in $(grep -oh 'templates/[A-Za-z0-9_-]*\.[A-Za-z0-9.]*[A-Za-z0-9]' skills/extend-process/SKILL.md | sort -u); do
  [ -f "skills/extend-process/$t" ] && ok "extend-process/$t" || bad "missing extend-process/$t"
done

echo "Coverage map files exist"
for p in $(grep -oh '`[A-Za-z0-9_./*-]*\.\(md\|sh\|json\|tpl\|yml\)`' COVERAGE.md | tr -d '`' | sort -u); do
  case "$p" in *\**|docs/*) continue;; esac
  found=$(find . -path "*$p" 2>/dev/null | head -1)
  [ -n "$found" ] && ok "$p" || bad "COVERAGE.md names missing file $p"
done

echo "guard.sh"
g() { printf '%s' "$1" | bash scripts/guard.sh >/dev/null 2>&1; echo $?; }
t() { [ "$(g "$2")" = "$1" ] && ok "$3" || bad "$3"; }
t 2 '{"tool_name":"Bash","tool_input":{"command":"git push --force origin main"}}' "blocks force-push"
t 2 '{"tool_name":"Bash","tool_input":{"command":"git push -f"}}' "blocks push -f"
t 0 '{"tool_name":"Bash","tool_input":{"command":"git push origin feature/x"}}' "allows normal push"
t 2 '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' "blocks rm -rf /"
t 2 '{"tool_name":"Bash","tool_input":{"command":"rm -rf ~/"}}' "blocks rm -rf ~"
t 0 '{"tool_name":"Bash","tool_input":{"command":"rm -rf build/cache"}}' "allows rm -rf of named folder"
t 2 '{"tool_name":"Bash","tool_input":{"command":"cat .env"}}' "blocks cat .env"
t 2 '{"tool_name":"Bash","tool_input":{"command":"grep KEY ./.env.production"}}' "blocks grep .env.production"
t 0 '{"tool_name":"Bash","tool_input":{"command":"cat .env.example"}}' "allows .env.example"
t 0 '{"tool_name":"Bash","tool_input":{"command":"npm test"}}' "allows npm test"
t 2 '{"tool_name":"Read","tool_input":{"file_path":"/repo/.env"}}' "blocks Read .env"
t 2 '{"tool_name":"Read","tool_input":{"file_path":"/repo/.env.local"}}' "blocks Read .env.local"
t 0 '{"tool_name":"Read","tool_input":{"file_path":"/repo/.env.example"}}' "allows Read .env.example"
t 0 '{"tool_name":"Read","tool_input":{"file_path":"/repo/src/environment.ts"}}' "allows Read environment.ts"
t 2 '{"tool_name":"Bash","tool_input":{"command":"git branch -D feature/x"}}' "blocks branch delete -D"
t 2 '{"tool_name":"Bash","tool_input":{"command":"git branch --delete old"}}' "blocks branch --delete"
t 2 '{"tool_name":"Bash","tool_input":{"command":"git push origin --delete old"}}' "blocks remote branch delete"
t 2 '{"tool_name":"Bash","tool_input":{"command":"git push origin :old"}}' "blocks remote delete by colon"
t 0 '{"tool_name":"Bash","tool_input":{"command":"git push origin HEAD:feature/x"}}' "allows push HEAD:branch"
t 0 '{"tool_name":"Bash","tool_input":{"command":"git branch feature/new"}}' "allows creating a branch"
t 0 'not json' "ignores bad input"

echo "prompt-guard.sh"
pg() { printf '%s' "$2" | bash scripts/prompt-guard.sh >/dev/null 2>&1; [ $? = "$1" ] && ok "$3" || bad "$3"; }
pg 2 '{"prompt":"here is my key AKIAIOSFODNN7EXAMPLE please debug"}' "blocks AWS key"
pg 2 '{"prompt":"-----BEGIN RSA PRIVATE KEY-----\nabc"}' "blocks private key"
pg 2 '{"prompt":"DATABASE_URL=postgres://admin:hunter2pass@db.internal:5432/app"}' "blocks connection string with password"
pg 2 '{"prompt":"password = SuperSecret123"}' "blocks password assignment"
pg 2 '{"prompt":"token ghp_abcdefghijklmnopqrstuvwxyz0123456789AB"}' "blocks GitHub token"
pg 0 '{"prompt":"Add an export button to the invoices page"}' "allows normal prompt"
pg 0 '{"prompt":"How do I reset my password flow in the UI?"}' "allows the word password"
pg 2 '{"prompt":"API_KEY=\"sk_live_abcdef1234567890\""}' "blocks quoted literal key"
pg 0 '{"prompt":"ADMIN_TOKEN = os.environ.get(\"ADMIN_TOKEN\", \"\")"}' "allows token read from environment"
pg 0 '{"prompt":"token = request.headers.get(\"X-Admin-Token\")"}' "allows token read from header"
pg 0 '{"prompt":"password = hash_password(user_input)"}' "allows password from a function call"
pg 0 '{"prompt":"API_KEY=\"your-api-key-here\""}' "allows placeholder value"
pg 0 'not json' "ignores bad input"
hd="$(mktemp -d)"; mkdir "$hd/.git"; export TMPDIR="$hd"
o1="$(printf '{"prompt":"fix it","cwd":"%s"}' "$hd" | bash scripts/prompt-guard.sh)"; o2="$(printf '{"prompt":"fix it","cwd":"%s"}' "$hd" | bash scripts/prompt-guard.sh)"
echo "$o1" | grep -q "not set up" && [ -z "$o2" ] && ok "setup hint once for a project without docs/PROCESS.md" || bad "setup hint"
mkdir "$hd/docs"; touch "$hd/docs/PROCESS.md"; rm -f "$hd"/dev-process-hint-*
o3="$(printf '{"prompt":"fix it","cwd":"%s"}' "$hd" | bash scripts/prompt-guard.sh)"; [ -z "$o3" ] && ok "no hint once set up" || bad "hint when set up"
unset TMPDIR; rm -rf "$hd"

echo "post-edit.sh"
tmp="$(mktemp -d)"; mkdir "$tmp/.devprocess"
export CLAUDE_PROJECT_DIR="$tmp"
bash scripts/post-edit.sh >/dev/null 2>&1; [ $? = 0 ] && ok "no config: skipped" || bad "no config"
echo '{"lint":"true","test":"true"}' > "$tmp/.devprocess/config.json"
bash scripts/post-edit.sh >/dev/null 2>&1; [ $? = 0 ] && ok "passing commands: exit 0" || bad "passing"
echo '{"lint":"true","test":"echo boom; false"}' > "$tmp/.devprocess/config.json"
out="$(bash scripts/post-edit.sh 2>&1 >/dev/null)"; rc=$?
[ $rc = 2 ] && echo "$out" | grep -q boom && ok "failing test: exit 2 with output" || bad "failing test"
echo '{"lint":"","test":""}' > "$tmp/.devprocess/config.json"
bash scripts/post-edit.sh >/dev/null 2>&1; [ $? = 0 ] && ok "empty commands: skipped" || bad "empty"
rm -rf "$tmp"

echo "token-report"
python3 tests/test-token-report.py >/dev/null 2>&1 && ok "token-record and token-report: none, insufficient, enough data, verdicts" || bad "token-report tests"

echo "update-check.sh"
ud="$(mktemp -d)"
printf '{"version": "9.9.9"}' > "$ud/new.json"; printf '{"version": "0.0.1"}' > "$ud/old.json"
V="$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([0-9.]*\)".*/\1/p' .claude-plugin/plugin.json | head -1)"; printf '{"version": "%s"}' "$V" > "$ud/same.json"
o="$(DEVPROCESS_LATEST_FILE="$ud/new.json" bash scripts/update-check.sh)"; echo "$o" | grep -q '"systemMessage"' && echo "$o" | grep -q "9.9.9" && echo "$o" | grep -q "plugin update dev-process@dev-process" && ok "newer version: notice with commands" || bad "update notice"
o="$(DEVPROCESS_LATEST_FILE="$ud/same.json" bash scripts/update-check.sh)"; [ -z "$o" ] && ok "same version: silent" || bad "same version"
o="$(DEVPROCESS_LATEST_FILE="$ud/old.json" bash scripts/update-check.sh)"; [ -z "$o" ] && ok "older remote: silent" || bad "older remote"
o="$(DEVPROCESS_LATEST_FILE="$ud/missing.json" bash scripts/update-check.sh)"; [ $? = 0 ] && [ -z "$o" ] && ok "unreadable remote: silent, exit 0" || bad "unreadable remote"
rm -rf "$ud"

echo "task-tokens"
python3 tests/test-task-tokens.py >/dev/null 2>&1 && ok "task-tokens: sums since last prompt, de-dupes chunks, fails silent" || bad "task-tokens tests"

[ $fail = 0 ] && echo "ALL PASS" || echo "FAILURES"
exit $fail
