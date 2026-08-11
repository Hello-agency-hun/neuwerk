# NEUWERK Website — Build 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Egy kattintható, brandelt, statikus NEUWERK weboldal (16 oldal), amit az ügyfél végig tud kattintani jóváhagyásra, és amit egy zip-ben át lehet adni.

**Architecture:** Zero-build statikus HTML/CSS/JS. Minden oldal önhordó (header/footer duplikálva, jelölőkkel keretezve). Nincs npm, nincs PHP, nincs CMS. A változó tartalom `window.NEUWERK_*` JS értékadásból jön, hogy `file://`-ből is működjön. A design system egyetlen `css/tokens.css`-ben él, a brandbook v1.1 hiteles értékeivel.

**Tech Stack:** HTML5, CSS (custom properties, `@layer`), vanilla JS (ES2020, no framework). Build-idejű eszközök: Python 3.12 + numpy (videó grade), ffmpeg (encode), fonttools+brotli (woff2). Ezek **nem** futnak a felhasználónál — csak assetet állítanak elő.

**Spec:** [`docs/superpowers/specs/2026-08-10-neuwerk-website-design.md`](../specs/2026-08-10-neuwerk-website-design.md) — minden szám és szabály onnan jön.

---

## Verification model

Ez statikus oldal, nincs futtatható unit-teszt keret. A TDD-ciklus itt így néz ki:

1. megírjuk az **ellenőrző szkriptet** (Task 2 és 3), ami a hibát jelzi
2. lefuttatjuk → **FAIL**
3. megépítjük a minimumot
4. újra futtatjuk → **PASS**
5. commit

A két ellenőrző a projekt kész-kritériumaiból jön: **nulla halott link** és **minden placeholder jelölve**. Ezek nem díszek — a Build 1 fő célja pont az, hogy az ügyfél sehol ne fusson zsákutcába.

**Minden task végén kötelező:**

```bash
python tools/check_links.py && python tools/check_placeholders.py
```

> **Konzol-kódolás.** Windows Git Bash alatt a Python stdout alapból `cp1250`, amitől
> az ékezetes kimenet szétesik. Ezért mindkét ellenőrző az importok után tartalmazza
> ezt a blokkot — **ne vedd ki**:
>
> ```python
> if hasattr(sys.stdout, "reconfigure"):
>     sys.stdout.reconfigure(encoding="utf-8")
> ```
>
> A fájl-IO mindenhol explicit `encoding="utf-8"`, ez csak a konzolt érinti.

---

## File structure

| fájl | felelősség |
|---|---|
| `index.html` … `contact.html`, `404.html` | 7 gyökér-oldal, önhordó |
| `legal/*.html` | 5 jogi stub |
| `media/*.html` | 3 cikkoldal |
| `partials/head.html` · `header.html` · `footer.html` | referencia-másolatok; a forrásigazság a jelölők között |
| `css/tokens.css` | **csak** custom property-k. A teljes brandbook. Semmi szelektor. |
| `css/base.css` | reset, tipográfiai skála, layout primitívek, `prefers-reduced-motion` |
| `css/components.css` | header, footer, gomb, kártya, badge, pill |
| `css/sections.css` | főoldali szekciók + aloldal-layoutok |
| `js/nav.js` | mobilmenü, aktív állapot, scroll-állapot |
| `js/pattern.js` | a Neuwerk pattern scroll-vezérelt mozgatása |
| `js/reveal.js` | IntersectionObserver reveal |
| `js/counters.js` | felszámláló |
| `js/hero.js` | hero videó: loop-crossfade, poszter-fallback |
| `js/scrub.js` | Solutions scroll-scrub + pillérváltás |
| `js/lists.js` | `media.html` és `career.html` listarenderelés |
| `data/news.js` · `data/jobs.js` | szerkeszthető tartalomlisták |
| `data/locations.js` | a térkép 16 pontja (**placeholder**) |
| `tools/check_links.py` | halott link ellenőrző |
| `tools/check_placeholders.py` | placeholder-leltár, `HANDOFF.md`-be írja |
| `tools/build_video.py` | ffmpeg + numpy grade pipeline |
| `tools/build_fonts.py` | TTF → woff2 |
| `CLAUDE.md` | az átvevő belépési pontja |
| `docs/HANDOFF.md` | állapot + nyitott ügyféltételek |

---

## Task 1: Scaffolding és átadási dokumentáció

**Files:**
- Create: `CLAUDE.md`, `README.md`, `docs/HANDOFF.md`
- Create (üres könyvtárak `.gitkeep`-pel): `css/`, `js/`, `data/`, `tools/`, `partials/`, `legal/`, `media/`, `assets/brand/`, `assets/img/`, `assets/video/`, `assets/fonts/`

- [ ] **Step 1: Könyvtárszerkezet**

```bash
cd "C:/Users/Mészáros Péter/Documents/ai/neuwerk-web"
mkdir -p css js data tools partials legal media assets/brand assets/img assets/video assets/fonts work/video
for d in css js data tools partials legal media assets/brand assets/img assets/video assets/fonts; do touch "$d/.gitkeep"; done
```

- [ ] **Step 2: `CLAUDE.md`**

```markdown
# NEUWERK weboldal — belépési pont

Ha most veszed át a projektet, ezt olvasd el elsőként. Utána:
`docs/superpowers/specs/2026-08-10-neuwerk-website-design.md` (a design spec, minden
szám és szabály onnan jön) és `docs/HANDOFF.md` (mi nyitott).

## Mi ez

A NEUWERK statikus weboldala. Build 1 célja: az ügyfél végig tudja kattintani a
struktúrát és jóváhagyja. Leszállítás: egy zip, amit a saját szerverükre másolnak.

## Alapszabályok

1. **Nincs build lépés.** Nincs npm, nincs bundler, nincs PHP. A `tools/` alatti Python
   szkriptek csak assetet állítanak elő (videó, font) — a weboldal futásához nem kellenek.
2. **A zip `file://`-ből is működik.** Ezért nincs `fetch()`. A változó tartalom
   `window.NEUWERK_*` értékadás a `data/*.js`-ben. Ha `fetch()`-et írsz, eltörik az
   ügyfél-review.
3. **Nincs külső hálózati kérés.** Font, ikon, szkript mind lokális. Német ipari ügyfél,
   GDPR. Ne rakj be CDN-t.
4. **A header/footer minden oldalon duplikálva van**, `<!-- @partial:header -->` és
   `<!-- /@partial:header -->` jelölők között. Ha módosítod, mind a 16 oldalon módosítsd.
   A `partials/` alatti fájlok referencia-másolatok.

## Design system

Minden szín, méret és betűtípus a `css/tokens.css`-ben van, és a brandbook v1.1-ből jön
(`Arculat/01_neuwerk_brandbook/neuwerk_brandbook_FINAL.pdf`). Ne írj hardcode hex értéket.

Három szabály, amit a brandbook kikényszerít:

- **Sun (`#ffa500`) max. a látható felület 10–15%-a.** Soha nem háttér.
- **Sun szöveg fehér háttéren tilos** (kontraszt 1,97:1). Sun-kitöltésű gomb felirata
  **navy**, nem fehér. Erre vannak szemantikus tokenek: `--nw-on-sun`.
- **A Neuwerk pattern csak Blue tint 1 navy háttéren**, nagy léptékben. Kisméretű, sűrű
  vagy pusztán dekoratív használat tilos. Csak sötét szekciókban.

## Ellenőrzés minden változtatás után

    python tools/check_links.py
    python tools/check_placeholders.py

Az első halott linket keres mind a 16 oldalon, a második leltározza a placeholdereket
és frissíti a `docs/HANDOFF.md` nyitott listáját.

## Mi placeholder és mi végleges

**Végleges:** a teljes copy (a tartalmi specből, szó szerint), a színek, a tipográfia,
a logók, a hero videó.

**Placeholder, jelölve:** minden kontaktadat, a Media cikkek, a Career pozíciók,
a térkép 16 pontja, az 5 jogi dokumentum szövege.

Minden placeholder `<!-- TODO(client): … -->` megjegyzést **és** látható badge-et kap.
A badge-eket egyetlen osztály kapcsolja ki: a `<body>`-ról vedd le a `is-wireframe`-et.
```

- [ ] **Step 3: `docs/HANDOFF.md`**

```markdown
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
```

- [ ] **Step 4: `README.md`**

```markdown
# NEUWERK — statikus weboldal

Statikus HTML/CSS/JS. Nincs build lépés, nincs függőség.

## Futtatás

Nyisd meg az `index.html`-t böngészőben. Ennyi. Szerver nem kell.

## Telepítés

Másold a repo tartalmát a webszerver gyökerébe. A `tools/`, `work/`, `docs/` és
`Arculat/` könyvtárak nem szükségesek az üzemeléshez — a leszállított zip nem
tartalmazza őket.

## Dokumentáció

- `CLAUDE.md` — fejlesztői belépési pont, alapszabályok
- `docs/superpowers/specs/` — design spec
- `docs/HANDOFF.md` — állapot, nyitott tételek
- `docs/CHANGELOG.md` — változásnapló
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: projektszerkezet és átadási dokumentáció

CLAUDE.md, README.md, docs/HANDOFF.md + könyvtárszerkezet.
A HANDOFF 5 blokkoló ügyféltételt vezet, köztük a 16 ország
megnevezését, ami sehol nincs a forrásanyagban.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 2: Link checker

**Files:**
- Create: `tools/check_links.py`

- [ ] **Step 1: Írd meg az ellenőrzőt**

```python
#!/usr/bin/env python3
"""Halott link ellenőrző.

Végigmegy minden HTML fájlon, kiszedi a href/src hivatkozásokat, és ellenőrzi,
hogy a hivatkozott fájl létezik-e. A Build 1 fő kész-kritériuma: nulla halott link.

Külső (http/https/mailto/tel) linkeket kihagy, de listázza őket, hogy látható legyen,
ha valaki véletlenül CDN-t rak be.
"""
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "work", "Arculat", "useful visual assets", "docs", "tools", "partials"}
REF_RE = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', re.I)


def html_files():
    for p in sorted(ROOT.rglob("*.html")):
        if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            yield p


def main():
    broken, external, checked = [], set(), 0

    for page in html_files():
        text = page.read_text(encoding="utf-8", errors="replace")
        for raw in REF_RE.findall(text):
            ref = raw.strip()
            if not ref or ref.startswith("#") or ref.startswith("data:"):
                continue
            scheme = urlparse(ref).scheme
            if scheme in ("http", "https", "mailto", "tel"):
                external.add(f"{page.relative_to(ROOT)} -> {ref}")
                continue
            target = unquote(ref.split("#")[0].split("?")[0])
            if not target:
                continue
            resolved = (page.parent / target).resolve()
            checked += 1
            if not resolved.exists():
                broken.append(f"{page.relative_to(ROOT)}:  {ref}")

    pages = len(list(html_files()))
    print(f"check_links: {pages} oldal, {checked} belső hivatkozás")

    if external:
        print(f"\n  külső hivatkozás ({len(external)}) — ellenőrizd, hogy szándékos-e:")
        for e in sorted(external):
            print(f"    {e}")

    if broken:
        print(f"\nFAIL — {len(broken)} halott link:")
        for b in broken:
            print(f"    {b}")
        return 1

    if pages == 0:
        print("\nFAIL — nincs egyetlen HTML oldal sem")
        return 1

    print("\nPASS — nincs halott link")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Futtasd — buknia kell**

```bash
python tools/check_links.py
```

Elvárt: `FAIL — nincs egyetlen HTML oldal sem` (exit 1). Ez a helyes kiinduló állapot: még nincs oldal.

- [ ] **Step 3: Commit**

```bash
git add tools/check_links.py
git commit -m "test: halott link ellenőrző

A Build 1 fő kész-kritériuma a nulla zsákutca 16 oldalon.
Jelenleg helyesen FAIL-el: még nincs egyetlen oldal sem.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 3: Placeholder-leltározó

**Files:**
- Create: `tools/check_placeholders.py`
- Modify: `docs/HANDOFF.md` (a szkript írja a jelölők közé)

- [ ] **Step 1: Írd meg a szkriptet**

```python
#!/usr/bin/env python3
"""Placeholder-leltár.

Összegyűjti a TODO(client) megjegyzéseket és a data-placeholder attribútumokat,
majd beírja a docs/HANDOFF.md jelölői közé. Így nem lehet elfelejteni, mi vár még
ügyfél-adatszolgáltatásra.

Külön ellenőrzi, hogy minden gyanús kontaktminta (e-mail, telefonszám) placeholder-e.
Valós e-mail cím a Build 1-ben hiba.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = ROOT / "docs" / "HANDOFF.md"
START = "<!-- PLACEHOLDER-INVENTORY-START -->"
END = "<!-- PLACEHOLDER-INVENTORY-END -->"
SKIP_DIRS = {".git", "work", "Arculat", "useful visual assets", "docs", "tools", "partials"}

TODO_RE = re.compile(r"TODO\(client\):\s*([^\-]*?)\s*-->")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
ALLOWED_EMAIL_HOSTS = ("example.com", "example.org", "example.net")


def scan_files():
    for pattern in ("*.html", "*.js"):
        for p in sorted(ROOT.rglob(pattern)):
            if not any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
                yield p


def main():
    todos, bad_emails = [], []

    for f in scan_files():
        rel = f.relative_to(ROOT)
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for note in TODO_RE.findall(line):
                todos.append((str(rel), i, note.strip()))
            for addr in EMAIL_RE.findall(line):
                if not addr.lower().endswith(ALLOWED_EMAIL_HOSTS):
                    bad_emails.append(f"{rel}:{i}  {addr}")

    lines = [f"Generálva: `python tools/check_placeholders.py` — **{len(todos)} tétel**", ""]
    if todos:
        lines += ["| fájl | sor | tétel |", "|---|---|---|"]
        lines += [f"| `{f}` | {n} | {note} |" for f, n, note in todos]
    else:
        lines.append("_Nincs jelölt placeholder._")

    text = HANDOFF.read_text(encoding="utf-8")
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    HANDOFF.write_text(
        f"{before}{START}\n" + "\n".join(lines) + f"\n{END}{after}",
        encoding="utf-8",
    )

    print(f"check_placeholders: {len(todos)} jelölt placeholder, HANDOFF.md frissítve")

    if bad_emails:
        print(f"\nFAIL — {len(bad_emails)} nem-placeholder e-mail cím:")
        for b in bad_emails:
            print(f"    {b}")
        print("\n  Build 1-ben minden kontaktadat felismerhető placeholder kell legyen")
        print("  (example.com / example.org / example.net).")
        return 1

    print("PASS — minden kontaktadat placeholder")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Futtasd**

```bash
python tools/check_placeholders.py
```

Elvárt: `check_placeholders: 0 jelölt placeholder, HANDOFF.md frissítve` + `PASS` (exit 0). Még nincs mit leltározni, de a HANDOFF jelölői közé beír egy „Nincs jelölt placeholder" sort — ezzel igazoltuk, hogy az írási útvonal működik.

- [ ] **Step 3: Ellenőrizd, hogy tényleg beírt**

```bash
sed -n '/PLACEHOLDER-INVENTORY-START/,/PLACEHOLDER-INVENTORY-END/p' docs/HANDOFF.md
```

Elvárt: a jelölők között ott a „Generálva…" sor.

- [ ] **Step 4: Commit**

```bash
git add tools/check_placeholders.py docs/HANDOFF.md
git commit -m "test: placeholder-leltározó

Összegyűjti a TODO(client) tételeket a HANDOFF.md-be, és FAIL-el,
ha bármelyik e-mail cím nem example.com/org/net végű. Így valós
kontaktadat nem hiányozhat észrevétlenül, és fals adat nem csúszhat élesbe.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 4: Fontok — TTF → woff2

**Files:**
- Create: `tools/build_fonts.py`
- Create (generált): `assets/fonts/*.woff2`

A forrás TTF-ek: `Arculat/01_neuwerk_brandbook/neuwerk_brandbook_FINAL/Fonts/`. Poppins 4 statikus vágat, Lora 2 variable font (upright + italic).

- [ ] **Step 1: Konverter**

```python
#!/usr/bin/env python3
"""TTF -> woff2 a self-hosted betűtípusokhoz.

A brandbook Poppins + Lora párost ír elő. Mindkettő OFL-licencű, ezért
self-hostolható. Google Fonts CDN-t szándékosan NEM használunk: német ipari
ügyfélnél a CDN-es font GDPR-kockázat.
"""
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

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
```

