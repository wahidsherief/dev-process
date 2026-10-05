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
