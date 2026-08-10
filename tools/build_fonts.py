#!/usr/bin/env python3
"""TTF -> woff2 a self-hosted betűtípusokhoz.

A brandbook Poppins + Lora párost ír elő. Mindkettő OFL-licencű, ezért
self-hostolható. Google Fonts CDN-t szándékosan NEM használunk: német ipari
ügyfélnél a CDN-es font GDPR-kockázat.
"""
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Arculat" / "01_neuwerk_brandbook" / "neuwerk_brandbook_FINAL" / "Fonts"
DST = ROOT / "assets" / "fonts"

FILES = {
    "POPPINS-REGULAR.TTF": "poppins-400.woff2",
    "Poppins-Medium.ttf": "poppins-500.woff2",
    "Poppins-SemiBold.ttf": "poppins-600.woff2",
    "Poppins-Bold.ttf": "poppins-700.woff2",
    "Lora-VariableFont_wght.ttf": "lora-var.woff2",
    "Lora-Italic-VariableFont_wght.ttf": "lora-var-italic.woff2",
}


def main():
    DST.mkdir(parents=True, exist_ok=True)
    missing = [s for s in FILES if not (SRC / s).exists()]
    if missing:
        print("FAIL — hiányzó forrás TTF:")
        for m in missing:
            print(f"    {SRC / m}")
        return 1

    total = 0
    for src_name, dst_name in FILES.items():
        font = TTFont(SRC / src_name)
        font.flavor = "woff2"
        out = DST / dst_name
        font.save(out)
        size = out.stat().st_size
        total += size
        print(f"  {dst_name:<24}{size / 1024:>7.1f} KB")

    print(f"\nbuild_fonts: {len(FILES)} fájl, összesen {total / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