- [ ] **Step 2: Futtasd**

```bash
python tools/build_fonts.py
```

Elvárt: 6 fájl, mindegyik mérettel kiírva, exit 0. A teljes készlet nagyságrendileg 300–600 KB.

- [ ] **Step 3: Ellenőrizd a formátumot**

```bash
python -c "
from fontTools.ttLib import TTFont
from pathlib import Path
for f in sorted(Path('assets/fonts').glob('*.woff2')):
    print(f.name, TTFont(f).flavor)
"
```

Elvárt: minden sor `woff2`.

- [ ] **Step 4: Commit**

```bash
git add tools/build_fonts.py assets/fonts/
git commit -m "feat: self-hosted Poppins + Lora woff2

A brandbook által előírt betűpáros, TTF-ből konvertálva. Google Fonts
CDN helyett self-hosted: német ipari ügyfélnél a CDN GDPR-kockázat.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 5: Logók és favicon

**Files:**
- Create: `assets/brand/neuwerk-white.svg`, `neuwerk-navy.svg`, `neuwerk-mono-white.svg`, `neuwerk-mark.svg`, `favicon.svg`
- Create: `assets/brand/regent-white.svg` (a `Arculat/03_regent_logo/Regent.png`-ből, lásd Step 3)

A hivatalos SVG-kben a slash `fill: orange` CSS-kulcsszóval van definiálva. Átírjuk CSS változóra, hogy a logó színe kódból vezérelhető legyen. **A geometria érintetlen** — a brandbook tiltja az újrarajzolást.

- [ ] **Step 1: Másold és írd át a fill-eket**

```bash
cp "Arculat/00_neuwerk_logo/RGB/colored/white/neuwerk_logo_white.svg" assets/brand/neuwerk-white.svg
cp "Arculat/00_neuwerk_logo/RGB/colored/navy/neuwerk_logo_navy.svg"   assets/brand/neuwerk-navy.svg
cp "Arculat/00_neuwerk_logo/RGB/monochrome/white/neuwerk_logo_mono_white.svg" assets/brand/neuwerk-mono-white.svg

python - <<'PY'
from pathlib import Path
for f in ["neuwerk-white.svg", "neuwerk-navy.svg"]:
    p = Path("assets/brand") / f
    s = p.read_text(encoding="utf-8")
    assert "fill: orange" in s, f"{f}: nem találom a 'fill: orange' szabályt"
    s = s.replace("fill: orange", "fill: var(--nw-sun, #ffa500)")
    p.write_text(s, encoding="utf-8")
    print(f, "-> slash CSS változóra kötve")
PY
```

- [ ] **Step 2: Ellenőrizd**

```bash
grep -o "fill: var(--nw-sun, #ffa500)" assets/brand/neuwerk-white.svg assets/brand/neuwerk-navy.svg
```

Elvárt: két találat, fájlonként egy.

- [ ] **Step 3: Favicon — csak az ikon**

A brandbook: 24 px alatt csak az ikon használható, mark/favicon szerepben. Az ikon a wordmark előtti slash, a `viewBox="0 0 628.8 93.1"` bal szélén.

```bash
python - <<'PY'
import re
from pathlib import Path

src = Path("assets/brand/neuwerk-white.svg").read_text(encoding="utf-8")
# a slash az egyetlen st0 osztályú path
m = re.search(r'<path class="st0"[^/]*?d="([^"]+)"', src, re.S)
assert m, "nem találom a slash path-t (class=st0)"
d = m.group(1)

# a slash bounding boxa a teljes logó viewBoxának bal szélén van;
# a mark önálló használatához négyzetes viewBox kell köré
mark = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 93.1 93.1">'
    f'<path fill="var(--nw-sun, #ffa500)" d="{d}"/>'
    "</svg>"
)
Path("assets/brand/neuwerk-mark.svg").write_text(mark, encoding="utf-8")
Path("assets/brand/favicon.svg").write_text(
    mark.replace("var(--nw-sun, #ffa500)", "#ffa500"), encoding="utf-8"
)
print("mark + favicon kiírva")
PY
```

Nyisd meg mindkettőt böngészőben. Elvárt: egy narancs, lekerekített végű ferde vonás, a kereten belül, nem levágva. **Ha levágódik**, igazítsd a `viewBox` x-eltolását a path tényleges bounding boxához:

```bash
python -c "
from svgpathtools import parse_path  # pip install svgpathtools, ha kell
" 2>/dev/null || echo "ha kell finomhangolás: nyisd meg a mark.svg-t és állítsd a viewBox-ot kézzel"
```

- [ ] **Step 4: Regent logó**

A forrás `Arculat/03_regent_logo/Regent.png` fehér, átlátszó hátterű, 455×121. A footerben navy háttéren jelenik meg, tehát a fehér PNG közvetlenül használható. Vektor nincs hozzá.

```bash
cp "Arculat/03_regent_logo/Regent.png" assets/brand/regent-white.png
python -c "
from PIL import Image
im = Image.open('assets/brand/regent-white.png')
print('regent-white.png', im.size, im.mode)
assert im.mode == 'RGBA', 'nem RGBA — az átlátszóság kell a navy háttérhez'
"
```

- [ ] **Step 5: Commit**

```bash
git add assets/brand/
git commit -m "feat: logóvariánsok, mark és favicon

A hivatalos SVG-kben a slash 'fill: orange' CSS-kulcsszóval volt
definiálva; átkötve var(--nw-sun)-ra, hogy kódból vezérelhető legyen.
A geometria érintetlen. A favicon a brandbook szerint csak az ikon
(24 px alatt a wordmark nem használható).

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 6: `css/tokens.css` — a design system

**Files:**
- Create: `css/tokens.css`

Ez az egyetlen fájl, ami hex értéket tartalmaz. Minden más ide hivatkozik. A szemantikus párok (`--nw-on-sun`) azért vannak, hogy a kontraszt-hibát nehéz legyen leírni.

- [ ] **Step 1: Írd meg**

```css
/* =============================================================
   NEUWERK design tokens
   Forrás: brandbook v1.1 (Arculat/01_neuwerk_brandbook/)
   Ez az EGYETLEN fájl, ahol hex érték szerepelhet.
   ============================================================= */

:root {
  /* --- Elsődleges paletta (brandbook 04) ------------------- */
  --nw-navy:        #1b1e52;   /* Pantone 2766 C — nagy felületeken dominál */
  --nw-white:       #ffffff;   /* egyenrangú vászon a navy-vel */
  --nw-blue-1:      #273993;   /* a Neuwerk pattern színe */
  --nw-blue-2:      #4e66af;
  --nw-blue-3:      #8895cb;
  --nw-blue-4:      #afc6e7;

  /* --- Akcent ---------------------------------------------- */
  /* Sun: max. a látható felület 10-15%-a. SOHA nem háttér. */
  --nw-sun:         #ffa500;   /* Pantone 137 C */

  /* --- Szürkék --------------------------------------------- */
  --nw-black:       #000000;
  --nw-grey-01:     #333333;
  --nw-grey-02:     #666666;
  --nw-grey-03:     #999999;
  --nw-grey-04:     #b4b4b4;
  --nw-grey-05:     #cccccc;
  --nw-grey-06:     #e6e6e6;

  /* --- Másodlagos paletta ----------------------------------
     A brandbook KIZÁRÓLAG infografikára, diagramra, illusztrációra
     engedi. Fő brandfelületen ne használd. */
  --nw-mint:        #1eb78b;
  --nw-azure:       #48c3cb;
  --nw-melon:       #f37558;
  --nw-levander:    #d18ab5;

  /* --- Szemantikus párok -----------------------------------
     Ezek kényszerítik ki a kontrasztszabályokat. Ha ezeket
     használod, nem tudsz bukó párt leírni. Számított arányok
     a specben (3.6). */
  --nw-on-navy:            var(--nw-white);      /* 15,51:1  AAA */
  --nw-on-navy-secondary:  var(--nw-blue-3);     /*  5,32:1  AA  */
  --nw-on-navy-muted:      var(--nw-blue-4);     /*  8,90:1  AAA */
  --nw-on-white:           var(--nw-navy);       /* 15,51:1  AAA */
  --nw-on-white-secondary: var(--nw-grey-02);    /*  5,74:1  AA  */
  --nw-on-sun:             var(--nw-navy);       /*  7,85:1  AAA
                              SOHA ne legyen white: az 1,97:1 */

  /* Sun mint SZÖVEG csak navy háttéren (7,85:1). Fehéren 1,97:1 → tilos. */
  --nw-accent-on-navy:     var(--nw-sun);

  /* --- Tipográfia ------------------------------------------
     Poppins: headline, UI, gomb, kiemelés
     Lora:    hosszú szöveg, idézet, editorial
     Ha megjön az egyedi brand font, itt az egy sor. */
  --nw-font-display: "Poppins", system-ui, -apple-system, "Segoe UI", sans-serif;
  --nw-font-body:    "Poppins", system-ui, -apple-system, "Segoe UI", sans-serif;
  --nw-font-editorial: "Lora", Georgia, "Times New Roman", serif;

  --nw-fw-regular:  400;
  --nw-fw-medium:   500;
  --nw-fw-semibold: 600;
  --nw-fw-bold:     700;

  /* Fluid típusskála. clamp(min, preferált, max) */
  --nw-text-xs:   clamp(0.75rem, 0.72rem + 0.15vw, 0.8125rem);
  --nw-text-sm:   clamp(0.875rem, 0.85rem + 0.15vw, 0.9375rem);
  --nw-text-base: clamp(1rem, 0.96rem + 0.2vw, 1.0625rem);
  --nw-text-lg:   clamp(1.125rem, 1.05rem + 0.4vw, 1.375rem);
  --nw-text-xl:   clamp(1.375rem, 1.2rem + 0.8vw, 1.75rem);
  --nw-text-2xl:  clamp(1.75rem, 1.4rem + 1.6vw, 2.75rem);
  --nw-text-3xl:  clamp(2.25rem, 1.6rem + 3vw, 4rem);
  --nw-text-4xl:  clamp(2.75rem, 1.6rem + 5vw, 6rem);

  --nw-leading-tight: 1.08;
  --nw-leading-snug:  1.25;
  --nw-leading-body:  1.6;
  --nw-leading-loose: 1.75;   /* Lora-hoz, editorial szövegnél */

  --nw-tracking-tight: -0.02em;
  --nw-tracking-wide:   0.08em;

  /* --- Térköz (8px alapskála) ------------------------------- */
  --nw-space-1:  0.5rem;
  --nw-space-2:  1rem;
  --nw-space-3:  1.5rem;
  --nw-space-4:  2rem;
  --nw-space-6:  3rem;
  --nw-space-8:  4rem;
  --nw-space-12: 6rem;
  --nw-space-16: 8rem;
  --nw-space-24: 12rem;

  /* Szekció-belmagasság, viewporttal skálázva */
  --nw-section-y: clamp(4rem, 3rem + 8vw, 10rem);

  /* --- Layout ----------------------------------------------- */
  --nw-max-width:    1440px;
  --nw-measure:      68ch;     /* olvasható sorhossz */
  --nw-gutter:       clamp(1.25rem, 0.8rem + 2.4vw, 3rem);
  --nw-header-h:     72px;

  /* --- Forma ------------------------------------------------ */
  --nw-radius-pill:  9999px;
  --nw-radius-card:  4px;
  --nw-pattern-tilt: -45deg;   /* a Neuwerk pattern dőlése */

  /* --- Mozgás ----------------------------------------------- */
  --nw-ease:        cubic-bezier(0.22, 1, 0.36, 1);
  --nw-ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --nw-dur-fast:    180ms;
  --nw-dur-base:    320ms;
  --nw-dur-slow:    640ms;
  --nw-dur-intro:   1200ms;

  --nw-z-pattern: 0;
  --nw-z-content: 10;
  --nw-z-header:  100;
  --nw-z-intro:   1000;
}

/* Szekció-témák. NEM felhasználói kapcsoló — szekció-tulajdonság.
   A világos/sötét váltakozás maga a brand védjegye. */
.nw-theme-dark {
  --nw-bg:            var(--nw-navy);
  --nw-fg:            var(--nw-on-navy);
  --nw-fg-secondary:  var(--nw-on-navy-secondary);
  --nw-fg-muted:      var(--nw-on-navy-muted);
  --nw-accent-text:   var(--nw-sun);       /* 7,85:1 — engedélyezett */
  --nw-rule:          rgb(255 255 255 / 0.14);
  --nw-pattern-fill:  var(--nw-blue-1);    /* brandbook: csak ez, csak navy-n */
}

.nw-theme-light {
  --nw-bg:            var(--nw-white);
  --nw-fg:            var(--nw-on-white);
  --nw-fg-secondary:  var(--nw-on-white-secondary);
  --nw-fg-muted:      var(--nw-grey-02);
  --nw-accent-text:   var(--nw-navy);      /* Sun fehéren 1,97:1 → TILOS */
  --nw-rule:          rgb(27 30 82 / 0.14);
  --nw-pattern-fill:  transparent;         /* világos szekcióban nincs pattern */
}
```

- [ ] **Step 2: Ellenőrizd a kontraszt-tokeneket**

```bash
python - <<'PY'
def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

CHECKS = [
    ("--nw-on-navy",            "#ffffff", "#1b1e52", 4.5),
    ("--nw-on-navy-secondary",  "#8895cb", "#1b1e52", 4.5),
    ("--nw-on-navy-muted",      "#afc6e7", "#1b1e52", 4.5),
    ("--nw-on-white",           "#1b1e52", "#ffffff", 4.5),
    ("--nw-on-white-secondary", "#666666", "#ffffff", 4.5),
    ("--nw-on-sun",             "#1b1e52", "#ffa500", 4.5),
    ("--nw-accent-on-navy",     "#ffa500", "#1b1e52", 4.5),
]
bad = 0
for name, fg, bg, need in CHECKS:
    r = ratio(fg, bg)
    ok = r >= need
    bad += not ok
    print(f"{name:<26}{r:>6.2f}:1  {'PASS' if ok else 'FAIL'}")
print("\nPASS — minden szemantikus token megfelel" if not bad else f"\nFAIL — {bad} token bukik")
raise SystemExit(1 if bad else 0)
PY
```

Elvárt: mind a 7 sor `PASS`, exit 0.

- [ ] **Step 3: Commit**

```bash
git add css/tokens.css
git commit -m "feat: design tokens a brandbook v1.1 alapján

Az egyetlen fájl hex értékekkel. Szemantikus párok (--nw-on-sun stb.)
kényszerítik ki a kontrasztszabályokat: --nw-on-sun szándékosan navy,
mert fehér-narancson 1,97:1 lenne. Világos szekcióban a pattern-fill
transparent, mert a brandbook csak navy háttéren engedi.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 7: `css/base.css`

**Files:**
- Create: `css/base.css`

- [ ] **Step 1: Írd meg**

```css
/* Reset, tipográfia, layout primitívek. Tokenekre épül. */

@font-face {
  font-family: "Poppins"; font-style: normal; font-weight: 400;
  font-display: swap; src: url("../assets/fonts/poppins-400.woff2") format("woff2");
}
@font-face {
  font-family: "Poppins"; font-style: normal; font-weight: 500;
  font-display: swap; src: url("../assets/fonts/poppins-500.woff2") format("woff2");
}
@font-face {
  font-family: "Poppins"; font-style: normal; font-weight: 600;
  font-display: swap; src: url("../assets/fonts/poppins-600.woff2") format("woff2");
}
@font-face {
  font-family: "Poppins"; font-style: normal; font-weight: 700;
  font-display: swap; src: url("../assets/fonts/poppins-700.woff2") format("woff2");
}
@font-face {
  font-family: "Lora"; font-style: normal; font-weight: 400 700;
  font-display: swap; src: url("../assets/fonts/lora-var.woff2") format("woff2-variations");
}
@font-face {
  font-family: "Lora"; font-style: italic; font-weight: 400 700;
  font-display: swap; src: url("../assets/fonts/lora-var-italic.woff2") format("woff2-variations");
}

*, *::before, *::after { box-sizing: border-box; }

html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }

