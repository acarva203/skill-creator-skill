#!/usr/bin/env python3
"""Scaffold a new skill directory.

Usage:
    python3 init_skill.py <skill-name> [parent-dir]

Creates:
    <parent-dir>/<skill-name>/
    ├── SKILL.md          (from the template, with name pre-filled)
    ├── scripts/
    ├── references/
    └── assets/

<skill-name> must be lowercase kebab-case (e.g. pdf-form-filler).
parent-dir defaults to the current directory.
"""
import os
import re
import sys

TEMPLATE = """---
name: {name}
description: REPLACE — state WHAT the skill does and WHEN to use it (situations, user phrasings, file types). Lean slightly pushy on trigger conditions, but never claim capabilities the skill lacks.
---

# {title}

One sentence: what this skill does.

## When to use this skill

- Bullet the concrete situations that should invoke it.

## Workflow

1. Step one.
2. Step two.

## Examples

Input:
```
REPLACE
```
Output:
```
REPLACE
```

## Bundled resources

- `references/REPLACE.md` — read when REPLACE.
"""


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    name = argv[1].strip()
    parent = argv[2] if len(argv) > 2 else "."

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        print(f"error: '{name}' is not valid kebab-case (use lowercase letters, "
              f"digits, and hyphens, e.g. my-skill)", file=sys.stderr)
        return 2

    skill_dir = os.path.join(parent, name)
    if os.path.exists(skill_dir):
        print(f"error: {skill_dir} already exists", file=sys.stderr)
        return 3

    for sub in ("scripts", "references", "assets"):
        os.makedirs(os.path.join(skill_dir, sub), exist_ok=True)

    title = name.replace("-", " ").title()
    skill_md = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md, "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(name=name, title=title))

    print(f"Created skill scaffold at {skill_dir}/")
    print(f"  - SKILL.md (edit the description: it's the trigger!)")
    print(f"  - scripts/  references/  assets/")
    print(f"\nNext: fill in {skill_md}, then test with representative prompts.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
