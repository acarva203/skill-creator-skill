# SKILL.md structure & progressive disclosure

## Frontmatter

Every `SKILL.md` opens with a YAML frontmatter block. Two fields are **required**:

```yaml
---
name: my-skill
description: What the skill does AND when to use it. Doubles as the trigger.
---
```

- **`name`** — the skill identifier. Use lowercase kebab-case (`pdf-form-filler`, not
  `PDF Form Filler`). It should match the directory name. Keep it short and descriptive.
- **`description`** — the single most important field. It is **always in context** and is
  what Claude uses to decide whether to invoke the skill. It must state both **what** the
  skill does and **when** to use it. See `description-optimization.md`.

Keep the combined `name` + `description` to roughly **100 words** — it's paid for on every
request whether the skill triggers or not.

## The three levels of progressive disclosure

| Level | What loads | When | Budget |
|-------|-----------|------|--------|
| 1 | `name` + `description` | Always | ~100 words |
| 2 | `SKILL.md` body | When the skill triggers | < 500 lines ideally |
| 3 | `scripts/`, `references/`, `assets/` | Only when the task needs them | unbounded, lazy |

The goal: Claude pays minimal context cost until it actually needs the detail. Don't inline
into the body what could live in a reference file that's only read when relevant.

## Directory layout

```
skill-name/
├── SKILL.md          ← required
├── scripts/          ← executable code for repetitive/deterministic tasks
├── references/       ← documentation loaded into context as needed
└── assets/           ← templates, icons, fonts, and other output materials
```

- **`scripts/`** — code Claude *runs* rather than reasons through. Good for deterministic,
  repetitive, or error-prone steps (parsing, validation, packaging). Reduces tokens and
  mistakes.
- **`references/`** — documentation Claude *reads* when it needs depth. Each file should
  cover one topic and be pointed to from `SKILL.md` with a one-line "read this when…".
- **`assets/`** — files used in the skill's *output*: templates, boilerplate, icons, fonts,
  CSS. Not meant to be read as instructions.

## Keeping the body under 500 lines

500 lines is a soft ceiling, not a hard limit — but past it, comprehension and triggering
degrade. When you approach it:

1. Identify sections that are only relevant in specific sub-cases.
2. Move each into a `references/<topic>.md` file.
3. Replace it in `SKILL.md` with a one-line pointer: *"For <case>, read
   `references/<topic>.md`."*

This adds a layer of hierarchy and keeps the always-on-trigger body lean. Clear pointers are
essential — Claude only reads a reference file if `SKILL.md` tells it when to.

## Body content checklist

A good `SKILL.md` body typically includes:

- A one-line restatement of what the skill does.
- Any guiding principles or constraints.
- The step-by-step workflow Claude should follow.
- Concrete examples (input → output) where format matters.
- Pointers to bundled resources with "read when…" conditions.
- Edge cases and how to handle them.
