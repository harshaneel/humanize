#!/usr/bin/env bash
# Install humanize and ai-check skills for any agent that reads from a skills directory.
#
# Usage:
#   ./install.sh                  # Claude Code     (~/.claude/skills)
#   ./install.sh codex            # Codex CLI       (~/.codex/skills)
#   ./install.sh chatgpt          # ChatGPT agents  (~/.agents/skills)
#   ./install.sh all              # all three of the above
#   ./install.sh --copy           # copy files instead of symlinking
#   ./install.sh all --copy       # combinable with any target
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
    claude)  TARGET="claude" ;;
    codex)   TARGET="codex" ;;
    chatgpt) TARGET="chatgpt" ;;
    all)     TARGET="all" ;;
    --copy)  MODE="copy" ;;
    -h|--help)
      sed -n '2,13p' "$0" | sed 's/^# *//'
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      echo "Run with --help for usage." >&2
      exit 1
      ;;
  esac
done

# Resolve target(s) to destination directories
DESTS=()
case "$TARGET" in
  claude)  DESTS=("$HOME/.claude/skills") ;;
  codex)   DESTS=("$HOME/.codex/skills") ;;
  chatgpt) DESTS=("$HOME/.agents/skills") ;;
  all)     DESTS=("$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.agents/skills") ;;
esac

install_into() {
  local dest="$1"
  mkdir -p "$dest"
  echo ""
  echo "Installing skills to $dest (mode: $MODE)"

  for skill in "${SKILLS[@]}"; do
    local src="$REPO_DIR/$skill"
    local dst="$dest/$skill"

    if [ ! -d "$src" ]; then
      echo "  SKIP $skill (missing source directory $src)"
      continue
    fi

    if [ -L "$dst" ] || [ -e "$dst" ]; then
      echo "  removing existing $dst"
      rm -rf "$dst"
    fi

    if [ "$MODE" = "symlink" ]; then
      ln -s "$src" "$dst"
      echo "  symlinked $skill"
    else
      cp -R "$src" "$dst"
      echo "  copied $skill"
    fi
  done
}

for dest in "${DESTS[@]}"; do
  install_into "$dest"
done

echo ""
echo "Done. Restart your agent (or run /reload-skills in Claude Code) to pick up the new skills."
echo ""
echo "Try it: ask your agent to 'humanize this paragraph' or 'run ai-check on this text'."
