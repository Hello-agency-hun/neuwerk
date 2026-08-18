# NEUWERK — weboldal, Build 1

Statikus HTML/CSS/JS weboldal a neuwerk (korábban Continental OESL) számára,
plusz a hozzá tartozó arculati anyagok és az asset-előállító eszközök.

**Ha most veszed át a projektet, ezt a fájlt olvasd végig.** A fejlesztői
belépési pont a [`CLAUDE.md`](CLAUDE.md), az aktuális állapot és a nyitott
kérdések a [`PROGRESS.md`](PROGRESS.md)-ben vannak.

---

## 1. Telepítés

### Fontos: a `main` ág üres

A munka a **`build/1-clickable-prototype`** ágon van. A `main` csak a kezdeti
tervet tartalmazza, weboldal nincs rajta. Ezért klónozáskor add meg az ágat:

```bash
git clone -b build/1-clickable-prototype https://github.com/Hello-agency-hun/neuwerk.git
```

Ha már klónoztad és üresnek tűnik:

```bash
git checkout build/1-clickable-prototype
```

A repo ~75 MB (benne a brandbook, a logók és a videók), a klónozás eltarthat
pár percig.

### Mit kapsz a klónnal, és mit nem

| Benne van | Nincs benne (helyileg előállítható) |
|---|---|
| a teljes weboldal (HTML/CSS/JS) | `work/` — köztes renderek, PDF-ek, zipek (~200 MB) |
| `assets/` — a kész, optimalizált assetek | `uj-neuwerk/` — a review-mappa (12 MB) |
| `Arculat/` — brandbook, logók | |
| `useful visual assets/` — animatik, sablonok | |
| `tools/` — az előállító szkriptek | |

A hiányzó kettőt egy-egy paranccsal újra tudod gyártani, lásd a 3. pontnál.

---

## 2. Futtatás

**A weboldalhoz semmit nem kell telepíteni.** Nincs npm, nincs build lépés,
nincs függőség.

```bash
python tools/serve.py
```

Vagy egyszerűen nyisd meg duplakattintással az `index.html`-t. A szerveres
verzió azért jobb, mert a videók és néhány böngésző-funkció `file://` alól
máshogy viselkedik.

---

## 3. Ha az eszközöket is használni akarod

Csak akkor kell, ha assetet állítasz elő vagy PDF-et generálsz. **A weboldal
szerkesztéséhez nem kell.**

```bash
pip install -r requirements.txt
```

Külső programok, amik néhány szkripthez kellenek:

