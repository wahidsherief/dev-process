**Summary format, real token count and pattern bullet are pushed as v1.4.3.**

*Plugin change · feature · 621 used (180k cached) · Low*

---

**Task:** Make the end-of-task summary readable, show real token usage, and update the README for 1.4.2/1.4.3.
**Issue:** The summary was a plain table with detached insights, a vague token level and no real numbers.
**Fixed By:** Plain report: headline, meta line, rule, bold labels with links, optional Insights. New `scripts/task-tokens.py` reads the transcript for used/cached tokens. Pattern candidate now goes in Insights.
**Changes:**
- [skills/dev-process/SKILL.md](skills/dev-process/SKILL.md): new summary format, token step, Insights rule.
- [skills/change-lanes/SKILL.md](skills/change-lanes/SKILL.md), [skills/fix-lanes/SKILL.md](skills/fix-lanes/SKILL.md): point to the shared format.
- [skills/dev-process/references/summary-resume.md](skills/dev-process/references/summary-resume.md): `/summary` layout, token and level rules.
- [skills/dev-process/references/patterns.md](skills/dev-process/references/patterns.md): pattern candidate as an Insights bullet.
- [scripts/task-tokens.py](scripts/task-tokens.py), [tests/test-task-tokens.py](tests/test-task-tokens.py), [tests/run.sh](tests/run.sh): token script and its test.
- [README.md](README.md), [COVERAGE.md](COVERAGE.md), [.claude-plugin/plugin.json](.claude-plugin/plugin.json): docs and version 1.4.3.
**Test Result:** `tests/test-task-tokens.py` passes; script prints real figures on this session. `bash tests/run.sh` not run: it fails broadly on this machine even unchanged.
**Standards:** Applied: guidance kept in skills, nothing hard-coded. Skipped: full suite, `claude plugin validate .`.
**Note saved to:** none (this repo has no docs/memory folder)

**Insights**
- Token figure counts only the last prompt, so it understates a multi-prompt task.
- Low/Medium/High cut-offs (30k, 150k) are guesses until tuned on real runs.
- Format is guidance only; Claude may still add text after Action needed.

**Action needed:** Run `/plugin marketplace update dev-process`, `/plugin update dev-process@dev-process`, `/reload-plugins`, then check one real task. Then `/clear` and `resume`.
