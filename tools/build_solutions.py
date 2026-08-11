#!/usr/bin/env python3
"""Solutions pillér-videók.

Négy külön fájl, pillérenként egy. A korábbi megoldás egyetlen fájlt
scrubbolt data-from/data-to alapján; azt lecseréltük, mert:

1. A közös fájl a hero volt (OESL_animatikv_v29 4,0-17,0 s), amelybe **bele
   van égetve** a padlóra vetített SAFETY / PERFORMANCE / EFFICIENCY / COMFORT
   tipográfia. A CSS csak megpróbálta levágni (`object-position: center 34%`),
   de a felirat nem az alsó harmadban ül: az EFFICIENCY szakaszban a képkocka
   közepén, az akkumulátorcsomagon fut keresztül. Vágással nem eltávolítható.
2. A négy pillér így saját vágóképet kaphat, és két <video> réteg között
   átúsztatható.

Forrás pillérenként (work/gen/, git-ignorált munkaterület):

  fluid    C1-fluid    3,10-6,00 s  a teljes, elülső-hátsó vezetékhálózat
  thermal  C2-thermal  1,50-4,40 s  az akkutálcát követő kör; a klip utolsó
                                    1,6 s-ában a narancs elönti a képet, az
                                    már sértené a Sun 10-15%-os korlátot
  sealing  C3-sealing  0,00-2,90 s  különálló borostyán harmonikák és bakok
                                    az elülső segédkereten
  multi    C4-multi    0,00-2,90 s  sokféle különálló elem fém és áttetsző
                                    műanyag között

A C4 bal oldalán egy fehér, vetített "O" gyűrű látszik végig az első ~3,6 s-ban,
ezért abból a bal 20%-ot kivágjuk (crop 1024x576 @ 256,72), majd vissza 1280x720-ra.
A többi klip vágatlan.

Grade: ugyanaz a split-tone, amit a hero kap (build_video.grade), így a
generált és az eredeti animatikból származó anyag egy családba kerül, és a
zavaros vörös-narancs a valódi Sun #ffa500-ra emelkedik.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

from build_video import grade

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "work" / "gen"
OUT = ROOT / "assets" / "video"

W, H = 1280, 720
FPS = 24
# A hero CRF 28-cal megy, mert 1920x1080 és 13 s. Itt négy 2,9 s-os 720p klip
# van, a keret ~6 MB, tehát bőven belefér a szebb kép. CRF 23-nál a C4
# felnagyított vágóképe is tiszta marad.
CRF = "23"
GOP = "24"

# név, forrásfájl, kezdet, vég, extra videoszűrő a nyers olvasás elé
CLIPS = [
    ("solution-fluid",   "C1-fluid.mp4",   3.10, 6.00, None),
    ("solution-thermal", "C2-thermal.mp4", 1.50, 4.40, None),
    ("solution-sealing", "C3-sealing.mp4", 0.00, 2.90, None),
    ("solution-multi",   "C4-multi.mp4",   0.00, 2.90, "crop=1024:576:256:72"),
]


def build(name, src, start, end, pre):
    vf = f"{pre},scale={W}:{H}" if pre else f"scale={W}:{H}"
    reader = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-ss", str(start), "-to", str(end), "-i", str(SRC / src),
         "-an", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE,
    )
    writer = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-crf", CRF, "-preset", "slow", "-g", GOP,
         "-pix_fmt", "yuv420p", "-movflags", "+faststart",
         str(OUT / f"{name}.mp4"), "-y"],
        stdin=subprocess.PIPE,
    )

    nbytes = W * H * 3
    frames = 0
    first = None
    while True:
        raw = reader.stdout.read(nbytes)
        if len(raw) < nbytes:
            break
        a = np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
        g = (grade(a) * 255).astype(np.uint8)
        if first is None:
            first = g
        writer.stdin.write(g.tobytes())
        frames += 1

    reader.stdout.close()
    reader.wait()
    writer.stdin.close()
    writer.wait()

    # Poszter: az első graded képkocka. Ez megy reduced-motion alatt és
    # a crossfade első pillanatában is, amíg a videó dekódol.
    subprocess.run(
        ["ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-i", "-", "-frames:v", "1", "-q:v", "4",
         str(OUT / f"{name}.jpg"), "-y"],
        input=first.tobytes(), check=True,
    )

    mp4 = (OUT / f"{name}.mp4").stat().st_size
    jpg = (OUT / f"{name}.jpg").stat().st_size
    print(f"  {name:<20}{frames:>4} frame  {mp4/1048576:>6.2f} MB  poszter {jpg/1024:>6.1f} KB")
    return mp4


def main():
    missing = [c[1] for c in CLIPS if not (SRC / c[1]).exists()]
    if missing:
        print(f"FAIL — hiányzó forrás a work/gen/ alatt: {', '.join(missing)}")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)

    print("build_solutions: cut + grade + encode")
    total = sum(build(*c) for c in CLIPS)
    print(f"\n  összesen {total/1048576:.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
