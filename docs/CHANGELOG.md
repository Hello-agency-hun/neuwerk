# Changelog

A NEUWERK weboldal fejlesztésének naplója. Minden érdemi változás ide kerül,
dátummal, hogy az átvevő fejlesztő vagy agent lássa, hol tartunk és miért.

Formátum: fordított időrend, legfrissebb legfelül.

---

## 2026-08-10 — Design fázis lezárva, spec elkészült

**Hozzáadva**
- `docs/superpowers/specs/2026-08-10-neuwerk-website-design.md` — a teljes design spec
- `.gitignore`
- Ez a changelog

**Feltárt forrásanyagok**
- Tartalmi spec: `Structure_and_Content_NEUWERK_Website_agi_review.pdf` (7 oldal, teljes EN copy)
- Arculat: brandbook v1.1, merch guideline, building signage, hivatalos logók (SVG/AI/EPS/PNG),
  Poppins + Lora TTF, logó reveal MP4, OESL és Regent logók
- `useful visual assets/OESL_animatikv_v29.mp4` — transparent car animatik, a hero forrása

**Elemzések, amikre a spec épül**
- A hero videó frame-by-frame idővonala feltérképezve (28,33 mp, 850 frame, nincs benne vágás,
  az audiósáv digitális csend)
- Encode-tesztek lemérve: az orbit-szegmens 1920-on 3,5 MB, 1280-on 1,75 MB
- Hero grade-tesztek: duotone változatok elvetve (részletvesztés), 50% split-tone kiválasztva
- WCAG kontrasztarányok kiszámolva a teljes palettára — két bukó pár azonosítva
  (Sun on White és White on Sun, mindkettő 1,97:1)

**Rögzített döntések** — lásd a spec 12. pontját (11 döntés)

**Elvetve**
- three.js hero car: a videó már tartalmaz professzionálisan renderelt transzparens autót,
  WebGL-ben csak rosszabb és nehezebben átadható születne
- Részecske-alapú pill-mező: a brandbook kifejezetten tiltja a kisméretű, sűrű,
  pusztán dekoratív pattern-használatot
- Google Fonts CDN: a fontok self-hosted woff2-ként mennek (GDPR)
- JSON + `fetch()` az adatlistákhoz: `file://`-ből CORS-ba fut, ezért JS értékadás lett

**Következő lépés**
- Ügyfél-oldali spec review, majd implementációs terv
