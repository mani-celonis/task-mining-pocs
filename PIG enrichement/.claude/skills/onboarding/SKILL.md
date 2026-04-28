---
name: onboarding
description: Help first-time users and agents clone, install, authenticate, run, and safely start prototyping in Emotion Playground.
---

# Emotion Playground Onboarding

Use this skill for first-run setup, dependency installation, and getting onto a safe working branch.

## Prerequisites Check

Before following the workflow below, verify the user has basic developer tools (`brew`, `git`, `node`, `yarn`). If any are missing, run the bootstrap script first:

```bash
bash scripts/bootstrap.sh
```

If the repo is not yet cloned, direct the user to download `bootstrap.sh` from the [landing page](https://supreme-chainsaw-4q5oznn.pages.github.io/) and run:

```bash
bash ~/Downloads/bootstrap.sh
```

The script is macOS-only and idempotent. It installs Xcode CLT, Homebrew, Git, Node.js 20, Yarn, and GitHub CLI, then clones and sets up the repo.

## Required Workflow

1. Check the current branch with `git branch --show-current`.
2. If the branch is `main`, create and switch to a descriptive working branch before editing files:

```bash
git checkout -b <descriptive-branch-name>
```

3. Read `README.md` and `AGENTS.md`.
4. Choose the setup path by operating system:
	- macOS: `yarn setup`
	- Linux and other non-macOS systems:

```bash
export GITHUB_TOKEN=your_token_here
yarn install
```

5. Start the app:

```bash
ng serve
```

The app runs at `http://localhost:4200`.

## Agent Rules

- Never make code changes while staying on `main`.
- On macOS, prefer `yarn setup` over manual token steps.
- On Linux, do not recommend `yarn setup` as the primary path.
- If install fails for `@celonis` packages, check `GITHUB_TOKEN` or GitHub CLI auth first.
- After setup, switch to the `emotion-ui` skill for implementation work.