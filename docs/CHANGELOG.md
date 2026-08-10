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

---

## 2026-08-10 (2) — Ügyfélkérdések lezárva, spec frissítve

Nyolcból hét kérdés megválaszolva. A spec 6., 7., 8.1, 10., 11. és 12. pontja frissült.

**Döntések**
- **SPEC: nem használjuk semmilyen formában.** A szó itt a *specification* rövidítése,
  nem márkanév. A videó vágási pontja ezért **17,0 mp** — a narancs SPEC betűk 20,0 és
  20,5 mp között állnak össze, a zászlós szakasz 18,0-tól jön, tehát 2,5 mp a ráhagyás.
- **Képesség → videószakasz leképezés** rögzítve: fluid handling 9,5–11,0 · thermal
  management 11,5–13,0 · sealing and damping 14,0–15,5 · multi-material 15,5–17,0.
  Ha egy szakasz nem elég jó, Higgsfielddel újragenerálható (tartalék, nem alapterv).
- **Egyetlen videófájl** (4,0–17,0 mp) szolgálja ki a herót és a Solutions scrubot is.
  A hurokvágás nem égetődik bele; a hero böngészőben old crossfade-et, hogy ugyanaz a
  fájl scrubbolható maradjon.
- **Media és Career: placeholder tartalom**, láthatóan jelölve. Az egyik cikk tartalma
  arról szól, hogyan tudja az ügyfél maga frissíteni és bővíteni a listát — így a
  placeholder egyben felhasználói dokumentáció.
- **Betűtípus: a brandbook szerint**, Poppins + Lora.
- **`Identity` nav-címke marad.**
- **Színeltérés: a vektoros logó a mérvadó** → `#ffa500` mindenhol, a videó
  `#c9901c` endcard-értéke nem.

**⚠️ NYITOTT — bekérendő az ügyféltől**
- **Valós kontaktadatok.** Build 1 felismerhető placeholderekkel megy
  (`example@example.com`, `+00 000 000 0000`, `Example Street 1, 00000 Example City`).
  Minden előfordulás `TODO(client)` jelöléssel és látható badge-dzsel.
  **Ez blokkoló tétel az éles indulás előtt**, és nem zárható le fejlesztői oldalról.
  Emlékeztető minden érintett commitban.
