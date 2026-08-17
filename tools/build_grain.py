#!/usr/bin/env python3
"""Csempezheto szemcse-textura.

Miert kell: a sav sik, vektoros szinfoltokbol all. Pont ez adja a
"generalt" benyomast -- a nyomtatott markaanyagoknak van anyagszerusegük,
a keprnyos sik szinfoltoknak nincs. Egy nagyon halvany szemcse ezt tori meg,
es mellesleg a nagy egyszinu feluleteken jelentkezo savosodast (banding) is
elmossa.

Miert PNG es nem futasideju SVG-szuro: a keringo megoldas
(feTurbulence + filter: contrast(170%) brightness(1000%)) minden festesnel
ujraszamol, Blinkben es WebKitben mashogy nez ki, es meresek szerint draga.
Egy elore legyartott, csempezett PNG nulla futasideju koltseg, minden
bongeszoben azonos, es file://-bol is mukodik.

Kimenet: assets/img/grain.png (96x96, szurkearnyalatos + alfa)

Futtatas csak akkor kell, ha a szemcse karaktere valtozik:
    python tools/build_grain.py
"""
import random
import sys
from pathlib import Path

from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "grain.png"

# 96x96: eleg nagy, hogy a csempehatar ne alljon ossze lathato racsba, es
# eleg kicsi, hogy par kB legyen. Finom, nagyfrekvenciás zaj -- nincs benne
# alacsony frekvenciás szerkezet, ezert a csempeel nem latszik.
SIZE = 96
# A szoras adja a szemcse erosseget. A tenyleges lathatosagot a CSS opacity
# allitja, ez csak a karaktere.
SIGMA = 42
SEED = 20260814


def build():
    random.seed(SEED)
    img = Image.new("L", (SIZE, SIZE))
    px = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            # Kozep 128 korul szoro Gauss-zaj. A CSS overlay blend modban a
            # 128 a semleges ertek: ami folotte van, vilagosit, ami alatta,
            # sotetit -- tehat a szemcse nem tolja el a felulet vilagossagat.
            v = int(random.gauss(128, SIGMA))
            px[x, y] = max(0, min(255, v))
    img.save(OUT, optimize=True)
    print(f"  {OUT.relative_to(ROOT)}  {SIZE}x{SIZE}  {OUT.stat().st_size / 1024:.1f} kB")


if __name__ == "__main__":
    build()
