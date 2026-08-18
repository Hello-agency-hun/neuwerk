# NEUWERK weboldal, Build 1

Statikus HTML/CSS/JS weboldal a neuwerk (korábban Continental OESL) számára.
A repóban van az arculati anyag és az asset-előállító szkriptek is.

Ha most veszed át a projektet, ezt a fájlt olvasd végig. Utána a
[`PROGRESS.md`](PROGRESS.md) jön: abban van, hol tartunk, mit döntöttünk el,
és mi az, amit már kipróbáltunk és nem működött.

---

## 1. Telepítés

```bash
git clone https://github.com/Hello-agency-hun/neuwerk.git
cd neuwerk
```

Ennyi. A `main` ágon minden rajta van.

(Van egy `build/1-clickable-prototype` ág is. Ugyanaz a tartalom, ugyanaz a
commit. Korábban ott folyt a munka, aztán átvezettük a `main`-re. Nem kell
vele foglalkoznod.)

A repo körülbelül 82 MB, a git-előzményekkel együtt 155 MB a lemezen. A
klónozás pár percig tart, mert benne van a brandbook és az animatik videó is.

### Mit tartalmaz a klón

| Mappa | Fájl | Méret | Mi ez |
|---|---|---|---|
| `useful visual assets/` | 5 | 42,1 MB | az ügyfél animatikja, PPT-sablonok, bannerek |
| `Arculat/` | 36 | 23,5 MB | brandbook, neuwerk/OESL/Regent logók |
| `assets/` | 48 | 12,3 MB | a kész assetek, ezek mennek ki az ügyfélhez |
| `assets-src/` | 4 | 3,2 MB | a generált képek nagy felbontású eredetije |
| gyökér | 14 | 0,3 MB | a 7 oldal és a dokumentáció |
| a többi | 61 | 0,5 MB | forráskód, szkriptek, spec |

### Mi nincs benne

Két mappa kimarad, mert mindkettő származtatott: `work/` (körülbelül 200 MB
köztes render) és `uj-neuwerk/` (13 MB review-mappa). Egy-egy paranccsal
újraépülnek, lásd a 3. pontot.

Ebben a két mappában van a három ügyfél-kimenet is: a wireframe-PDF, a
review-zip és a leszállítható zip. Ha valamelyikre azonnal szükséged van,
gyorsabb, ha elkéred, mint ha legenerálod.

---

## 2. Futtatás

A weboldalhoz nem kell telepíteni semmit. Nincs npm, nincs build lépés,
nincs függőség.

```bash
python tools/serve.py
```

Vagy nyisd meg duplakattintással az `index.html`-t. A szerveres verzió azért
jobb, mert a videók `file://` alól máshogy viselkednek.

---

## 3. Az eszközök

Ezekre csak akkor van szükség, ha assetet állítasz elő vagy PDF-et
generálsz. A weboldal szerkesztéséhez nem kellenek.

```bash
pip install -r requirements.txt
```

Néhány szkript külső programot is használ:

