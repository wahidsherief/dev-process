# Data fix: <short title>

Date: <YYYY-MM-DD> · Requested by: <name> · Approved by: <technical lead> · Rollback approved by: <release owner>

## Intent
Rows affected, why, expected count, expected result.

## Script
Path: `scripts/data-fixes/<name>`. Safe to run twice: <yes/how>. Dry-run command: `<cmd>` (prints counts and a redacted sample, changes nothing).

## Backup and rollback
Snapshot taken: <where, when>. Rollback script: `<path>`. Rollback tested on a copy: <yes/result>.

## Dry run on a copy
Counts before: <n>. Counts after: <n>. Reconciled: <yes/no>.

## Run log (filled by the human who runs it)
| When | Who | Environment | Rows changed | Result |
|---|---|---|---|---|
