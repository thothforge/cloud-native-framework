#!/usr/bin/env python3
"""Insert a blank line before Markdown lists that directly follow a text line.

Python-Markdown / Zensical requires a blank line between a paragraph and a
following list; without it the list items collapse into the paragraph and
render as one run-on line. This script finds every such "tight" boundary in
docs/*.md and inserts the missing blank line.

Rules (conservative — only inserts blank lines, never removes content):
  - A list item is a line matching  ^\\s*([-*+]\\s+ | \\d+[.)]\\s+)
  - Insert a blank line before a list item ONLY when the previous line is:
      * non-blank, AND
      * not itself a list item (so nested / consecutive items are untouched), AND
      * not a blockquote (>), AND
      * not a table row (|)
  - Lines inside fenced code blocks (``` or ~~~) are ignored entirely.
  - The item must be at the same indentation as the paragraph (top-level list),
    i.e. indent <= 3 spaces, to avoid touching indented continuation lists.

Usage:
    python3 scripts/fix_tight_lists.py           # apply
    python3 scripts/fix_tight_lists.py --check    # report only
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

ITEM = re.compile(r"^(\s*)([-*+]\s+|\d+[.)]\s+)\S")
FENCE = re.compile(r"^\s*(```|~~~)")


def fix_lines(lines: list[str]) -> tuple[list[str], int]:
    out: list[str] = []
    in_fence = False
    inserted = 0
    for i, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        m = ITEM.match(line)
        if m and out:
            indent = len(m.group(1))
            prev = out[-1]
            prev_is_item = bool(ITEM.match(prev))
            prev_stripped = prev.strip()
            if (
                indent <= 3
                and prev_stripped != ""
                and not prev_is_item
                and not prev_stripped.startswith(">")
                and not prev_stripped.startswith("|")
            ):
                out.append("")
                inserted += 1
        out.append(line)
    return out, inserted


def main() -> int:
    check = "--check" in sys.argv
    total = 0
    touched = 0
    for md in sorted(DOCS.glob("*.md")):
        original = md.read_text(encoding="utf-8")
        lines = original.split("\n")
        fixed, n = fix_lines(lines)
        if n:
            total += n
            touched += 1
            if not check:
                md.write_text("\n".join(fixed), encoding="utf-8")
    verb = "would insert" if check else "inserted"
    print(f"{verb} {total} blank line(s) across {touched} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
