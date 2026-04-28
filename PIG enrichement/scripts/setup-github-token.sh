#!/usr/bin/env bash

set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
    cat <<'EOF'
This setup helper is intended for macOS.

On other systems, set GITHUB_TOKEN manually before running yarn install.
EOF
    exit 1
fi

if ! command -v yarn >/dev/null 2>&1; then
    cat <<'EOF'
Yarn is required for this repository.

Install it, then rerun this script:
  npm install -g yarn
EOF
    exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
    if ! command -v curl >/dev/null 2>&1; then
        echo "curl is required to install Homebrew."
        exit 1
    fi

    echo "Homebrew not found. Installing Homebrew..."
    NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    if [[ -x /opt/homebrew/bin/brew ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -x /usr/local/bin/brew ]]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
fi

if ! command -v gh >/dev/null 2>&1; then
    echo "GitHub CLI is required to authenticate with GitHub Packages."
    echo "Installing GitHub CLI with Homebrew..."
    brew install gh
fi

if ! gh auth status -h github.com >/dev/null 2>&1; then
    echo "Opening your browser to authenticate with GitHub..."
    gh auth login -h github.com -w -s read:packages
else
    echo "GitHub CLI is already authenticated."
fi

if ! gh auth status -h github.com -t 2>&1 | grep -q 'read:packages'; then
    echo "Refreshing GitHub CLI token to include read:packages..."
    gh auth refresh -h github.com -s read:packages
fi

token="$(gh auth token)"

if [[ -z "$token" ]]; then
    echo "Unable to read a GitHub token from GitHub CLI."
    exit 1
fi

echo "Installing dependencies with your GitHub Packages token..."
GITHUB_TOKEN="$token" yarn install

cat <<'EOF'

Setup complete.

The token came from GitHub CLI and was used only for this install command.
Rerun this helper any time you need to reinstall dependencies:
  yarn setup
EOF