---
name: update-rwsdk-docs
description: >
  This skill should be used when the user asks to "update the docs", "refresh rwsdk docs",
  "sync RedwoodSDK documentation", "pull latest docs", "update the rwsdk plugin", or when the
  rwsdk-docs references appear stale or outdated. Trigger when the user mentions that
  documentation seems wrong, out of date, or when they want to ensure they have the latest
  RedwoodSDK API changes. Fetches the latest official documentation from the redwoodjs/sdk
  GitHub repository, cross-checks it against the published rwsdk release notes to catch places
  where the docs lag the library, and rebuilds the rwsdk-docs skill index, changelog, and
  doc-accuracy report. Run this periodically or after major RedwoodSDK releases.
---

# Update rwsdk-docs

Refresh the `skills/rwsdk-docs/` skill from `https://github.com/redwoodjs/sdk`.

## The one thing to understand before starting

**The RedwoodSDK docs site lags the published `rwsdk` package, sometimes by several minor
versions.** A sync that only mirrors `docs/src/content/docs` will therefore produce a skill
that is quietly wrong. This has happened concretely:

- 1.0.4 → 1.2.13 (5 releases): only 2 doc files changed.
- 1.2.13 → 1.7.3 (4 minor releases, ~2.5 months): only 1 new documented feature, while the
  library shipped a **default-behavior change** to navigation error recovery, three new
  opt-in APIs, and a Vite 8 migration that **invalidated the config printed in a shipped
  reference file**.

So the sync has two independent sources of truth, and both must be consulted:

| Source | Answers | Lands in |
|---|---|---|
| `docs/src/content/docs` (git diff) | What changed in the **documentation** | `references/`, `SKILL.md`, `CHANGELOG.md` |
| GitHub releases + PR bodies | What changed in the **library** | `DOC-ACCURACY.md` |

**Never skip the second one.** Steps 3 and 6 are the whole reason this skill exists in its
current form.

## Non-negotiable output rule

Consumers of this plugin are agents that installed it. They have **no access to this repo,
its git history, or any diff.** They see only the shipped files: `SKILL.md`, `CHANGELOG.md`,
`DOC-ACCURACY.md`, `references/*`. And `references/` only ever shows the *current* docs.

Therefore every entry you write in `CHANGELOG.md` and `DOC-ACCURACY.md` must be **fully
self-contained**: inline the actual `Before`/`After` code, name the release it landed in, and
give a concrete "Files to check" line. Never write "see file X" or "as shown in the diff" —
embed the pattern itself.

---

## Workflow

### Step 1: Confirm a clean starting point

```bash
git status --short
```

The sync replaces `references/` wholesale. **Git is the diff source** — the committed state
is the only record of what the docs said before. Commit or stash anything pending under
`plugins/rwsdk-toolkit/` before continuing.

### Step 2: Run the sync script

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/update-rwsdk-docs/scripts/update-rwsdk-docs.sh <repo-root>
```

`<repo-root>` is the directory containing `plugins/`. It can be omitted when the working
directory is inside the repo — the script walks up to find it.

The script clones before it deletes, so a failed fetch leaves the existing references
intact. It prints the **previous** `sync-meta.json` before overwriting it: note the old
`rwsdk_latest_release` and `docs_commit` — that pair defines the range you are reporting on.
Afterwards it writes a fresh `skills/rwsdk-docs/sync-meta.json`.

### Step 3: Establish the version range

From the previous `sync-meta.json` (printed in step 2) and the new one, you now have:

- **docs range** — old `docs_commit` → new `docs_commit`
- **library range** — old `rwsdk_latest_release` → new `rwsdk_latest_release`

List the library releases in that range:

```bash
gh api 'repos/redwoodjs/sdk/releases?per_page=100' \
  --jq '.[] | select(.tag_name | test("test|canary") | not) | "\(.tag_name)\t\(.published_at[0:10])"'
```

Then read the bodies of the releases inside the range:

```bash
gh api 'repos/redwoodjs/sdk/releases?per_page=100' \
  --jq '.[] | select(.tag_name | test("test|canary") | not) | "\n### \(.tag_name) (\(.published_at[0:10]))\n\(.body)"'
