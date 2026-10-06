---
name: db-check
description: 'Apply and check the backend and database standards: N+1 queries, indexes, migrations, caching, background jobs, email, API design. Use when writing or reviewing API endpoints, ORM queries, schema or migrations, cache, queues, or email code, or when asked to optimize a slow query.'
---

# db-check

Backend and data standards. Apply them automatically while building. Do not ask the developer for rules you can apply yourself. [S] = Safe and Risk; no tag = Risk only.


[S] = Safe standard (always applies). No tag = Risk standard only (risky tasks). Apply these automatically when the task touches API, data, jobs or email.

**Scope.** Rule 8 in `dev-process`: apply to the lines this task changes or adds; note nearby gaps as "Noticed, not changed".

## Before you finish (every time)
1. Lists are paginated. Every foreign-key, filter and sort column has an index, checked with the real query plan.
2. A test fails if the query count grows.
3. Caching has a named key pattern, a TTL and invalidation in the write path.
4. The summary has the numbers: `queries: before -> after`, and the plan line.

## Always report
In the summary, state both numbers, for example `queries: 1,001 -> 1`, for the endpoints touched (if you did not measure the before count, compute it from the code, such as 1 + N, and say it is computed); the index check on the filter, sort and foreign-key columns, with the real query plan (run `EXPLAIN QUERY PLAN` on SQLite or `EXPLAIN` elsewhere and quote the plan line; do not assume an index exists), and the cache key pattern with its TTL and invalidation when caching is added.

## API and access
- [S] **API design.** Consistent names, response shape and error format. Validate every input on the server. Paginate every list; filter and sort only on indexed fields. Document the API; version it when a change can break clients.
- [S] **Authentication and authorization.** Identity on every request, role on every action, deny by default. Expire sessions; rate-limit sign-in attempts; modern password hash. Log permission changes.

## Data
- [S] **Database and ORM.** All queries through the ORM. No N+1: load related data in one query or in batches, never in a loop. Select only needed columns; paginate; keep joins simple. Index every foreign key and every filter or sort column; check the query plan. Add a test that fails when a key endpoint's query count grows.
- [S] **Migrations.** Versioned files, each with a rollback. Additive first: add, backfill, switch, remove later. Test on a copy of realistic data. Never edit production by hand.
- **Scalable design.** Stateless services. No unbounded queries. Heavy work in queues. Rate-limit expensive endpoints. Load-test key flows against the baseline.
- **Backups and rollback.** Automated backups, tested restore, feature flags for risky changes.
- Before: loop over orders, one query per user (1 + N queries). After: one batched query, needed columns only, paginated, indexed.

## Caching and jobs
- **Caching.** Cache data that is read often and rarely changes: settings, lookups, heavy reports. Name the key pattern (for example `currency:list:v1`) and the TTL. Invalidate inside the write path itself, not through a helper callers must remember to call. Never put per-user data under a shared key. Provide an admin clear-cache action.
- **Background jobs.** Slow work runs in a queue: email, imports, reports, AI calls. Safe to retry, with a timeout and a failed-job list.

## Email and configuration
- **Email.** Mailpit in dev and test. An email settings page with test-send: host, port, user, from-address, encryption. Send through a queue; templates in one place.
- **Configuration.** Environment config for deployment, database settings for admins. Validate on read and write; encrypt stored secrets; audit changes; clear the cache on save.

## Observability and tests
- [S] **Logging and audit.** One audit helper. Request id on every log line. Health checks plus error-rate and latency alerts.
- **Test data.** Seed, reset, factories. Mock external services. Unit, integration and contract tests run from an empty database.

## Proof to gather
Query count before and after for key endpoints; query plan showing index use; migration up and down output; test output from an empty database; a log line for a critical action; a test email in Mailpit.
