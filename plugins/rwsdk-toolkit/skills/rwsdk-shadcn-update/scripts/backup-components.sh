#!/usr/bin/env bash
set -euo pipefail
# Snapshot every shadcn/ui component in this project before an update.
#
# Usage: backup-components.sh
#   Run from the project root. No editing required — the whole UI directory is
#   copied, so nothing can be missed by a stale hand-maintained list.
#
# Env: SHADCN_UI_DIR (override detection), SHADCN_BACKUP_DIR (default .shadcn-backup)

# shellcheck source=_common.sh
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

require_project_root
UI_DIR="$(detect_ui_dir)"
[ -d "$UI_DIR" ] || die "UI directory '$UI_DIR' does not exist."

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
DEST="$BACKUP_ROOT/$STAMP"
mkdir -p "$DEST"
cp -R "$UI_DIR"/. "$DEST"/

COUNT="$(find "$DEST" -type f | wc -l | tr -d ' ')"
echo "[SUCCESS] Backed up $COUNT file(s) from $UI_DIR -> $DEST"

if [ -f .gitignore ] && ! grep -qx "${BACKUP_ROOT%/}/" .gitignore 2>/dev/null \
   && ! grep -qx "${BACKUP_ROOT%/}" .gitignore 2>/dev/null; then
    echo "[INFO] Consider adding '${BACKUP_ROOT%/}/' to .gitignore"
fi
