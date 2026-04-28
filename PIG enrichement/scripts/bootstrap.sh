#!/usr/bin/env bash
#
# Emotion Playground — zero-to-running bootstrap
#
# Installs every prerequisite on a fresh macOS machine, clones the repo,
# authenticates with GitHub Packages, and installs dependencies.
#
# Usage (before you have the repo — download from the landing page first):
#   bash ~/Downloads/bootstrap.sh
#
# Usage (from inside the repo):
#   bash scripts/bootstrap.sh

set -euo pipefail

REPO_URL="https://github.com/celonis/emotion-playground.git"
CLONE_ROOT="$HOME/dev"
REPO_DIR="$CLONE_ROOT/emotion-playground"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

step() { printf '\n\033[1;34m==>\033[0m \033[1m%s\033[0m\n' "$1"; }
ok()   { printf '    \033[32m✔\033[0m %s\n' "$1"; }
fail() { printf '    \033[31m✘\033[0m %s\n' "$1" >&2; exit 1; }

# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------

cols=$(tput cols 2>/dev/null || echo 80)
m=$(( (cols - 47) / 2 ))
[[ $m -lt 0 ]] && m=0
S=$(printf "%${m}s" "")

printf '\n'
printf '\033[38;5;39m'
printf '%s%s\n' "$S" '    ______                __  _'
printf '%s%s\n' "$S" '   / ____/___ ___  ____  / /_(_)___  ____'
printf '\033[38;5;75m'
printf '%s%s\n' "$S" '  / __/ / __ `__ \/ __ \/ __/ / __ \/ __ \'
printf '%s%s\n' "$S" ' / /___/ / / / / / /_/ / /_/ / /_/ / / / /'
printf '\033[38;5;111m'
printf '%s%s\n' "$S" '/_____/_/ /_/ /_/\____/\__/_/\____/_/ /_/'
printf '\033[0m'
printf '\n'
printf '\033[1;37m'
printf '%s%s\n' "$S" '     ---- P L A Y G R O U N D ----'
printf '\033[0m'
printf '\033[2m'
printf '%s%s\n' "$S" '  Prototype Celonis-style apps with AI'
printf '\033[0m'
printf '\n'

# ---------------------------------------------------------------------------
# 1. macOS gate
# ---------------------------------------------------------------------------

if [[ "$(uname -s)" != "Darwin" ]]; then
    fail "This bootstrap script is for macOS only. On other systems, install Node 20+, Yarn, and Git manually, then run: export GITHUB_TOKEN=<token> && yarn install"
fi

# ---------------------------------------------------------------------------
# 2. Xcode Command Line Tools
# ---------------------------------------------------------------------------

step "Checking Xcode Command Line Tools"
if xcode-select -p >/dev/null 2>&1; then
    ok "Already installed"
else
    echo "    Installing Xcode Command Line Tools (this may take a few minutes)..."
    xcode-select --install 2>/dev/null || true
    MAX_WAIT=900
    start_time=$(date +%s)
    echo "    Waiting for installation to finish (up to $((MAX_WAIT / 60)) minutes)..."
    while ! xcode-select -p >/dev/null 2>&1; do
        if (( $(date +%s) - start_time >= MAX_WAIT )); then
            fail "Xcode Command Line Tools installation did not complete within $((MAX_WAIT / 60)) minutes. Please finish or cancel the installer, then re-run this script."
        fi
        sleep 5
    done
    ok "Installed"
fi

# ---------------------------------------------------------------------------
# 3. Homebrew
# ---------------------------------------------------------------------------

step "Checking Homebrew"
if command -v brew >/dev/null 2>&1; then
    ok "Already installed ($(brew --version | head -1))"
else
    echo "    Installing Homebrew..."
    NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    if [[ -x /opt/homebrew/bin/brew ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -x /usr/local/bin/brew ]]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
    ok "Installed"
fi

# ---------------------------------------------------------------------------
# 4. Git
# ---------------------------------------------------------------------------

step "Checking Git"
if command -v git >/dev/null 2>&1; then
    ok "Already installed ($(git --version))"
else
    echo "    Installing Git..."
    brew install git
    ok "Installed"
fi

# ---------------------------------------------------------------------------
# 5. Node.js 20
# ---------------------------------------------------------------------------

step "Checking Node.js"
needs_node=true
if command -v node >/dev/null 2>&1; then
    node_major="$(node -v | sed 's/v\([0-9]*\).*/\1/')"
    if [[ "$node_major" -ge 20 ]]; then
        ok "Already installed ($(node -v))"
        needs_node=false
    else
        echo "    Found Node $(node -v) but 20+ is required."
    fi
fi

