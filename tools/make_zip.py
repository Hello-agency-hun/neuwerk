#!/usr/bin/env python3
"""Leszállítható zip.

Csak az üzemeléshez szükséges fájlok kerülnek bele. Kimarad: a forrásassetek
(Arculat/, useful visual assets/, vendor/), a build eszközök (tools/, work/)
és a fejlesztői dokumentáció (docs/, .git/). Ezek a repóban maradnak, de az
ügyfél szerverére nem valók.

A partials/ SZINTÉN kimarad: azok fejlesztői referencia-másolatok feloldatlan
{{ROOT}} tokenekkel. Ha felkerülnének a szerverre, törött oldalakként lennének
kiszolgálhatók és indexelhetők.

A CLAUDE.md szándékosan BENNE van: ha az ügyfél továbbadja a csomagot egy
fejlesztőnek, az abból azonnal érti a szabályokat.
"""
import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "work" / "neuwerk-website-build1.zip"

INCLUDE_DIRS = ["assets", "css", "js", "data", "media"]
INCLUDE_FILES = [
    "index.html", "identity.html", "career.html", "media.html",
    "responsibility.html", "contact.html", "404.html",
    "README.md", "CLAUDE.md",
]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    missing = [n for n in INCLUDE_FILES if not (ROOT / n).exists()]
    missing += [d for d in INCLUDE_DIRS if not (ROOT / d).is_dir()]
    if missing:
        print("FAIL — hiányzik:")
        for m in missing:
            print(f"    {m}")
        return 1

    entries = []
    for name in INCLUDE_FILES:
        entries.append((ROOT / name, name))
    for d in INCLUDE_DIRS:
        for p in sorted((ROOT / d).rglob("*")):
            if p.is_file() and p.name != ".gitkeep":
                entries.append((p, p.relative_to(ROOT).as_posix()))

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for src, arc in entries:
            z.write(src, arc)

    raw = sum(src.stat().st_size for src, _ in entries)
    size = OUT.stat().st_size
    print(f"make_zip: {len(entries)} fájl")
    print(f"  nyers:      {raw / 1048576:>7.2f} MB")
    print(f"  tömörítve:  {size / 1048576:>7.2f} MB")
    print(f"  {OUT.relative_to(ROOT).as_posix()}")

    # A legnagyobb tételek -- hasznos, ha valaki azon gondolkodik, mit lehet még faragni
    top = sorted(entries, key=lambda e: e[0].stat().st_size, reverse=True)[:5]
    print("\n  legnagyobb fájlok:")
    for src, arc in top:
        print(f"    {arc:<40}{src.stat().st_size / 1048576:>6.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
