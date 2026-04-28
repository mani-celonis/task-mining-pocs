#!/usr/bin/env bash
#
# Emotion Playground — double-click installer
#
# This is a .command file: double-clicking it in Finder opens Terminal
# and runs the bootstrap script automatically. The user sees all output
# and can interact with GitHub CLI auth prompts.

# Resolve the directory this .command file lives in, so we can find
# bootstrap.sh next to it (works whether run from Finder or Terminal).
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

clear

# Calculate left margin to center a 47-column block in the terminal
cols=$(tput cols 2>/dev/null || echo 80)
m=$(( (cols - 47) / 2 ))
[[ $m -lt 0 ]] && m=0
S=$(printf "%${m}s" "")

printf '\n\n'

# Logo
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
printf '\033[0m'
printf '%s%s\n' "$S" '  Prototype Celonis-style apps with AI'
printf '\033[0m'

printf '\n\n'
printf '\033[2m'
printf '%s%s\n' "$S" '+---------------------------------------------+'
printf '%s%s\n' "$S" '|                                             |'
printf '%s%s\n' "$S" '|  This installer will set up your Mac with:  |'
printf '%s%s\n' "$S" '|                                             |'
printf '\033[0m'
printf '\033[38;5;75m'
printf '%s%s\n' "$S" '|  > Xcode CLT    > Homebrew    > Git         |'
printf '%s%s\n' "$S" '|  > Node.js 20   > Yarn        > GitHub CLI  |'
printf '%s%s\n' "$S" '|  > Cursor CLI   > The project repo          |'
printf '\033[0m'
printf '\033[2m'
printf '%s%s\n' "$S" '|                                             |'
printf '%s%s\n' "$S" '|  Clone to: ~/dev/emotion-playground         |'
printf '%s%s\n' "$S" '|                                             |'
printf '%s%s\n' "$S" '+---------------------------------------------+'
printf '\033[0m'

printf '\n'
printf '\033[2m'
printf '%s%s\n' "$S" ' Press Enter to start / Close window to cancel'
printf '\033[0m'
printf ' '

read -r

exec bash "$SCRIPT_DIR/bootstrap.sh"
