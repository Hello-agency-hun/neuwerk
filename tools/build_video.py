#!/usr/bin/env python3
"""Hero videó pipeline.

Forrás: useful visual assets/OESL_animatikv_v29.mp4 (35,9 MB, 28,33 s)
Vágás:  4,0-17,0 s  -- a SPEC betűk 20,0-20,5 között állnak össze, a zászlós
        szakasz 18,0-tól jön, tehát 2,5 s ráhagyással minden SPEC-utalás kimarad.
Grade:  50% split-tone (árnyék -> navy, csúcsfény -> hideg fehér), a meleg
        pixelek maszkolva és a valódi Sun #ffa500-ra emelve.
Encode: -g 15 (kulcskocka félmásodpercenként), mert a Solutions szekció
        scrubbolja a fájlt. Enélkül a currentTime-ugrás akadozik.

Mért célméretek: 1920 -> 5,07 MB, 1280 -> 2,56 MB.
Ha az 5 MB soknak bizonyul, a CRF-et emeld 31-re (1920 -> 3,59 MB).
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "useful visual assets" / "OESL_animatikv_v29.mp4"
OUT = ROOT / "assets" / "video"

START, END = 4.0, 17.0
FPS = 30
CRF = "28"
GOP = "15"
STRENGTH = 0.50

NAVY = np.array([0x1B, 0x1E, 0x52], np.float32) / 255
HIGH = np.array([0xF2, 0xF5, 0xFF], np.float32) / 255
SUN = np.array([0xFF, 0xA5, 0x00], np.float32) / 255


def grade(a):
    """a: (H,W,3) float32 0..1 -> graded float32 0..1"""
    lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]

    split = NAVY * (1 - lum) + HIGH * lum
    out = a * (1 - STRENGTH) + (a * 0.35 + split * 0.65) * STRENGTH

    mx = a.max(2)
    mn = a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    warm = (a[..., 0] > a[..., 2] + 0.05) & (a[..., 0] >= a[..., 1]) & (sat > 0.10)
    w = (np.clip((sat - 0.10) / 0.30, 0, 1) * warm)[..., None]

    sun = SUN * (0.5 + 0.5 * lum)
    return np.clip(out * (1 - w) + (out * 0.15 + sun * 0.85) * w, 0, 1)


def build(width, height, name):
    reader = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-ss", str(START), "-to", str(END), "-i", str(SRC),
         "-an", "-vf", f"scale={width}:{height}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE,
    )
    writer = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{width}x{height}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-crf", CRF, "-preset", "slow", "-g", GOP,
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT / name), "-y"],
        stdin=subprocess.PIPE,
    )

    nbytes = width * height * 3
    frames = 0
    while True:
        raw = reader.stdout.read(nbytes)
        if len(raw) < nbytes:
            break
        a = np.frombuffer(raw, np.uint8).reshape(height, width, 3).astype(np.float32) / 255
        writer.stdin.write((grade(a) * 255).astype(np.uint8).tobytes())
        frames += 1

    reader.stdout.close()
    reader.wait()
    writer.stdin.close()
    writer.wait()

    size = (OUT / name).stat().st_size / 1048576
    print(f"  {name:<20}{frames:>5} frame  {size:>6.2f} MB")
    return size


def main():
    if not SRC.exists():
        print(f"FAIL — nincs meg a forrás: {SRC}")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)

    print("build_video: grade + encode")
    build(1920, 1080, "hero-1920.mp4")
    build(1280, 720, "hero-1280.mp4")

    # Poszter: az első graded frame, ez megy reduced-motion és mobil fallbackként
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(OUT / "hero-1920.mp4"),
         "-frames:v", "1", "-q:v", "3", str(OUT / "hero-poster.jpg"), "-y"],
        check=True,
    )
    print(f"  hero-poster.jpg      {(OUT / 'hero-poster.jpg').stat().st_size / 1024:>9.1f} KB")

    # Intro: a hivatalos logó reveal utolsó 1,2 másodperce, hang nélkül
    subprocess.run(
        ["ffmpeg", "-v", "error", "-sseof", "-1.2",
         "-i", str(ROOT / "Arculat" / "03_neuwerk_logo_anim" / "neuwerk_logo_reveal.mp4"),
         "-an", "-c:v", "libx264", "-crf", "30", "-preset", "slow",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT / "intro.mp4"), "-y"],
        check=True,
    )
    print(f"  intro.mp4            {(OUT / 'intro.mp4').stat().st_size / 1024:>9.1f} KB")

    print("\nbuild_video: kész")
    return 0


if __name__ == "__main__":
    sys.exit(main())
