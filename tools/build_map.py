#!/usr/bin/env python3
"""Pont-rácsos világtérkép a Global Footprint szekcióhoz.

Forrás: vendor/land-110m.json -- Natural Earth 110m szárazföld, TopoJSON.
A Natural Earth PUBLIC DOMAIN, semmilyen megszorítás nincs rajta, ezért
gond nélkül beépíthető egy ügyfélnek leszállított csomagba.

Miért pont-rács és nem sziluett: a brand vizuális nyelve geometrikus --
lekerekített formák, pill, kör. Egy pontokból rakott kontinens ebbe
illeszkedik, egy fotórealisztikus sziluett nem. Ráadásul lényegesen
kisebb és élesen skálázódik.

A kimenet egyetlen statikus SVG, szín nélkül: a pontok `currentColor`-t
öröklik, tehát a színt a CSS adja (--nw-pattern-fill / --nw-fg-secondary).

Futtatás csak akkor kell, ha a forrás vagy a rácssűrűség változik:
    python tools/build_map.py
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "vendor" / "land-110m.json"
OUT = ROOT / "assets" / "img" / "world.svg"

# A rács finomsága. 150 oszlop nagyjából 2,4 fok/pont az egyenlítőn --
# elég sűrű, hogy a kontinensek felismerhetők legyenek, elég ritka,
# hogy a DOM kezelhető maradjon (~2700 pont, ~90 KB).
COLS = 150
# Equirectangular vágás: a sarkvidékek üresek és csak torzítanak,
# ezért 83 fok felett és 60 fok alatt levágjuk.
LAT_TOP, LAT_BOTTOM = 83.0, -60.0
DOT_R = 0.34          # pontsugár rácsegységben
MASK_SCALE = 6        # a maszkot ennyiszeres felbontáson rajzoljuk, majd mintavételezünk


def decode_arcs(topo):
    """TopoJSON delta-kódolt arcok -> abszolút [lon, lat] listák."""
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    out = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        out.append(pts)
    return out


def ring_points(arcs, indices):
    """Egy gyűrű arc-indexekből. A negatív index a fordított arcot jelenti."""
    pts = []
    for i in indices:
        if i >= 0:
            seg = arcs[i]
        else:
            seg = arcs[-i - 1][::-1]
        pts.extend(seg[1:] if pts else seg)
    return pts


def polygons(topo, arcs):
    """Minden szárazföld-gyűrű, külső és belső egyaránt."""
    rings = []
    for geom in topo["objects"]["land"]["geometries"]:
        kind = geom["type"]
        if kind == "Polygon":
            groups = [geom["arcs"]]
        elif kind == "MultiPolygon":
            groups = geom["arcs"]
        else:
            continue
        for poly in groups:
            for ring in poly:
                rings.append(ring_points(arcs, ring))
    return rings


def main():
    if not SRC.exists():
        print(f"FAIL — nincs meg a forrás: {SRC}")
        return 1

    topo = json.load(open(SRC, encoding="utf-8"))
    arcs = decode_arcs(topo)
    rings = polygons(topo, arcs)

    rows = int(round(COLS * (LAT_TOP - LAT_BOTTOM) / 360.0))
    mw, mh = COLS * MASK_SCALE, rows * MASK_SCALE

    def project(lon, lat):
        px = (lon + 180.0) / 360.0 * mw
        py = (LAT_TOP - lat) / (LAT_TOP - LAT_BOTTOM) * mh
        return px, py

    mask = Image.new("1", (mw, mh), 0)
    draw = ImageDraw.Draw(mask)
    for ring in rings:
        if len(ring) < 3:
            continue

        # A dátumvonalat átlépő gyűrűk (Csukcs-félsziget, Fidzsi, Antarktisz)
        # a nyers vetítésben végigsöpörnek a képen, és vízszintes csíkot
        # hagynak. Ezért előbb "kitekerjük" a hosszúságokat folytonosra,
        # majd három eltolásban rajzoljuk: a -180..180 ablakba így mindig
        # a helyes darab esik bele.
        lons = [ring[0][0]]
        for lon, _ in ring[1:]:
            prev = lons[-1]
            while lon - prev > 180:
                lon -= 360
            while prev - lon > 180:
                lon += 360
            lons.append(lon)
        lats = [lat for _, lat in ring]

        for shift in (-360, 0, 360):
            draw.polygon(
                [project(lon + shift, lat) for lon, lat in zip(lons, lats)],
                fill=1,
            )

    px = mask.load()
    dots = []
    for gy in range(rows):
        for gx in range(COLS):
            # a rácscella közepét mintavételezzük
            sx = int((gx + 0.5) * MASK_SCALE)
            sy = int((gy + 0.5) * MASK_SCALE)
            if 0 <= sx < mw and 0 <= sy < mh and px[sx, sy]:
                dots.append((gx, gy))

    # Egész koordináták: a viewBox-ot fél egységgel eltoljuk, így a
    # cellaközepek egészre esnek. Tizedesjegyenként ~2 byte / pont,
    # ami ennyi pontnál már számít.
    # Az r NEM öröklődő SVG-tulajdonság, ezért nem tehető a <g>-re --
    # pontonként kell kiírni, különben minden kör r=0 lesz és eltűnik.
    r = f"{DOT_R:g}".lstrip("0")
    body = "".join(f'<circle cx="{gx}" cy="{gy}" r="{r}"/>' for gx, gy in dots)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="-0.5 -0.5 {COLS} {rows}" '
        f'fill="currentColor" role="img" aria-label="World map">'
        f"{body}</svg>"
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")

    size = OUT.stat().st_size
    print(f"build_map: {COLS}×{rows} rács, {len(dots)} pont, {size / 1024:.1f} KB")
    print(f"  {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
