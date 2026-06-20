# Testing & evaluation

The goal: know that the skill produces correct outputs **and** triggers at the right times,
measured repeatably rather than by vibes.

## Build a test set

Collect representative prompts in two buckets:

- **Should-trigger / should-handle** — realistic user requests the skill is meant to serve,
  spanning the edge cases captured in the interview.
- **Should-NOT-trigger** — nearby prompts the skill should stay out of. These catch
  over-triggering.

Aim for variety in phrasing, not just topic. Real users word things many ways.

## Run the tests

Run Claude-with-the-skill on each prompt and capture the output. **How you run them depends
on the environment** (see `environments.md`):

- **Claude.ai** — no subagents; run test cases **in series**, one at a time.
- **Claude Code** — full subagent support; you can fan out test cases in parallel via
  subagents, and use the browser-based eval viewer.
- **Cowork** — subagents yes, browser no; pass `--static` to the eval viewer to get a
  self-contained HTML file.

## Evaluate qualitatively

A human (or you, on the user's behalf) reads each output and judges:

- Is it correct and complete?
- Is the format right?
- Would the user be satisfied?
- Did it surprise — do something the description didn't promise?

Qualitative review catches subtle quality issues assertions miss.

## Evaluate quantitatively (assertions)

An **assertion** is a check that passes or fails automatically — it turns "is this good?"
into a yes/no the computer can score. For each test case, write assertions over the output,
e.g.:

- Output contains a `## Summary` section.
- Output is valid JSON and has the keys `title`, `date`, `items`.
- The expected file (`report.pdf`) was produced.
- The skill triggered (for should-trigger prompts) / did not (for should-not).

Tally pass/fail across the whole test set to get a score. Re-running after each iteration
shows whether a change helped or regressed.

> For non-technical users: explain that assertions are just "automatic checks — like a
> checklist the computer runs for us so we don't have to eyeball every result." Offer to
> write them yourself.

## Use both

Quantitative scores make iteration measurable; qualitative review catches what assertions
can't encode. A skill is ready when it passes its assertions **and** reads well to a human.
