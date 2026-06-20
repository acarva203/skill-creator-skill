---
name: skill-creator
description: Creates, tests, evaluates, and packages Claude skills (SKILL.md-based capabilities). Use this skill whenever the user wants to build a new skill, author or scaffold a SKILL.md, improve an existing skill, fix a skill that won't trigger reliably, evaluate or benchmark a skill, or package a skill into an installable .skill file. Trigger on phrases like "create a skill", "make a skill", "write a SKILL.md", "my skill isn't triggering", "package this skill", or "turn this workflow into a skill".
---

# Skill Creator

This skill guides you through building a high-quality Claude skill end-to-end: capturing
intent, interviewing the user, drafting the `SKILL.md`, testing, evaluating, iterating,
optimizing the trigger description, and packaging a `.skill` file.

## Core design principle: principle of least surprise

Every decision should make the skill's behavior **predictable and faithful to its
description**. If the description promises behavior X, the skill must do X — no more, no
less. When in doubt, choose the behavior a user would reasonably expect from reading the
`name` and `description` alone. Surprising side effects, silent scope creep, and
under/over-triggering are the failures this skill exists to prevent.

## First: adapt to the user's technical level

Before anything else, gauge who you're talking to and **adjust your language accordingly**:

- **Non-technical users**: avoid or explain jargon. Terms like "JSON", "YAML
  frontmatter", "assertions", "subagents", and "benchmark" need a plain-English gloss the
  first time you use them. Offer to handle technical packaging steps for them.
- **Developers**: use precise terms directly; don't over-explain.

If you can't tell, ask one calibrating question or start plain and ratchet up. Re-check as
the conversation reveals their comfort level. This adaptation applies to **every** step
below.

## What a skill is (quick model)

A skill is a directory whose entry point is `SKILL.md`. It uses **progressive disclosure** —
a three-level loading system so Claude only pays the context cost of what it needs:

1. **Always loaded (~100 words)**: the `name` + `description` from frontmatter. This is the
   triggering layer.
2. **Loaded on trigger**: the `SKILL.md` body. Keep it focused — ideally **under 500 lines**.
3. **Loaded as needed**: bundled files under `scripts/`, `references/`, `assets/`, pulled in
   only when the task calls for them.

```
skill-name/
├── SKILL.md          ← required: frontmatter + body
├── scripts/          ← executable code for repetitive/deterministic tasks
├── references/       ← docs loaded into context as needed
└── assets/           ← templates, icons, fonts used in the skill's output
```

If `SKILL.md` approaches 500 lines, **add a layer of hierarchy** instead of growing it: move
detail into `references/` and leave a one-line pointer ("For X, read `references/x.md`").

For the full anatomy of frontmatter and progressive disclosure, read
`references/skill-md-structure.md`.

## The workflow

Follow these steps in order. Don't skip ahead — each step de-risks the next. For the
detailed playbook of each step, read `references/workflow.md`.

1. **Capture intent** — What should the skill do? When should it trigger? What's the
   expected output format? Get a one-paragraph answer before designing.
2. **Interview & research (grill for detail)** — Relentlessly probe edge cases,
   input/output formats, success criteria, and dependencies until there is *nothing left to
   assume*. Look at any examples the user has. See "Grill for extreme detail" below.
3. **Write the draft** — Scaffold the directory and fill in `SKILL.md` from the interview.
   Start from `assets/SKILL_template.md`. Run `scripts/init_skill.py` to create the
   structure.
4. **Test** — Run Claude-with-the-skill against representative test prompts. See
   `references/testing-and-evaluation.md`.
5. **Evaluate** — Both **qualitatively** (human review of outputs) and **quantitatively**
   (benchmark assertions that pass/fail automatically). See
   `references/testing-and-evaluation.md`.
6. **Iterate** — Refine based on what testing and evaluation surface. Repeat 4–6 as a
   measured loop until the skill meets its success criteria. See "The iterative
   improvement loop" below.
7. **Optimize the description** — Run the trigger-optimization loop to maximize triggering
   accuracy (minimize both under- and over-triggering). See
   `references/description-optimization.md`.
8. **Package** — Produce an installable `.skill` file with `scripts/package_skill.py`.

You don't always run all eight in one sitting. If the user only wants a draft, stop after
step 3 and tell them what's left. If they're fixing triggering, jump to step 7. Match the
work to the request (principle of least surprise applies to *your* behavior too).

## Grill for extreme detail

