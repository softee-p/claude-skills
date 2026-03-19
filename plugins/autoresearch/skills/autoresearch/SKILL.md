---
name: autoresearch
description: >
  This skill should be used when the user asks to "run autoresearch",
  "auto-improve a skill", "optimize my skill", "test and improve a skill",
  "iterate on a skill", "improve skill reliability", or mentions autoresearch,
  skill optimization, or iterative prompt improvement. Implements Andrej
  Karpathy's autoresearch method for autonomous skill improvement via
  iterative testing with a yes/no scoring checklist.
version: 0.1.0
---

# Autoresearch: Iterative Skill Improvement

This skill enables autonomous improvement of any Claude skill through iterative
testing. It applies stochastic hill climbing to prompt engineering: test a skill,
score the output, make one small change, test again, keep or revert.

## Core Loop

1. **Baseline** — Run the target skill N times, score each output, establish a starting pass rate.
2. **Analyze** — Identify which checklist items fail most often.
3. **Hypothesize** — Propose ONE small, targeted change to the skill prompt addressing the most common failure.
4. **Test** — Run the skill N times with the change applied, score all outputs.
5. **Decide** — Keep the change if the score improved; revert if it didn't.
6. **Repeat** — Return to step 2 with the current best version.
7. **Stop** — When score hits target 3× in a row, max rounds reached, or 3 consecutive reverts (plateau).

## Setup Phase

### Step 1: Locate the Target Skill

Find the target skill's `SKILL.md` file in the codebase. Read and understand its
full prompt — this is the "recipe" to improve.

### Step 2: Gather Configuration

Collect three inputs from the user (offer smart defaults and help for each):

**Test inputs** — What inputs to test the skill with.
- Suggest 2–3 diverse inputs covering different use cases
- More diverse inputs produce more robust improvements

**Scoring checklist** — 3–6 yes/no questions defining "good output."
- Help turn intuitions into specific, binary questions
- Offer to review the skill's prompt and suggest checklist items
- Consult `references/method-guide.md` for checklist design best practices

**Run parameters** (with defaults):
- `samples_per_round`: Runs per test round (default: 5)
- `max_rounds`: Maximum improvement rounds (default: 10)
- `target_score`: Stop threshold hit 3× in a row (default: 95%)

### Step 3: Confirm and Start

Summarize configuration back to the user. Begin only after confirmation.

## Improvement Loop

### Baseline (Round 0)

1. Run the skill `samples_per_round` times per test input.
2. Score each output against every checklist question (Yes=1, No=0).
3. Calculate overall pass rate: `(total Yes) / (total questions × total samples) × 100%`.
4. Report baseline score and per-question breakdown.

### Each Improvement Round

1. **Analyze failures** — Determine which checklist questions fail most. Review failing outputs to understand root causes.

2. **Propose one change** — Design a single, targeted modification:
   - Add a specific rule for the most common failure pattern
   - Add a banned-items list (words, patterns, structures to avoid)
   - Add a worked example showing what good output looks like
   - Tighten or loosen a constraint
   - Reorder existing instructions for clarity

   Each change must be specific, minimal, and targeted. Consult
   `references/method-guide.md` for change strategy guidance.

3. **Apply and test** — Modify the skill prompt, run `samples_per_round` tests per input, score all outputs.

4. **Decide** — Keep if overall score improved and no individual question regressed significantly. Revert otherwise.

5. **Log** — Record round number, proposed change, before/after scores, per-question breakdown, and keep/revert decision.

6. **Check stopping conditions**:
   - Score ≥ `target_score` for 3 consecutive rounds → **STOP** (success)
   - `max_rounds` reached → **STOP** (limit)
   - 3 consecutive reverts → **STOP** (plateau)

## Scoring Rules

- Strict and consistent — the same output always gets the same score.
- Binary only: Yes (1) or No (0). No partial credit.
- Score what is actually in the output, not what was intended.
- Default to No when ambiguous (stricter scoring drives better improvement).
- Include brief justification per score to track patterns.

## Key Principles

- **One change at a time.** Never combine multiple changes in a single round.
- **Preserve voice and intent.** Tune the skill, do not rewrite it.
- **Detect gaming.** If outputs become formulaic, flag checklist issues to the user.
- **Never modify the original.** Always work on a copy; keep `SKILL.md` untouched.
- **Log everything.** The changelog enables future agents or smarter models to continue the work.

## Output Artifacts

On completion, produce four files in the target skill's directory:

| File | Purpose |
|------|---------|
| `SKILL.improved.md` | Improved skill prompt with all kept changes applied |
| `SKILL.backup.md` | Copy of original skill (safety net) |
| `autoresearch-results.md` | Full round-by-round scores and breakdowns |
| `autoresearch-changelog.md` | Every change tried, rationale, and outcome |

Consult `references/output-templates.md` for the exact format of each artifact.

## Reporting

After each round, output a brief status line:

```
Round N: Score X% → Y% (KEPT/REVERTED: [short description])
```

On completion, output a final summary:

```
Autoresearch complete.
  Skill: [name]
  Score: X% → Y% (+Z%)
  Rounds: N (K kept, R reverted)
  Files saved:
    - SKILL.improved.md
    - SKILL.backup.md
    - autoresearch-results.md
    - autoresearch-changelog.md
```

## Additional Resources

### Reference Files

- **`references/method-guide.md`** — Checklist design best practices, change strategy, stopping conditions, and interpreting results
- **`references/output-templates.md`** — Exact templates for results log and changelog artifacts
