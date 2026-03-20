#!/usr/bin/env bash
# Install ~/.local/bin/agi and ensure PATH in .zshrc + .bashrc
set -euo pipefail

BIN_DIR="${HOME}/.local/bin"
MARKER='# <<< TS-Core agi: ~/.local/bin PATH (do not duplicate) >>>'
PATH_LINE='export PATH="${HOME}/.local/bin:${PATH}"'

mkdir -p "$BIN_DIR"

# Copy bundled agi next to this script, or curl from raw — here we expect script alongside agi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/agi" ]]; then
	cp "$SCRIPT_DIR/agi" "$BIN_DIR/agi"
else
	echo "error: scripts/agi not found next to install-agi-launcher.sh" >&2
	exit 1
fi
chmod +x "$BIN_DIR/agi"

append_path_block() {
	local rcfile="$1"
	if [[ -f "$rcfile" ]] && grep -qF "$MARKER" "$rcfile" 2>/dev/null; then
		return 0
	fi
	{
		printf '\n%s\n' "$MARKER"
		printf '%s\n' "$PATH_LINE"
	} >>"$rcfile"
}

touch "${HOME}/.zshrc"
touch "${HOME}/.bashrc"
append_path_block "${HOME}/.zshrc"
append_path_block "${HOME}/.bashrc"

echo "Installed: $BIN_DIR/agi"
echo "PATH hook added to ~/.zshrc and ~/.bashrc"
echo "Open a new terminal or: source ~/.zshrc  (or ~/.bashrc)"
echo "Then run: agi"