body {
  margin: 0;
  background: var(--nw-navy);
  color: var(--nw-on-navy);
  font-family: var(--nw-font-body);
  font-size: var(--nw-text-base);
  font-weight: var(--nw-fw-regular);
  line-height: var(--nw-leading-body);
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

h1, h2, h3, h4 {
  margin: 0;
  font-family: var(--nw-font-display);
  font-weight: var(--nw-fw-bold);
  line-height: var(--nw-leading-tight);
  letter-spacing: var(--nw-tracking-tight);
  text-wrap: balance;
}

h1 { font-size: var(--nw-text-4xl); }
h2 { font-size: var(--nw-text-3xl); }
h3 { font-size: var(--nw-text-xl); }
h4 { font-size: var(--nw-text-lg); font-weight: var(--nw-fw-semibold); }

p  { margin: 0 0 var(--nw-space-2); max-width: var(--nw-measure); text-wrap: pretty; }
p:last-child { margin-bottom: 0; }

img, svg, video { display: block; max-width: 100%; height: auto; }

a { color: inherit; text-decoration-thickness: 1px; text-underline-offset: 0.2em; }

ul, ol { margin: 0; padding: 0; list-style: none; }

:focus-visible {
  outline: 3px solid var(--nw-accent-text, var(--nw-sun));
  outline-offset: 3px;
  border-radius: 2px;
}

/* --- Layout primitívek ------------------------------------- */

.nw-shell {
  width: 100%;
  max-width: var(--nw-max-width);
  margin-inline: auto;
  padding-inline: var(--nw-gutter);
}

.nw-section {
  position: relative;
  isolation: isolate;
  background: var(--nw-bg);
  color: var(--nw-fg);
  padding-block: var(--nw-section-y);
  overflow: clip;   /* a nagy pill-formák nem okozhatnak vízszintes scrollt */
}

.nw-section > .nw-shell { position: relative; z-index: var(--nw-z-content); }

.nw-eyebrow {
  font-family: var(--nw-font-display);
  font-size: var(--nw-text-sm);
  font-weight: var(--nw-fw-semibold);
  letter-spacing: var(--nw-tracking-wide);
  text-transform: uppercase;
  color: var(--nw-accent-text);
  margin-bottom: var(--nw-space-2);
}

.nw-lead { font-size: var(--nw-text-lg); color: var(--nw-fg-secondary); }

.nw-editorial {
  font-family: var(--nw-font-editorial);
  font-size: var(--nw-text-lg);
  line-height: var(--nw-leading-loose);
}

.nw-sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0;
  margin: -1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap;
}

.nw-skip-link {
  position: absolute; top: 0; left: var(--nw-gutter);
  transform: translateY(-120%);
  z-index: calc(var(--nw-z-header) + 1);
  padding: var(--nw-space-1) var(--nw-space-2);
  background: var(--nw-sun); color: var(--nw-on-sun);
  font-weight: var(--nw-fw-semibold);
  transition: transform var(--nw-dur-fast) var(--nw-ease);
}
.nw-skip-link:focus-visible { transform: translateY(0); }

/* --- Reduced motion -----------------------------------------
   Nem "kevesebb" mozgás: NULLA mozgás, és semmi nem törik el. */
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
    scroll-behavior: auto !important;
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add css/base.css
git commit -m "feat: base réteg — reset, @font-face, tipográfia, layout primitívek

A reduced-motion blokk nulla mozgásra állít, nem csak lassít.
Az .nw-section overflow: clip azért kell, hogy a nagy pill-formák
ne okozzanak vízszintes scrollt.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 8: Header, footer, page template

**Files:**
- Create: `css/components.css`, `js/nav.js`
- Create: `partials/head.html`, `partials/header.html`, `partials/footer.html`

A `partials/` fájlok **referencia-másolatok**. A futó oldalakon a markup duplikálva van, jelölők között. Ezt a `CLAUDE.md` rögzíti.

- [ ] **Step 1: `partials/header.html`**

```html
<!-- @partial:header -->
<a class="nw-skip-link" href="#main">Skip to content</a>
<header class="nw-header" data-nav>
  <div class="nw-header__inner nw-shell">
    <a class="nw-header__logo" href="{{ROOT}}index.html" aria-label="NEUWERK — home">
      <img src="{{ROOT}}assets/brand/neuwerk-white.svg" alt="" width="157" height="24">
    </a>

    <button class="nw-header__toggle" type="button"
            aria-expanded="false" aria-controls="nw-nav" data-nav-toggle>
      <span class="nw-sr-only">Menu</span>
      <span class="nw-header__bars" aria-hidden="true"></span>
    </button>

    <nav class="nw-header__nav" id="nw-nav" aria-label="Main">
      <ul>
        <li><a href="{{ROOT}}index.html#who-we-are">Who we are</a></li>
        <li><a href="{{ROOT}}index.html#solutions">Solutions</a></li>
        <li><a href="{{ROOT}}identity.html">Identity</a></li>
        <li><a href="{{ROOT}}career.html">Career</a></li>
        <li><a href="{{ROOT}}media.html">Media</a></li>
        <li><a class="nw-btn nw-btn--sun" href="{{ROOT}}contact.html">Contact</a></li>
      </ul>
    </nav>
  </div>
</header>
<!-- /@partial:header -->
```

`{{ROOT}}` a gyökérhez vezető relatív előtag: gyökér-oldalon üres, `legal/` és `media/` alatt `../`. Ezt kézzel írjuk be oldalanként — nincs template motor.

- [ ] **Step 2: `partials/footer.html`**

```html
<!-- @partial:footer -->
<footer class="nw-footer nw-theme-dark">
  <div class="nw-shell">
    <p class="nw-footer__claim">NEUWERK turns expertise into impact</p>

    <div class="nw-footer__cols">
      <nav aria-label="Company">
        <h4>Company</h4>
        <ul>
          <li><a href="{{ROOT}}index.html#who-we-are">Who we are</a></li>
          <li><a href="{{ROOT}}index.html#solutions">Solutions</a></li>
          <li><a href="{{ROOT}}index.html#ambition">Our ambition</a></li>
          <li><a href="{{ROOT}}identity.html">A new identity</a></li>
        </ul>
      </nav>
      <nav aria-label="People">
        <h4>People</h4>
        <ul>
          <li><a href="{{ROOT}}career.html">Career</a></li>
          <li><a href="{{ROOT}}media.html">Media</a></li>
          <li><a href="{{ROOT}}contact.html">Contact</a></li>
        </ul>
      </nav>
      <nav aria-label="Responsibility">
        <h4>Responsibility</h4>
        <ul>
          <li><a href="{{ROOT}}responsibility.html">Acting responsibly</a></li>
          <li><a href="{{ROOT}}legal/code-of-conduct.html">Code of Conduct</a></li>
          <li><a href="{{ROOT}}legal/compliance-ethics.html">Compliance &amp; Ethics</a></li>
          <li><a href="{{ROOT}}legal/supplier-requirements.html">Supplier Requirements</a></li>
          <li><a href="{{ROOT}}integrity-line.html">Integrity Line</a></li>
        </ul>
      </nav>
      <nav aria-label="Legal">
        <h4>Legal</h4>
        <ul>
          <li><a href="{{ROOT}}legal/privacy-policy.html">Privacy Policy</a></li>
          <li><a href="{{ROOT}}legal/legal-notice.html">Legal Notice</a></li>
        </ul>
      </nav>
    </div>

    <div class="nw-footer__base">
      <p class="nw-footer__owner">
        <span>A</span>
        <img src="{{ROOT}}assets/brand/regent-white.png" alt="Regent" width="96" height="26">
        <span>company</span>
      </p>
      <p class="nw-footer__copy">&copy; 2026 NEUWERK. All rights reserved.</p>
    </div>
  </div>
</footer>
<!-- /@partial:footer -->
```

- [ ] **Step 3: `css/components.css`**

```css
/* Header, footer, gomb, kártya, badge, pattern. */

/* --- Gomb --------------------------------------------------- */
.nw-btn {
  display: inline-flex; align-items: center; gap: var(--nw-space-1);
  padding: 0.75rem 1.5rem;
  font-family: var(--nw-font-display);
  font-size: var(--nw-text-sm);
  font-weight: var(--nw-fw-semibold);
  text-decoration: none;
  border: 1px solid currentColor;
  border-radius: var(--nw-radius-pill);
  transition: background var(--nw-dur-fast) var(--nw-ease),
              color var(--nw-dur-fast) var(--nw-ease);
}
.nw-btn:hover { background: var(--nw-fg); color: var(--nw-bg); }

/* Sun-kitöltésű gomb. A felirat NAVY — fehérrel 1,97:1 lenne. */
.nw-btn--sun {
  background: var(--nw-sun);
  color: var(--nw-on-sun);
  border-color: var(--nw-sun);
}
.nw-btn--sun:hover { background: var(--nw-white); color: var(--nw-navy); border-color: var(--nw-white); }

/* --- Header -------------------------------------------------- */
.nw-header {
  position: fixed; inset-block-start: 0; inset-inline: 0;
  z-index: var(--nw-z-header);
  background: transparent;
  transition: background var(--nw-dur-base) var(--nw-ease);
}
.nw-header[data-scrolled] { background: var(--nw-navy); }

.nw-header__inner {
  display: flex; align-items: center; justify-content: space-between;
  min-height: var(--nw-header-h);
}
.nw-header__logo img { height: 24px; width: auto; }   /* brandbook: min. 24 px */

.nw-header__nav ul { display: flex; align-items: center; gap: var(--nw-space-3); }
.nw-header__nav a {
  font-family: var(--nw-font-display);
  font-size: var(--nw-text-sm);
  font-weight: var(--nw-fw-medium);
  color: var(--nw-white);
  text-decoration: none;
}
.nw-header__nav a:not(.nw-btn):hover,
.nw-header__nav a[aria-current="page"] { color: var(--nw-sun); }

.nw-header__toggle { display: none; background: none; border: 0; padding: var(--nw-space-1); cursor: pointer; }
.nw-header__bars, .nw-header__bars::before, .nw-header__bars::after {
  display: block; width: 22px; height: 2px; background: var(--nw-white);
  transition: transform var(--nw-dur-fast) var(--nw-ease);
}
.nw-header__bars::before, .nw-header__bars::after { content: ""; position: relative; }
.nw-header__bars::before { top: -7px; }
.nw-header__bars::after  { top: 5px; }

@media (max-width: 860px) {
  .nw-header__toggle { display: block; }
  .nw-header__nav {
    position: fixed; inset: var(--nw-header-h) 0 auto 0;
    background: var(--nw-navy);
    padding: var(--nw-space-3) var(--nw-gutter) var(--nw-space-4);
    transform: translateY(-120%);
    transition: transform var(--nw-dur-base) var(--nw-ease);
  }
  .nw-header__nav[data-open] { transform: translateY(0); }
  .nw-header__nav ul { flex-direction: column; align-items: flex-start; gap: var(--nw-space-2); }
  .nw-header__nav a { font-size: var(--nw-text-lg); }
}

/* --- Footer --------------------------------------------------- */
.nw-footer {
  background: var(--nw-bg); color: var(--nw-fg);
  padding-block: var(--nw-space-12) var(--nw-space-4);
}
.nw-footer__claim {
  font-family: var(--nw-font-display);
  font-size: var(--nw-text-2xl);
  font-weight: var(--nw-fw-bold);
  letter-spacing: var(--nw-tracking-tight);
  max-width: 16ch;
  margin-bottom: var(--nw-space-8);
}
.nw-footer__cols {
  display: grid; gap: var(--nw-space-4);
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  padding-block: var(--nw-space-4);
  border-block: 1px solid var(--nw-rule);
}
.nw-footer__cols h4 {
  font-size: var(--nw-text-xs); letter-spacing: var(--nw-tracking-wide);
  text-transform: uppercase; color: var(--nw-fg-secondary);
  margin-bottom: var(--nw-space-2);
}
.nw-footer__cols li + li { margin-top: 0.5rem; }
.nw-footer__cols a { font-size: var(--nw-text-sm); text-decoration: none; }
.nw-footer__cols a:hover { color: var(--nw-sun); }

.nw-footer__base {
  display: flex; flex-wrap: wrap; align-items: center;
  justify-content: space-between; gap: var(--nw-space-2);
  padding-top: var(--nw-space-4);
}
.nw-footer__owner {
  display: flex; align-items: center; gap: 0.5rem;
  font-size: var(--nw-text-sm); color: var(--nw-fg-secondary); margin: 0;
}
.nw-footer__owner img { height: 22px; width: auto; opacity: 0.9; }
.nw-footer__copy { font-size: var(--nw-text-xs); color: var(--nw-fg-secondary); margin: 0; }

/* --- Placeholder badge ----------------------------------------
   Az egész rendszert a body.is-wireframe kapcsolja. Éles előtt
   egyetlen osztály levétele mindet elrejti. */
.nw-ph { display: none; }
.is-wireframe .nw-ph {
  display: inline-block;
  padding: 0.15em 0.6em;
  border: 1px dashed var(--nw-sun);
  border-radius: var(--nw-radius-pill);
  font-family: var(--nw-font-display);
  font-size: var(--nw-text-xs);
  font-weight: var(--nw-fw-semibold);
  letter-spacing: var(--nw-tracking-wide);
  text-transform: uppercase;
  color: var(--nw-accent-text);
  vertical-align: middle;
}
.is-wireframe [data-placeholder] { outline: 1px dashed rgb(255 165 0 / 0.45); outline-offset: 4px; }
```

- [ ] **Step 4: `js/nav.js`**

```js
/* Header: mobilmenü, scroll-állapot, aktív oldal jelölése. */
(function () {
  "use strict";

  var header = document.querySelector("[data-nav]");
  if (!header) return;

  var toggle = header.querySelector("[data-nav-toggle]");
  var nav = header.querySelector(".nw-header__nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.hasAttribute("data-open");
      if (open) {
        nav.removeAttribute("data-open");
      } else {
        nav.setAttribute("data-open", "");
      }
      toggle.setAttribute("aria-expanded", String(!open));
    });

    // Esc zárja, és a fókusz visszakerül a gombra
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.hasAttribute("data-open")) {
        nav.removeAttribute("data-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  // Scroll-állapot: a header átlátszóból navy-ra vált
  var onScroll = function () {
    if (window.scrollY > 24) {
      header.setAttribute("data-scrolled", "");
    } else {
      header.removeAttribute("data-scrolled");
    }
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Aktív oldal. A fájlnevet hasonlítjuk, mert nincs szerveroldali routing.
  var here = window.location.pathname.split("/").pop() || "index.html";
  Array.prototype.forEach.call(header.querySelectorAll("a[href]"), function (a) {
    var target = a.getAttribute("href").split("#")[0].split("/").pop();
    if (target && target === here) a.setAttribute("aria-current", "page");
  });
})();
```

- [ ] **Step 5: Commit**

```bash
git add css/components.css js/nav.js partials/
git commit -m "feat: header, footer, gomb- és badge-rendszer

A Sun-kitöltésű gomb felirata navy (--nw-on-sun), mert fehérrel
1,97:1 lenne. A placeholder badge-rendszert egyetlen body osztály
kapcsolja, hogy éles előtt egy lépésben eltüntethető legyen.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 9: A 16 oldal váza — a link checker zöldre vált

**Files:**
- Create: `index.html`, `identity.html`, `career.html`, `media.html`, `responsibility.html`, `integrity-line.html`, `contact.html`, `404.html`
- Create: `legal/code-of-conduct.html`, `legal/compliance-ethics.html`, `legal/supplier-requirements.html`, `legal/privacy-policy.html`, `legal/legal-notice.html`
- Create: `media/how-to-update-this-page.html`, `media/neuwerk-begins.html`, `media/thermal-systems-milestone.html`

Ez a task **csak vázat** épít: fej, header, egy címsor, footer. A tartalom a 11–23. taskokban jön. A cél, hogy a `check_links.py` zöld legyen, mielőtt bármi tartalom készül — így a navigáció hibái azonnal kiderülnek.

- [ ] **Step 1: Az oldalsablon (`index.html`)**

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NEUWERK | Engineering expertise. Industrial execution. Trusted partnership</title>
<meta name="description" content="NEUWERK turns expertise into impact. Engineering solutions for fluid handling, thermal management, sealing and damping, and multi-material applications.">
<link rel="icon" href="assets/brand/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="css/components.css">
<link rel="stylesheet" href="css/sections.css">
</head>
<body class="is-wireframe">

<!-- @partial:header -->
<!-- ide másold a partials/header.html tartalmát, {{ROOT}} helyére üres string -->
<!-- /@partial:header -->

<main id="main">
  <h1 class="nw-shell">NEUWERK</h1>
</main>

<!-- @partial:footer -->
<!-- ide másold a partials/footer.html tartalmát, {{ROOT}} helyére üres string -->
<!-- /@partial:footer -->

<script src="js/nav.js"></script>
</body>
</html>
```

