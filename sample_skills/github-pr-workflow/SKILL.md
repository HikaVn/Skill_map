---
name: github-pr-workflow
description: GitHub PR, Actions, and Pages verification workflow for safe release checks.
---

# github-pr-workflow

## Purpose

Provide a repeatable PR review and release confirmation flow using GitHub.

## When to use

Use this skill when validating pull requests and deployment visibility on GitHub Pages.

## Inputs

- PR URL
- Target branch

## Outputs

- Review checklist result
- Actions and Pages status summary

## Steps

1. Confirm PR scope and changed files.
2. Check CI results in GitHub Actions.
3. Validate required reviewers and merge policy.
4. Confirm Pages build/deploy status.
5. Report pass/fail points with evidence.

## Examples

### Example input

```text
Review PR #42 and ensure pages deploy succeeded.
```

### Example output

```text
PR checks passed, Pages deployed successfully, ready to merge.
```

## Cautions

- Do not merge when required checks are pending.
- Distinguish flaky CI from deterministic failures.

## Troubleshooting

If Actions fail, isolate failing job logs and rerun only after root cause is documented.
