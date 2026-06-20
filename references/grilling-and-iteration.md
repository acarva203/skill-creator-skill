# Grilling for detail & the iterative improvement loop

Two disciplines that separate a mediocre skill from a reliable one: (1) interviewing the
user until the requirements are airtight, and (2) improving the skill through a measured
loop rather than a single draft. Both exist to make the final skill **explicit about exactly
what it must do** — the principle of least surprise depends on it.

## Why grill?

Every requirement you fail to extract becomes a gap the skill fills by guessing. Guesses are
unpredictable, and unpredictable skills surprise users. The cost of an extra question now is
far lower than the cost of a wrong output later. Be persistent — politely refuse to move on
from a vague answer.

## The grilling battery

Walk these in order. For each, the goal is a concrete, checkable answer — not "it depends."

### 1. Exact behavior
- Narrate a complete run start-to-finish; have the user correct each step.
- "What must this skill *never* do?" (Negative scope is as important as positive.)
- "Where could it reasonably do A or B? Which one, and why?" Pin every fork.

### 2. Inputs
- Exact format(s). Required vs. optional fields. Allowed value ranges.
- "Show me a real input." Get an actual sample, not a description of one.
- Malformed / missing / oversized input — what's the correct response to each?

### 3. Outputs
- Exact format, structure, tone, length, file type.
- "Show me one *perfect* output and one *barely acceptable* one." The delta between them is
  your quality bar and your assertions.
- Are there outputs that look right but are wrong? How do we catch them?

### 4. Edge cases
- Empty input, huge input, conflicting instructions, missing dependency, ambiguous request,
  non-English / unexpected content. For each: the correct behavior, stated explicitly.

### 5. Success criteria
- "How would a test *prove* an output is correct?" Push until each criterion is a yes/no
  check. These become the assertions in `testing-and-evaluation.md`.

### 6. Triggering boundaries
- The phrasings and situations that should fire it.
- The near-miss situations that should NOT fire it, even though they look similar.
- Both lists feed the optimization loop in `description-optimization.md`.

### 7. Dependencies & environment
- External tools, libraries, APIs, credentials, file access.
- Which environment(s) must it run in? (See `environments.md`.)

After grilling, **write the answers back as a short spec and get explicit sign-off** before
drafting. If a question exposes an undecided point, make the user decide now — do not defer
it into the draft.

> Non-technical users: ask the same questions in plain language. "Show me a finished result
> you'd be thrilled with, and one you'd grudgingly accept" beats "define the output schema."

## Carrying precision into the skill: be explicit

Turn the spec into unambiguous instructions in `SKILL.md`:

- Use imperative, testable statements: "Always include a `## Summary`. If the date is
  missing, ask before proceeding." — not "try to summarize and handle missing dates."
- State negative scope explicitly: "Never modify files outside the target directory."
- Name each edge case and its handling.
- If you *can't* write an explicit instruction for something, that's a missing requirement —
  go back and grill, don't paper over it with soft wording.

## The iterative improvement loop

Treat testing → evaluation → refinement as a measured cycle:

1. **Run** the skill against the full test set.
2. **Score** — qualitative review + quantitative assertions. Record the pass rate.
3. **Log every failure** with its diagnosed cause (missing instruction, ambiguity,
   uncovered edge case, body bloat, wrong scope, triggering miss).
4. **Change one thing** per iteration so score movement is attributable.
5. **Re-run and compare.** Keep wins; revert regressions.
6. **Repeat** until the score plateaus at the success criteria *and* outputs read well to a
   human.

### Keep an iteration log

A tiny table makes progress visible and changes reversible:

| Iter | Change made | Score (pass/total) | Notes |
|------|-------------|--------------------|-------|
| 0 | initial draft | 6/10 | 2 fail empty-input, 2 fail format |
| 1 | added empty-input rule | 8/10 | format failures remain |
| 2 | added output example | 10/10 | qualitatively clean |

### When the loop stalls

If the score won't climb, the cause is usually an **under-specified requirement**, not a
wording tweak. Return to the grilling battery, extract the missing detail, make the skill
explicit about it, and resume the loop. The grill and the loop are connected: evaluation
surfaces the questions you should have asked.
