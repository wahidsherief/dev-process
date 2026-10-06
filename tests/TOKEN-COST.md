# Token cost

Method: `claude -p` on the mini-app fixture, same task with and without the plugin, 3 parallel runs, one run per cell. Single runs are noisy; treat the percentages as rough. Script: `tokmeasure.py`.

| Task | Lane | Plain | With plugin | Turns (plain / plugin) | Cost change |
|---|---|---|---|---|---|
| Change a button label | quick change | $0.063 | $0.068 | 3 / 3 | +8% |
| Fix a wrong total | bug fix | $0.090 | $0.087 | 5 / 4 | about 0% |
| Slow orders page (N+1) | bug fix / perf | $0.082 | $0.089 | 4 / 4 | +9% |
| Add a count endpoint with test | small feature | $0.084 | $0.094 | 4 / 4 | +12% |
| Orders CSV export, admin only, with UI | full flow | $0.114 | $0.148 | 4 / 7 | +30% |

## Reading

- Small work costs about 0 to 12% more. The fixed cost is the plugin's skill text (about 1,000 to 1,500 extra cached tokens per run).
- The full flow costs about 30% more and uses 3 more turns (brief, plan, verify, handoff). It is the heavy case, and it is where the process adds the most value.
- These runs were non-interactive, so they do not include the developer's waiting or answering time. A real full-flow task also has one or two confirmation turns.
- Not measured: the `standards-reviewer` agent (it did not trigger on these small diffs) and long migrations. A reviewer run adds its own context, so expect a larger jump on big or risky changes.

## Controls built in

- Quick change and bug fix skip the brief, plan and reviewer
- Standards skills load only for the areas touched
- The reviewer runs once, and only for the full flow when the diff is over about 80 lines or touches auth, permissions, migrations or money
- No nested agents; notes capped at 8 to 20 lines; handoff under 12 lines
- Clear the session between slices

## For the pilot

Record cost and turns per task (usage line or `--output-format json`) and compare medians against similar work done without the plugin. Decide in the retro whether the extra cost on full-flow tasks is worth the rework it prevents.


## v1.4 re-measure (Safe/Risk, hint hook, analyze modes)

Same method, one run per cell, so treat as rough.

| Task | Plain | With plugin | Turns (plain / plugin) | Cost change |
|---|---|---|---|---|
| Change a button label | $0.063 | $0.069 | 3 / 3 | +10% |
| Fix a wrong total | $0.070 | $0.087 | 3 / 4 | +24% |
| Slow orders page (N+1) | $0.099 | $0.106 | 5 / 5 | +7% |
| Add a count endpoint with test | $0.084 | $0.089 | 4 / 4 | +6% |
| Orders CSV export, admin only, with UI | $0.115 | $0.156 | 4 / 7 | +36% |

The bug-fix row is noisy (the plain run was cheaper than in v1.2). Full flow is slightly heavier than v1.2 (+36% vs +30%); the new Standard text and logging check add a little. Not yet re-measured: `analyze`, `init`, and any run where the reviewer triggers.

## v1.4.1 versus v1.4 (2 runs per cell, same machine and time, recorded in `tests/token-runs-v1.4*.jsonl`)

Report: `python3 scripts/token-report.py --file tests/token-runs-v1.4.1.jsonl` (and the v1.4 file). Median of per-task overhead, 5 tasks:

| | v1.4 | v1.4.1 |
|---|---|---|
| Median overhead | +31.3% | +17.7% |
| Average overhead | +22.4% | +16.0% |
| Quick tasks (UI label, endpoint) | +3% | +10% |

Read with care: totals are dominated by cached tokens and swing with the number of turns (the same task sometimes takes 3 turns, sometimes 4, and a plugin run sometimes takes 8 or 9). The two versions are not clearly different. The one stable change is a small fixed saving on the simplest task (about 3.4k extra tokens versus 3.9k). Instruction size: `SKILL.md` 1,228 to 1,099 words; skill descriptions loaded every session 436 to 324 words (-26%); all instruction text 10,709 to about 10,450 words.
No rework or review-round data exists yet, so the report's verdict is INSUFFICIENT DATA. That needs the pilot.