```

If `sync-meta.json` did not exist (first run under this workflow), fall back to the version
stated in the newest `CHANGELOG.md` entry.

### Step 4: Diff the documentation

```bash
git add -A plugins/rwsdk-toolkit/skills/rwsdk-docs/references
git diff --cached --stat -M -- plugins/rwsdk-toolkit/skills/rwsdk-docs/references   # file-level
git diff --cached -- plugins/rwsdk-toolkit/skills/rwsdk-docs/references             # content
```

Ignore pure noise: MDX import-list churn, prose rewording, link reshuffles. You are looking
for changed **APIs, options, defaults, file renames, and required call patterns**.

For each real change, find the release that caused it (step 3) so the changelog can name it.
A change presented upstream as a doc "clarification" is often a library behavior change —
check the PR before describing it as cosmetic.

### Step 5: Rebuild the `rwsdk-docs` index

Update `${CLAUDE_PLUGIN_ROOT}/skills/rwsdk-docs/SKILL.md`:

1. Add or remove index rows so **every** file in `references/` has exactly one row, and no
   row points at a missing file.
2. Update the Topics cell for each changed file with the new API names — this cell is what
   an agent greps to decide which file to open, so new API names must appear here.
3. Add Topic Quick-Lookup lines for new user-facing features, phrased as the **symptom or
   question** a user would bring ("blank page after deploy"), not the internal name.
4. Mark rows with ⚠ where DOC-ACCURACY.md contradicts or supplements that file, and keep the
   "Docs mirror synced …" line at the top current.
5. Preserve the existing structure: frontmatter, intro, "How to Use This Skill", the section
   groupings, and the `${CLAUDE_PLUGIN_ROOT}/skills/rwsdk-docs/...` path prefix on every link.

### Step 6: Rewrite `DOC-ACCURACY.md`

This is the step a docs-only sync misses. Working from the release notes in step 3, and the
PR bodies behind them:

```bash
gh api repos/redwoodjs/sdk/pulls/<number> --jq '.title, .body'
```

Rebuild `${CLAUDE_PLUGIN_ROOT}/skills/rwsdk-docs/DOC-ACCURACY.md` from scratch each sync, so
it always describes the *current* pair of versions. It has exactly two kinds of entry:

1. **Corrections** — a shipped `references/` file whose instructions are wrong for the
   current release. Mark it **superseded**, give the `Before` (as printed in the doc) and the
   `After`, and say how to tell which path applies. These matter most: an agent that trusts
   the stale file writes broken code.
2. **Undocumented released APIs** — user-facing behavior in the published package with no
   documentation. Note whether it is opt-in or a changed default, and give a working example.

Then check the published package for facts the docs never state:

```bash
gh api repos/redwoodjs/sdk/contents/sdk/package.json --jq '.content' | base64 -d \
  | python3 -c "import json,sys; p=json.load(sys.stdin); print(p['version']); print(json.dumps(p.get('peerDependencies',{}),indent=1)); print('\n'.join(sorted(p.get('exports',{}))))"
```

Peer-dependency ranges (Vite, React, wrangler) and the export map are the usual sources of
"the doc says Vite 6+ but the plugin it tells you to install no longer works that way".

**Deliberately out of scope:** internal refactors, dependency bumps, CI changes, and
build-pipeline fixes. Only include what changes the code a developer writes.

### Step 7: Add the `CHANGELOG.md` entry

Prepend a dated, newest-first entry to
`${CLAUDE_PLUGIN_ROOT}/skills/rwsdk-docs/CHANGELOG.md`:

```markdown
## YYYY-MM-DD — Docs sync: <short summary of the documented changes>

Synced all N reference files from the official RedwoodSDK repo. Docs are current as of
**rwsdk X.Y.Z** (released YYYY-MM-DD). The previous sync reflected **rwsdk A.B.C**; since
then the library released … , with <no / the following> `BREAKING CHANGE` declared in any
upstream release note in that range.

### <Area>: <what changed>

<one paragraph, naming the release the change landed in>

**Before:**
```tsx
…
```

**After:**
```tsx
…
```

**Action:** additive | required migration | …
**Files to check:** <concrete paths and what to grep for>
```

Scope rules:

- **This changelog covers documentation changes only.** Library changes that are not yet
  documented belong in `DOC-ACCURACY.md`, not here.
- When the two diverge notably, add one short pointer line to DOC-ACCURACY.md in the entry.
- If the docs did not change at all, still add an entry recording the range and stating
  that — a silent gap looks like a missed sync to the next person.

### Step 8: Bump the version

Bump **both** files — they drift apart easily and a mismatch breaks install/uninstall:

- `plugins/rwsdk-toolkit/.claude-plugin/plugin.json` → `version`
- `.claude-plugin/marketplace.json` → the `rwsdk-toolkit` entry's `version`

Minor bump for new documented APIs or new DOC-ACCURACY corrections; patch for a no-op sync.

### Step 9: Verify

```bash
# every reference file has an index row, and every row points at a real file
cd plugins/rwsdk-toolkit/skills/rwsdk-docs
find references -type f \( -name '*.mdx' -o -name '*.md' \) | sed 's|^|references/|' | sort > /tmp/have.txt
grep -o 'references/[a-z0-9/-]*\.mdx' SKILL.md | sort -u > /tmp/indexed.txt
diff /tmp/have.txt /tmp/indexed.txt
```

Then confirm by reading:

- Every `⚠` in SKILL.md corresponds to a real DOC-ACCURACY.md section.
- Every code block in CHANGELOG.md and DOC-ACCURACY.md is complete enough to apply **without
  opening any other file** — the non-negotiable output rule above.
- Both version numbers match.
