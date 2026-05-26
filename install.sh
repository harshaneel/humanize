#!/usr/bin/env bash
# Install humanize and ai-check skills for Claude Code or Codex CLI.
#
# Usage:
#   ./install.sh                  # installs to Claude Code (~/.claude/skills)
#   ./install.sh codex            # installs to Codex CLI (~/.agents/skills)
#   ./install.sh --copy           # copy files instead of symlinking
#   ./install.sh codex --copy
#
# By default the script symlinks the skill directories so that future `git pull`
# updates pick up automatically. Use --copy if you prefer self-contained files.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS=(humanize ai-check)

TARGET="claude"
MODE="symlink"

for arg in "$@"; do
  case "$arg" in
    claude) TARGET="claude" ;;
    codex)  TARGET="codex" ;;
    --copy) MODE="copy" ;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# *//'
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      echo "Run with --help for usage." >&2
      exit 1
      ;;
  esac
done

case "$TARGET" in
  claude) DEST="$HOME/.claude/skills" ;;
  codex)  DEST="$HOME/.agents/skills" ;;
esac

mkdir -p "$DEST"

echo "Installing skills to $DEST (mode: $MODE)"

for SKILL in "${SKILLS[@]}"; do
  SRC="$REPO_DIR/$SKILL"
  DST="$DEST/$SKILL"

  if [ ! -d "$SRC" ]; then
    echo "  SKIP $SKILL (missing source directory $SRC)"
    continue
  fi

  if [ -L "$DST" ] || [ -e "$DST" ]; then
    echo "  removing existing $DST"
    rm -rf "$DST"
  fi

  if [ "$MODE" = "symlink" ]; then
    ln -s "$SRC" "$DST"
    echo "  symlinked $SKILL"
  else
    cp -R "$SRC" "$DST"
    echo "  copied $SKILL"
  fi
done

echo ""
echo "Done. Restart your agent (or run /reload-skills in Claude Code) to pick up the new skills."
echo ""
echo "Try it: ask your agent to 'humanize this paragraph' or 'run ai-check on this text'."
