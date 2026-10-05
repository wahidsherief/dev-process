# Eval results (claude CLI, real runs)

Each eval runs a prompt with the plugin in a fresh copy of `tests/fixtures/mini-app`, then a second call grades every assertion. Runs are noisy: the same eval can differ by one or two assertions between runs.

| Run | Assertions passed | What changed before the next run |
|---|---|---|
| 1 | 55 / 94 (58%) | Evals now say "proceed without questions" for build tasks; skills fixed: acceptance criteria always drafted, legacy skill holds the line on skipping tests, personal-data rule |
| 2 | 77 / 94 (82%) | Judge parsing fixed; fixes to encryption of AI keys, cache key pattern, golden page, UI feedback patterns |
| 3 | 80 / 93 (86%) | Hook false positive found (see below); finish checklists added to the db and UI skills |
| 4 | 70 / 93 (75%) | Judge no longer loads the plugin (it was being blocked by the prompt hook) |
| 5 | 82 / 93 (88%) | Final |

## Found by the evals and fixed

- The secret-in-prompt hook blocked ordinary code such as `token = os.environ.get(...)`. It now flags only quoted literals and literal-looking values, and ignores placeholders and code. Five new hook tests cover it.
- `legacy-migration` agreed to skip tests when asked. It now refuses, offers the smallest characterization test set and names the gates.
- `dev-process start` left acceptance criteria empty when a question was open. It now drafts them with recommended answers.

## Still weak (needs a human look in the pilot)

- `db-review`: on "add an endpoint that lists orders" it fixes the N+1 but sometimes skips pagination, the index check and the query-count test. On caching it names a TTL but not always a key pattern.
- `ui-check`: sometimes leaves a literal colour outside the token block (shadows, overlays).
- `extend-process`: when run non-interactively it sometimes asks questions instead of creating the files.
- Headless runs cannot take screenshots or run a browser, so UI proof is only listed, not gathered.

Do not read the percentage as a quality score for real use. It shows which rules the model follows without being reminded, and where the CI and the reviewer agent must catch the rest.
