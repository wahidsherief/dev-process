# token-report

Answers one question: is dev-process worth its extra token cost compared with using Claude normally?

- `/dev-process:token-report` runs `scripts/token-report.py` and shows the output unchanged. Do not add analysis or invent numbers.
- Data lives in `.devprocess/token-runs.jsonl`, one line per run. Nothing is recorded automatically.
- Record a run: `scripts/token-record.py --arm plugin|baseline --task <id> --lane <lane> --from-json <claude -p JSON>` (or `--input/--output/--turns`). Use the same `--task` id for the same task done with and without the plugin.
- Add rework and review rounds later: `scripts/token-record.py --annotate <id> --rework N --review-rounds N`.
- Overhead = extra tokens. Efficiency = fewer rework or review rounds. The verdict needs both; fewer than 5 comparable tasks, or no rework data, gives INSUFFICIENT DATA.
- `tests/tokmeasure.py --record` records the plugin test scenarios (plugin and without-plugin) with a version label.
