#!/usr/bin/env python3
"""Static validation of the docs set (no site build required).

Checks:
  1. Every nav target in zensical.toml resolves to a file in docs/.
  2. Every nav target is a real file; every docs/*.md chapter is in the nav
     (except index.md).
  3. Every internal markdown link ([text](target)) in each docs/*.md resolves:
     - relative .md links point to an existing file
     - intra-page (#anchor) links are not validated here (Zensical slugs vary)
     - external (http/https/mailto) links are skipped
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TOML = ROOT / "zensical.toml"

NAV_ENTRY = re.compile(r'\{\s*"[^"]+"\s*=\s*"([^"]+)"\s*\}')
# markdown links, ignoring image ![]() by requiring not preceded by '!'
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def nav_targets() -> list[str]:
    text = TOML.read_text(encoding="utf-8")
    m = re.search(r"^nav\s*=\s*\[(.*?)^\]", text, re.S | re.M)
    block = m.group(1)
    return NAV_ENTRY.findall(block)


def main() -> int:
    errors: list[str] = []

    # 1 + 2: nav <-> files
    nav = nav_targets()
    for t in nav:
        if not (DOCS / t).exists():
            errors.append(f"nav target missing on disk: {t}")
    nav_set = {t for t in nav if t != "index.md"}
    chapter_files = {p.name for p in DOCS.glob("*.md") if p.name != "index.md"}
    for f in sorted(chapter_files - nav_set):
        errors.append(f"chapter not in nav: {f}")
    for f in sorted(nav_set - chapter_files):
        errors.append(f"nav entry has no file: {f}")

    # 3: internal links in every markdown file (incl. index.md)
    link_count = 0
    for md in sorted(DOCS.glob("*.md")):
        for target in LINK.findall(md.read_text(encoding="utf-8")):
            t = target.strip()
            if t.startswith(("http://", "https://", "mailto:", "#")):
                continue
            link_count += 1
            path_part = t.split("#", 1)[0]
            if not path_part:  # pure anchor
                continue
            resolved = (md.parent / path_part).resolve()
            if not resolved.exists():
                errors.append(f"{md.name}: broken link -> {t}")

    print(f"nav entries: {len(nav)} | chapters: {len(chapter_files)} | "
          f"internal links checked: {link_count}")
    if errors:
        print(f"\n{len(errors)} PROBLEM(S):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: nav and all internal .md links resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
