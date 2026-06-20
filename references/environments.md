# Environment-specific adaptations

Where the skill runs — and where *you* test and evaluate it — changes which capabilities are
available. Detect the environment first, then adapt. The principle of least surprise applies:
a skill should behave predictably in whatever environment hosts it.

## Capability matrix

| Environment  | Subagents | Browser | Eval viewer            |
|--------------|-----------|---------|------------------------|
| Claude.ai    | No        | No      | Not browser-based      |
| Claude Code  | Yes       | Yes     | Browser-based viewer   |
| Cowork       | Yes       | No      | HTML viewer, `--static`|

## Claude.ai

- **No subagents.** You can't fan out work to parallel agents.
- **No browser.** Don't rely on browser-driven steps or a browser-based eval viewer.
- **Run test cases in series** — one prompt at a time, collecting results sequentially.
- Keep workflows linear and self-contained.

## Claude Code

- **Full subagent support.** You can parallelize test cases across subagents to speed up
  evaluation.
- **Browser available.** Use the browser-based eval viewer to inspect results.
- Scripts can run locally with full filesystem and shell access.

## Cowork

- **Subagents: yes.** Parallel test execution is available.
- **Browser: no.** The eval viewer can't open in a browser, so **generate a static HTML
  file** instead: pass the `--static` flag to the eval viewer. The user opens the file
  themselves.

## How to detect & adapt

Infer the environment from available tooling and context. When unsure, ask the user, or
choose the most conservative path (assume no subagents, no browser) so behavior stays
predictable. Tell the user which environment you detected and what that implies for testing
(e.g., "Since we're on Claude.ai, I'll run the test cases one at a time").
