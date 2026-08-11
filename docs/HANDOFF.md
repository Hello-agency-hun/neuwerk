# Handoff — állapot és nyitott tételek

Utolsó frissítés: 2026-08-10

## Állapot

Build 1 fejlesztés alatt. Design spec jóváhagyva.

## ⚠️ Blokkoló tételek éles indulás előtt

| # | tétel | státusz |
|---|---|---|
| 1 | **Valós kontaktadatok** (címek, telefonszámok, e-mailek, cégadatok) | ügyféltől bekérendő |
| 2 | **A 16 ország megnevezése.** Sem a tartalmi spec, sem a brandbook nem sorolja fel őket. A térkép addig jelölt placeholder-pozíciókkal megy. | ügyféltől bekérendő |
| 3 | Media cikkek valós tartalma | ügyféltől bekérendő |
| 4 | Career pozíciók valós listája | ügyféltől bekérendő |
| 5 | Az 5 jogi dokumentum szövege (Code of Conduct, Compliance & Ethics, Supplier Requirements, Privacy Policy, Legal Notice) | ügyféltől bekérendő |

Ezek egyike sem zárható le fejlesztői oldalról.

## Placeholder-leltár

Ezt a szakaszt a `python tools/check_placeholders.py` generálja. Ne szerkeszd kézzel.

<!-- PLACEHOLDER-INVENTORY-START -->
Generálva: `python tools/check_placeholders.py` — **2 tétel**

| fájl | sor | tétel |
|---|---|---|
| `index.html` | 131 | a 16 ország tényleges listája bekérendő |
| `data\locations.js` | 7 | a 16 ország tényleges listája bekérendő |
<!-- PLACEHOLDER-INVENTORY-END -->

## Asset pipeline

Egyik sem fut a felhasználónál. Csak akkor futtasd, ha a forrás változik.

    python tools/build_fonts.py    # TTF -> woff2, assets/fonts/
    python tools/build_video.py    # ffmpeg + grade, assets/video/

## Hogyan frissíti az ügyfél a tartalmat

Media: `data/news.js`. Career: `data/jobs.js`. Mindkettő egyszerű JS lista, kommentelve.
Új cikkhez a listába egy új objektum **és** egy új `media/<slug>.html` kell — a meglévő
cikkoldal másolásával. Ez a folyamat magán az oldalon is dokumentálva van, a
"How to update this page" című demó cikkben.
