---
name: new-branch-and-pr
description: Create a fresh branch, complete work, and open a pull request
---

# New branch and PR

## Trigger

Starting work that should be shipped through a clean branch and pull request workflow.

## Workflow

1. Ensure the working tree is clean or explicitly handled.
2. Create a descriptive branch from the latest main.
3. Complete implementation.
4. Commit focused changes and push.
5. Create a concise PR with summary.

## Guardrails

- Keep branch scope focused on one change set.

## Output

- New branch name
- PR summary
- PR URL
- Preview URL (https://celonis.github.io/emotion-playground/pr-<number>/)
