#!/usr/bin/env python3
"""Branded placeholder PDF-ek a responsibility oldal letöltéseihez.

Valós jogi dokumentumok még nincsenek, de a letöltési folyamatot az ügyfélnek
végig kell tudnia próbálni. Ezért minden dokumentum kap egy ~3 KB-os, arculatos
placeholder PDF-et, láthatóan megjelölve.

A valós szövegek megérkezésekor CSAK a PDF-eket kell cserélni az assets/docs/
mappában -- a HTML nem változik, a linkek nem törnek el.
"""
import sys
from pathlib import Path

import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "assets" / "docs"

NAVY = (0x1B / 255, 0x1E / 255, 0x52 / 255)
SUN = (1, 0xA5 / 255, 0)
WHITE = (1, 1, 1)
GREY = (0.4, 0.4, 0.4)
INK = (0.1, 0.1, 0.1)

PAGE_W, PAGE_H = 595, 842   # A4 pont

DOCS = [
    ("code-of-conduct", "Code of Conduct",
     "How we behave: integrity, fair competition, anti-corruption, conflicts of "
     "interest, and respect in the workplace."),
    ("compliance-ethics", "Compliance & Ethics",
     "Our compliance framework, governance responsibilities, training obligations "
     "and reporting duties."),
    ("supplier-requirements", "Supplier Requirements",
     "What we expect from suppliers: quality, sustainability, human rights, "
     "environmental and sourcing standards."),
    ("privacy-policy", "Privacy Policy",
     "How we collect, use, store and protect personal data, and the rights "
     "available to data subjects."),
    ("legal-notice", "Legal Notice",
     "Company details, registration, responsible parties and liability information "
     "for this website."),
    ("whistleblower-procedure", "Whistleblower Procedure",
     "How to raise a concern confidentially, what happens next, and the protection "
     "against retaliation."),
]

BODY = (
    "This is a placeholder document generated for the website wireframe. It exists "
    "so the download flow can be reviewed end to end. The final text will be "
    "supplied by neuwerk before launch."
)


def build(slug, title, description):
    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    page.draw_rect(fitz.Rect(0, 0, PAGE_W, 300), color=None, fill=NAVY)
    # A logó slash-e. Nem a hivatalos SVG-ből jön, ezért itt csak jelzés
    # értékű -- a PDF placeholder, nem márkakommunikációs anyag.
    page.draw_polyline([fitz.Point(56, 118), fitz.Point(84, 72)],
                       color=SUN, width=11, lineCap=1)
    page.insert_text(fitz.Point(96, 118), "neuwerk",
                     fontname="hebo", fontsize=30, color=WHITE)
    page.insert_text(fitz.Point(56, 205), title,
                     fontname="hebo", fontsize=26, color=WHITE)
    page.insert_text(fitz.Point(56, 240), "PLACEHOLDER  —  content pending",
                     fontname="heit", fontsize=11, color=SUN)

    page.insert_textbox(fitz.Rect(56, 340, PAGE_W - 56, 430), description,
                        fontname="helv", fontsize=12, color=INK)
    page.insert_textbox(fitz.Rect(56, 450, PAGE_W - 56, 600), BODY,
                        fontname="helv", fontsize=10.5, color=GREY)

    page.draw_line(fitz.Point(56, PAGE_H - 70), fitz.Point(PAGE_W - 56, PAGE_H - 70),
                   color=(0.85, 0.85, 0.85), width=0.7)
    page.insert_text(fitz.Point(56, PAGE_H - 52),
                     f"neuwerk  ·  {title}  ·  placeholder",
                     fontname="helv", fontsize=8.5, color=GREY)

    out = DST / f"{slug}.pdf"
    doc.save(out)
    doc.close()
    return out


def main():
    DST.mkdir(parents=True, exist_ok=True)
    total = 0
    for slug, title, description in DOCS:
        out = build(slug, title, description)
        size = out.stat().st_size
        total += size
        print(f"  {out.name:<32}{size / 1024:>6.1f} KB")
    print(f"\nbuild_docs: {len(DOCS)} PDF, összesen {total / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