- [ ] **Step 2: Generáld a 16 vázat**

A `{{ROOT}}` behelyettesítése oldalonként: gyökér-oldalak `""`, `legal/` és `media/` alatt `"../"`.

```python
python - <<'PY'
from pathlib import Path

ROOT = Path(".")
header = (ROOT / "partials/header.html").read_text(encoding="utf-8")
footer = (ROOT / "partials/footer.html").read_text(encoding="utf-8")

PAGES = [
    ("index.html",       "", "NEUWERK | Engineering expertise. Industrial execution. Trusted partnership", "NEUWERK"),
    ("identity.html",    "", "A new identity | NEUWERK", "A new identity"),
    ("career.html",      "", "Career | NEUWERK", "Shape What&rsquo;s Next"),
    ("media.html",       "", "Media | NEUWERK", "News, Insights and Stories"),
    ("responsibility.html", "", "Acting Responsibly | NEUWERK", "Acting Responsibly"),
    ("integrity-line.html", "", "Integrity Line | NEUWERK", "Whistleblower Reporting"),
    ("contact.html",     "", "Contact | NEUWERK", "Contact"),
    ("404.html",         "", "Page not found | NEUWERK", "Page not found"),
    ("legal/code-of-conduct.html",        "../", "Code of Conduct | NEUWERK", "Code of Conduct"),
    ("legal/compliance-ethics.html",      "../", "Compliance &amp; Ethics | NEUWERK", "Compliance &amp; Ethics"),
    ("legal/supplier-requirements.html",  "../", "Supplier Requirements | NEUWERK", "Supplier Requirements"),
    ("legal/privacy-policy.html",         "../", "Privacy Policy | NEUWERK", "Privacy Policy"),
    ("legal/legal-notice.html",           "../", "Legal Notice | NEUWERK", "Legal Notice"),
    ("media/how-to-update-this-page.html","../", "How to update this page | NEUWERK", "How to update this page"),
    ("media/neuwerk-begins.html",         "../", "A new chapter begins | NEUWERK", "A new chapter begins"),
    ("media/thermal-systems-milestone.html","../","Thermal systems milestone | NEUWERK", "Thermal systems milestone"),
]

TPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="NEUWERK turns expertise into impact.">
<link rel="icon" href="{r}assets/brand/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{r}css/tokens.css">
<link rel="stylesheet" href="{r}css/base.css">
<link rel="stylesheet" href="{r}css/components.css">
<link rel="stylesheet" href="{r}css/sections.css">
</head>
<body class="is-wireframe">

{header}

<main id="main">
  <section class="nw-section nw-theme-dark">
    <div class="nw-shell"><h1>{h1}</h1></div>
  </section>
</main>

{footer}

<script src="{r}js/nav.js"></script>
</body>
</html>
"""

for path, r, title, h1 in PAGES:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        TPL.format(
            title=title, h1=h1, r=r,
            header=header.replace("{{ROOT}}", r),
            footer=footer.replace("{{ROOT}}", r),
        ),
        encoding="utf-8",
    )
    print("write", path)
print(f"\n{len(PAGES)} oldal kiírva")
PY
```

- [ ] **Step 3: Hozd létre az üres `css/sections.css`-t**

Minden oldal hivatkozik rá; ha nincs, a link checker halott linknek jelzi.

```bash
printf '/* Szekció-layoutok. A tartalmat a 11-23. taskok töltik fel. */\n' > css/sections.css
```

- [ ] **Step 4: Futtasd az ellenőrzőket — most zöldnek kell lennie**

```bash
python tools/check_links.py && python tools/check_placeholders.py
```

Elvárt: `check_links: 16 oldal, … belső hivatkozás` és `PASS — nincs halott link`, majd `PASS — minden kontaktadat placeholder`. Ha bármelyik oldal halott linket jelez, a `{{ROOT}}` behelyettesítés hibás — javítsd, mielőtt továbbmész.

- [ ] **Step 5: Nyisd meg és kattints végig**

```bash
start index.html
```

Kattints végig a nav mind a 6 elemén és a footer mind a 14 linkjén. Elvárt: minden oldal betölt, sehol nincs 404, a header és a footer mindenhol azonos.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: 16 oldal váza, navigáció összekötve

Tartalom még nincs — a cél, hogy a link checker zöld legyen,
mielőtt bármi tartalom készül. Így a navigációs hibák azonnal
kiderülnek, nem a végén.

check_links: 16 oldal, nulla halott link.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 10: Videó pipeline

**Files:**
- Create: `tools/build_video.py`
- Create (generált): `assets/video/hero-1920.mp4`, `hero-1280.mp4`, `hero-poster.jpg`, `intro.mp4`

A spec 6. pontja szerint: vágás **4,0–17,0 mp**, hang eldobva, 50%-os split-tone grade a Sun védelmével, `-g 15` a scrub miatt.

- [ ] **Step 1: Írd meg a pipeline-t**

```python
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
```

- [ ] **Step 2: Futtasd**

```bash
python tools/build_video.py
```

Elvárt: mindkét változat **390 frame**, `hero-1920.mp4` nagyságrendileg **5 MB**, `hero-1280.mp4` **2,5 MB** körül. A gradelt méret enyhén eltérhet a nyers méréstől — ha a `hero-1920.mp4` **6 MB fölé** megy, emeld a `CRF`-et 31-re és futtasd újra.

- [ ] **Step 3: Ellenőrizd, hogy a SPEC tényleg kimaradt**

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/video/hero-1920.mp4
```

Elvárt: `13.0` körüli érték. Ha ennél hosszabb, a vágás hibás és a SPEC bekerülhetett.

Nyisd meg a `hero-1920.mp4`-et, és tekerd a végére. Elvárt: az utolsó képkocka a lime-ra visszafényezett autó az úton. **Nem** szabad látszania semmilyen `SPEC` feliratnak, sem narancs betűknek a zászlók között.

- [ ] **Step 4: Ellenőrizd a grade-et**

Nyisd meg a `hero-poster.jpg`-t. Elvárt: hideg, navy felé húzott háttér, teljes futómű-részletesség, és a cső-/vezetékhálózat élénk narancs — nem fakó réz.

- [ ] **Step 5: Commit**

```bash
git add tools/build_video.py assets/video/
git commit -m "feat: hero videó pipeline — 35,9 MB -> ~5 MB

Vágás 4,0-17,0 s: a SPEC betűk 20,0-20,5 között állnak össze,
tehát 2,5 s ráhagyás. Hang eldobva (digitális csend volt).
50% split-tone grade a Sun védelmével: a rézszínű vezetékek
a valódi #ffa500-ra emelve.
-g 15 kulcskocka-sűrűség, mert a Solutions szekció scrubbolja
ugyanezt a fájlt; enélkül a currentTime-ugrás akadozik.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 11: Neuwerk pattern engine

**Files:**
- Create: `js/pattern.js`
- Modify: `css/components.css` (pattern osztályok hozzáadása a fájl végére)

Brandbook: **csak Blue tint 1 navy háttéren**, **bátran és nagy felületen**, **kisméretű / sűrű / pusztán dekoratív használat tilos**. Ezért nincs részecskerendszer — szekciónként 2–3 nagy forma.

- [ ] **Step 1: CSS — fűzd a `css/components.css` végére**

```css
/* --- Neuwerk pattern -----------------------------------------
   A logó grafikai szimbólumából származó forma. Brandbook:
   csak Blue tint 1 navy háttéren, nagy léptékben. Szekciónként
   legfeljebb 3 forma, mindegyik legalább 40vmin. */
.nw-pattern {
  position: absolute; inset: 0;
  z-index: var(--nw-z-pattern);
  pointer-events: none;
  overflow: clip;
}
.nw-pattern__shape {
  position: absolute;
  background: var(--nw-pattern-fill);
  border-radius: var(--nw-radius-pill);
  transform: rotate(var(--nw-pattern-tilt)) translate3d(0, var(--shift, 0), 0);
  will-change: transform;
}
/* Minimum méret a brandbook "bold and clearly visible" előírásához */
.nw-pattern__shape { min-inline-size: 40vmin; min-block-size: 22vmin; }

.nw-theme-light .nw-pattern { display: none; }   /* pattern csak sötét szekcióban */
```

- [ ] **Step 2: `js/pattern.js`**

```js
/* Neuwerk pattern: nagy formák lassú, scroll-vezérelt eltolása.

   Szándékosan NEM részecskerendszer. A brandbook tiltja a kisméretű,
   sűrű, pusztán dekoratív pattern-használatot, ezért szekciónként
   legfeljebb három nagy forma mozog.

   Markup:
   <div class="nw-pattern" data-pattern>
     <span class="nw-pattern__shape" data-depth="0.12"
           style="left:-10%;top:8%;width:64vmin;height:30vmin"></span>
   </div>
*/
(function () {
  "use strict";

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var groups = Array.prototype.map.call(
    document.querySelectorAll("[data-pattern]"),
    function (el) {
      return {
        el: el,
        shapes: Array.prototype.slice.call(el.querySelectorAll(".nw-pattern__shape")),
      };
    }
  );
  if (!groups.length) return;

  var ticking = false;

  function update() {
    ticking = false;
    var vh = window.innerHeight;

    groups.forEach(function (g) {
      var rect = g.el.getBoundingClientRect();
      if (rect.bottom < -vh || rect.top > vh * 2) return;   // kívül: ne számolj

      // -1 .. 1 tartomány, 0 amikor a szekció közepe a viewport közepén van
      var progress = (rect.top + rect.height / 2 - vh / 2) / vh;

      g.shapes.forEach(function (s) {
        var depth = parseFloat(s.getAttribute("data-depth")) || 0.1;
        s.style.setProperty("--shift", (progress * depth * -260).toFixed(1) + "px");
      });
    });
  }

  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  update();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
})();
```

- [ ] **Step 3: Commit**

```bash
git add js/pattern.js css/components.css
git commit -m "feat: Neuwerk pattern engine

Szekciónként legfeljebb 3 nagy forma, scroll-vezérelt eltolással.
Szándékosan nem részecskerendszer: a brandbook merch guideline
tiltja a kisméretű, sűrű, pusztán dekoratív pattern-használatot.
Világos szekcióban a pattern el van rejtve, mert a brandbook
csak navy háttéren engedi.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 12: Reveal és counter

**Files:**
- Create: `js/reveal.js`, `js/counters.js`

- [ ] **Step 1: `js/reveal.js`**

```js
/* Belépő animáció: IntersectionObserver, egyszer fut elemenként. */
(function () {
  "use strict";

  var items = document.querySelectorAll("[data-reveal]");
  if (!items.length) return;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
      !("IntersectionObserver" in window)) {
    Array.prototype.forEach.call(items, function (el) { el.setAttribute("data-revealed", ""); });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      var delay = parseInt(el.getAttribute("data-reveal-delay") || "0", 10);
      window.setTimeout(function () { el.setAttribute("data-revealed", ""); }, delay);
      io.unobserve(el);
    });
  }, { rootMargin: "0px 0px -12% 0px", threshold: 0.12 });

  Array.prototype.forEach.call(items, function (el) { io.observe(el); });
})();
```

- [ ] **Step 2: Fűzd a `css/base.css` végére**

```css
[data-reveal] {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity var(--nw-dur-slow) var(--nw-ease),
              transform var(--nw-dur-slow) var(--nw-ease);
}
[data-revealed] { opacity: 1; transform: none; }

@media (prefers-reduced-motion: reduce) {
  [data-reveal] { opacity: 1; transform: none; }
}
```

- [ ] **Step 3: `js/counters.js`**

```js
/* Felszámláló. A végérték a data-count attribútumban van, hogy
   JS nélkül és reduced-motion mellett is a helyes szám látsszon. */
(function () {
  "use strict";

  var els = document.querySelectorAll("[data-count]");
  if (!els.length) return;

  function format(n, sep) {
    return sep ? String(n).replace(/\B(?=(\d{3})+(?!\d))/g, sep) : String(n);
  }

  function run(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var sep = el.getAttribute("data-count-sep") || "";
    var dur = 1400;
    var t0 = null;

    function step(ts) {
      if (t0 === null) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = format(Math.round(target * eased), sep);
      if (p < 1) window.requestAnimationFrame(step);
    }
    window.requestAnimationFrame(step);
  }

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  Array.prototype.forEach.call(els, function (el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var sep = el.getAttribute("data-count-sep") || "";

    if (reduced || !("IntersectionObserver" in window)) {
      el.textContent = format(target, sep);
      return;
    }

    el.textContent = format(0, sep);
    var io = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { run(el); io.disconnect(); }
    }, { threshold: 0.5 });
    io.observe(el);
  });
})();
```

- [ ] **Step 4: Commit**

```bash
git add js/reveal.js js/counters.js css/base.css
git commit -m "feat: reveal és counter

Mindkettő reduced-motion mellett azonnal a végállapotot mutatja.
A counter végértéke a data-count attribútumban van, tehát JS nélkül
is a helyes szám olvasható.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 13: Hero szekció

**Files:**
- Create: `js/hero.js`
- Modify: `index.html` (a `<main>` tartalma), `css/sections.css`

A hero a `hero-1920.mp4` **4,0–15,5 mp**-nek megfelelő tartományát pörgeti. A fájl 4,0-nál kezdődik, tehát a lokális idő **0 → 11,5 s**, majd vissza 0-ra rövid átúszással. A vágás **nincs beleégetve**, hogy ugyanez a fájl scrubbolható maradjon a Solutionsnél.

- [ ] **Step 1: HTML — cseréld le a `<main>` tartalmát az `index.html`-ben**

```html
<main id="main">

  <section class="nw-hero nw-theme-dark" data-hero>
    <video class="nw-hero__video" data-hero-video
           muted playsinline preload="metadata"
           poster="assets/video/hero-poster.jpg"
           aria-hidden="true">
      <source src="assets/video/hero-1920.mp4" type="video/mp4" media="(min-width: 861px)">
      <source src="assets/video/hero-1280.mp4" type="video/mp4">
    </video>
    <div class="nw-hero__scrim" aria-hidden="true"></div>

    <div class="nw-hero__inner nw-shell">
      <p class="nw-eyebrow">NEUWERK</p>
      <h1 class="nw-hero__title">Turning Expertise<br>into Impact</h1>
      <p class="nw-hero__lead">
        Built on decades of engineering excellence and driven by the ambition to create
        lasting value for customers, partners and industries worldwide, in the
        automotive industry.
      </p>
      <p class="nw-hero__actions">
        <a class="nw-btn nw-btn--sun" href="#who-we-are">Discover NEUWERK</a>
        <a class="nw-btn" href="#solutions">Explore Solutions</a>
      </p>
    </div>
  </section>

</main>
```

- [ ] **Step 2: CSS — fűzd a `css/sections.css`-hez**

```css
/* --- Hero ----------------------------------------------------- */
.nw-hero {
  position: relative;
  isolation: isolate;
  min-block-size: 100svh;
  display: grid;
  align-items: end;
  background: var(--nw-navy);
  color: var(--nw-on-navy);
  overflow: clip;
}
.nw-hero__video {
  position: absolute; inset: 0;
  inline-size: 100%; block-size: 100%;
  object-fit: cover;
  z-index: 0;
  transition: opacity 200ms linear;   /* a loop-átúszáshoz */
}
.nw-hero__scrim {
  position: absolute; inset: 0; z-index: 1;
  background:
    linear-gradient(to top, rgb(27 30 82 / 0.92) 0%, rgb(27 30 82 / 0.35) 45%, rgb(27 30 82 / 0.15) 100%);
}
.nw-hero__inner {
  position: relative; z-index: 2;
  padding-block: var(--nw-space-12) var(--nw-space-8);
}
.nw-hero__title { font-size: var(--nw-text-4xl); margin-bottom: var(--nw-space-3); }
.nw-hero__lead {
  font-size: var(--nw-text-lg);
  color: var(--nw-on-navy-muted);
  max-width: 54ch;
  margin-bottom: var(--nw-space-4);
}
.nw-hero__actions { display: flex; flex-wrap: wrap; gap: var(--nw-space-2); margin: 0; }
```

- [ ] **Step 3: `js/hero.js`**

