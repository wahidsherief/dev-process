#!/usr/bin/env python3
"""Run the skill evals with the real Claude Code CLI, then grade each assertion with a second call.
Usage: python3 tests/run-evals.py [skill-name ...]   (default: all)
Needs the `claude` CLI signed in. Each eval runs in a fresh empty temp project. Results: tests/eval-results/*.json
"""
import json, os, shutil, subprocess, sys, tempfile, glob, concurrent.futures as cf, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'tests', 'eval-results'); os.makedirs(OUT, exist_ok=True)
want = set(sys.argv[1:])

def run(prompt, cwd, plugin=True):
    r = subprocess.run(['claude', '-p', prompt, *(['--plugin-dir', ROOT] if plugin else []), '--dangerously-skip-permissions'],
                       cwd=cwd, capture_output=True, text=True, timeout=420)
    return (r.stdout or '') + (('\n[stderr] ' + r.stderr[-500:]) if r.returncode and r.stderr else '')

def files(cwd):
    out = []
    for dp, dn, fn in os.walk(cwd):
        dn[:] = [d for d in dn if d != '.git']
        for f in fn: out.append(os.path.relpath(os.path.join(dp, f), cwd))
    return sorted(out)

def one(skill, ev):
    prompt = ev['prompt']
    prompt = re.sub(r'^/dev-process\b(?!:)', '/dev-process:dev-process', prompt)
    if ev.get('autonomous'):
        prompt += '\n\n(Non-interactive test run: nobody can answer questions and the plan is approved. Make reasonable choices, state them in one line, and complete the work.)'
    with tempfile.TemporaryDirectory() as d:
        fx = ev.get('fixture', 'empty')
        if fx != 'empty':
            shutil.copytree(os.path.join(ROOT, 'tests', 'fixtures', fx), d, dirs_exist_ok=True)
        g = lambda *a: subprocess.run(['git', *a], cwd=d, capture_output=True, text=True)
        g('init', '-q'); g('add', '-A'); g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'base', '--allow-empty')
        try: out = run(prompt, d)
        except Exception as e: out = 'ERROR: %s' % e
        g('add', '-A'); made = [l for l in g('status', '--short').stdout.splitlines()]
        diff = g('diff', '--cached', 'HEAD').stdout[:14000]
        judge = ("You grade an AI assistant's response against assertions. Be strict and literal.\n\n"
                 "USER PROMPT:\n%s\n\nASSISTANT RESPONSE:\n%s\n\nFILES CHANGED IN THE PROJECT (git status):\n%s\n\nDIFF:\n%s\n\n"
                 "Should the process skill have been used? %s\n\nASSERTIONS:\n%s\n\n"
                 "Return ONLY JSON: {\"results\":[{\"assertion\":str,\"pass\":bool,\"why\":str}]}"
                 % (ev['prompt'], out[:6000], '\n'.join(made[:60]) or '(none)', diff or '(none)',
                    'yes' if ev.get('should_trigger', True) else 'no, it should NOT be used',
                    '\n'.join('- ' + a for a in ev['assertions'])))
        res = None
        for attempt in range(3):
            try:
                j = run(judge, tempfile.gettempdir(), plugin=False)
                i = j.index('{"results"') if '{"results"' in j else j.index('{')
                res = json.JSONDecoder().raw_decode(j[i:])[0]['results']
                break
            except Exception as e:
                err = '%s | raw: %s' % (e, j[:300].replace('\n', ' ') if 'j' in dir() else '')
        if res is None:
            res = [{'assertion': a, 'pass': False, 'why': 'judge failed: %s' % err} for a in ev['assertions']]
    ok = sum(1 for r in res if r.get('pass'))
    rec = {'skill': skill, 'id': ev['id'], 'prompt': ev['prompt'], 'passed': ok, 'total': len(res), 'results': res, 'output_head': out[:1500], 'files': made}
    json.dump(rec, open(os.path.join(OUT, '%s-%s.json' % (skill, ev['id'])), 'w'), indent=2)
    print('%-18s #%s  %d/%d' % (skill, ev['id'], ok, len(res)), flush=True)
    return rec

jobs = []
for f in sorted(glob.glob(os.path.join(ROOT, 'skills', '*', 'evals', 'evals.json'))):
    d = json.load(open(f))
    if want and d['skill_name'] not in want: continue
    for ev in d['evals']: jobs.append((d['skill_name'], ev))
with cf.ThreadPoolExecutor(4) as ex: recs = list(ex.map(lambda a: one(*a), jobs))
p = sum(r['passed'] for r in recs); t = sum(r['total'] for r in recs)
print('TOTAL assertions passed: %d/%d across %d evals' % (p, t, len(recs)))
