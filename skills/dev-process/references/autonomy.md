# Autonomy: what to do silently, what to ask, what always stops

Goal: easy for the developer, strict underneath.

## Apply automatically (no question)

- N+1 prevention, selected columns only, pagination, keep joins simple
- Indexes on foreign keys and on filter or sort columns; check the query plan
- Caching for data read often and changed rarely: a named key pattern, a TTL, and invalidation inside the write path
- Validation (client and server), toasts and alerts, loading / empty / error states, fallback pages
- Dark and light mode, layout density, responsive layout, accessibility basics
- Logging of critical actions, error reporting, audit entry
- Values that an admin may change go to the settings page, not into code
- Tests for what is built; mocks and seed data
- Gathering proof: query counts, test output, screenshots at 360 / 768 / 1280 px, accessibility scan, log line

## Ask only when needed

- The requirement is unclear or has more than one reasonable reading
- A real trade-off with a cost (for example caching that makes data slightly stale)
- A new setting, table or dependency the plan did not expect
- A rule you want to mark N/A: propose the reason, the developer confirms
- A conflict between a rule and the requirement
- Red-class data would be involved

Ask once, with a recommended answer. Never ask a question you can answer from the repo.

## Always stop for a human

- Brief (when unclear), plan (new or large work), PR approval
- Migration gates 1 to 4, release sign-off
- Destructive or hard-to-undo actions

## Report

At the end of each task, list what was applied automatically in one line, with numbers: query count before and after (for example `queries: 1,001 -> 1`), the index and query-plan result, and the cache key pattern and TTL when caching was added. Example:

- Applied: batched the invoice query (1 query, was 1+N), index on invoices.customer_id, cache 'export-lookups' 10 min, audit entry on export, setting 'export_max_rows'.
