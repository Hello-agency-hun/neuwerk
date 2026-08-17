#!/usr/bin/env python3
"""Alapkep a brand-sav generalt loopjahoz.

Miert kell: a Higgsfield ket korben azert bukott, mert SZOVEGBOL kellett
kitalalnia a szineket es a formakat -- gyogyszerkapszulat, lila gomboket es
konzekvensen cian-keket adott a navy helyett. Kepbol indulva ez a hibaforras
megszunik: a paletta es a formanyelv az input kepbol jon, a modellnek csak
mozgatnia kell.

Ezert ez a szkript NEM "szep hattert" rajzol, hanem pontosan azt a
kompoziciot, ami most CSS-bol fut a .nw-brandband-ben -- ugyanazokkal a
token-szinekkel, ugyanazzal a -45 fokos dolessel es ugyanazokkal az
aranyokkal.

Kimenet: work/gen/band/base.png (2208x946, 21:9).

Miert 21:9 es nem a sav sajat ~5:1 aranya: az elso kor 1920x512-vel ment, es
a modell 2206x946-ra komponalta at -- vagyis a sajat kimeneti aranyara
skalazta, majd hogy kitoltse, KICSINYITVE TAPETAZTA a mintat. Az eredmeny
suru pasztilla-mezo lett, ami serti a brandbook "nagy leptek" szabalyat, es a
savra vagva a pasztillak vegei is levagodtak: szogletes cikcakk maradt.

Ezert a bemenet mostantol a modell sajat aranyaban keszul, tehat nincs oka
atskalazni. A savkent LATHATO resz a kepkocka kozepso savja (STRIP_FRAC), a
formak merete ehhez van szabva -- folotte es alatta ugyanilyen leptekű sorok
futnak, hogy a modell ne talaljon ki oda semmit.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "work" / "gen" / "band"

W, H = 2208, 946            # 21:9 -- a seedance_2_0 tenyleges kimeneti aranya
SS = 2                      # supersampling: elsimitja a forgatas lepcsoit

# A kepkockanak ez a hanyada lesz a lapon lathato sav (object-fit: cover).
# 946 * 0,43 = 407 px -- ez a "sav magassag", amihez a formak meretezve vannak.
STRIP_FRAC = 0.43

# --- Szinek. Forras: css/tokens.css. Ne ird at itt: ott ird at. ----------
DEEP = (0x27, 0x39, 0x93)   # --nw-deep,   a sav hattere
DEEPER = (0x1e, 0x2c, 0x72)  # --nw-deeper, a sotet formak
BLUE2 = (0x4e, 0x66, 0xaf)  # --nw-blue-2, a vilagos formak alapja


def mix(a, b, t):
    """color-mix(in oklab, a t%, b) kozelitese sRGB-ben.

    Nem pontos oklab, de itt ket kozeli kek kozott interpolalunk, ahol a ket
    terben szamolt eredmeny kulonbsege szabad szemmel nem lathato -- es ez
    egy generator-input, nem a vegleges asset.
    """
    return tuple(round(a[i] * t + b[i] * (1 - t)) for i in range(3))


# A CSS-ben: nth-child(2) -> blue-2 58%, (4) -> 34%, (6) -> 48%, tobbi deeper.
FILLS = [DEEPER, mix(BLUE2, DEEP, 0.58), DEEPER,
         mix(BLUE2, DEEP, 0.34), DEEPER, mix(BLUE2, DEEP, 0.48)]

# --- Geometria. Forras: css/sections.css .nw-brandband__shape ------------
# k = a forma szelessege a SAV magassagahoz kepest, r = hossz/szelesseg arany.
# A formak a LATHATO sav magassagahoz vannak meretezve, nem a kepkockaehoz.
# Igy a kozepso savba pontosan az a kompozicio kerul, ami most CSS-bol fut.
BH = int(H * STRIP_FRAC)

# Hany sor fer a kepkockaba. A kozepso a "musoros" sor, a tobbi csak azert
# van ott, hogy a modell ne talaljon ki sajat tartalmat a szelekre.
ROWS = [-1, 0, 1]
SHAPES = [
    # (k,    r,    x_szazalek)
    (0.40, 2.70, -0.06),
    (0.36, 3.05, 0.11),
    (0.44, 2.30, 0.28),
    (0.38, 2.85, 0.45),
    (0.42, 2.45, 0.62),
    (0.34, 3.30, 0.79),
]


def build():
    canvas = Image.new("RGB", (W * SS, H * SS), DEEP)

    for row in ROWS:
      # A szomszedos sorok fel lepessel el vannak tolva, kulonben a
      # fuggoleges ismetlodes racsnak latszana, nem folyamatos mintanak.
      offset = 0.085 if row % 2 else 0.0
      for (k, r, xp), fill in zip(SHAPES, FILLS):
        w = int(BH * k * SS)
        h = int(w * r)
        # A formát sajat, atlatszo lapon rajzoljuk meg allo helyzetben, majd
        # elforgatjuk -- igy a lekerekites nem torzul.
        pad = int((w + h) * 0.5)
        layer = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.rounded_rectangle(
            [pad, pad, pad + w, pad + h], radius=w // 2, fill=fill + (255,)
        )
        layer = layer.rotate(45, resample=Image.BICUBIC, expand=True)

        # A CSS-ben az inset-inline-start a forgatas ELOTTI doboz bal elet
        # adja meg, a forgatas pedig a doboz kozepe korul tortenik. A forma
        # kozeppontja tehat xp * W + w / 2 -- a forgatott layer sajat
        # (atlatszo paddinggel felduzzasztott) meretetol fuggetlenul.
        cx = int((xp + offset) * W * SS) + w // 2
        cy = (H * SS) // 2 + row * BH * SS
        canvas.paste(layer, (cx - layer.width // 2, cy - layer.height // 2), layer)

    canvas = canvas.resize((W, H), Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / "base.png"
    canvas.save(dst, optimize=True)
    kb = dst.stat().st_size / 1024
    print(f"  {dst.relative_to(ROOT)}  {W}x{H}  {kb:.0f} kB")
    return dst


if __name__ == "__main__":
    build()