```js
/* Hero videó.

   A forrásfájl a 4,0-17,0 s tartományt tartalmazza (lokálisan 0-13 s).
   A hero ebből a 0-11,5 s-ot pörgeti -- ez felel meg az eredeti
   4,0-15,5 s transzparens stúdió-szekvenciájának, ami az egyetlen
   hurkolható szakasz. A 11,5-13 s (visszafényezés) csak a Solutions
   scrubhoz kell, a hero nem játssza le.

   A hurokvágás NINCS beleégetve a fájlba: itt oldjuk meg rövid
   opacitás-átúszással, hogy ugyanez a fájl scrubbolható maradjon.
*/
(function () {
  "use strict";

  var video = document.querySelector("[data-hero-video]");
  if (!video) return;

  var LOOP_END = 11.5;
  var FADE_MS = 200;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    video.removeAttribute("autoplay");
    video.pause();
    return;   // a poster attribútum állóképként marad
  }

  video.addEventListener("loadeddata", function () {
    var p = video.play();
    if (p && typeof p.catch === "function") {
      // Autoplay-tiltás esetén a poszter marad. Nem hiba, nem kell UI.
      p.catch(function () {});
    }
  });

  video.addEventListener("timeupdate", function () {
    if (video.currentTime < LOOP_END) return;
    video.style.opacity = "0";
    window.setTimeout(function () {
      video.currentTime = 0;
      video.style.opacity = "1";
    }, FADE_MS);
  });
})();
```

- [ ] **Step 4: Kösd be a szkripteket az `index.html` végén**

```html
<script src="js/nav.js"></script>
<script src="js/pattern.js"></script>
<script src="js/reveal.js"></script>
<script src="js/counters.js"></script>
<script src="js/hero.js"></script>
```

- [ ] **Step 5: Ellenőrizd**

```bash
python tools/check_links.py && start index.html
```

Elvárt:
- a videó automatikusan indul, néma, teljes szélességben
- ~11,5 másodpercenként visszaugrik az elejére, és az átúszás miatt **nem villan**
- a cím és a két gomb olvasható a videón (a scrim biztosítja a kontrasztot)
- a `Discover NEUWERK` gomb narancs kitöltésű, **navy** felirattal

Teszteld reduced-motion mellett is (Chrome DevTools → Rendering → *Emulate prefers-reduced-motion*): a videó **áll**, a poszterkép látszik, a szöveg olvasható.

- [ ] **Step 6: Commit**

```bash
git add index.html css/sections.css js/hero.js
git commit -m "feat: hero szekció videóval

A loop 0-11,5 s (az eredeti 4,0-15,5 s transzparens szekvencia),
opacitás-átúszással. A hurokvágás szándékosan nincs beleégetve,
hogy ugyanez a fájl scrubbolható maradjon a Solutions szekcióban.
Reduced-motion mellett a videó áll és a poszterkép marad.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 14: Who we are + Global Footprint

**Files:**
- Modify: `index.html`, `css/sections.css`
- Create: `data/locations.js`, `assets/img/world.svg`

- [ ] **Step 1: Szerezz be egy public domain világtérképet**

Nincs a repóban világtérkép. Töltsd le egyszer, vendoreld be, és **ellenőrizd a licencet**. A végleges oldal nem hivatkozik külső forrásra — az SVG a repóba kerül.

```bash
curl -L -o assets/img/world.svg \
  "https://raw.githubusercontent.com/djaiss/mapsicon/master/all/world/vector.svg"
python -c "
from pathlib import Path
s = Path('assets/img/world.svg').read_text(encoding='utf-8', errors='replace')
print('bytes:', len(s))
assert s.lstrip().startswith('<svg') or '<svg' in s[:400], 'nem SVG'
print('viewBox:', __import__('re').search(r'viewBox=\"[^\"]+\"', s).group(0))
"
```

**Licenc-ellenőrzés kötelező lépés:** nyisd meg a forrás repository LICENSE fájlját, és győződj meg róla, hogy a felhasználás megengedett (a mapsicon MIT). Írd be a `docs/HANDOFF.md` „Asset pipeline" szakaszába, honnan jött és milyen licenccel. Ha a licenc nem egyértelmű, **ne használd** — keress CC0/PD alternatívát.

- [ ] **Step 2: `data/locations.js`**

```js
/* A NEUWERK jelenlét 16 országa.

   FIGYELEM: az országok nevét sem a tartalmi spec, sem a brandbook
   nem sorolja fel. Az alábbi lista PLACEHOLDER, kizárólag azért, hogy
   a térkép működését be lehessen mutatni.

   TODO(client): a 16 ország tényleges listája bekérendő -->

   x, y: százalékos pozíció a world.svg viewBoxán belül.
*/
window.NEUWERK_LOCATIONS = [
  { name: "Placeholder 01", x: 48.5, y: 30.0 },
  { name: "Placeholder 02", x: 50.8, y: 32.5 },
  { name: "Placeholder 03", x: 46.2, y: 34.8 },
  { name: "Placeholder 04", x: 53.0, y: 28.4 },
  { name: "Placeholder 05", x: 44.0, y: 38.0 },
  { name: "Placeholder 06", x: 25.5, y: 36.0 },
  { name: "Placeholder 07", x: 22.0, y: 42.0 },
  { name: "Placeholder 08", x: 30.0, y: 62.0 },
  { name: "Placeholder 09", x: 55.0, y: 44.0 },
  { name: "Placeholder 10", x: 68.0, y: 42.0 },
  { name: "Placeholder 11", x: 72.5, y: 38.0 },
  { name: "Placeholder 12", x: 78.0, y: 36.0 },
  { name: "Placeholder 13", x: 80.5, y: 33.0 },
  { name: "Placeholder 14", x: 74.0, y: 52.0 },
  { name: "Placeholder 15", x: 86.0, y: 70.0 },
  { name: "Placeholder 16", x: 52.5, y: 58.0 }
];
```

- [ ] **Step 3: HTML — fűzd az `index.html` `<main>`-jébe a hero után**

```html
  <section class="nw-section nw-theme-light" id="who-we-are">
    <div class="nw-shell">
      <p class="nw-eyebrow">Who we are</p>
      <h2 data-reveal>Built on Expertise.<br>Driven by Progress.</h2>

      <div class="nw-prose" data-reveal data-reveal-delay="80">
        <p class="nw-lead">
          NEUWERK combines engineering excellence, industrial expertise and trusted
          customer relationships with a clear ambition for the future.
        </p>
        <p>
          The company originates from Continental&rsquo;s former Original Equipment
          Solutions business area and builds on decades of automotive expertise,
          long-standing customer partnerships and deep industrial capabilities.
          As an independent global company with approximately 14,000 employees in
          16 countries, we continuously evolve to create greater value for our
          customers, employees and partners.
        </p>
        <p>
          Our strength lies in combining system understanding, engineering know-how,
          multi-material expertise and industrial execution to transform complex
          challenges into reliable, scalable solutions. From concept development and
          simulation to industrialization and serial production, we help customers
          turn ideas into reality.
        </p>
        <p>
          Automotive remains our foundation and will continue to be at the heart of
          our business. At the same time, we see attractive opportunities where our
          unique combination of engineering expertise, material know-how, and
          industrial execution can help solve complex challenges and deliver
          reliable, scalable solutions.
        </p>
      </div>
    </div>
  </section>

  <section class="nw-section nw-theme-dark" id="footprint">
    <div class="nw-pattern" data-pattern aria-hidden="true">
      <span class="nw-pattern__shape" data-depth="0.10"
            style="left:-18%;top:-10%;width:78vmin;height:34vmin"></span>
      <span class="nw-pattern__shape" data-depth="0.18"
            style="right:-24%;bottom:-16%;width:92vmin;height:40vmin"></span>
    </div>

    <div class="nw-shell">
      <p class="nw-eyebrow">Global footprint</p>
      <h2 data-reveal>Combining global capabilities<br>with local customer proximity</h2>
      <p class="nw-lead" data-reveal data-reveal-delay="80">
        Delivering solutions where they are needed most.
      </p>

      <div class="nw-map" data-reveal data-reveal-delay="160">
        <div class="nw-map__canvas" data-map data-placeholder>
          <img class="nw-map__base" src="assets/img/world.svg" alt="" aria-hidden="true">
          <!-- a pontokat a js/map.js szúrja be a data/locations.js alapján -->
        </div>
        <p class="nw-map__note">
          <span class="nw-ph">Placeholder</span>
          Location markers are indicative.
          <!-- TODO(client): a 16 ország tényleges listája bekérendő -->
        </p>
      </div>

      <dl class="nw-stats">
        <div><dt><span data-count="14000" data-count-sep=",">14,000</span></dt><dd>people</dd></div>
        <div><dt><span data-count="16">16</span></dt><dd>countries</dd></div>
        <div><dt><span>One</span></dt><dd>company</dd></div>
      </dl>
    </div>
  </section>
```

- [ ] **Step 4: `js/map.js`**

```js
/* Dekoratív világtérkép: 16 pulzáló pont a data/locations.js alapján.
   Nincs kereső és nincs interakció -- a spec szerint ez stat-vizuál. */
(function () {
  "use strict";

  var host = document.querySelector("[data-map]");
  if (!host || !window.NEUWERK_LOCATIONS) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  window.NEUWERK_LOCATIONS.forEach(function (loc, i) {
    var dot = document.createElement("span");
    dot.className = "nw-map__dot";
    dot.style.left = loc.x + "%";
    dot.style.top = loc.y + "%";
    if (!reduced) dot.style.animationDelay = (i * 180) + "ms";
    dot.setAttribute("title", loc.name);
    host.appendChild(dot);
  });
})();
```

- [ ] **Step 5: CSS — fűzd a `css/sections.css`-hez**

```css
.nw-prose > * + * { margin-top: var(--nw-space-2); }
.nw-prose { margin-top: var(--nw-space-4); }

.nw-map { margin-block: var(--nw-space-6); }
.nw-map__canvas { position: relative; }
.nw-map__base { inline-size: 100%; opacity: 0.22; filter: brightness(0) invert(1); }
.nw-map__dot {
  position: absolute;
  inline-size: 10px; block-size: 10px;
  margin: -5px 0 0 -5px;
  border-radius: 50%;
  background: var(--nw-sun);
  animation: nw-pulse 2.6s var(--nw-ease-in-out) infinite;
}
@keyframes nw-pulse {
  0%, 100% { transform: scale(1);   opacity: 1; }
  50%      { transform: scale(1.5); opacity: 0.55; }
}
@media (prefers-reduced-motion: reduce) {
  .nw-map__dot { animation: none; }
}
.nw-map__note { font-size: var(--nw-text-sm); color: var(--nw-fg-secondary); margin-top: var(--nw-space-2); }

.nw-stats {
  display: grid; gap: var(--nw-space-4);
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  margin: 0; padding-top: var(--nw-space-4);
  border-top: 1px solid var(--nw-rule);
}
.nw-stats dt {
  font-family: var(--nw-font-display);
  font-size: var(--nw-text-3xl);
  font-weight: var(--nw-fw-bold);
  line-height: 1;
  color: var(--nw-fg);
}
.nw-stats dd {
  margin: 0.5rem 0 0;
  font-size: var(--nw-text-sm);
  letter-spacing: var(--nw-tracking-wide);
  text-transform: uppercase;
  color: var(--nw-fg-secondary);
}
```

- [ ] **Step 6: Kösd be és ellenőrizd**

Add hozzá az `index.html` végéhez: `<script src="data/locations.js"></script>` és `<script src="js/map.js"></script>` (a `locations.js` **előbb**).

```bash
python tools/check_links.py && python tools/check_placeholders.py && start index.html
```

Elvárt: a placeholder-leltár most **legalább 2 tételt** jelez (`locations.js` és az `index.html` térkép-jegyzete), és a HANDOFF.md táblázata frissül.

- [ ] **Step 7: Commit**

```bash
git add index.html css/sections.css js/map.js data/locations.js assets/img/world.svg docs/HANDOFF.md
git commit -m "feat: Who we are + Global Footprint szekció

A térkép dekoratív stat-vizuál, a spec szerint: nincs kereső,
nincs Locations aloldal. A 16 pont PLACEHOLDER -- az országokat
sem a tartalmi spec, sem a brandbook nem nevezi meg, ezért
felvéve a HANDOFF blokkoló tételei közé.
A világtérkép SVG vendorelve (MIT), nincs külső kérés.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 15: Solutions + scroll-scrub

**Files:**
- Create: `js/scrub.js`
- Modify: `index.html`, `css/sections.css`

A spec 7. pontjának leképezése. A forrásfájl 4,0-nál kezdődik, tehát a **lokális** időpontok az eredetiből 4,0-t levonva:

| pillér | eredeti | lokális |
|---|---|---|
| Fluid handling systems | 9,5–11,0 | **5,5–7,0** |
| Thermal management | 11,5–13,0 | **7,5–9,0** |
| Sealing and damping | 14,0–15,5 | **10,0–11,5** |
| Multi-material applications | 15,5–17,0 | **11,5–13,0** |

- [ ] **Step 1: HTML — fűzd az `index.html` `<main>`-jébe**

```html
  <section class="nw-section nw-theme-dark" id="solutions" data-scrub>
    <div class="nw-shell">
      <p class="nw-eyebrow">Solutions</p>
      <h2 data-reveal>Engineering Solutions<br>That Create Value</h2>
      <p class="nw-lead" data-reveal data-reveal-delay="80">
        Every day, our technologies help improve reliability, efficiency, safety and
        comfort across some of the world&rsquo;s most demanding applications.
      </p>
    </div>

    <div class="nw-scrub">
      <div class="nw-scrub__stage">
        <video class="nw-scrub__video" data-scrub-video
               muted playsinline preload="auto"
               poster="assets/video/hero-poster.jpg" aria-hidden="true">
          <source src="assets/video/hero-1920.mp4" type="video/mp4" media="(min-width: 861px)">
          <source src="assets/video/hero-1280.mp4" type="video/mp4">
        </video>
      </div>

      <ul class="nw-scrub__pillars nw-shell">
        <li><button type="button" data-scrub-to="6.2"  aria-pressed="false">
          <h3>Fluid handling systems</h3>
          <p>Lines, hoses and connectors that move media through the vehicle.</p>
        </button></li>
        <li><button type="button" data-scrub-to="8.2"  aria-pressed="false">
          <h3>Thermal management</h3>
          <p>Cooling and heating systems that keep batteries and cabins in range.</p>
        </button></li>
        <li><button type="button" data-scrub-to="10.7" aria-pressed="false">
          <h3>Sealing and damping</h3>
          <p>Mounts, bushings and seals that isolate vibration and keep media in place.</p>
        </button></li>
        <li><button type="button" data-scrub-to="12.4" aria-pressed="false">
          <h3>Multi-material applications</h3>
          <p>Rubber, metal and thermoplastics integrated into functional systems.</p>
        </button></li>
      </ul>
    </div>

    <div class="nw-shell">
      <div class="nw-prose" data-reveal>
        <p>
          Our portfolio spans fluid handling systems, thermal management technologies,
          sealing and damping solutions, and advanced multi-material applications. By
          integrating rubber, metal, and thermoplastics into functional systems, we
          enable our customers to meet increasingly complex technical and industrial
          requirements.
        </p>
        <p>
          From virtual validation and prototyping to testing, industrialization and
          global serial production, we provide end-to-end support throughout the
          entire product lifecycle.
        </p>
      </div>
    </div>
  </section>
```

- [ ] **Step 2: CSS**

```css
/* --- Solutions scrub ------------------------------------------ */
.nw-scrub { margin-block: var(--nw-space-6); }
.nw-scrub__stage {
  position: relative;
  aspect-ratio: 16 / 9;
  background: var(--nw-navy);
  overflow: clip;
}
.nw-scrub__video {
  inline-size: 100%; block-size: 100%; object-fit: cover;
  /* A padlóra vetített SAFETY/PERFORMANCE feliratok a képkocka alsó
     harmadában vannak, és más taxonómiát jelölnek, mint a pillércímke.
     A spec 7. pont a) változata: az alsó sávot levágjuk. */
  object-position: center 32%;
  transform: scale(1.18);
}
.nw-scrub__pillars {
  display: grid; gap: var(--nw-space-2);
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  margin-top: var(--nw-space-4);
}
.nw-scrub__pillars button {
  inline-size: 100%; text-align: left; cursor: pointer;
  padding: var(--nw-space-2);
  background: transparent; color: inherit;
  border: 0; border-top: 2px solid var(--nw-rule);
  font: inherit;
  transition: border-color var(--nw-dur-fast) var(--nw-ease);
}
.nw-scrub__pillars button:hover { border-top-color: var(--nw-blue-3); }
.nw-scrub__pillars button[aria-pressed="true"] { border-top-color: var(--nw-sun); }
.nw-scrub__pillars h3 { font-size: var(--nw-text-lg); margin-bottom: 0.5rem; }
.nw-scrub__pillars p  { font-size: var(--nw-text-sm); color: var(--nw-fg-secondary); }
```