if $needs_node; then
    echo "    Installing Node.js 20 via Homebrew..."
    brew install node@20
    brew link --overwrite node@20 2>/dev/null || true

    node20_prefix="$(brew --prefix node@20 2>/dev/null || true)"
    if [[ -n "${node20_prefix:-}" && -d "$node20_prefix/bin" ]]; then
        export PATH="$node20_prefix/bin:$PATH"
    fi

    if ! command -v node >/dev/null 2>&1; then
        fail "Node.js 20 was installed via Homebrew but 'node' is not on PATH. Add $(brew --prefix node@20)/bin to your PATH and re-run this script."
    fi

    node_major="$(node -v | sed 's/v\([0-9]*\).*/\1/')"
    if [[ "$node_major" -lt 20 ]]; then
        fail "Node.js 20+ is required but 'node -v' reports $(node -v). Ensure $(brew --prefix node@20)/bin comes before other Node installations on your PATH, then re-run."
    fi

    ok "Installed ($(node -v))"
fi

# ---------------------------------------------------------------------------
# 6. Corepack / Yarn
# ---------------------------------------------------------------------------

step "Checking Yarn"
corepack enable 2>/dev/null || true
if command -v yarn >/dev/null 2>&1; then
    yarn_major="$(yarn --version | sed 's/\([0-9]*\).*/\1/')"
    if [[ "$yarn_major" -eq 1 ]]; then
        ok "Already available ($(yarn --version))"
    else
        echo "    Found Yarn $(yarn --version) but this repo requires 1.x. Preparing yarn@1.22.22..."
        corepack prepare yarn@1.22.22 --activate
        ok "Prepared yarn@1.22.22"
    fi
else
    echo "    Enabling Corepack and preparing Yarn..."
    corepack enable
    corepack prepare yarn@1.22.22 --activate
    ok "Installed ($(yarn --version))"
fi

# ---------------------------------------------------------------------------
# 7. GitHub CLI
# ---------------------------------------------------------------------------

step "Checking GitHub CLI"
if command -v gh >/dev/null 2>&1; then
    ok "Already installed ($(gh --version | head -1))"
else
    echo "    Installing GitHub CLI..."
    brew install gh
    ok "Installed"
fi

# ---------------------------------------------------------------------------
# 8. Clone repo (if not already inside it)
# ---------------------------------------------------------------------------

step "Checking repository"
inside_repo=false
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    remote_url="$(git remote get-url origin 2>/dev/null || true)"
    if [[ "$remote_url" == *"emotion-playground"* ]]; then
        inside_repo=true
        cd "$(git rev-parse --show-toplevel)"
        ok "Already inside the repository ($(pwd))"
    fi
fi

if ! $inside_repo; then
    mkdir -p "$CLONE_ROOT"
    if [[ -d "$REPO_DIR" ]]; then
        if [[ -d "$REPO_DIR/.git" ]]; then
            dir_remote="$(git -C "$REPO_DIR" remote get-url origin 2>/dev/null || true)"
            if [[ "$dir_remote" == *"emotion-playground"* ]]; then
                ok "Directory $REPO_DIR already exists with correct remote — skipping clone"
            else
                fail "Directory $REPO_DIR exists but points to a different remote ($dir_remote). Please rename or remove it and re-run this script."
            fi
        else
            fail "Directory $REPO_DIR exists but is not a git repository. Please rename or remove it and re-run this script."
        fi
    else
        echo "    Cloning into $REPO_DIR ..."
        git clone "$REPO_URL" "$REPO_DIR"
    fi
    cd "$REPO_DIR"
fi

# ---------------------------------------------------------------------------
# 9. Authenticate and install dependencies (delegates to existing script)
# ---------------------------------------------------------------------------

step "Running setup (GitHub auth + dependency install)"
bash scripts/setup-github-token.sh

# ---------------------------------------------------------------------------
# 10. Cursor CLI
# ---------------------------------------------------------------------------

CURSOR_APP="/Applications/Cursor.app"
CURSOR_BIN="$CURSOR_APP/Contents/Resources/app/bin/cursor"

step "Checking Cursor CLI"
if command -v cursor >/dev/null 2>&1; then
    ok "Already on PATH ($(which cursor))"
elif [[ -x "$CURSOR_BIN" ]]; then
    echo "    Cursor.app found but 'cursor' CLI is not on PATH."
    echo "    Creating symlink in /usr/local/bin..."
    mkdir -p /usr/local/bin
    ln -sf "$CURSOR_BIN" /usr/local/bin/cursor 2>/dev/null \
        || sudo ln -sf "$CURSOR_BIN" /usr/local/bin/cursor
    ok "Linked to /usr/local/bin/cursor"
else
    echo "    Cursor.app not found in /Applications."
    echo "    Install Cursor from https://cursor.com and re-run, or open the project manually."
fi

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------

repo_path="$(pwd)"

cat <<EOF

──────────────────────────────────────────────
  Bootstrap complete!
──────────────────────────────────────────────

  Project location: $repo_path

EOF

if command -v cursor >/dev/null 2>&1; then
    echo "  Opening project in Cursor..."
    echo ""
    cursor "$repo_path"
else
    cat <<EOF
  To open in Cursor, run:

    cursor $repo_path

  To start the dev server:

    cd $repo_path
    ng serve

  Then open http://localhost:4200

  To start prototyping, create a branch:

    git checkout -b my-prototype

  and tell your AI agent what to build.

EOF
fi
