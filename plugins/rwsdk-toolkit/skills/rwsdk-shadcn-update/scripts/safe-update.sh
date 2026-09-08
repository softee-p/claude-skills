#!/usr/bin/env bash
set -euo pipefail
# Backup -> update the named components -> report what changed -> validate.
#
# Usage: safe-update.sh <component> [component...]
#   e.g. safe-update.sh input alert label
#
# Pass ONLY components you determined are safe to overwrite (Phase 1 of SKILL.md).
# Customized components are deliberately NOT auto-restored: that would silently
# discard the update you just asked for. Use restore-components.sh if you need to
# roll one back.
#
# Env: SHADCN_UI_DIR, SHADCN_BACKUP_DIR

# shellcheck source=_common.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$SCRIPT_DIR/_common.sh"

[ "$#" -ge 1 ] || die "no components given. Usage: safe-update.sh <component> [component...]"

require_project_root
UI_DIR="$(detect_ui_dir)"
PKG_MGR="$(detect_pkg_mgr)"
PKG_EXEC="$(detect_pkg_exec)"

echo "[INFO] Project:         $(pwd)"
echo "[INFO] UI directory:    $UI_DIR"
echo "[INFO] Package manager: $PKG_MGR (exec: $PKG_EXEC)"
echo "[INFO] Components:      $*"
echo ""

echo "=== STEP 1: Backup ==="
bash "$SCRIPT_DIR/backup-components.sh"
BACKUP="$(latest_backup || true)"; BACKUP="${BACKUP%/}"
[ -n "$BACKUP" ] || die "backup step did not produce a snapshot."
echo ""

echo "=== STEP 2: Update ==="
# shellcheck disable=SC2086
$PKG_EXEC shadcn@latest add "$@" --overwrite --yes
echo ""

echo "=== STEP 3: What actually changed ==="
CHANGED=0
while IFS= read -r f; do
    rel="${f#"$UI_DIR"/}"
    if [ ! -f "$BACKUP/$rel" ]; then
        echo "  [NEW]      $rel"; CHANGED=$((CHANGED+1))
    elif ! cmp -s "$f" "$BACKUP/$rel"; then
        echo "  [MODIFIED] $rel"; CHANGED=$((CHANGED+1))
    fi
done < <(find "$UI_DIR" -type f | sort)
if [ "$CHANGED" -eq 0 ]; then echo "  (no files changed)"; fi
echo ""
echo "[INFO] Review each MODIFIED file for customizations that were overwritten:"
echo "       diff $BACKUP/<file> $UI_DIR/<file>"
echo "       Roll one back with: bash $SCRIPT_DIR/restore-components.sh <file>"
echo ""

echo "=== STEP 4: Type check ==="
if grep -q '"types"' package.json; then
    $PKG_MGR run types || die "type check failed — review the errors above."
    echo "[SUCCESS] Type check passed"
else
    echo "[WARNING] No 'types' script in package.json, skipping"
fi
echo ""

echo "=== STEP 5: Build ==="
if grep -q '"build"' package.json; then
    $PKG_MGR run build || die "build failed — review the errors above."
    echo "[SUCCESS] Build succeeded"
else
    echo "[WARNING] No 'build' script in package.json, skipping"
fi
echo ""

echo "[SUCCESS] SAFE UPDATE COMPLETE"
echo "Next: run the app ($PKG_MGR run dev), check the pages that use these components, then commit."