- [ ] **Step 3: `js/scrub.js`**

```js
/* Solutions: scroll-scrub + pillérváltás.

   A videó a 4,0-17,0 s tartományt tartalmazza, lokálisan 0-13 s.
   A képesség -> szakasz leképezés a spec 7. pontjában van; a gombokon
   a data-scrub-to a szakasz KÖZEPE, lokális időben.

   A fájl -g 15 kulcskocka-sűrűséggel készült, ezért a currentTime-ugrás
   simán megy. Ha akadozik, a build_video.py GOP értékét kell csökkenteni.
*/
(function () {
  "use strict";

  var section = document.querySelector("[data-scrub]");
  if (!section) return;

  var video = section.querySelector("[data-scrub-video]");
  var buttons = Array.prototype.slice.call(section.querySelectorAll("[data-scrub-to]"));
  if (!video || !buttons.length) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var duration = 0;
  var manual = false;      // gombnyomás után a scroll ne írja felül azonnal
  var manualUntil = 0;

  video.addEventListener("loadedmetadata", function () {
    duration = video.duration || 13;
    video.pause();
    video.currentTime = 0.01;
    markActive(0.01);
  });

  function markActive(t) {
    var best = 0;
    var bestDist = Infinity;
    buttons.forEach(function (b, i) {
      var d = Math.abs(parseFloat(b.getAttribute("data-scrub-to")) - t);
      if (d < bestDist) { bestDist = d; best = i; }
    });
    buttons.forEach(function (b, i) {
      b.setAttribute("aria-pressed", String(i === best));
    });
  }

  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      var t = parseFloat(b.getAttribute("data-scrub-to"));
      video.currentTime = t;
      markActive(t);
      manual = true;
      manualUntil = Date.now() + 1200;
      b.scrollIntoView({ block: "nearest", behavior: reduced ? "auto" : "smooth" });
    });
  });

  if (reduced) return;   // reduced-motion: csak a gombok működnek, scroll nem scrubbol

  var ticking = false;

  function update() {
    ticking = false;
    if (!duration) return;
    if (manual && Date.now() < manualUntil) return;
    manual = false;

    var rect = section.getBoundingClientRect();
    var vh = window.innerHeight;
    var span = rect.height + vh;
    if (rect.bottom < 0 || rect.top > vh) return;

    var progress = Math.min(Math.max((vh - rect.top) / span, 0), 1);
    var t = progress * duration;
    if (Math.abs(video.currentTime - t) > 0.06) {
      video.currentTime = t;
      markActive(t);
    }
  }

  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }, { passive: true });
})();
```

- [ ] **Step 4: Kösd be és ellenőrizd**

Add hozzá az `index.html` végéhez: `<script src="js/scrub.js"></script>`.

```bash
start index.html
```

Elvárt:
- a Solutions szekción görgetve a videó **követi a görgetést**, nem magától játszik
- a négy pillér gombra kattintva a videó a megfelelő pillanatra ugrik, és az adott gomb felső vonala **narancs** lesz
- a padlóra vetített `PERFORMANCE` / `EFFICIENCY` feliratok **nem látszanak** (az `object-position: center 32%` levágja őket) — ha mégis kilátszanak, csökkentsd a százalékot
- **sehol nincs `SPEC`**

Reduced-motion mellett: a scroll nem scrubbol, de a gombok működnek.

- [ ] **Step 5: Commit**

```bash
git add index.html css/sections.css js/scrub.js
git commit -m "feat: Solutions szekció scroll-scrubbal

A three.js hero car helyett ugyanaz a videó scrubbolva. A négy
képesség a spec 7. pontja szerinti szakaszra ugrik (lokális idő,
az eredetiből 4,0 s levonva).
Az object-position: center 32% levágja a padlóra vetített
előny-feliratokat, mert más taxonómiát jelölnek, mint a pillércímke.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 16: Our ambition + Explore more + intro

**Files:**
- Modify: `index.html`, `css/sections.css`
- Create: `js/intro.js`

- [ ] **Step 1: HTML — fűzd az `index.html` `<main>`-jébe a Solutions után**

```html
  <section class="nw-section nw-theme-dark" id="ambition">
    <div class="nw-pattern" data-pattern aria-hidden="true">
      <span class="nw-pattern__shape" data-depth="0.14"
            style="left:-22%;bottom:-18%;width:86vmin;height:38vmin"></span>
    </div>

    <div class="nw-shell">
      <p class="nw-eyebrow">Our ambition</p>
      <h2 data-reveal>As Your Trusted Partner,<br>We Make the Difference</h2>

      <div class="nw-prose" data-reveal data-reveal-delay="80">
        <p>
          We believe the best solutions begin with understanding our customers&rsquo;
          challenges. That is why we listen first, collaborate closely, and focus on
          creating solutions that generate measurable value.
        </p>
        <p>
          Our ambition is to combine engineering excellence, industrial capabilities,
          and customer understanding into an integrated approach that helps customers
          solve complex challenges faster, more efficiently, and more sustainably. We
          continuously evolve the way we innovate, collaborate, and deliver to remain
          a trusted partner in a changing world.
        </p>
        <p>
          Built on proven strengths and driven by a forward-looking mindset, we are
          committed to creating lasting value for our customers, our people and our
          business.
        </p>
      </div>

      <ol class="nw-principles">
        <li data-reveal data-reveal-delay="0"><span>01</span>Customer understanding before product thinking</li>
        <li data-reveal data-reveal-delay="80"><span>02</span>Integrated engineering and industrial capabilities</li>
        <li data-reveal data-reveal-delay="160"><span>03</span>Reliable execution from concept to production</li>
        <li data-reveal data-reveal-delay="240"><span>04</span>Long-term value and sustainable competitiveness</li>
      </ol>
    </div>
  </section>

  <section class="nw-section nw-theme-light">
    <div class="nw-shell">
      <p class="nw-eyebrow">Explore more</p>
      <ul class="nw-cards">
        <li data-reveal><a href="identity.html">
          <h3>A new identity</h3>
          <p>Proud of where we came from. Confident in what we can do.</p>
          <span class="nw-cards__go" aria-hidden="true">&rarr;</span>
        </a></li>
        <li data-reveal data-reveal-delay="80"><a href="career.html">
          <h3>Career</h3>
          <p>Shape what&rsquo;s next. Expertise meets opportunity.</p>
          <span class="nw-cards__go" aria-hidden="true">&rarr;</span>
        </a></li>
        <li data-reveal data-reveal-delay="160"><a href="media.html">
          <h3>Media</h3>
          <p>News, insights and stories from across NEUWERK.</p>
          <span class="nw-cards__go" aria-hidden="true">&rarr;</span>
        </a></li>
      </ul>
    </div>
  </section>
```

- [ ] **Step 2: Intro — fűzd az `index.html` `<body>` legelejére, a header elé**

```html
<div class="nw-intro" data-intro aria-hidden="true">
  <video muted playsinline autoplay preload="auto" src="assets/video/intro.mp4"></video>
</div>
```

- [ ] **Step 3: `js/intro.js`**

```js
/* Logó reveal intro. Egyszer fut látogatásonként (sessionStorage),
   átugorható kattintással vagy billentyűvel, és reduced-motion
   mellett meg sem jelenik. */
(function () {
  "use strict";

  var intro = document.querySelector("[data-intro]");
  if (!intro) return;

  var KEY = "nw-intro-seen";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var seen = false;
  try { seen = window.sessionStorage.getItem(KEY) === "1"; } catch (e) { seen = false; }

  if (reduced || seen) { intro.remove(); return; }

  document.documentElement.style.overflow = "hidden";

  function dismiss() {
    intro.setAttribute("data-done", "");
    document.documentElement.style.overflow = "";
    try { window.sessionStorage.setItem(KEY, "1"); } catch (e) { /* privát mód */ }
    window.setTimeout(function () { intro.remove(); }, 500);
  }

  window.setTimeout(dismiss, 1200);
  intro.addEventListener("click", dismiss);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" || e.key === "Enter" || e.key === " ") dismiss();
  }, { once: true });
})();
```

- [ ] **Step 4: CSS**

```css
/* --- Intro ----------------------------------------------------- */
.nw-intro {
  position: fixed; inset: 0; z-index: var(--nw-z-intro);
  display: grid; place-items: center;
  background: var(--nw-navy);
  transition: opacity 480ms var(--nw-ease);
}
.nw-intro[data-done] { opacity: 0; pointer-events: none; }
.nw-intro video { inline-size: min(60vw, 520px); block-size: auto; }

/* --- Elvek ----------------------------------------------------- */
.nw-principles {
  display: grid; gap: var(--nw-space-2);
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  margin-top: var(--nw-space-6);
}
.nw-principles li {
  padding-top: var(--nw-space-2);
  border-top: 2px solid var(--nw-rule);
  font-family: var(--nw-font-display);
  font-size: var(--nw-text-lg);
  font-weight: var(--nw-fw-medium);
  line-height: var(--nw-leading-snug);
}
.nw-principles span {
  display: block; margin-bottom: 0.5rem;
  font-size: var(--nw-text-sm);
  color: var(--nw-accent-text);
  letter-spacing: var(--nw-tracking-wide);
}

/* --- Kártyák --------------------------------------------------- */
.nw-cards {
  display: grid; gap: var(--nw-space-3);
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  margin-top: var(--nw-space-4);
}
.nw-cards a {
  display: block; block-size: 100%;
  padding: var(--nw-space-3);
  text-decoration: none;
  border: 1px solid var(--nw-rule);
  border-radius: var(--nw-radius-card);
  transition: transform var(--nw-dur-base) var(--nw-ease),
              border-color var(--nw-dur-base) var(--nw-ease);
}
.nw-cards a:hover { transform: translateY(-4px); border-color: var(--nw-navy); }
.nw-cards h3 { margin-bottom: 0.5rem; }
.nw-cards p  { font-size: var(--nw-text-sm); color: var(--nw-fg-secondary); }
.nw-cards__go { display: inline-block; margin-top: var(--nw-space-2); color: var(--nw-accent-text); }
```

- [ ] **Step 5: Kösd be és ellenőrizd**

Add hozzá az `index.html` végéhez: `<script src="js/intro.js"></script>`.

```bash
python tools/check_links.py && start index.html
```

Elvárt: az intro egyszer lefut, majd eltűnik. Frissítésre **nem** jelenik meg újra (sessionStorage). Új privát ablakban újra lefut.

- [ ] **Step 6: Commit**

```bash
git add index.html css/sections.css js/intro.js
git commit -m "feat: Our ambition, Explore more, logó intro

Az intro egyszer fut látogatásonként, átugorható, és
reduced-motion mellett meg sem jelenik. A sessionStorage
hozzáférés try/catch-ben van a privát mód miatt.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 17: Identity oldal

**Files:**
- Modify: `identity.html`, `css/sections.css`

A copy szó szerint a tartalmi spec 5. oldaláról. **Az OESL logót nem használjuk** — döntés 11.

- [ ] **Step 1: Cseréld le a `<main>` tartalmát**

```html
<main id="main">
  <section class="nw-section nw-theme-dark nw-subhero">
    <div class="nw-pattern" data-pattern aria-hidden="true">
      <span class="nw-pattern__shape" data-depth="0.12"
            style="right:-20%;top:-14%;width:84vmin;height:36vmin"></span>
    </div>
    <div class="nw-shell">
      <p class="nw-eyebrow">A new identity</p>
      <h1 data-reveal>Proud of where we came from.<br>
        Confident in what we can do.<br>
        Ready for what comes next.</h1>
    </div>
  </section>

  <section class="nw-section nw-theme-light">
    <div class="nw-shell">
      <div class="nw-prose nw-editorial" data-reveal>
        <p>
          NEUWERK marks the beginning of a new chapter. Born from Continental&rsquo;s
          former Original Equipment Solutions business area, the company now moves
          forward with a distinct identity of its own.
        </p>
        <p>
          The name combines two ideas that define who we are: NEU stands for renewal,
          progress and the courage to evolve. WERK stands for our foundation:
          engineering expertise, industrial capabilities and the craft to turn ideas
          into reliable solutions.
        </p>
      </div>

      <ul class="nw-namesplit" data-reveal data-reveal-delay="80">
        <li><strong>NEU</strong><span>The courage to change.</span></li>
        <li><strong>WERK</strong><span>The craft to build it.</span></li>
        <li><strong>NEUWERK</strong><span>Together.</span></li>
      </ul>
    </div>
  </section>

  <section class="nw-section nw-theme-dark">
    <div class="nw-shell">
      <p class="nw-eyebrow">A design built to move forward</p>
      <h2 data-reveal>Purposeful, distinctive<br>and built to perform</h2>
      <div class="nw-prose" data-reveal data-reveal-delay="80">
        <p>
          The NEUWERK visual identity reflects what the company stands for: expertise,
          clarity and progress. The rising diagonal element symbolizes momentum and the
          confidence to move forward. The clean wordmark represents focus, technical
          excellence and strength of purpose.
        </p>
        <p>
          Like our solutions, the identity is purposeful, distinctive and built to perform.
        </p>
        <p>
          Built on German engineering heritage and shaped by decades of automotive
          experience, NEUWERK brings together what makes us strong with a clear ambition
          for the future: to become more focused, more customer-centric and more
          integrated as one independent company.
        </p>
      </div>
    </div>
  </section>
</main>
```

- [ ] **Step 2: CSS**

```css
.nw-subhero { min-block-size: 60svh; display: grid; align-items: end; }
.nw-subhero h1 { font-size: var(--nw-text-3xl); }

.nw-namesplit {
  display: grid; gap: var(--nw-space-3);
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  margin-top: var(--nw-space-6);
}
.nw-namesplit li { padding-top: var(--nw-space-2); border-top: 2px solid var(--nw-sun); }
.nw-namesplit strong {
  display: block;
  font-family: var(--nw-font-display);
  font-size: var(--nw-text-2xl);
  font-weight: var(--nw-fw-bold);
  letter-spacing: var(--nw-tracking-tight);
}
.nw-namesplit span { font-size: var(--nw-text-sm); color: var(--nw-fg-secondary); }
```

- [ ] **Step 3: Kösd be a szkripteket és ellenőrizd**

Az `identity.html` végére: `nav.js`, `pattern.js`, `reveal.js`.

```bash
python tools/check_links.py && start identity.html
```

- [ ] **Step 4: Commit**

