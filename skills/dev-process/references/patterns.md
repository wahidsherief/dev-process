# Patterns: reusable approved project patterns

Registry: `docs/PATTERNS.md` (one table). A pattern is metadata plus a pointer to the canonical source file. Never copy source code into the registry.

| Field | Meaning |
|---|---|
| Name | for example `standard modal` |
| Category | modal, data table, form, api, query, job, email... |
| Status | Candidate, Approved, Active or Deprecated |
| When to use | one line |
| Canonical source | path (and symbol) of the real implementation |
| Constraints | dependencies or limits, if any |

## Lifecycle

Candidate → Approved → Active → Deprecated.

- Only **Approved** and **Active** patterns are recommended or applied automatically.
- Candidate: suggested, not yet reviewed. Deprecated: never recommended; say what replaces it.
- Only a human moves a pattern to Approved (the technical lead, or the developer when they say so). Claude never does it on its own.

## `patterns [filter]`

List matching patterns from `docs/PATTERNS.md`: name, category, status, when to use, source. With no filter, list Approved and Active. With a filter (`modal`, `data table`, `api`), match category or name. `patterns all` includes Candidate and Deprecated. If the file is missing or empty, say so. Do not search the codebase.

## Using a pattern in a task

- When the task clearly matches an Approved or Active pattern (match category and name by search; do not read the whole file when it is long), read only its canonical source and build on it. Say in the summary which pattern was used.
- If the developer says "apply the standard modal pattern", look it up by name. If it is missing or not Approved, say so and ask.
- Do not recreate something an approved pattern already provides.

## Suggesting a new pattern

After work that went well and is likely to be reused, add a bold bullet inside the summary's **Insights** section: `- **Pattern candidate:** <name> (<category>) at [path](path). Add as Candidate?` (it counts toward the 3-bullet limit and creates the section if there is none). Add the row only if the developer says yes, with status Candidate. Never mark it Approved.

Approving or deprecating: when the developer says so, change the Status cell and nothing else.
