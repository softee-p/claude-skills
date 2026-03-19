# Output Templates

Templates for the artifacts produced by an autoresearch run. Save each file
in the target skill's directory.

## Results Log (`autoresearch-results.md`)

```markdown
# Autoresearch Results: [Skill Name]

## Configuration
- **Test inputs**: [list]
- **Checklist**: [list of yes/no questions]
- **Samples per round**: N
- **Max rounds**: N
- **Target score**: N%

## Summary
- **Starting score**: X%
- **Final score**: Y%
- **Rounds completed**: N
- **Changes kept**: N
- **Changes reverted**: N
- **Stop reason**: [target reached / max rounds / plateau]

## Round-by-Round Results

### Round 0 (Baseline)
- **Score**: X%
- **Breakdown**:
  - Q1 "...": X/N passed
  - Q2 "...": X/N passed
  - ...

### Round 1
- **Proposed change**: [description of what was changed]
- **Rationale**: [which failure this change addressed and why]
- **Score before**: X% → **Score after**: Y%
- **Decision**: KEPT / REVERTED
- **Breakdown**:
  - Q1 "...": X/N passed (was X/N)
  - Q2 "...": X/N passed (was X/N)
  - ...

[...repeat for each round...]
```

## Changelog (`autoresearch-changelog.md`)

```markdown
# Autoresearch Changelog: [Skill Name]

## Changes Kept

### Change 1 (Round N): [short description]
- **What**: [exact text added/modified/removed in the skill prompt]
- **Why**: [which checklist question(s) it addressed]
- **Impact**: Score X% → Y%

### Change 2 (Round N): [short description]
- **What**: [exact text added/modified/removed]
- **Why**: [which checklist question(s) it addressed]
- **Impact**: Score X% → Y%

## Changes Reverted

### Reverted 1 (Round N): [short description]
- **What**: [exact text that was tried]
- **Why it was tried**: [which failure it targeted]
- **Why it was reverted**: [score did not improve / hurt other questions]

### Reverted 2 (Round N): [short description]
- **What**: [exact text that was tried]
- **Why it was tried**: [which failure it targeted]
- **Why it was reverted**: [reason for revert]
```

## Improved Skill (`SKILL.improved.md`)

Format identically to the original `SKILL.md` — same YAML frontmatter structure,
same markdown conventions — but with all kept changes applied. Append a comment
at the end noting the autoresearch run:

```markdown
<!-- Autoresearch: improved from X% to Y% in N rounds. See autoresearch-changelog.md for details. -->
```

## Backup (`SKILL.backup.md`)

Exact copy of the original `SKILL.md` before any modifications. No changes.
