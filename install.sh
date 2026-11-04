#!/usr/bin/env sh
# Install the ANTI-SLOP skill.
#   ./install.sh              -> ~/.claude/skills/anti-slop   (all your projects)
#   ./install.sh --project    -> ./.claude/skills/anti-slop    (current project; commit it to share)
#   ./install.sh --agents     -> ~/.agents/skills/anti-slop    (Codex and other SKILL.md agents)
set -eu
SRC="$(cd "$(dirname "$0")" && pwd)/skills/anti-slop"
case "${1:-}" in
  --project) DEST="$(pwd)/.claude/skills/anti-slop" ;;
  --agents)  DEST="$HOME/.agents/skills/anti-slop" ;;
  ""|--global) DEST="$HOME/.claude/skills/anti-slop" ;;
  *) echo "usage: $0 [--global|--project|--agents]"; exit 2 ;;
esac
[ -f "$SRC/SKILL.md" ] || { echo "SKILL.md not found next to install.sh"; exit 1; }
mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"
echo "ANTI-SLOP installed to $DEST"
echo "Optional, for rendered-page checks: pip install playwright && python3 -m playwright install chromium"
