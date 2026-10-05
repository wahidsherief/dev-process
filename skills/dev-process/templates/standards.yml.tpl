# Standards checks. Fill the <placeholders> for the project's stack, then save as
# .github/workflows/standards.yml. Mark these jobs as required in branch protection
# so a failure blocks the merge.
name: standards
on: [pull_request]

jobs:
  pr-size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: Max 400 changed lines
        run: |
          base="origin/${{ github.base_ref }}"
          n=$(git diff --numstat "$base"...HEAD -- . ':!*lock*' ':!docs/proof/**' | awk '{a+=$1+$2} END {print a+0}')
          echo "changed lines: $n"
          [ "$n" -le 400 ] || { echo "PR is over 400 changed lines. Split it into slices."; exit 1; }

  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # <setup step for the stack, for example setup-node or setup-python>
      - name: Lint
        run: <lint command>
      - name: Types
        run: <type check command>
      - name: Tests
        run: <test command>

  secrets-and-dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: Secret scan
        uses: gitleaks/gitleaks-action@v2
      - name: Dependency scan (fails on high severity)
        run: <for example: npm audit --audit-level=high | pip-audit | composer audit>

  pr-checklist:
    runs-on: ubuntu-latest
    steps:
      - name: PR description has the done check and a memory note ticked
        env:
          BODY: ${{ github.event.pull_request.body }}
        run: |
          echo "$BODY" | grep -q "## Lane" || { echo "PR template missing."; exit 1; }
          if echo "$BODY" | grep -E "^\- \[ \] (Tests pass|Approver named)"; then
            echo "Process items are not ticked."; exit 1
          fi

  fix-has-test:
    # Bug fixes must include a test change, so the bug cannot come back.
    runs-on: ubuntu-latest
    if: startsWith(github.head_ref, 'fix/') || startsWith(github.head_ref, 'hotfix/')
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: A fix needs a test change (a hotfix may add it within 24 hours)
        run: |
          base="origin/${{ github.base_ref }}"
          if git diff --name-only "$base"...HEAD | grep -Eqi '(test|spec)'; then echo "test changed"; exit 0; fi
          case "${{ github.head_ref }}" in hotfix/*) echo "hotfix: test due within 24 hours"; exit 0;; esac
          echo "No test file changed in a bug-fix PR."; exit 1
