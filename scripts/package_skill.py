#!/usr/bin/env python3
"""Validate and package a skill into an installable .skill file.

Usage:
    python3 package_skill.py <skill-dir> [-o output.skill] [--force]

A .skill file is a zip archive of the skill directory. This script first validates
the skill (frontmatter present, required fields, body size) and refuses to package an
invalid skill unless --force is given.

Validation checks:
    - SKILL.md exists at the top level.
    - YAML frontmatter block is present and well-formed.
    - Required fields `name` and `description` are present and non-empty.
    - `name` is lowercase kebab-case.
    - Body length is reported; a warning is printed past 500 lines.
"""
import argparse
import os
import re
import sys
import zipfile

REQUIRED_FIELDS = ("name", "description")
BODY_LINE_SOFT_LIMIT = 500


def parse_frontmatter(text):
    """Return (fields_dict, body_str) or raise ValueError."""
    if not text.startswith("---"):
        raise ValueError("SKILL.md must start with a YAML frontmatter block (---)")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("frontmatter block is not closed with a second '---'")
    raw, body = parts[1], parts[2]
    fields = {}
    for line in raw.splitlines():
        line = line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields, body


def validate(skill_dir):
    """Return list of (level, message). level in {'error','warning'}."""
    issues = []
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return [("error", f"no SKILL.md found in {skill_dir}")]

    with open(skill_md, encoding="utf-8") as f:
        text = f.read()

    try:
        fields, body = parse_frontmatter(text)
    except ValueError as e:
        return [("error", str(e))]

    for field in REQUIRED_FIELDS:
        if not fields.get(field):
            issues.append(("error", f"required frontmatter field '{field}' is missing or empty"))

    name = fields.get("name", "")
    if name and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        issues.append(("error", f"name '{name}' is not lowercase kebab-case"))

    desc = fields.get("description", "")
    if desc and len(desc.split()) < 6:
        issues.append(("warning", "description is very short — does it say WHAT and WHEN?"))

    body_lines = len(body.strip().splitlines())
    if body_lines > BODY_LINE_SOFT_LIMIT:
        issues.append(("warning", f"SKILL.md body is {body_lines} lines (> {BODY_LINE_SOFT_LIMIT}); "
                                  f"consider moving detail into references/"))
    return issues


EXCLUDE_DIRS = {".git", ".claude", "__pycache__", ".pytest_cache", "node_modules"}
EXCLUDE_FILES = {".DS_Store"}


def package(skill_dir, output):
    base = os.path.basename(os.path.normpath(skill_dir))
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_dir):
            # prune excluded directories in place so os.walk skips them
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for fn in files:
                if fn in EXCLUDE_FILES or fn.endswith(".skill") or fn.endswith(".pyc"):
                    continue
                full = os.path.join(root, fn)
                rel = os.path.join(base, os.path.relpath(full, skill_dir))
                zf.write(full, rel)
    return output


def main(argv):
    ap = argparse.ArgumentParser(description="Validate and package a skill into a .skill file.")
    ap.add_argument("skill_dir")
    ap.add_argument("-o", "--output", help="output path (default: <name>.skill)")
    ap.add_argument("--force", action="store_true", help="package even if validation finds errors")
    args = ap.parse_args(argv[1:])

    skill_dir = args.skill_dir
    if not os.path.isdir(skill_dir):
        print(f"error: {skill_dir} is not a directory", file=sys.stderr)
        return 2

    issues = validate(skill_dir)
    errors = [m for lvl, m in issues if lvl == "error"]
    warnings = [m for lvl, m in issues if lvl == "warning"]
    for m in errors:
        print(f"  ERROR:   {m}")
    for m in warnings:
        print(f"  warning: {m}")

    if errors and not args.force:
        print("\nValidation failed. Fix the errors above, or pass --force to package anyway.",
              file=sys.stderr)
        return 1

    name = os.path.basename(os.path.normpath(skill_dir))
    output = args.output or f"{name}.skill"
    package(skill_dir, output)
    print(f"\nPackaged -> {output}")
    if warnings:
        print("(packaged with warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
