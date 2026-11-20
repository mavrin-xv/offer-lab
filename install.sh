#!/usr/bin/env bash
# offer-lab installer: copies the eight skills into Claude Code.
#
#   ./install.sh             into ~/.claude/skills (all projects)
#   ./install.sh --project   into ./.claude/skills (this project only)
#
# Existing skills with the same name are backed up to <name>.bak.<timestamp> first.
# No keys, no network: every script runs offline on local files.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude"
while [ $# -gt 0 ]; do
  case "$1" in
    --project) DEST="$(pwd)/.claude" ;;
    -h|--help) sed -n 2,8p "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

say()  { printf '\033[1m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[33m!!\033[0m %s\n' "$*" >&2; }

PY=""
for c in python3 python py; do   # first one that really runs (Windows ships a python3 stub)
  if command -v "$c" >/dev/null && "$c" -c "import sys; sys.exit(sys.version_info < (3, 8))" 2>/dev/null; then PY="$c"; break; fi
done
[ -n "$PY" ] || warn "No Python 3.8+ found. The skills still work by hand; the helper scripts need Python."

mkdir -p "$DEST/skills"
for s in "$HERE"/skills/*/; do
  name="$(basename "$s")"
  if [ -d "$DEST/skills/$name" ]; then
    mv "$DEST/skills/$name" "$DEST/skills/$name.bak.$(date +%s)"
    warn "backed up existing $name"
  fi
  cp -R "$s" "$DEST/skills/$name"
  find "$DEST/skills/$name" -name __pycache__ -type d -prune -exec rm -r {} + 2>/dev/null || true
  say "installed skill $name"
done

if [ -n "$PY" ]; then
  "$PY" "$DEST/skills/niche-score/scripts/niche_score.py" --help >/dev/null && say "scripts run with $PY"
fi
say "done. Try: \"score these niches: ...\" or \"reality check this idea: ...\"."
