---
name: wsl-chrome-patch
description: >
  Patch Claude Code binary to enable the /chrome slash command on WSL2.
  Use this skill when: (1) the user reports /chrome says "not supported in WSL",
  (2) Chrome browser tools fail to connect on WSL, (3) after a Claude Code update
  to verify the WSL Chrome patch is still applied, (4) the user mentions Claude Code
  update and uses Chrome/browser features on WSL. Proactively check patch status
  when Chrome or WSL issues arise.
---

# WSL Chrome Patch

## Background

Claude Code's `/chrome` command hard-blocks on WSL by checking `fs.existsSync("/proc/sys/fs/binfmt_misc/WSLInterop")` via the `isWslEnvironment()` function. This is a separate check from the main platform detector `sA()` which reads `/proc/version` — patching does NOT affect platform detection, native messaging paths, or `case"linux":case"wsl":` fallthrough logic.

The env var `CLAUDE_CODE_ENABLE_CFC=1` (set in `~/.bashrc`) enables Chrome MCP tools but does NOT bypass the `/chrome` UI gate.

## Patch method

Replace all occurrences of `/proc/sys/fs/binfmt_misc/WSLInterop` with `/proc/sys/fs/binfmt_misc/PATCHED_OK` (identical byte length) in the compiled binary. This makes `isWslEnvironment()` return `false`.

## Usage

Run `scripts/patch_wsl_chrome.sh` via Bash:

```bash
# Check current status
bash ${CLAUDE_PLUGIN_ROOT}/scripts/patch_wsl_chrome.sh check

# Apply patch
bash ${CLAUDE_PLUGIN_ROOT}/scripts/patch_wsl_chrome.sh patch

# Restore original binary
bash ${CLAUDE_PLUGIN_ROOT}/scripts/patch_wsl_chrome.sh restore
```

## After a Claude Code update

1. Run `check` — if status is UNPATCHED, run `patch`.
2. If status is UNKNOWN (no WSLInterop string found), Anthropic may have changed the detection method or added official WSL support. Investigate before patching.
3. Tell the user to restart Claude Code after patching.

## Companion hook

`hooks/hookify.wsl-chrome-check.local.md` — a hookify rule that triggers on `/chrome` and reminds Claude to run the patch check. Copy to your project's `.claude/` directory:

```bash
cp hooks/hookify.wsl-chrome-check.local.md /path/to/project/.claude/
```

## Prerequisites

`export CLAUDE_CODE_ENABLE_CFC=1` must be in `~/.bashrc`.