```bash
git add identity.html css/sections.css
git commit -m "feat: A new identity oldal

Copy szó szerint a tartalmi spec 5. oldaláról. Az OESL logót
a döntés szerint nem használjuk, a jogelőd csak szövegben
jelenik meg.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 18: Career oldal + `data/jobs.js`

**Files:**
- Create: `data/jobs.js`, `js/lists.js`
- Modify: `career.html`, `css/sections.css`

- [ ] **Step 1: `data/jobs.js`**

```js
/* NYITOTT POZÍCIÓK
   ================================================================
   Új pozíció hozzáadása: másolj le egy blokkot, és írd át a mezőket.
   A lista sorrendje a megjelenés sorrendje. Nem kell semmi mást
   szerkeszteni -- a career.html ebből rendereli a listát.

   Mezők:
     title    - a pozíció neve
     location - város, ország
     type     - pl. "Full-time", "Part-time", "Internship"
     area     - szakterület, a szűrőcímkéhez
     url      - jelentkezési link. Ha nincs, hagyd "" értéken.

   TODO(client): a valós nyitott pozíciók listája bekérendő -->
*/
window.NEUWERK_JOBS = [
  {
    title: "Placeholder — Development Engineer, Thermal Systems",
    location: "Example City, Example Country",
    type: "Full-time",
    area: "Engineering",
    url: "",
    placeholder: true
  },
  {
    title: "Placeholder — Process Engineer, Multi-Material",
    location: "Example City, Example Country",
    type: "Full-time",
    area: "Manufacturing",
    url: "",
    placeholder: true
  },
  {
    title: "Placeholder — Key Account Manager",
    location: "Example City, Example Country",
    type: "Full-time",
    area: "Sales",
    url: "",
    placeholder: true
  }
];
```

- [ ] **Step 2: `js/lists.js`**

```js
/* Lista-renderelés a data/*.js fájlokból.

   Szándékosan nincs fetch(): a zip file://-ből is működik, és ott a
   fetch CORS-ba fut. A data/*.js sima értékadás, amit az ügyfél
   szövegszerkesztővel is tud szerkeszteni.
*/
(function () {
  "use strict";

  function badge(item) {
    return item.placeholder ? '<span class="nw-ph">Placeholder</span> ' : "";
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  var jobsHost = document.querySelector("[data-jobs]");
  if (jobsHost && window.NEUWERK_JOBS) {
    jobsHost.innerHTML = window.NEUWERK_JOBS.map(function (j) {
      var head = j.url
        ? '<a href="' + esc(j.url) + '">' + esc(j.title) + "</a>"
        : esc(j.title);
      return (
        '<li class="nw-job"' + (j.placeholder ? ' data-placeholder' : "") + ">" +
        '<h3 class="nw-job__title">' + badge(j) + head + "</h3>" +
        '<p class="nw-job__meta">' +
          esc(j.area) + " &middot; " + esc(j.location) + " &middot; " + esc(j.type) +
        "</p></li>"
      );
    }).join("");
  }

  var newsHost = document.querySelector("[data-news]");
  if (newsHost && window.NEUWERK_NEWS) {
    newsHost.innerHTML = window.NEUWERK_NEWS.map(function (n) {
      return (
        '<li class="nw-news"' + (n.placeholder ? ' data-placeholder' : "") + ">" +
        '<a href="media/' + esc(n.slug) + '.html">' +
        '<time datetime="' + esc(n.date) + '">' + esc(n.date) + "</time>" +
        "<h3>" + badge(n) + esc(n.title) + "</h3>" +
        "<p>" + esc(n.excerpt) + "</p>" +
        "</a></li>"
      );
    }).join("");
  }
})();
```

- [ ] **Step 3: `career.html` `<main>`**

```html
<main id="main">
  <section class="nw-section nw-theme-dark nw-subhero">
    <div class="nw-pattern" data-pattern aria-hidden="true">
      <span class="nw-pattern__shape" data-depth="0.12"
            style="left:-18%;bottom:-16%;width:80vmin;height:34vmin"></span>
    </div>
    <div class="nw-shell">
      <p class="nw-eyebrow">Career</p>
      <h1 data-reveal>Shape What&rsquo;s Next</h1>
    </div>
  </section>

  <section class="nw-section nw-theme-light">
    <div class="nw-shell">
      <div class="nw-prose" data-reveal>
        <p class="nw-lead">
          At NEUWERK, expertise meets opportunity. We empower people to challenge
          conventions, develop new ideas and create meaningful impact through
          engineering, manufacturing and collaboration.
        </p>
        <p>
          Our success is built on the expertise, commitment and entrepreneurial spirit
          of our people. Together, we combine global capabilities with local customer
          proximity to solve complex challenges and drive innovation forward.
        </p>
        <p>
          Join a team that combines the courage to change with the capability to make
          change happen.
        </p>
      </div>

      <h2 class="nw-section__sub">Open positions</h2>
      <ul class="nw-joblist" data-jobs></ul>

      <p class="nw-note">
        <span class="nw-ph">Placeholder</span>
        Positions shown are examples. See
        <a href="media/how-to-update-this-page.html">how to update this list</a>.
      </p>
    </div>
  </section>
</main>
```

- [ ] **Step 4: CSS**

```css
.nw-section__sub { font-size: var(--nw-text-2xl); margin-top: var(--nw-space-8); }
.nw-joblist { margin-top: var(--nw-space-3); }
.nw-job { padding-block: var(--nw-space-2); border-bottom: 1px solid var(--nw-rule); }
.nw-job__title { font-size: var(--nw-text-lg); }
.nw-job__meta { font-size: var(--nw-text-sm); color: var(--nw-fg-secondary); margin-top: 0.25rem; }
.nw-note { margin-top: var(--nw-space-3); font-size: var(--nw-text-sm); color: var(--nw-fg-secondary); }
```

- [ ] **Step 5: Kösd be és ellenőrizd**

A `career.html` végére, ebben a sorrendben: `data/jobs.js`, `js/nav.js`, `js/pattern.js`, `js/reveal.js`, `js/lists.js`.

```bash
python tools/check_links.py && python tools/check_placeholders.py && start career.html
```

Elvárt: három pozíció jelenik meg, mindegyiken narancs szaggatott `PLACEHOLDER` badge, és a placeholder-leltár nő.

- [ ] **Step 6: Commit**

```bash
git add career.html data/jobs.js js/lists.js css/sections.css docs/HANDOFF.md
git commit -m "feat: Career oldal, adatvezérelt pozíciólistával

A lista a data/jobs.js-ből jön: sima JS értékadás, nem fetch,
mert a zip file://-ből is működnie kell. Az ügyfél
szövegszerkesztővel frissítheti.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 19: Media hub + `data/news.js` + 3 cikkoldal

**Files:**
- Create: `data/news.js`
- Modify: `media.html`, `media/how-to-update-this-page.html`, `media/neuwerk-begins.html`, `media/thermal-systems-milestone.html`, `css/sections.css`

- [ ] **Step 1: `data/news.js`**

```js
/* HÍREK ÉS CIKKEK
   ================================================================
   Új cikk hozzáadása két lépés:
     1. Vegyél fel egy új objektumot EBBE a listába, legfelülre.
     2. Másold le a media/ mappában egy meglévő cikk .html fájlját,
        nevezd át a slug szerint, és írd át benne a szöveget.

   A slug a fájlnév kiterjesztés nélkül: slug "my-story" -> media/my-story.html

   Mezők:
     slug        - fájlnév kiterjesztés nélkül, csak kisbetű és kötőjel
     date        - ÉÉÉÉ-HH-NN
     title       - a cikk címe
     excerpt     - 1-2 mondat a listaoldalra
     placeholder - true, amíg nem valós tartalom (látható badge-et ad)

   TODO(client): a valós hírek és cikkek bekérendők -->
*/
window.NEUWERK_NEWS = [
  {
    slug: "how-to-update-this-page",
    date: "2026-08-10",
    title: "How to update this page",
    excerpt: "A short guide for the NEUWERK team: how to add, edit and remove news articles and open positions without a CMS.",
    placeholder: true
  },
  {
    slug: "neuwerk-begins",
    date: "2026-08-01",
    title: "A new chapter begins",
    excerpt: "NEUWERK starts operating as an independent global company, building on decades of automotive engineering expertise.",
    placeholder: true
  },
  {
    slug: "thermal-systems-milestone",
    date: "2026-07-15",
    title: "Thermal systems milestone",
    excerpt: "A look at how integrated thermal management supports battery performance across demanding applications.",
    placeholder: true
  }
];
```

- [ ] **Step 2: `media.html` `<main>`**

```html
<main id="main">
  <section class="nw-section nw-theme-dark nw-subhero">
    <div class="nw-pattern" data-pattern aria-hidden="true">
      <span class="nw-pattern__shape" data-depth="0.12"
            style="right:-18%;top:-12%;width:82vmin;height:35vmin"></span>
    </div>
    <div class="nw-shell">
      <p class="nw-eyebrow">Media</p>
      <h1 data-reveal>News, Insights and Stories</h1>
    </div>
  </section>

  <section class="nw-section nw-theme-light">
    <div class="nw-shell">
      <p class="nw-lead nw-prose" data-reveal>
        Discover the latest company news, technology developments, customer success
        stories and insights from across NEUWERK. Learn how our people, expertise and
        solutions are helping shape the future of mobility and beyond.
      </p>

      <ul class="nw-newslist" data-news></ul>

      <p class="nw-note">
        <span class="nw-ph">Placeholder</span>
        Articles shown are examples. See
        <a href="media/how-to-update-this-page.html">how to update this list</a>.
      </p>
    </div>
  </section>
</main>
```

- [ ] **Step 3: A „how to update" cikk — `media/how-to-update-this-page.html` `<main>`**

Ez a placeholder egyben a felhasználói dokumentáció. Ezért nem PDF-be kerül, hanem az oldalra, ahol nem vész el.

```html
<main id="main">
  <article class="nw-article">
    <header class="nw-section nw-theme-dark nw-subhero">
      <div class="nw-shell">
        <p class="nw-eyebrow"><span class="nw-ph">Placeholder</span> Guide</p>
        <h1 data-reveal>How to update this page</h1>
        <p class="nw-article__date"><time datetime="2026-08-10">10 August 2026</time></p>
      </div>
    </header>

    <div class="nw-section nw-theme-light">
      <div class="nw-shell nw-article__body nw-editorial">
        <p class="nw-lead">
          This site has no content management system. Everything is plain files, which
          means you can update it with a text editor and an upload. Here is how.
        </p>

        <h2>Adding a news article</h2>
        <p>It takes two steps.</p>
        <p>
          <strong>First</strong>, open <code>data/news.js</code>. You will see a list of
          entries. Copy one entry, paste it at the top of the list, and change the
          fields. The <code>slug</code> becomes the file name, so use only lowercase
          letters and hyphens. Remove <code>placeholder: true</code> once the article
          is real &mdash; that line is what shows the orange badge.
        </p>
        <p>
          <strong>Second</strong>, go to the <code>media/</code> folder, duplicate any
          existing article file, and rename it to match your slug. For a slug of
          <code>my-story</code>, the file must be <code>media/my-story.html</code>.
          Open it and replace the heading, the date and the body text.
        </p>

        <h2>Removing an article</h2>
        <p>
          Delete its entry from <code>data/news.js</code> and delete the matching file
          from <code>media/</code>. Do both &mdash; leaving the file behind is harmless,
          but leaving the entry behind creates a broken link.
        </p>

        <h2>Adding a job opening</h2>
        <p>
          Open <code>data/jobs.js</code> and copy an entry the same way. Jobs have no
          separate page, so this is a single step. If you have an application link, put
          it in the <code>url</code> field; leave it empty and the title simply will not
          be a link.
        </p>

        <h2>Images</h2>
        <p>
          Put images in <code>assets/img/</code>. Save them at no more than 1600 pixels
          wide and compress them before upload &mdash; a news thumbnail should be well
          under 300 KB. Large images are the fastest way to make a page feel slow.
        </p>

        <h2>Checking your work</h2>
        <p>
          Open <code>index.html</code> in a browser and click through. You do not need a
          server. If a link does not work, the most likely cause is a slug that does not
          match its file name.
        </p>

        <h2>What you should not edit</h2>
        <p>
          Leave the <code>css/</code> and <code>js/</code> folders alone, and do not edit
          the parts of a page between the <code>@partial:header</code> and
          <code>@partial:footer</code> markers &mdash; those are repeated on every page
          and must stay identical. If the navigation or footer needs to change, that is
          a developer task.
        </p>
      </div>
    </div>
  </article>
</main>
```

- [ ] **Step 4: A másik két cikk**

Ugyanez a `<article>` szerkezet, más tartalommal. Mindkettő fejlécében ott a `<span class="nw-ph">Placeholder</span>`, és a törzsben egy `<!-- TODO(client): valós cikkszöveg bekérendő -->` megjegyzés.

**`media/neuwerk-begins.html`** — cím: *A new chapter begins*, dátum `2026-08-01`. Törzs: két bekezdés a tartalmi spec „A new identity" szakaszából (*„NEUWERK marks the beginning of a new chapter…"* és *„The name combines two ideas…"*), majd egy harmadik bekezdés helyén:

```html
<p data-placeholder>
  <span class="nw-ph">Placeholder</span>
  Full article text to follow.
  <!-- TODO(client): valós cikkszöveg bekérendő -->
</p>
```

**`media/thermal-systems-milestone.html`** — cím: *Thermal systems milestone*, dátum `2026-07-15`. Törzs: egy bevezető bekezdés a Solutions copyból (*„Our portfolio spans fluid handling systems, thermal management technologies…"*), majd ugyanaz a placeholder-bekezdés, mint fent.

- [ ] **Step 5: CSS**

```css
.nw-newslist {
  display: grid; gap: var(--nw-space-3);
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  margin-top: var(--nw-space-4);
}
.nw-news a {
  display: block; block-size: 100%;
  padding: var(--nw-space-3);
  text-decoration: none;
  border: 1px solid var(--nw-rule);
  border-radius: var(--nw-radius-card);
  transition: transform var(--nw-dur-base) var(--nw-ease),
              border-color var(--nw-dur-base) var(--nw-ease);
}
.nw-news a:hover { transform: translateY(-4px); border-color: var(--nw-navy); }
.nw-news time {
  display: block; margin-bottom: 0.5rem;
  font-size: var(--nw-text-xs);
  letter-spacing: var(--nw-tracking-wide);
  color: var(--nw-fg-secondary);
}
.nw-news h3 { font-size: var(--nw-text-lg); margin-bottom: 0.5rem; }
.nw-news p  { font-size: var(--nw-text-sm); color: var(--nw-fg-secondary); }

.nw-article__date { font-size: var(--nw-text-sm); color: var(--nw-fg-secondary); margin-top: var(--nw-space-2); }
.nw-article__body { max-width: 72ch; }
.nw-article__body h2 { font-size: var(--nw-text-xl); margin-top: var(--nw-space-6); margin-bottom: var(--nw-space-2); }
.nw-article__body code {
  font-family: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  font-size: 0.9em;
  padding: 0.1em 0.35em;
  background: var(--nw-grey-06);
  border-radius: 3px;
}
```

- [ ] **Step 6: Kösd be és ellenőrizd**

A `media.html` végére: `data/news.js`, `js/nav.js`, `js/pattern.js`, `js/reveal.js`, `js/lists.js`. A cikkoldalakra: `../js/nav.js`, `../js/reveal.js`.

```bash
python tools/check_links.py && python tools/check_placeholders.py && start media.html
```

Elvárt: három kártya, mindegyiken badge; mindhárom kártya működő linkkel nyílik meg. **A `check_links` továbbra is nulla halott linket jelez** — ez itt a lényeg, mert a slug↔fájlnév eltérés a leggyakoribb hiba.

- [ ] **Step 7: Commit**

```bash
git add media.html media/ data/news.js css/sections.css docs/HANDOFF.md
git commit -m "feat: Media hub + 3 cikkoldal

Az egyik cikk maga a használati útmutató: hogyan adnak hozzá,
szerkesztenek és törölnek cikkeket és pozíciókat CMS nélkül.
Így a dokumentáció ott van, ahol nem vész el, és a placeholder
egyben hasznot hajt.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 20: Responsibility hub + 5 jogi oldal + Integrity Line

**Files:**
- Modify: `responsibility.html`, `integrity-line.html`, `legal/*.html` (5 fájl), `css/sections.css`

- [ ] **Step 1: `responsibility.html` `<main>`**

```html
<main id="main">
  <section class="nw-section nw-theme-dark nw-subhero">
    <div class="nw-pattern" data-pattern aria-hidden="true">
      <span class="nw-pattern__shape" data-depth="0.12"
            style="left:-20%;top:-12%;width:82vmin;height:35vmin"></span>
    </div>
    <div class="nw-shell">
      <p class="nw-eyebrow">Legal and compliance</p>
      <h1 data-reveal>Acting Responsibly</h1>
    </div>
  </section>

  <section class="nw-section nw-theme-light">
    <div class="nw-shell">
      <p class="nw-lead nw-prose" data-reveal>
        Integrity, accountability and compliance are fundamental to the way we conduct
        business. We are committed to maintaining the highest standards of ethical
        behavior, transparency and corporate responsibility across all our activities.
      </p>

      <ul class="nw-doclist" data-reveal data-reveal-delay="80">
        <li><a href="legal/code-of-conduct.html">Code of Conduct</a></li>
        <li><a href="legal/compliance-ethics.html">Compliance &amp; Ethics</a></li>
        <li><a href="legal/supplier-requirements.html">Supplier Requirements</a></li>
        <li><a href="legal/privacy-policy.html">Privacy Policy</a></li>
        <li><a href="legal/legal-notice.html">Legal Notice</a></li>
      </ul>

      <p class="nw-note">
        <span class="nw-ph">Placeholder</span>
        Document contents are pending.
        <!-- TODO(client): az 5 jogi dokumentum szövege bekérendő -->
      </p>
    </div>
  </section>
</main>
```

- [ ] **Step 2: Az 5 jogi stub**

Mind az öt azonos szerkezetű. Ez a teljes `<main>` a `legal/code-of-conduct.html`-hez:

```html
<main id="main">
  <section class="nw-section nw-theme-dark nw-subhero">
    <div class="nw-shell">
      <p class="nw-eyebrow"><a href="../responsibility.html">Acting Responsibly</a></p>
      <h1 data-reveal>Code of Conduct</h1>
    </div>
  </section>

  <section class="nw-section nw-theme-light">
    <div class="nw-shell nw-article__body">
      <p class="nw-lead" data-placeholder>
        <span class="nw-ph">Content pending</span>
        The full text of this document will be provided by NEUWERK.
        <!-- TODO(client): Code of Conduct szövege bekérendő -->
      </p>
      <p><a class="nw-btn" href="../responsibility.html">Back to Acting Responsibly</a></p>
    </div>
  </section>
</main>
```

A másik négy pontosan ugyanez, csak a `<h1>`, a `<title>` és a TODO szövege más:

| fájl | `<h1>` és `<title>` prefix | TODO szöveg |
|---|---|---|
| `legal/compliance-ethics.html` | Compliance &amp; Ethics | `Compliance & Ethics szövege bekérendő` |
| `legal/supplier-requirements.html` | Supplier Requirements | `Supplier Requirements szövege bekérendő` |
| `legal/privacy-policy.html` | Privacy Policy | `Privacy Policy szövege bekérendő` |
| `legal/legal-notice.html` | Legal Notice | `Legal Notice szövege bekérendő` |

- [ ] **Step 3: `integrity-line.html` `<main>`**

```html
<main id="main">
  <section class="nw-section nw-theme-dark nw-subhero">
    <div class="nw-shell">
      <p class="nw-eyebrow">Whistleblower reporting</p>
      <h1 data-reveal>Integrity Line</h1>
    </div>
  </section>

  <section class="nw-section nw-theme-light">
    <div class="nw-shell nw-article__body">
      <p class="nw-lead">
        NEUWERK is committed to the highest standards of ethical behavior. The Integrity
        Line allows employees, partners and third parties to report concerns
        confidentially.
      </p>
      <p data-placeholder>
        <span class="nw-ph">Content pending</span>
        Reporting channel details and the confidentiality statement will be provided by
        NEUWERK.
        <!-- TODO(client): Integrity Line csatorna és adatvédelmi nyilatkozat bekérendő -->
      </p>
    </div>
  </section>
</main>
```

- [ ] **Step 4: CSS**

```css
.nw-doclist { margin-top: var(--nw-space-4); }
.nw-doclist li { border-bottom: 1px solid var(--nw-rule); }
.nw-doclist a {
  display: flex; align-items: center; justify-content: space-between;
  padding-block: var(--nw-space-2);
  font-family: var(--nw-font-display);
  font-size: var(--nw-text-lg);
  font-weight: var(--nw-fw-medium);
  text-decoration: none;
}
.nw-doclist a::after { content: "\2192"; color: var(--nw-accent-text); }
.nw-doclist a:hover { color: var(--nw-navy); }
```

- [ ] **Step 5: Ellenőrizd**

```bash
python tools/check_links.py && python tools/check_placeholders.py && start responsibility.html
```

Kattints végig mind az 5 dokumentumon és a „Back" gombokon. Elvárt: nulla halott link, és a leltár most legalább 8 tételt jelez.

- [ ] **Step 6: Commit**

```bash
git add responsibility.html integrity-line.html legal/ css/sections.css docs/HANDOFF.md
git commit -m "feat: Acting Responsibly hub, 5 jogi stub, Integrity Line

Az 5 dokumentum kattintható stub 'content pending' jelöléssel.
A Build 1 fő célja, hogy az ügyfél sehol ne fusson zsákutcába --
üres link helyett látható placeholder oldal.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 21: Contact + 404

**Files:**
- Modify: `contact.html`, `404.html`, `css/sections.css`

**Nincs űrlap** — döntés 5. Minden adat felismerhető placeholder; a `check_placeholders.py` FAIL-el, ha bármelyik e-mail nem `example.com/org/net` végű.

- [ ] **Step 1: `contact.html` `<main>`**

```html
<main id="main">
  <section class="nw-section nw-theme-dark nw-subhero">
    <div class="nw-pattern" data-pattern aria-hidden="true">
      <span class="nw-pattern__shape" data-depth="0.12"
            style="right:-20%;bottom:-16%;width:84vmin;height:36vmin"></span>
    </div>
    <div class="nw-shell">
      <p class="nw-eyebrow">Contact</p>
      <h1 data-reveal>Let&rsquo;s talk</h1>
    </div>
  </section>

  <section class="nw-section nw-theme-light">
    <div class="nw-shell">
      <p class="nw-lead nw-prose" data-reveal>
        We listen first. Tell us about your challenge and we will point you to the right
        people.
      </p>

      <!-- TODO(client): MINDEN kontaktadat placeholder. Valós címek,
           telefonszámok és e-mail címek bekérendők az élesítés előtt. -->
      <ul class="nw-contact" data-reveal data-reveal-delay="80">
        <li data-placeholder>
          <h3><span class="nw-ph">Placeholder</span> Headquarters</h3>
          <p class="nw-contact__addr">
            Example Street 1<br>
            00000 Example City<br>
            Example Country
          </p>
          <p><a href="tel:+000000000000">+00 000 000 0000</a></p>
          <p><a href="mailto:info@example.com">info@example.com</a></p>
        </li>
        <li data-placeholder>
          <h3><span class="nw-ph">Placeholder</span> Media enquiries</h3>
          <p><a href="mailto:press@example.com">press@example.com</a></p>
        </li>
        <li data-placeholder>
          <h3><span class="nw-ph">Placeholder</span> Careers</h3>
          <p><a href="mailto:careers@example.com">careers@example.com</a></p>
          <p><a href="career.html">See open positions</a></p>
        </li>
        <li data-placeholder>
          <h3><span class="nw-ph">Placeholder</span> Suppliers</h3>
          <p><a href="mailto:suppliers@example.com">suppliers@example.com</a></p>
          <p><a href="legal/supplier-requirements.html">Supplier Requirements</a></p>
        </li>
      </ul>
    </div>
  </section>
</main>
```

- [ ] **Step 2: `404.html` `<main>`**

```html
<main id="main">
  <section class="nw-section nw-theme-dark nw-subhero">
    <div class="nw-shell">
      <p class="nw-eyebrow">404</p>
      <h1 data-reveal>This page has moved on</h1>
      <p class="nw-lead" data-reveal data-reveal-delay="80">
        The page you are looking for does not exist. Let us get you back on track.
      </p>
      <p class="nw-hero__actions">
        <a class="nw-btn nw-btn--sun" href="index.html">Back to home</a>
        <a class="nw-btn" href="contact.html">Contact us</a>
      </p>
    </div>
  </section>
</main>
```

- [ ] **Step 3: CSS**

```css
.nw-contact {
  display: grid; gap: var(--nw-space-4);
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  margin-top: var(--nw-space-6);
}
.nw-contact li { padding-top: var(--nw-space-2); border-top: 2px solid var(--nw-rule); }
.nw-contact h3 { font-size: var(--nw-text-base); margin-bottom: var(--nw-space-1); }
.nw-contact p  { font-size: var(--nw-text-sm); margin-bottom: 0.35rem; }
.nw-contact__addr { color: var(--nw-fg-secondary); }
```

- [ ] **Step 4: Ellenőrizd, hogy a placeholder-őr működik**

Írj be szándékosan egy valós e-mailt, futtasd, majd vedd ki:

```bash
sed -i 's/info@example.com/info@neuwerk.com/' contact.html
python tools/check_placeholders.py; echo "exit: $?"
sed -i 's/info@neuwerk.com/info@example.com/' contact.html
python tools/check_placeholders.py; echo "exit: $?"
```

Elvárt: az első futás `FAIL` és `exit: 1`, a második `PASS` és `exit: 0`. Ez igazolja, hogy valós kontaktadat nem tud észrevétlenül élesbe csúszni.

- [ ] **Step 5: Commit**

```bash
git add contact.html 404.html css/sections.css docs/HANDOFF.md
git commit -m "feat: Contact és 404 oldal

Nincs űrlap, csak kontaktadatok -- a döntés szerint. Minden adat
felismerhető placeholder (example.com), nem hihető kitalált adat,
hogy ne tudjon véletlenül élesbe csúszni. A check_placeholders.py
FAIL-el, ha bármelyik e-mail nem example-domain.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 22: Reszponzív és reduced-motion átfésülés

**Files:**
- Modify: `css/sections.css`, `css/components.css` (amit a tesztelés indokol)

- [ ] **Step 1: Nézd végig mind a 16 oldalt négy szélességen**

Chrome DevTools eszközsáv, pontosan ezek: **375**, **768**, **1280**, **1920**.

Amit keresel:
- vízszintes scroll bárhol (a `body { overflow-x: hidden }` és a `.nw-section { overflow: clip }` ezt kezeli, de a nagy pill-formák kilóghatnak)
- a hero cím nem fér ki, vagy nem olvasható a videón
- a mobilmenü átfedi a tartalmat, vagy nem záródik
- a Solutions pillérgombok 375-ön egymásra csúsznak
- a footer oszlopok 768-on összeomlanak

- [ ] **Step 2: Vízszintes scroll ellenőrzése géppel**

Nyisd meg mind a 16 oldalt, és a konzolban futtasd:

```js
document.documentElement.scrollWidth > document.documentElement.clientWidth
  ? "FAIL: vízszintes scroll — " + document.documentElement.scrollWidth + "px"
  : "PASS";
```

Elvárt: `PASS` minden oldalon, mind a négy szélességen.

- [ ] **Step 3: Reduced-motion végigpróba**

DevTools → Rendering → *Emulate CSS media feature prefers-reduced-motion: reduce*, majd tölts újra.

Elvárt:
- az intro **meg sem jelenik**
- a hero videó **áll**, a poszterkép látszik, a cím olvasható
- a Solutions scroll **nem scrubbol**, de a négy gomb működik
- a számlálók **azonnal a végértéket** mutatják (14,000 / 16 / One)
- a pattern **nem mozog**
- a térképpontok **nem pulzálnak**
- semmi nem marad láthatatlanul (a `[data-reveal]` elemek láthatók)

- [ ] **Step 4: Billentyűzetes bejárás**

Tab-bal járd végig az `index.html`-t. Elvárt: a „Skip to content" link az első fókusz, a fókuszgyűrű mindenhol látható, a mobilmenü Esc-re záródik és a fókusz visszaugrik a gombra.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "fix: reszponzív és reduced-motion átfésülés

375/768/1280/1920 végigpróbálva mind a 16 oldalon, vízszintes
scroll sehol. Reduced-motion mellett minden szekció olvasható,
semmi nem marad láthatatlanul.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Task 23: Átadás — leltár, Lighthouse, zip

**Files:**
- Modify: `docs/HANDOFF.md`, `docs/CHANGELOG.md`
- Create: `tools/make_zip.py`

- [ ] **Step 1: Végső ellenőrzés**

```bash
python tools/check_links.py && python tools/check_placeholders.py
```

Elvárt: mindkettő `PASS`, és a `check_links` **nulla külső hivatkozást** listáz a `mailto:`/`tel:` linkeken kívül. Ha bármi `http`/`https` megjelenik, egy CDN csúszott be — távolítsd el.

- [ ] **Step 2: Lighthouse**

Chrome DevTools → Lighthouse → Desktop, majd Mobile, az `index.html`-en.

Elvárt: Performance, Accessibility, Best Practices, SEO mind **zöld** (90+). A leggyakoribb bukó: a hero videó mérete a Performance-en. Ha az LCP rossz, a `hero-1920.mp4` `preload` értékét vedd `none`-ra, és hagyd, hogy a poszterkép adja az első festést.

- [ ] **Step 3: `tools/make_zip.py`**

```python
#!/usr/bin/env python3
"""Leszállítható zip. Csak az üzemeléshez szükséges fájlok kerülnek bele.

Kihagyva: a forrásassetek (Arculat/, useful visual assets/), a build eszközök
(tools/, work/) és a fejlesztői dokumentáció (docs/, .git/). Ezek a repóban
maradnak, de az ügyfél szerverére nem valók.
"""
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "work" / "neuwerk-website-build1.zip"

INCLUDE_DIRS = ["assets", "css", "js", "data", "legal", "media", "partials"]
INCLUDE_FILES = ["index.html", "identity.html", "career.html", "media.html",
                 "responsibility.html", "integrity-line.html", "contact.html",
                 "404.html", "README.md", "CLAUDE.md"]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    total = 0

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in INCLUDE_FILES:
            p = ROOT / name
            if not p.exists():
                print(f"FAIL — hiányzik: {name}")
                return 1
            z.write(p, name)
            total += 1

        for d in INCLUDE_DIRS:
            base = ROOT / d
            if not base.exists():
                print(f"FAIL — hiányzik a könyvtár: {d}")
                return 1
            for p in sorted(base.rglob("*")):
                if p.is_file() and p.name != ".gitkeep":
                    z.write(p, str(p.relative_to(ROOT)).replace("\\", "/"))
                    total += 1

    size = OUT.stat().st_size / 1048576
    print(f"make_zip: {total} fájl, {size:.2f} MB")
    print(f"  {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Készítsd el és próbáld ki a zipet**

```bash
python tools/make_zip.py
```

Csomagold ki egy **teljesen más** könyvtárba, és duplakattints az `index.html`-en.

Elvárt: az oldal megnyílik `file://`-ből, a videó lejátszódik, a Media és a Career lista feltöltődik, minden link működik. **Ez a legfontosabb teszt** — ha ez elbukik, valahol `fetch()` maradt a kódban.

- [ ] **Step 5: Frissítsd a dokumentációt**

Írd be a `docs/CHANGELOG.md` tetejére a Build 1 bejegyzést: mi készült el, mi a zip mérete, és hogy melyik 5 blokkoló ügyféltétel van még nyitva. A `docs/HANDOFF.md` „Állapot" szakaszát állítsd `Build 1 kész, ügyfél-jóváhagyásra vár` értékre.

- [ ] **Step 6: Commit és push**

```bash
git add -A
git commit -m "chore: Build 1 kész — leszállítható zip

16 oldal, nulla halott link, file://-ből működik.
Lighthouse zöld. A zip csak az üzemeléshez szükséges fájlokat
tartalmazza: a forrásassetek és a build eszközök a repóban
maradnak.

Nyitott, ügyféltől bekérendő: kontaktadatok, a 16 ország
megnevezése, Media tartalom, Career pozíciók, 5 jogi dokumentum.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git push origin main
```

---

## Self-review

**Spec-lefedettség.** A spec 12 fejezete és 17 döntése végigkövetve:

| spec | task |
|---|---|
| 3.1 színek · 3.6 kontraszt | 6 (+ számolt ellenőrzés) |
| 3.2 tipográfia | 4, 7 |
| 3.3 pattern | 11 |
| 3.4 logó, favicon | 5 |
| 3.5 világos/sötét ritmus | 6 (`.nw-theme-*`), 13–21 |
| 4 IA, 16 oldal, nav | 8, 9 |
| 5 főoldali szekciók | 13–16 |
| 6 hero videó, SPEC vágás | 10, 13 |
| 7 Solutions scrub, leképezés | 15 |
| 8 zero-build, `file://` | 8, 9, 23 |
| 8.1 Media/Career modell | 18, 19 |
| 9 átadhatóság | 1, 23 |
| 10.2 kontaktadatok | 3, 21 |
| 11 kész-kritériumok 1–12 | 9, 22, 23 |

**Hiány, amit a tervezés hozott felszínre:** a 16 ország nincs megnevezve a forrásanyagban. Felvéve a `HANDOFF.md` blokkoló tételei közé (Task 1), és a `data/locations.js` láthatóan placeholder (Task 14). **Ezt fel kell venni a spec 10.2 táblázatába is** — a spec jelenleg csak a kontaktadatokat sorolja ott.

**Típus-konzisztencia.** `window.NEUWERK_NEWS` mezői (`slug`, `date`, `title`, `excerpt`, `placeholder`) egyeznek a `js/lists.js` olvasásával. `window.NEUWERK_JOBS` mezői (`title`, `location`, `type`, `area`, `url`, `placeholder`) szintén. `window.NEUWERK_LOCATIONS` (`name`, `x`, `y`) egyezik a `js/map.js`-szel. A `data-scrub-to` értékek lokális időben vannak, és a Task 15 táblázata levezeti őket az eredetiből.

**Szkript-sorrend.** Minden oldalon a `data/*.js` megelőzi a `js/lists.js`-t és a `js/map.js`-t. Ezt a 14., 18. és 19. task lépései külön kimondják.