| Program | Mihez | Ha nincs meg |
|---|---|---|
| **ffmpeg** | `build_video.py`, `build_solutions.py` (videóvágás, grade) | [ffmpeg.org](https://ffmpeg.org/download.html) |
| **Google Chrome** | `build_wireframe.py` (PDF-nyomtatás) | valószínűleg már fent van |
| **PHP** | csak a review-mappa megjegyzés-gyűjtője | csak ha helyben teszteled |

A Chrome útvonala a `tools/build_wireframe.py` tetején van beégetve — ha
nálad máshol van, ott írd át.

### A leggyakoribb parancsok

```bash
python tools/check_links.py
python tools/check_placeholders.py
python tools/build_wireframe.py
python tools/build_review.py
python tools/make_zip.py
```

Sorrendben: halott linkek keresése mind a 10 oldalon · placeholder-leltár és a
`HANDOFF.md` frissítése · kattintható wireframe-PDF az ügyfélnek · az
`uj-neuwerk/` review-mappa · a leszállítható zip.

**Minden változtatás után futtasd az első kettőt.** Ez a projekt szabálya.

---

## 4. Mit jelent az, hogy „design HTML"

Ebben a projektben **nincs Figma-fájl, amiből aztán valaki lekódolja az
oldalt. A HTML/CSS maga a design.** Ez a szokásosnál fontosabb különbség,
ezért érdemes átgondolni, mielőtt hozzányúlsz:

- **A tervezés forrása a `css/tokens.css`.** Minden szín, betűméret, térköz és
  sarokkerekítés ott van definiálva, a brandbook v1.1-ből levezetve. Ha színt
  akarsz állítani, ott állítod — és az egész oldalon átmegy.
  **Hardcode hex értéket ne írj sehova máshova.**
- **A `design-system.html` az élő stíluskatalógus.** Nyisd meg böngészőben:
  ott van egy helyen az összes token, gomb, kártya és tipográfia, ahogy
  tényleg kinéznek. Ez a projekt „stílusoldala".
- **A CSS kommentelve van, és a kommentek indokolnak.** Nem azt írják le, mit
  csinál a kód, hanem hogy miért úgy. Sok döntés mögött mérés vagy
  ügyfél-visszajelzés van — érdemes elolvasni, mielőtt átírsz valamit.

### Három szabály, amit a brandbook kikényszerít

Ezeket a tokenek védik, de kézzel könnyű megsérteni:

1. **A Sun (`#ffa500`) maximum a látható felület 10–15%-a.** Soha nem háttér.
2. **Sun szöveg fehér háttéren tilos** — a kontraszt 1,97:1, bukott. A
   Sun-kitöltésű gomb felirata **navy**. Erre van szemantikus token:
   `--nw-on-sun`.
3. **A neuwerk pattern csak Blue tint 1 navy háttéren**, nagy léptékben.
   Kisméretű, sűrű vagy pusztán dekoratív használat tilos.

### Négy szabály, ami a projekt működéséből jön

A [`CLAUDE.md`](CLAUDE.md) részletezi, de a lényeg:

1. **Nincs build lépés.** Nincs npm, nincs bundler, nincs PHP a végleges
   csomagban.
2. **A zip `file://`-ből is működik**, ezért **nincs `fetch()`**. A változó
   tartalom `window.NEUWERK_*` értékadás a `data/*.js`-ben.
3. **Nincs külső hálózati kérés.** Font, ikon, szkript mind lokális. Német
   ipari ügyfél, GDPR. **Ne rakj be CDN-t.**
4. **A header/footer mind a 10 oldalon duplikálva van**, `<!-- @partial:header -->`
   jelölők között. Ha módosítod, mind a 10 oldalon módosítsd. A `partials/`
   alatti fájlok referencia-másolatok.

---

## 5. Mi hol van

```
index.html, identity.html, career.html, media.html,
legal-compliance.html, contact.html, 404.html    a 7 fő oldal
media/*.html                                     3 cikkoldal
design-system.html                               élő stíluskatalógus (nem publikus)

css/tokens.css      MINDEN szín, méret, betű — az egyetlen hely, ahol hex lehet
css/base.css        reset, tipográfia, layout-primitívek
css/components.css  header, footer, gomb, kártya, badge
css/sections.css    a szekciók (hero, térkép, solutions, brand-sáv…)

js/                 kis, önálló szkriptek — nincs framework
data/               a változó tartalom (hírek, telephelyek, pozíciók)
partials/           a header/footer referencia-másolata
assets/             a KÉSZ, optimalizált assetek (ezek mennek ki)
assets-src/         a generált képek eredetije (nem megy ki az ügyfélnek)

Arculat/               brandbook, neuwerk/OESL/Regent logók, logó-animáció
useful visual assets/  animatik videó, PPT-sablonok, bannerek
vendor/                Natural Earth térkép-adat (public domain)

tools/              az előállító és ellenőrző szkriptek
docs/               spec, changelog, handoff, benchmark-elemzés
review/             a megjegyzés-gyűjtő widget forrása
```

### Az assetekről

- **`assets/`** — ez megy ki az ügyfélnek. Optimalizált, méretre vágott.
  Kézzel ne szerkeszd: a legtöbbjét szkript állítja elő.
- **`assets-src/`** — a generált képek nagy felbontású eredetije. Szándékosan
  a gyökérben van, **nem** az `assets/` alatt: különben bekerülne az
  ügyfélcsomagba.
- **`Arculat/`** — a hivatalos arculati anyag. A `01_neuwerk_brandbook/` alatti
  PDF az igazság forrása minden szín- és tipográfia-kérdésben.
- **`useful visual assets/OESL_animatikv_v29.mp4`** — az ügyfél saját
  animatikja. **Minden videó ebből készül** (`tools/build_video.py`,
  `tools/build_solutions.py`), split-tone grade-del. Az áttetsző autós x-ray
  hatás ebbe bele van renderelve, nem mi csináltuk.

---

## 6. Ha AI-eszközzel dolgoznál tovább

### Claude Code — ez a projekt natív környezete

A repóban van egy [`CLAUDE.md`](CLAUDE.md), amit a Claude Code automatikusan
beolvas, és egy `.claude/launch.json`, amiből a helyi szerver egy paranccsal
indul.

```bash
cd neuwerk
claude
```

Jó első kérdés: *„Olvasd el a PROGRESS.md-t és mondd el, hol tartunk."*

### Claude.ai — designra, artifactra

A statikus HTML jól átvihető: nyiss egy **Project**-et a claude.ai-on, és told
fel a `css/tokens.css`-t plusz azt az egy-két oldalt, amin dolgozol. Az egész
repót ne töltsd fel — a videók és a brandbook elviszik a helyet, és a
designhoz nem is kellenek.

Ha egy szekciót akarsz újratervezni, a legjobb input a **`tokens.css` + az
adott szekció HTML-je + a `design-system.html`**. Így a javaslat a meglévő
rendszerben marad, nem talál ki új színeket.

### Lovable

**Ez nem egy sima import.** A Lovable React/Vite/Tailwind projekteket generál,
és azt szinkronizálja GitHubra. Ez a repo viszont szándékosan sima statikus
HTML, build lépés nélkül — a kettő nem ugyanaz a formátum, tehát **a repót nem
lehet úgy „megnyitni" a Lovable-ben, hogy onnantól ugyanez a projekt legyen.**

Két reális út:

1. **Referenciaként használod.** Létrehozol egy új Lovable-projektet, és
   inputként megadod a `tokens.css` értékeit (színek, betűk, térközök) meg
   képernyőképeket. A Lovable ebből épít egy React-változatot. Ilyenkor **két
   külön kódbázis lesz** — el kell dönteni, melyik az igazi.
2. **Nem viszed át.** Ha a cél a Build 1 ügyfél-jóváhagyás, a statikus verzió
   erre alkalmasabb: nincs build, nincs függőség, `file://`-ből is megy, és a
   leszállítás egy zip.

A Lovable és a hasonló eszközök gyorsan változnak — mielőtt belevágsz, nézd
meg az aktuális dokumentációjukat, hogy a GitHub-import éppen mit tud.

**Amire bármelyik eszközzel figyelj:** a fenti négy projekt-szabály (nincs
build, nincs `fetch()`, nincs CDN, `file://`-nek működnie kell) nem stílus
kérdése — ezek az ügyfél-leszállítás feltételei. Egy generált React-app
egyiket sem teljesíti alapból.

---

## 7. Az ügyfélnek szóló három kimenet

| | Mire való | Hogyan készül |
|---|---|---|
| **wireframe-PDF** | tartalmi jóváhagyás — szürke, kép nélküli, kattintható | `python tools/build_wireframe.py` |
| **review-mappa** | a kész oldal végigkattintása + megjegyzés-gyűjtő | `python tools/build_review.py` |
| **leszállítható zip** | a végleges csomag a szerverükre | `python tools/make_zip.py` |

A **wireframe-PDF** azért létezik, mert a kész, színes verziót nézve az ügyfél
a színekről és az animációkról kezdett visszajelzést adni, nem a szövegről. A
szürke, képek helyett feliratozott dobozokat mutató változat visszatereli a
beszélgetést a tartalomra. Minden a valódi oldalakból generálódik, tehát nem
tud elcsúszni attól, ami végül kimegy.

A **review-mappa** PHP-t igényel (a megjegyzés-gyűjtő miatt), és egy
webtárhelyre kell feltölteni. A `README-FELTOLTES.txt` benne van a mappában.

---

## 8. Dokumentáció

| Fájl | Mi van benne |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | fejlesztői belépési pont, alapszabályok, mi placeholder |
| [`PROGRESS.md`](PROGRESS.md) | **az aktuális állapot, minden döntés, zsákutca és nyitott kérdés** |
| `docs/HANDOFF.md` | nyitott tételek, placeholder-lista (szkript frissíti) |
| `docs/CHANGELOG.md` | változásnapló |
| `docs/superpowers/specs/` | a design spec és a három amendment |
| `docs/benchmark-analysis.md` | a versenytárs-elemzés, amiből a layout-döntések jöttek |

**A `PROGRESS.md`-t olvasd el elsőként.** Abban van a „zsákutcák" szakasz is:
olyan dolgok, amiket már kipróbáltunk és nem működtek — hogy ne menjen rá még
egyszer valakinek egy napja.
