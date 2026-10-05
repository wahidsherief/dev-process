---
name: security-check
description: 'Apply and check security, secrets, logging, audit and error-reporting standards. Use when touching authentication, authorization, input handling, secrets, config, logging, audit trails, error reporting, dependencies, or when asked for a security review.'
---

# security-check

Apply automatically. Gather proof (scan output, a log line, a test error in the reporting tool). [L] = Light and Full tiers; no tag = Full only.

## Security
- [L] Identity and role checked on every route and API. Deny by default.
- [L] Secrets only in environment variables or a secret store. Never in code, prompts, logs or notes.
- [L] Validate all input. Encode all output.
- [L] Dependency and secret scans in CI. High severity blocks the merge.
- Automated backups with a tested restore. A rollback step for every release.
- Sessions expire, sign-in attempts are rate-limited, passwords use a modern hash.

## Logging and audit
- [L] Structured logs with request id and user id on every line.
- [L] Log critical actions: sign-in, create, update, delete, permission changes, imports, background jobs.
- [L] Error reporting (Sentry where applicable or decided), with environment and release.
- [L] Audit table: who changed what and when.
- [L] Never log secrets or personal data.

## Prompt data
Green (code, public docs): allowed. Amber (logs, database samples, config): redact first. Red (secrets, credentials, personal or customer data, production dumps): never. If Red data was pasted, rotate any exposed secret and tell the technical lead.

## If personal or production data is pasted
Open the answer with one plain sentence: personal or production data should be replaced with fake values. Do not name the people or quote any value from the pasted rows, even to say you will not use them: call them "the pasted rows". Then still help: work from the code and synthetic data, and if the code to debug is missing, say exactly what you need (the export code or the error message) and offer a synthetic fixture. If it is a secret, also say to rotate it.

## Proof to gather
Scan results, a test showing a forbidden role is denied, a log line for a critical action, a forced error visible in the reporting tool.
