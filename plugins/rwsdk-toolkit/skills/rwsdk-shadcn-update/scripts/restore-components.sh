#!/usr/bin/env bash
set -euo pipefail
# Restore shadcn/ui components from the most recent backup.
#
# Usage:
#   restore-components.sh --all                 Restore every backed-up file
#   restore-components.sh button.tsx card.tsx   Restore only these files
#   restore-components.sh --list                Show what the backup contains
#
# Env: SHADCN_UI_DIR, SHADCN_BACKUP_DIR

# shellcheck source=_common.sh
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"

require_project_root
UI_DIR="$(detect_ui_dir)"

SRC="$(latest_backup || true)"
[ -n "$SRC" ] || die "no backup found under '$BACKUP_ROOT'. Run backup-components.sh first."
SRC="${SRC%/}"
echo "[INFO] Restoring from $SRC -> $UI_DIR"

if [ "$#" -eq 0 ]; then
    die "nothing to restore. Pass --all, --list, or one or more filenames."
fi

if [ "$1" = "--list" ]; then
    (cd "$SRC" && find . -type f | sed 's|^\./|  |' | sort)
    exit 0
fi

mkdir -p "$UI_DIR"

if [ "$1" = "--all" ]; then
    cp -R "$SRC"/. "$UI_DIR"/
    echo "[SUCCESS] Restored all files from backup"
else
    for name in "$@"; do
        if [ -f "$SRC/$name" ]; then
            cp "$SRC/$name" "$UI_DIR/$name"
            echo "[SUCCESS] Restored $name"
        else
            echo "[WARNING] $name not found in backup — skipped"
        fi
    done
fi

echo ""
echo "[INFO] For components that were customized:"
echo "   - diff against the freshly-added version to see what upstream changed"
echo "   - re-apply any upstream improvements you still want by hand"
echo "   - type check and build before committing"