| Program | Mihez kell | Ha nincs meg |
|---|---|---|
| ffmpeg | videóvágás és színkorrekció | [ffmpeg.org](https://ffmpeg.org/download.html) |
| Google Chrome | a wireframe-PDF nyomtatása | valószínűleg már fent van |
| PHP | a review-mappa megjegyzés-gyűjtője | csak helyi teszthez |

A Chrome útvonala be van égetve a `tools/build_wireframe.py` tetejére. Ha
nálad máshol van, ott írd át.

### A leggyakoribb parancsok

```bash
python tools/check_links.py          # halott linkek mind a 10 oldalon
python tools/check_placeholders.py   # placeholder-leltár, frissíti a HANDOFF.md-t
python tools/build_wireframe.py      # kattintható wireframe-PDF
python tools/build_review.py         # uj-neuwerk/, a feltölthető review-mappa
python tools/make_zip.py             # a leszállítható zip
```

Az első kettőt futtasd le minden változtatás után. Ez a projekt szabálya.

---

## 4. Mit jelent az, hogy „design HTML"

Ebben a projektben nincs Figma-fájl, amiből valaki utána lekódolja az oldalt.
A HTML és a CSS maga a design. Ebből három dolog következik.

A tervezés forrása a `css/tokens.css`. Minden szín, betűméret, térköz és
sarokkerekítés ott van definiálva, a brandbook v1.1-ből levezetve. Ha színt
akarsz állítani, ott állítod, és az egész oldalon átmegy. Máshova ne írj
hardcode hex értéket.

A `design-system.html` az élő stíluskatalógus. Nyisd meg böngészőben: egy
helyen ott van az összes token, gomb, kártya és tipográfia, ahogy tényleg
kinéznek.

A CSS-kommentek indokolnak, nem leírnak. Nem azt mondják el, mit csinál a
kód, hanem hogy miért úgy. Sok döntés mögött mérés vagy ügyfél-visszajelzés
van, úgyhogy érdemes elolvasni őket, mielőtt átírsz valamit.

### Amit a brandbook kikényszerít

A tokenek védik ezeket, de kézzel könnyű megsérteni:

1. A Sun (`#ffa500`) legfeljebb a látható felület 10 vagy 15 százaléka
   lehet. Háttérnek soha.
2. Sun szöveg fehér háttéren tilos, mert a kontraszt 1,97:1, ami bukott
   érték. A Sun-kitöltésű gomb felirata navy. Erre van szemantikus token:
   `--nw-on-sun`.
3. A neuwerk pattern csak Blue tint 1 navy háttéren jelenhet meg, nagy
   léptékben. Kisméretű, sűrű vagy pusztán dekoratív használat tilos.

### Amit a leszállítás kikényszerít

Ez a négy nem stíluskérdés, hanem az ügyfél-átadás feltétele. A
[`CLAUDE.md`](CLAUDE.md) részletezi őket.

1. Nincs build lépés. Nincs npm, nincs bundler, és a végleges csomagban
   nincs PHP.
2. A zipnek `file://`-ből is működnie kell, ezért nincs `fetch()`. A
   változó tartalom `window.NEUWERK_*` értékadás a `data/*.js`-ben.
3. Nincs külső hálózati kérés. Font, ikon, szkript mind lokális. Német ipari
   ügyfél, GDPR, ezért CDN-t ne rakj be.
4. A header és a footer mind a 10 oldalon duplikálva van, a
   `<!-- @partial:header -->` jelölők között. Ha módosítod, mind a 10 oldalon
   módosítsd. A `partials/` alatti fájlok referencia-másolatok.

---

## 5. Mi hol van

```
index.html, identity.html, career.html, media.html,
legal-compliance.html, contact.html, 404.html    a 7 fő oldal
media/*.html                                     3 cikkoldal
design-system.html                               stíluskatalógus, nem publikus

css/tokens.css      minden szín, méret, betű. Az egyetlen hely, ahol hex lehet
css/base.css        reset, tipográfia, layout-primitívek
css/components.css  header, footer, gomb, kártya, badge
css/sections.css    a szekciók (hero, térkép, solutions, brand-sáv)

js/                 kis, önálló szkriptek. Nincs framework
data/               a változó tartalom: hírek, telephelyek, pozíciók
partials/           a header és a footer referencia-másolata
assets/             a kész assetek, ezek mennek ki
assets-src/         a generált képek eredetije, ez nem megy ki

Arculat/               brandbook, logók, logó-animáció
useful visual assets/  animatik videó, PPT-sablonok, bannerek
vendor/                Natural Earth térkép-adat, public domain

tools/              az előállító és ellenőrző szkriptek
docs/               spec, changelog, handoff, benchmark-elemzés
review/             a megjegyzés-gyűjtő widget forrása
```

### Az assetekről

Négy mappa van, és könnyű összekeverni őket.

Az `assets/` az, ami kimegy az ügyfélhez. Optimalizált és méretre vágott.
Kézzel ne szerkeszd, mert a legtöbbjét szkript állítja elő.

Az `assets-src/` a generált képek nagy felbontású eredetije. Szándékosan a
gyökérben van és nem az `assets/` alatt, mert különben bekerülne az
ügyfélcsomagba.

Az `Arculat/` a hivatalos arculati anyag. A `01_neuwerk_brandbook/` alatti
PDF az igazság forrása minden szín- és tipográfia-kérdésben.

A `useful visual assets/OESL_animatikv_v29.mp4` az ügyfél saját animatikja.
Minden videó ebből készül, split-tone színkorrekcióval (`tools/build_video.py`
és `tools/build_solutions.py`). Az áttetsző autós x-ray hatás ebbe bele van
renderelve, azt nem mi csináltuk.

---

## 6. Ha AI-eszközzel dolgoznál tovább

### Claude Code

Ez a projekt natív környezete. A repóban van egy [`CLAUDE.md`](CLAUDE.md),
amit a Claude Code magától beolvas, és egy `.claude/launch.json`, amiből a
helyi szerver egy paranccsal indul.

```bash
cd neuwerk
claude
```

Jó első kérdés: „Olvasd el a PROGRESS.md-t és mondd el, hol tartunk."

### claude.ai

Ha designon dolgoznál, nyiss egy Projectet a claude.ai-on, és told fel a
`css/tokens.css`-t meg azt az egy-két oldalt, amin épp dolgozol. Az egész
repót ne töltsd fel: a videók és a brandbook elviszik a helyet, és a
designhoz nem kellenek.

Ha egy szekciót terveznél újra, a legjobb input a `tokens.css`, az adott
szekció HTML-je és a `design-system.html`. Így a javaslat a meglévő
rendszerben marad, és nem talál ki új színeket.

### Lovable

Ez nem sima import, és érdemes tudni, miért. A Lovable React/Vite/Tailwind
projekteket generál, és azt szinkronizálja GitHubra. Ez a repo viszont
szándékosan statikus HTML, build lépés nélkül. A kettő nem ugyanaz a
formátum, tehát a repót nem tudod úgy megnyitni a Lovable-ben, hogy onnantól
ugyanez a projekt legyen.

Két reális út van. Az egyik, hogy referenciaként használod: létrehozol egy új
Lovable-projektet, és megadod neki a `tokens.css` értékeit meg
képernyőképeket. Ebből épít egy React-változatot. Ilyenkor két külön kódbázis
lesz, és el kell dönteni, melyik az igazi. A másik, hogy nem viszed át. Ha a
cél a Build 1 ügyfél-jóváhagyás, arra a statikus verzió alkalmasabb: nincs
build, nincs függőség, `file://`-ből is megy, és a leszállítás egy zip.

Ezek az eszközök gyorsan változnak, úgyhogy mielőtt belevágsz, nézd meg az
aktuális dokumentációjukat.

### A wireframe-PDF mint ellenőrzőpont

A `docs/neuwerk-wireframe.pdf` a teljes oldal szürke, kép nélküli vázlata,
11 lapon. Jól használható referenciának, ha bármelyik AI-eszközbe beviszed a
projektet. Egy helyen látod rajta, milyen szekciók vannak, milyen sorrendben,
mi van a headerben és a footerben, és hol lesz kép, videó vagy interakció.
Ha a generált változatból kimarad egy szekció vagy felcserélődik a sorrend,
ezen azonnal feltűnik.

A PDF pillanatkép, a dátuma rajta van a borítóján. Ha közben változott az
oldal, építsd újra:

```bash
python tools/build_wireframe.py
```

Bármelyiket is választod, a 4. pont végén felsorolt négy szabály nem
alkuképes. Egy generált React-app egyiket sem teljesíti alapból.

---

## 7. A három ügyfél-kimenet

| Kimenet | Mire való | Parancs |
|---|---|---|
| wireframe-PDF | tartalmi jóváhagyás | `python tools/build_wireframe.py` |
| review-mappa | a kész oldal végigkattintása, megjegyzésekkel | `python tools/build_review.py` |
| leszállítható zip | a végleges csomag a szerverükre | `python tools/make_zip.py` |

A wireframe-PDF azért készült, mert a kész, színes verziót nézve az ügyfél a
színekről és az animációkról kezdett visszajelzést adni, nem a szövegről. A
szürke, képek helyett feliratozott dobozokat mutató változat visszatereli a
beszélgetést a tartalomra. A valódi oldalakból generálódik, tehát nem tud
elcsúszni attól, ami végül kimegy.

A wireframe-PDF-ből egy legenerált példány be van commitolva ide:
`docs/neuwerk-wireframe.pdf`. Ez az egyetlen kimenet, ami a klónnal együtt
érkezik. A másik kettőt neked kell legenerálnod.

A review-mappához PHP kell a megjegyzés-gyűjtő miatt, és webtárhelyre kell
feltölteni. A `README-FELTOLTES.txt` benne van a mappában.

---

## 8. Dokumentáció

| Fájl | Mi van benne |
|---|---|
| [`PROGRESS.md`](PROGRESS.md) | az aktuális állapot, a döntések, a zsákutcák és a nyitott kérdések |
| [`CLAUDE.md`](CLAUDE.md) | fejlesztői belépési pont, alapszabályok, mi placeholder |
| `docs/HANDOFF.md` | nyitott tételek és placeholder-lista, szkript frissíti |
| `docs/CHANGELOG.md` | változásnapló |
| `docs/superpowers/specs/` | a design spec és a három amendment |
| `docs/benchmark-analysis.md` | a versenytárs-elemzés, amiből a layout-döntések jöttek |
| `docs/neuwerk-wireframe.pdf` | a teljes oldal szürke vázlata, 11 lapon. Pillanatkép |

A `PROGRESS.md`-vel kezdd. Van benne egy „zsákutcák" szakasz: olyan dolgok,
amiket már kipróbáltunk és nem működtek. Azért írtuk le, hogy ne menjen rá
még egyszer valakinek egy napja.
