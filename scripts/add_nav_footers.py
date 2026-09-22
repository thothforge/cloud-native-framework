#!/usr/bin/env python3
"""Append/refresh consistent prev/next navigation footers on every chapter.

The ordering and titles are read from the `nav` array in zensical.toml so the
footers can never drift from the site navigation. Re-running the script is
idempotent: an existing footer (delimited by the FOOTER_START marker) is
stripped and rewritten.

Usage:
    python3 scripts/add_nav_footers.py          # apply
    python3 scripts/add_nav_footers.py --check   # report only, no writes
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TOML = ROOT / "zensical.toml"

FOOTER_START = "<!-- FRAMEWORK-NAV -->"

# Parse the nav = [ ... ] block: entries look like { "Title" = "file.md" }
NAV_ENTRY = re.compile(r'\{\s*"(?P<title>[^"]+)"\s*=\s*"(?P<file>[^"]+)"\s*\}')


def parse_nav() -> list[tuple[str, str]]:
    text = TOML.read_text(encoding="utf-8")
    m = re.search(r"^nav\s*=\s*\[(.*?)^\]", text, re.S | re.M)
    if not m:
        raise SystemExit("Could not locate nav array in zensical.toml")
    block = m.group(1)
    entries = [(t, f) for t, f in NAV_ENTRY.findall(block)]
    # Drop the Home/index entry from prev/next chaining.
    return [(t, f) for (t, f) in entries if f != "index.md"]


def strip_existing_footer(body: str) -> str:
    idx = body.find(FOOTER_START)
    if idx == -1:
        return body.rstrip() + "\n"
    return body[:idx].rstrip() + "\n"


def build_footer(prev, nxt) -> str:
    prev_cell = f"← [{prev[0]}]({prev[1]})" if prev else "&nbsp;"
    next_cell = f"[{nxt[0]}]({nxt[1]}) →" if nxt else "&nbsp;"
    return (
        f"\n{FOOTER_START}\n"
        "---\n\n"
        "[← Back to index](index.md)\n\n"
        "| Previous | Next |\n"
        "|:---------|-----:|\n"
        f"| {prev_cell} | {next_cell} |\n"
    )


def main() -> int:
    check = "--check" in sys.argv
    nav = parse_nav()
    changed = 0
    for i, (title, fname) in enumerate(nav):
        path = DOCS / fname
        if not path.exists():
            print(f"MISSING nav target: {fname}")
            return 1
        prev = nav[i - 1] if i > 0 else None
        nxt = nav[i + 1] if i < len(nav) - 1 else None
        original = path.read_text(encoding="utf-8")
        new = strip_existing_footer(original) + build_footer(prev, nxt)
        if new != original:
            changed += 1
            if not check:
                path.write_text(new, encoding="utf-8")
    verb = "would update" if check else "updated"
    print(f"{verb} {changed} of {len(nav)} chapters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
