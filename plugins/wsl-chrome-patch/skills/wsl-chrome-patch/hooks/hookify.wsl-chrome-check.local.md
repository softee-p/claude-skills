---
name: check-wsl-chrome-patch
enabled: true
event: prompt
pattern: ^\/chrome$
action: warn
---

**WSL Chrome Patch Check Required**

Before using Chrome browser tools, run the WSL patch status check:

```
bash ~/.claude/skills/wsl-chrome-patch/scripts/patch_wsl_chrome.sh check
```

If status is UNPATCHED, run:

```
bash ~/.claude/skills/wsl-chrome-patch/scripts/patch_wsl_chrome.sh patch
```

Then tell the user to restart Claude Code.

Only run this check once per conversation — skip if already checked.
