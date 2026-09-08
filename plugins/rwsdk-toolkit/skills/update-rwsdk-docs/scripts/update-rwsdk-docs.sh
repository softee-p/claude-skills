#!/usr/bin/env bash
set -euo pipefail

# Sync the rwsdk-docs skill references with the official RedwoodSDK documentation.
#
# Usage: update-rwsdk-docs.sh [repo-root]
#   repo-root   Path to the claude-skills repository root (the directory containing
#               plugins/). Optional — if omitted, the script walks up from $PWD
#               looking for plugins/rwsdk-toolkit/skills/rwsdk-docs.
#
# Guarantees:
#   - Nothing is deleted until a complete clone is on disk (a failed fetch leaves
#     the existing references untouched).
#   - The temp clone is always removed, including on failure or interrupt.
#   - Provenance (upstream commit, docs commit date, latest rwsdk release) is written
#     to sync-meta.json so the next sync knows exactly what range it is diffing.

SDK_REPO_URL="https://github.com/redwoodjs/sdk.git"
REMOTE_DOCS_PATH="docs/src/content/docs"

# ---------------------------------------------------------------- locate target
resolve_repo_root() {
    if [ "$#" -ge 1 ] && [ -n "${1:-}" ]; then
        printf '%s\n' "$1"
        return
    fi
    local dir
    dir="$(pwd)"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/plugins/rwsdk-toolkit/skills/rwsdk-docs" ]; then
            printf '%s\n' "$dir"
            return
        fi
        dir="$(dirname "$dir")"
    done
    echo "ERROR: could not locate the repo root. Pass it explicitly:" >&2
    echo "  update-rwsdk-docs.sh /path/to/claude-skills" >&2
    exit 1
}

REPO_ROOT="$(cd "$(resolve_repo_root "${1:-}")" && pwd)"
SKILL_DIR="$REPO_ROOT/plugins/rwsdk-toolkit/skills/rwsdk-docs"
REFERENCES_DIR="$SKILL_DIR/references"
META_FILE="$SKILL_DIR/sync-meta.json"

if [ ! -d "$SKILL_DIR" ]; then
    echo "ERROR: $SKILL_DIR does not exist — is '$REPO_ROOT' the repo root?" >&2
    exit 1
fi

TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT INT TERM

echo "=== Updating rwsdk-docs skill references ==="
echo "Repo root:  $REPO_ROOT"
echo "Target dir: $REFERENCES_DIR"
echo ""

if [ -f "$META_FILE" ]; then
    echo "[0/6] Previous sync:"
    sed 's/^/      /' "$META_FILE"
    echo ""
fi

# ------------------------------------------------------------------ fetch first
echo "[1/6] Cloning RedwoodSDK repository (shallow, sparse)..."
git clone --depth 1 --filter=blob:none --sparse "$SDK_REPO_URL" "$TEMP_DIR" --quiet

echo "[2/6] Checking out $REMOTE_DOCS_PATH ..."
git -C "$TEMP_DIR" sparse-checkout set "$REMOTE_DOCS_PATH"

SRC_DIR="$TEMP_DIR/$REMOTE_DOCS_PATH"
if [ ! -d "$SRC_DIR" ] || [ -z "$(ls -A "$SRC_DIR" 2>/dev/null)" ]; then
    echo "ERROR: upstream docs path '$REMOTE_DOCS_PATH' is missing or empty." >&2
    echo "       The docs may have moved. Existing references were NOT modified." >&2
    exit 1
fi

# Stage into a scratch dir and prune there, so the live references are replaced
# in one step by content that is already known-good.
STAGING="$TEMP_DIR/staging"
mkdir -p "$STAGING"
cp -R "$SRC_DIR"/. "$STAGING"/
find "$STAGING" -type d \( -name images -o -name img -o -name assets \) -prune -exec rm -rf {} + 2>/dev/null || true

STAGED_COUNT="$(find "$STAGING" -type f \( -name '*.mdx' -o -name '*.md' \) | wc -l | tr -d ' ')"
if [ "$STAGED_COUNT" -lt 10 ]; then
    echo "ERROR: only $STAGED_COUNT doc files found upstream — refusing to replace" >&2
    echo "       $REFERENCES_DIR with a suspiciously small set." >&2
    exit 1
fi

# ---------------------------------------------------------------------- swap in
echo "[3/6] Replacing references ($STAGED_COUNT files)..."
rm -rf "$REFERENCES_DIR"
mkdir -p "$REFERENCES_DIR"
cp -R "$STAGING"/. "$REFERENCES_DIR"/

# ------------------------------------------------------------------- provenance
echo "[4/6] Recording provenance..."
DOCS_COMMIT="$(git -C "$TEMP_DIR" rev-parse HEAD)"
DOCS_COMMIT_DATE="$(git -C "$TEMP_DIR" log -1 --format=%cI)"

RWSDK_LATEST="$(npm view rwsdk version 2>/dev/null || echo unknown)"
RWSDK_LATEST_TAG="unknown"
if command -v gh >/dev/null 2>&1; then
    RWSDK_LATEST_TAG="$(gh api 'repos/redwoodjs/sdk/releases?per_page=30' \
        --jq 'map(select(.tag_name | test("test|canary") | not)) | .[0].tag_name' 2>/dev/null || echo unknown)"
fi

cat > "$META_FILE" <<JSON
{
  "synced_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "docs_repo": "redwoodjs/sdk",
  "docs_path": "$REMOTE_DOCS_PATH",
  "docs_commit": "$DOCS_COMMIT",
  "docs_commit_date": "$DOCS_COMMIT_DATE",
  "rwsdk_latest_npm": "$RWSDK_LATEST",
  "rwsdk_latest_release": "$RWSDK_LATEST_TAG",
  "file_count": $STAGED_COUNT
}
JSON
sed 's/^/      /' "$META_FILE"

# ----------------------------------------------------------------------- report
echo ""
echo "[5/6] Files synced:"
find "$REFERENCES_DIR" -type f \( -name '*.mdx' -o -name '*.md' \) | sort | while read -r f; do
    echo "      ${f#"$REFERENCES_DIR"/}"
done

echo ""
echo "[6/6] Next steps (see the update-rwsdk-docs SKILL.md):"
echo "      1. git add -A $REFERENCES_DIR && git diff --cached --stat -M"
echo "      2. Cross-check the release notes for the range above:"
echo "         gh api 'repos/redwoodjs/sdk/releases?per_page=100' --jq '.[] | select(.tag_name|test(\"test|canary\")|not) | \"\\(.tag_name)\\t\\(.published_at[0:10])\"'"
echo "      3. Update SKILL.md index, CHANGELOG.md, and DOC-ACCURACY.md"
echo ""
echo "Done."
