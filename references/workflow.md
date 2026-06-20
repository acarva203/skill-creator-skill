# Detailed workflow playbook

The eight steps from `SKILL.md`, expanded. Adapt depth to the user's request — a quick draft
may only need steps 1–3; a triggering fix jumps to step 7.

## 1. Capture intent

Get a crisp answer to three questions before designing anything:

- **What** should the skill do? (one sentence)
- **When** should it trigger? (situations, phrasings, file types, task shapes)
- **What output** is expected? (format, structure, examples)

If the user gives a vague ask ("make a skill for my reports"), reflect back a concrete
one-paragraph summary and confirm it before proceeding. Don't start writing on a guess.

## 2. Interview & research

Probe the parts that determine quality:

- **Edge cases** — what unusual inputs or situations must the skill handle?
- **Input/output formats** — exact shapes, sample files, required fields.
- **Success criteria** — how will we know an output is correct? This becomes your
  evaluation assertions later, so capture it concretely.
- **Dependencies** — external tools, libraries, APIs, credentials, file access.
- **Existing examples** — ask for real samples of good output. They anchor the draft.

Research anything you're unsure about (formats, APIs, conventions). For non-technical users,
translate your questions into plain language ("Can you show me an example of a finished
report you'd be happy with?" rather than "what's the output schema?").

**Grill, don't accept vagueness.** Push until there is nothing left to assume, then write
the answers back as a spec and get sign-off before drafting. The full question battery is in
`grilling-and-iteration.md`.

## 3. Write the draft

1. Scaffold the directory — run `scripts/init_skill.py <skill-name> [parent-dir]`. It
   creates `SKILL.md` (from the template), `scripts/`, `references/`, `assets/`.
2. Fill in `SKILL.md` from the interview: frontmatter first (especially the description),
   then the body following the checklist in `skill-md-structure.md`.
3. Put deterministic logic in `scripts/`, deep docs in `references/`, output materials in
   `assets/`.
4. Keep the body under ~500 lines; push detail into references with clear pointers.

## 4. Test

Run Claude-with-the-skill against representative prompts — both prompts that **should**
trigger it and prompts that **should not**. See `testing-and-evaluation.md` for mechanics
and environment differences (series vs. parallel).

## 5. Evaluate

Two complementary lenses:

- **Qualitative** — a human reads the outputs. Are they correct, well-formatted, useful?
- **Quantitative** — automated **assertions** (checks that pass or fail) over each test
  case: did the output contain the required section? valid JSON? right file produced? This
  gives a repeatable score so iteration is measurable.

See `testing-and-evaluation.md` for how to write assertions and view results.

## 6. Iterate

Feed evaluation findings back into the draft as a **measured loop**: change one thing at a
time, re-run, and compare the score so each edit's effect is attributable. Keep wins, revert
regressions, and log iteration → change → score. Common fixes: clarify ambiguous
instructions, add a missing edge case, move bloat into references, add an example. If the
score stalls, the cause is usually an under-specified requirement — go back and grill the
user (step 2). Full loop and worked example in `grilling-and-iteration.md`.

## 7. Optimize the description

Once behavior is good, maximize triggering accuracy with the loop in
`description-optimization.md`: build a set of should-trigger and should-not-trigger prompts,
measure under/over-triggering, and refine the description until both are minimized.

## 8. Package

Run `scripts/package_skill.py <skill-dir>`. It validates the structure (frontmatter present,
required fields, body size) and produces an installable `.skill` file. Hand the file to the
user with install instructions appropriate to their environment.
