# Emotion Playground

A sandbox for prototyping Celonis-style applications using the [Emotion design system](https://github.com/celonis/emotion). Designers, product managers, and developers can build prototypes with the help of AI coding agents — no Angular experience required.

Every prototype gets an automatic preview URL when you open a pull request, just like Vercel.

## How it works

1. Clone this repo and create a branch
2. Describe what you want to build to your AI agent (Cursor, GitHub Copilot, Kiro, etc.)
3. Open a pull request
4. A preview URL is posted as a comment on your PR — share it with your team
5. Every push to your branch updates the preview

Prototypes live in branches only. The `main` branch stays clean as a starting point.

## Getting started

Tell your agent to help you set up this project if needed.

If your agent supports repo skills, use the `onboarding` skill first for clone/setup/run help, then switch to `emotion-ui` for UI implementation.

### Starting from scratch?

If you don't have Homebrew, Git, Node.js, or any developer tools installed, download the bootstrap script from the [landing page](https://supreme-chainsaw-4q5oznn.pages.github.io/) and run it in Terminal:

```bash
bash ~/Downloads/bootstrap.sh
```

Or if you already have the repo cloned:

```bash
bash scripts/bootstrap.sh
```

The script is macOS-only, idempotent (safe to re-run), and does not modify your shell profile. It installs Xcode Command Line Tools, Homebrew, Git, Node.js 20, Yarn, and GitHub CLI, then clones the repo and installs dependencies.

Once it finishes, skip ahead to [Building a prototype](#building-a-prototype).

### Prerequisites

If you already have developer tools installed, make sure you have:

- [GitHub account with Celonis org access](https://celonis.roadie.so/docs/default/component/documentation-engineering-central/local-development/github/)
- macOS
- Node.js 20+
- Yarn (`npm install -g yarn`)


### Setup

Use the guided setup helper to authenticate with GitHub Packages and install dependencies:

```bash
yarn setup
```

The helper script will:

- Install Homebrew if it is missing
- Install GitHub CLI with Homebrew if `gh` is missing
- Open your browser and authenticate `gh` with the `read:packages` scope if needed
- Use the GitHub CLI token for `yarn install`
- Avoid modifying your shell profile

If you prefer to do it manually, use a `GITHUB_TOKEN` with read access to the `@celonis` GitHub Packages registry:

https://celonis.roadie.so/docs/default/component/documentation-engineering-central/local-development/github/#add-github-token-to-npm

```bash
export GITHUB_TOKEN=your_token_here

yarn install

ng serve
```

Open http://localhost:4200 — you'll see the Celonis app shell (`ce-main-layout`) ready for you to build inside.

## Building a prototype

The app shell gives every prototype the Celonis look and feel automatically. You just build your content inside it.

If your AI agent notices the repo is on `main`, it should create a new prototype branch automatically before making changes.

Tell your AI agent something like:

> "Build a dashboard with a KPI bar at the top showing 4 metrics, and a data table below with sortable columns."

> "Create a settings page with a form that has text inputs, dropdowns, and a save button."

> "Add a sidebar navigation to the app shell with links for Dashboard, Settings, and Reports."

The agent will use Emotion components and follow the rules in [`AGENTS.md`](./AGENTS.md) to build it right.

### Push and get a preview

```bash
git checkout -b my-prototype
# ... make your changes with your AI agent ...
git add -A
git commit -m "My prototype"
git push origin my-prototype
```

Then open a pull request on GitHub. The CI pipeline builds your app and deploys a preview at:

```
https://celonis.github.io/emotion-playground/pr-<number>/
```

The URL is posted as a comment on your PR.

## For AI agents

All project rules, Emotion component guidelines, and conventions live in [`AGENTS.md`](./AGENTS.md). Tool-specific pointer files (`.cursor/rules/agents.mdc`, `.github/copilot-instructions.md`, `.kiro/steering/agents.md`) reference it so your agent picks up the rules automatically.

For detailed component APIs, read `node_modules/@celonis/emotion/ai-docs/component-catalog.md`.

## Key commands

| Command | Description |
|---------|-------------|
| `bash scripts/bootstrap.sh` | First-time setup from scratch (installs all prerequisites) |
| `yarn install` | Install dependencies |
| `ng serve` | Start dev server at localhost:4200 |
| `ng build` | Production build |
| `ng test` | Run unit tests |