A vague interview produces a vague skill. **Do not accept hand-wavy answers.** Your job in
step 2 is to extract enough precision that the resulting `SKILL.md` can be *explicit about
exactly what it must do* — no gaps for Claude to guess into later. Be persistent and
specific; keep pushing until the user is slightly tired of how detailed you're being.

Drill on each of these until you get a concrete, unambiguous answer (not "it depends"):

- **Exact behavior** — Step by step, what must the skill do? What must it *never* do? Walk a
  full example start to finish out loud and have the user correct you.
- **Inputs** — Exact formats, required vs. optional fields, sample values, malformed-input
  handling. Ask for a real example file.
- **Outputs** — Exact format, structure, tone, length. Ask: "show me one perfect output and
  one barely-acceptable one." The gap between them defines your success criteria.
- **Edge cases** — Empty input, huge input, conflicting instructions, missing dependencies,
  ambiguous requests. For each: what's the correct behavior?
- **Decision points** — Wherever the skill could reasonably do A or B, pin down which one and
  *why*. Ambiguity here is what makes a skill unpredictable (violating least surprise).
- **Success criteria** — "How would you, or a test, *prove* an output is correct?" Push for
  checkable statements — these become your evaluation assertions in step 5.
- **Triggering boundaries** — When should it fire? When should it explicitly NOT fire, even
  though it's close? Collect both for step 7.

Reflect the answers back as a written spec and get explicit confirmation before drafting. If
a question reveals the user hasn't decided, make them decide now — don't defer it into the
draft. The deeper batteries of questions live in `references/grilling-and-iteration.md`.

**Make the skill explicit.** Carry that precision into `SKILL.md`: state plainly what the
skill must do, must not do, and how to handle each named edge case. Prefer imperative,
unambiguous instructions ("Always produce X; if Y is missing, do Z") over soft guidance
("try to handle Y"). If the draft can't be explicit about something, that's a signal to go
back and grill the user further — not to paper over it with vague wording.

## The iterative improvement loop

A skill is rarely right on the first draft. Treat steps 4–6 as a **measured loop**, not a
one-shot pass:

1. **Run** the current skill against the full test set (step 4).
2. **Score** it — qualitative review *and* quantitative assertions (step 5). Record the
   pass rate and note every failure with its cause.
3. **Diagnose** each failure: missing instruction, ambiguous wording, uncovered edge case,
   bloated body, wrong scope, or a triggering miss.
4. **Change one thing at a time** so you can attribute any score movement to a specific edit.
5. **Re-run and compare** to the previous score. Keep changes that help; revert ones that
   regress.
6. **Repeat** until the score plateaus at the success criteria *and* the outputs read well
   to a human. If you're stuck, the gap is usually an under-specified requirement — go back
   and **grill the user again** (the loop feeds back into step 2).

Keep a short running log of iteration → change → score so progress is visible and reversible.
Details and a worked example are in `references/grilling-and-iteration.md`.

## Writing the description (the most important field)

The `description` is both documentation **and** the trigger mechanism. It must specify:

- **What** the skill does, and
- **When** to use it (concrete situations, user phrasings, file types, task shapes).

Lean slightly **"pushy"** — Claude tends to *under*-trigger skills, so err toward including
trigger conditions rather than omitting them. But don't claim capabilities the skill lacks
(that violates least surprise and causes over-triggering). Full guidance and the
optimization loop are in `references/description-optimization.md`.

## Environment-specific adaptations

Where the skill (and your testing of it) runs changes what's available. **Detect the
environment and adapt** — read `references/environments.md` for details. Summary:

| Environment  | Subagents | Browser | Notes                                              |
|--------------|-----------|---------|----------------------------------------------------|
| Claude.ai    | No        | No      | Run test cases **in series**, not parallel.        |
| Claude Code  | Yes       | Yes     | Full subagent support; browser-based eval viewer.  |
| Cowork       | Yes       | No      | Use the `--static` flag for the HTML eval viewer.  |

## Bundled resources

- `references/skill-md-structure.md` — frontmatter fields, progressive disclosure, directory layout.
- `references/workflow.md` — detailed playbook for each of the 8 steps.
- `references/grilling-and-iteration.md` — the question battery for grilling out requirements and the measured iterative improvement loop.
- `references/testing-and-evaluation.md` — testing, qualitative + quantitative evaluation, assertions.
- `references/description-optimization.md` — the trigger-optimization loop.
- `references/environments.md` — Claude.ai / Claude Code / Cowork differences.
- `assets/SKILL_template.md` — starting template for a new `SKILL.md`.
- `scripts/init_skill.py` — scaffold a new skill directory.
- `scripts/package_skill.py` — validate and package a skill into a `.skill` file.
