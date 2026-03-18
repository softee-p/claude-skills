#!/bin/bash
# Patches Claude Code binary to enable /chrome on WSL.
# Replaces fs.existsSync("/proc/sys/fs/binfmt_misc/WSLInterop") check path
# with a non-existent path of identical byte length, making isWslEnvironment()
# return false. Does NOT affect sA() platform detection (uses /proc/version).
#
# Usage: bash patch_wsl_chrome.sh [check|patch|restore]
#   check   - Report patch status (default)
#   patch   - Apply the patch
#   restore - Restore from backup

set -euo pipefail

ACTION="${1:-check}"
VERSIONS_DIR="$HOME/.local/share/claude/versions"
ORIGINAL="/proc/sys/fs/binfmt_misc/WSLInterop"
PATCHED="/proc/sys/fs/binfmt_misc/PATCHED_OK"

find_binary() {
  local link
  link="$(readlink -f "$(which claude 2>/dev/null)")" 2>/dev/null
  if [[ -f "$link" ]]; then
    echo "$link"
    return
  fi
  # Fallback: newest file in versions dir
  if [[ -d "$VERSIONS_DIR" ]]; then
    local newest
    newest="$(ls -t "$VERSIONS_DIR" | head -1)"
    if [[ -n "$newest" && -f "$VERSIONS_DIR/$newest" ]]; then
      echo "$VERSIONS_DIR/$newest"
      return
    fi
  fi
  echo ""
}

BINARY="$(find_binary)"
if [[ -z "$BINARY" ]]; then
  echo "ERROR: Could not find Claude Code binary"
  exit 1
fi

VERSION="$(basename "$BINARY")"
BACKUP="${BINARY}.bak"

count_original() { local n; n=$(grep -ao "$ORIGINAL" "$BINARY" 2>/dev/null | wc -l) || true; echo "$n"; }
count_patched() { local n; n=$(grep -ao "$PATCHED" "$BINARY" 2>/dev/null | wc -l) || true; echo "$n"; }

case "$ACTION" in
  check)
    echo "Binary: $BINARY"
    echo "Version: $VERSION"
    orig=$(count_original)
    patched=$(count_patched)
    if [[ "$orig" -eq 0 && "$patched" -gt 0 ]]; then
      echo "Status: PATCHED ($patched replacements)"
    elif [[ "$orig" -gt 0 && "$patched" -eq 0 ]]; then
      echo "Status: UNPATCHED ($orig occurrences to patch)"
    elif [[ "$orig" -eq 0 && "$patched" -eq 0 ]]; then
      echo "Status: UNKNOWN (no WSLInterop or PATCHED_OK found — binary may have changed)"
    else
      echo "Status: PARTIAL (original=$orig, patched=$patched)"
    fi
    [[ -f "$BACKUP" ]] && echo "Backup: $BACKUP" || echo "Backup: none"
    ;;

  patch)
    orig=$(count_original)
    if [[ "$orig" -eq 0 ]]; then
      patched=$(count_patched)
      if [[ "$patched" -gt 0 ]]; then
        echo "Already patched ($patched replacements). Nothing to do."
      else
        echo "No WSLInterop found in binary. May already be fixed upstream or binary changed."
      fi
      exit 0
    fi
    cp "$BINARY" "$BACKUP"
    echo "Backup: $BACKUP"
    perl -pi -e "s|$ORIGINAL|$PATCHED|g" "$BINARY"
    new_count=$(count_patched)
    echo "Patched $new_count occurrence(s) in $BINARY"
    echo "Restart Claude Code for changes to take effect."
    ;;

  restore)
    if [[ ! -f "$BACKUP" ]]; then
      echo "ERROR: No backup found at $BACKUP"
      exit 1
    fi
    cp "$BACKUP" "$BINARY"
    echo "Restored from $BACKUP"
    echo "Restart Claude Code for changes to take effect."
    ;;

  *)
    echo "Usage: $0 [check|patch|restore]"
    exit 1
    ;;
esac
