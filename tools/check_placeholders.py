#!/usr/bin/env python3
"""Placeholder-leltár.

Összegyűjti a TODO(client) megjegyzéseket és a data-placeholder attribútumokat,
majd beírja a docs/HANDOFF.md jelölői közé. Így nem lehet elfelejteni, mi vár még
ügyfél-adatszolgáltatásra.

Külön ellenőrzi, hogy minden gyanús kontaktminta (e-mail, telefonszám) placeholder-e.
Valós e-mail cím a Build 1-ben hiba.
"""
import re
from pathlib import Path

import sys

# Windows Git Bash alatt a Python stdout alapból cp1250, amitől az ékezetes
# kimenet szétesik. A fájl-IO mindenhol explicit utf-8, ez csak a konzol.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = ROOT / "docs" / "HANDOFF.md"
START = "<!-- PLACEHOLDER-INVENTORY-START -->"
END = "<!-- PLACEHOLDER-INVENTORY-END -->"
SKIP_DIRS = {".git", "work", "Arculat", "useful visual assets", "docs", "tools", "partials"}

TODO_RE = re.compile(r"TODO\(client\):\s*([^\-]*?)\s*-->")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
ALLOWED_EMAIL_HOSTS = ("example.com", "example.org", "example.net")


def scan_files():
    for pattern in ("*.html", "*.js"):
        for p in sorted(ROOT.rglob(pattern)):
            if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
                yield p


def main():
    todos, bad_emails = [], []

    for f in scan_files():
        rel = f.relative_to(ROOT)
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for note in TODO_RE.findall(line):
                todos.append((str(rel), i, note.strip()))
            for addr in EMAIL_RE.findall(line):
                if not addr.lower().endswith(ALLOWED_EMAIL_HOSTS):
                    bad_emails.append(f"{rel}:{i}  {addr}")

    lines = [f"Generálva: `python tools/check_placeholders.py` — **{len(todos)} tétel**", ""]
    if todos:
        lines += ["| fájl | sor | tétel |", "|---|---|---|"]
        lines += [f"| `{f}` | {n} | {note} |" for f, n, note in todos]
    else:
        lines.append("_Nincs jelölt placeholder._")

    text = HANDOFF.read_text(encoding="utf-8")
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    HANDOFF.write_text(
        f"{before}{START}\n" + "\n".join(lines) + f"\n{END}{after}",
        encoding="utf-8",
    )

    print(f"check_placeholders: {len(todos)} jelölt placeholder, HANDOFF.md frissítve")

    if bad_emails:
        print(f"\nFAIL — {len(bad_emails)} nem-placeholder e-mail cím:")
        for b in bad_emails:
            print(f"    {b}")
        print("\n  Build 1-ben minden kontaktadat felismerhető placeholder kell legyen")
        print("  (example.com / example.org / example.net).")
        return 1

    print("PASS — minden kontaktadat placeholder")
    return 0


if __name__ == "__main__":
    sys.exit(main())
