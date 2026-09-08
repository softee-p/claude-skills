#!/usr/bin/env bash
# Shared helpers for the rwsdk-shadcn-update scripts.
#
# These scripts operate on the PROJECT in the current working directory.
# They never read or write anything inside the installed plugin — plugin files are
# shared across every project and are replaced on plugin update.

BACKUP_ROOT="${SHADCN_BACKUP_DIR:-.shadcn-backup}"

die() { echo "[ERROR] $*" >&2; exit 1; }

require_project_root() {
    [ -f "package.json" ] || die "no package.json in $(pwd) — run this from your project root."
}

# Resolve the shadcn UI directory from components.json, falling back to conventions.
detect_ui_dir() {
    if [ -n "${SHADCN_UI_DIR:-}" ]; then
        printf '%s\n' "$SHADCN_UI_DIR"; return
    fi
    if [ -f "components.json" ] && command -v python3 >/dev/null 2>&1; then
        local dir
        dir="$(python3 - <<'PY' 2>/dev/null || true
import json, os
try:
    cfg = json.load(open("components.json"))
except Exception:
    raise SystemExit(1)
alias = cfg.get("aliases", {}).get("ui")
if not alias:
    raise SystemExit(1)
# "@/app/components/ui" -> src/app/components/ui  (honours a tsconfig-style "@/" -> src/)
rel = alias[2:] if alias.startswith("@/") else alias.lstrip("./")
for base in ("src", "."):
    cand = os.path.join(base, rel)
    if os.path.isdir(cand):
        print(cand); raise SystemExit(0)
print(os.path.join("src", rel))
PY
)"
        if [ -n "$dir" ]; then printf '%s\n' "$dir"; return; fi
    fi
    for cand in src/app/components/ui src/components/ui app/components/ui components/ui; do
        [ -d "$cand" ] && { printf '%s\n' "$cand"; return; }
    done
    die "could not find the shadcn UI directory. Set SHADCN_UI_DIR=<path> and retry."
}

detect_pkg_mgr() {
    if [ -f "pnpm-lock.yaml" ]; then echo "pnpm"
    elif [ -f "yarn.lock" ]; then echo "yarn"
    elif [ -f "package-lock.json" ]; then echo "npm"
    elif [ -f "bun.lockb" ] || [ -f "bun.lock" ]; then echo "bun"
    else echo "npm"; fi
}

detect_pkg_exec() {
    case "$(detect_pkg_mgr)" in
        pnpm) echo "pnpm dlx" ;;
        yarn) echo "yarn dlx" ;;
        bun)  echo "bunx" ;;
        *)    echo "npx" ;;
    esac
}

latest_backup() {
    [ -d "$BACKUP_ROOT" ] || return 1
    ls -1d "$BACKUP_ROOT"/*/ 2>/dev/null | sort | tail -1
}
