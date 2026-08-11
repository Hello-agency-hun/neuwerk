#!/usr/bin/env python3
"""Halott link ellenőrző.

Végigmegy minden HTML fájlon, kiszedi a href/src hivatkozásokat, és ellenőrzi,
hogy a hivatkozott fájl létezik-e. A Build 1 fő kész-kritériuma: nulla halott link.

Külső (http/https/mailto/tel) linkeket kihagy, de listázza őket, hogy látható legyen,
ha valaki véletlenül CDN-t rak be.
"""
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

import sys

# Windows Git Bash alatt a Python stdout alapból cp1250, amitől az ékezetes
# kimenet szétesik. A fájl-IO mindenhol explicit utf-8, ez csak a konzol.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "work", "Arculat", "useful visual assets", "docs", "tools", "partials"}
REF_RE = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', re.I)


def html_files():
    for p in sorted(ROOT.rglob("*.html")):
        if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            yield p


def main():
    broken, external, checked = [], set(), 0

    for page in html_files():
        text = page.read_text(encoding="utf-8", errors="replace")
        for raw in REF_RE.findall(text):
            ref = raw.strip()
            if not ref or ref.startswith("#") or ref.startswith("data:"):
                continue
            scheme = urlparse(ref).scheme
            if scheme in ("http", "https", "mailto", "tel"):
                external.add(f"{page.relative_to(ROOT)} -> {ref}")
                continue
            target = unquote(ref.split("#")[0].split("?")[0])
            if not target:
                continue
            resolved = (page.parent / target).resolve()
            checked += 1
            if not resolved.exists():
                broken.append(f"{page.relative_to(ROOT)}:  {ref}")

    pages = len(list(html_files()))
    print(f"check_links: {pages} oldal, {checked} belső hivatkozás")

    if external:
        print(f"\n  külső hivatkozás ({len(external)}) — ellenőrizd, hogy szándékos-e:")
        for e in sorted(external):
            print(f"    {e}")

    if broken:
        print(f"\nFAIL — {len(broken)} halott link:")
        for b in broken:
            print(f"    {b}")
        return 1

    if pages == 0:
        print("\nFAIL — nincs egyetlen HTML oldal sem")
        return 1

    print("\nPASS — nincs halott link")
    return 0


if __name__ == "__main__":
    sys.exit(main())
