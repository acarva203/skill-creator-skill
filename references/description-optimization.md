# Trigger optimization: writing & tuning the description

The `description` is always in context and is what Claude uses to decide whether to invoke
the skill. Getting it right is the single highest-leverage tuning you can do.

## What a good description contains

- **What** the skill does — the capability, concretely.
- **When** to use it — situations, user phrasings, file types, task shapes. Be specific:
  name the trigger phrases a real user would type.

Example (good):

> Creates, tests, and packages Claude skills. Use when the user wants to build a new skill,
> author a SKILL.md, fix a skill that won't trigger, or package a skill into a .skill file.
> Trigger on "create a skill", "make a skill", "my skill isn't triggering".

Example (weak — vague on *when*):

> A helpful skill for working with skills.

## Be a bit "pushy"

Claude tends to **under-trigger** skills — it errs toward not invoking them. Counteract this
by leaning slightly aggressive on trigger conditions: enumerate phrasings and situations
generously. But never claim a capability the skill lacks — that causes **over-triggering**
and violates the principle of least surprise. Push on *coverage of real cases*, not on
inflated scope.

## The optimization loop

1. **Assemble two prompt sets**:
   - **Positives** — prompts that *should* trigger the skill (cover the real range of
     phrasings and situations).
   - **Negatives** — nearby prompts that should *not* trigger it.
2. **Measure**: run each prompt and record whether the skill triggered.
   - **Under-triggering** = positives that failed to trigger (false negatives).
   - **Over-triggering** = negatives that triggered anyway (false positives).
3. **Diagnose**:
   - Under-triggering → the description is too narrow or vague; add the missing phrasings /
     situations.
   - Over-triggering → the description is too broad or overclaims; tighten scope, remove
     language that matches the negatives.
4. **Edit the description** and re-run. Change one thing at a time so you know what moved the
   numbers.
5. **Repeat** until both error rates are acceptably low.

## Tips

- Front-load the most distinctive trigger terms.
- Mirror the words real users actually type.
- If positives and negatives both contain a term, that term can't disambiguate — find what
  truly separates them and lead with that.
- Re-run the loop whenever you change the skill's scope.
