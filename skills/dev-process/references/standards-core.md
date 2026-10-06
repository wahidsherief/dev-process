# Core standards (frontend and backend)

Security, secrets, logging and audit are in the `security-check` skill.

[S] = Safe standard (always applies). No tag = Risk standard only (risky tasks).

## Git and PR
- [S] One branch per slice. Maximum 400 changed lines per PR.
- [S] Reviewer agent first, approver last. One named approver per PR (security-sensitive changes included).
- [S] Use the PR template. All checks green before merge.

## Settings
- A settings page for every admin-changeable value: limits, toggles, prices, email, AI keys.
- Each setting has defaults, validation, role protection, masked secrets and audited changes.
- Clear the cache when a setting is saved.
- Before: a limit hard-coded in code, a release needed to change it. After: a setting with default, validation and audit, changed by an admin.

## Test environment
- Test mode flag with a visible TEST banner.
- Seed and reset commands.
- Mocks or sandboxes for email, AI and payments.
- Fake clock where time matters.
- Mailpit catches all email in dev and test.
