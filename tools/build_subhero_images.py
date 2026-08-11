#!/usr/bin/env python3
"""Aloldal-hero képek optimalizálása.

Forrás: work/gen/subhero/*.png -- Higgsfield / nano_banana_pro, 21:9, 4K
(6336x2688). A generálás promptja minden esetben tiltotta a szöveget, a
logót és a vízjelet, és mind az öt kép átment a vizuális ellenőrzésen.

A képek a .nw-subhero--image mintába kerülnek: háttérkép + navy scrim +
fölötte a szöveg. A scrim alul 0,95 opacitású, fölül 0,38 -- ezért a
kompozíció a képkocka felső felére van súlyozva, az alsó harmad
szándékosan üres és sötét, hogy a cím olvasható maradjon.

Méret: 2400 px széles. A subhero teljes viewport-szélességű, tehát nagy
monitoron is élesnek kell lennie; 21:9-ből ez 2400x1018. Progresszív
JPEG, mert a kép a hajtás fölött van, és a fokozatos megjelenés jobb,
mint a soronkénti.

A minőség fájlonként keresett: a legmagasabb, ami még belefér a
MAX_KB korlátba. Ezek nagyon sima navy gradiensek, ezért alacsony
minőségen sávosodnának -- inkább a méretet hagyjuk feljebb menni.
"""
import sys
from pathlib import Path

from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "work" / "gen" / "subhero"
OUT = ROOT / "assets" / "img" / "subhero"

WIDTH = 2400
MAX_KB = 290

NAMES = ["identity", "career", "media", "responsibility", "contact"]


def build(name):
    src = SRC / f"{name}.png"
    if not src.exists():
        print(f"  {name:<16} HIÁNYZIK: {src.relative_to(ROOT)}")
        return None

    im = Image.open(src).convert("RGB")
    h = round(im.height * WIDTH / im.width)
    im = im.resize((WIDTH, h), Image.LANCZOS)

    dst = OUT / f"{name}.jpg"
    for q in range(92, 55, -3):
        im.save(dst, "JPEG", quality=q, optimize=True, progressive=True,
                subsampling=0)
        if dst.stat().st_size <= MAX_KB * 1024:
            break

    kb = dst.stat().st_size / 1024
    print(f"  {name:<16} {WIDTH}x{h}  q={q}  {kb:>6.1f} KB")
    return kb


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("build_subhero_images: resize + progressive JPEG")
    sizes = [build(n) for n in NAMES]
    done = [s for s in sizes if s is not None]
    print(f"\n  {len(done)}/{len(NAMES)} kép, összesen {sum(done)/1024:.2f} MB")
    return 0 if len(done) == len(NAMES) else 1


if __name__ == "__main__":
    sys.exit(main())
