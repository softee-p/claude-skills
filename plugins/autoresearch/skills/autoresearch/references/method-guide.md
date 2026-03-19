# Autoresearch Method Guide

## Origin

This method is adapted from Andrej Karpathy's **autoresearch** concept: instead
of manually improving something, an AI agent does it in a loop. Try a small
change, measure if the result improved, keep it if so, revert if not. Repeat.

## Core Principle: Hill Climbing with Guard Rails

The method is essentially **stochastic hill climbing** applied to prompt
engineering:

- The "position" is the current skill prompt.
- The "fitness function" is the checklist pass rate.
- Each "step" is a single targeted change.
- The "guard rail" is automatic revert on regression.

This avoids the trap of rewriting everything from scratch (which usually makes
things worse) and instead makes small, measurable, reversible improvements.

## Checklist Design Best Practices

The checklist is the most important input. Bad checklists lead to bad
improvements.

### Good Checklist Questions

- **Specific**: "Does the headline include a specific number?" not "Is the
  headline good?"
- **Observable**: Can be answered by looking at the output alone, no external
  context needed.
- **Binary**: Clear yes or no. No "sort of" or "partially."
- **Independent**: Each question tests one distinct thing.
- **Balanced**: Cover different aspects of quality (content, style, structure,
  constraints).

### Common Pitfalls

- **Too many questions** (>6): The skill starts gaming the checklist, producing
  formulaic outputs that technically pass but feel mechanical.
- **Too few questions** (<3): Not enough signal to guide improvements.
- **Vague questions**: "Is the output high quality?" — this means something
  different every time you evaluate it.
- **Overlapping questions**: Two questions that test the same thing inflate that
  aspect's weight.
- **Threshold questions only**: All questions about minimum bars ("at least X")
  with none about maximum caps can lead to bloated outputs.

### Suggested Question Templates

- "Does the output include [specific element]?"
- "Is the output free of [specific anti-pattern]?"
- "Does [specific section] contain [specific quality]?"
- "Is [measurable property] within [specific range]?"
- "Does the [first/last] [sentence/paragraph] do [specific thing]?"

## Change Strategy

### What Makes a Good Change

- **Addresses the #1 failure mode**: Always fix the most common problem first.
- **Is concrete**: "Add rule: headline must include a number" not "make
  headlines better."
- **Is minimal**: One rule, one example, one constraint per round.
- **Is testable**: You can tell from the output whether the change worked.

### Types of Changes (Ordered by Effectiveness)

1. **Add a specific rule**: "The headline MUST include a specific number or
   metric. Never use vague promises."
2. **Add a banned list**: "NEVER use these words: revolutionary, cutting-edge,
   synergy, leverage, unlock, transform, game-changing."
3. **Add a worked example**: Show exactly what good output looks like for a
   specific part.
4. **Tighten a constraint**: "Keep total copy under 120 words" (was 150).
5. **Loosen a constraint**: "Allow up to 180 words" (if quality suffered from
   being too tight).
6. **Reorder instructions**: Put the most-violated rule earlier / more
   prominently.

### Common Traps

- **Over-constraining**: Adding too many rules makes output formulaic. If
  outputs start sounding identical, too many constraints have been added.
- **Conflicting rules**: A tight word count + requirement for detailed examples
  can fight each other. Watch for changes that help one metric but hurt another.
- **Rule stacking**: If you have more than 3-4 added rules after several
  rounds, consider consolidating rather than adding more.

## Stopping Conditions

Three valid reasons to stop:

1. **Target reached**: Score ≥ target for 3 consecutive rounds. The skill is
   reliably good.
2. **Plateau**: 3 consecutive reverts with no improvement. The skill has hit
   its ceiling with the current checklist (might need checklist revision, not
   more prompt changes).
3. **Max rounds**: Safety limit to prevent infinite loops. Default 10 rounds.

## Interpreting Results

- **56% → 92%**: Excellent. Major reliability improvement.
- **80% → 88%**: Good. Meaningful but the skill was already decent.
- **70% → 72%**: Minimal. Either the checklist isn't capturing real issues, or
  the skill's problems are fundamental (not fixable with prompt tweaks).
- **Score drops after early gains**: Sign of over-optimization. The last few
  changes may be hurting. Consider reverting to the peak version.
