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

### Áttétel Claude designba, lépésről lépésre

Innen indulsz: leklónoztad a repót, és megnyitottad a mappát.

1. Menj a claude.ai-ra és hozz létre egy új Projectet. Adj neki nevet,
   például „neuwerk website".

2. Told fel a Project tudásbázisába pontosan ezt a négy dolgot:

   - `css/tokens.css`, mert ebben van minden szín, betűméret és térköz
   - `design-system.html`, mert ez mutatja meg, hogyan néznek ki a
     komponensek együtt
   - `docs/neuwerk-wireframe.pdf`, mert ezen látszik a szekciók sorrendje
     és a teljes oldalszerkezet
   - azt az egy oldalt, amin dolgozni fogsz, például `index.html`

3. Az egész repót ne töltsd fel. A videók és a brandbook elviszik a helyet,
   és a designhoz nem adnak hozzá semmit. Ha a brandbookra is szükség van,
   told fel külön az `Arculat/01_neuwerk_brandbook/neuwerk_brandbook_FINAL.pdf`-et.

4. Az első üzenetben mondd meg, mi a keret. Valami ilyesmi működik:

   > Ez egy statikus HTML weboldal. A `tokens.css` tartalmazza az összes
   > design tokent, ezekből dolgozz, és ne találj ki új színt vagy
   > betűméretet. A Sun (#ffa500) legfeljebb a felület 10 vagy 15 százaléka
   > lehet, és fehér háttéren tilos szövegszínként. Ne használj CDN-t és
   > `fetch()`-et.

5. Ha egy szekciót terveznél újra, add meg az adott szekció HTML-jét, és
   kérj több változatot. A visszakapott kódot a `tokens.css` változóival
   ellenőrizd: ha hardcode hex érték van benne, az hibás.

Amit érdemes előre tudni: az artifact-előnézet nem fog pontosan úgy kinézni,
mint a valódi oldal. A betűtípusok lokálisan vannak beágyazva, a videók pedig
nincsenek feltöltve, ezért az előnézet ezek nélkül renderel. A szerkezet és a
színek viszont helyesek lesznek.

A claude.ai felülete változik, úgyhogy a gombok neve lehet más, mint itt. A
lényeg minden verzióban ugyanaz: egy Project, benne a fenti négy fájl.

### Áttétel Figmába, lépésről lépésre

A Figma natívan nem tud HTML-t importálni, ehhez plugin kell. Az alábbi
lépések után lesz egy réteges, szerkeszthető Figma-fájlod.

1. Indítsd el a helyi szervert, hogy a plugin lássa az oldalt:

   ```bash
   python tools/serve.py
   ```

   Ez a `http://localhost:8000` címen szolgálja ki a projektet.

2. Figmában nyiss egy új fájlt, és telepíts egy HTML-importáló plugint. A
   legelterjedtebb a html.to.design, de több hasonló is van. Keress a
   Figma Community-ben a „html to design" kifejezésre.

3. Importálj oldalanként, ne egyben. Az importálók általában kétféle
   bemenetet fogadnak:

   - URL, például `http://localhost:8000/index.html`
   - beillesztett HTML forrás

   Ha az URL-es mód nem éri el a localhostot (a plugin a Figma felhőjéből
   fut, tehát ez előfordulhat), akkor vagy a beillesztős módot használd,
   vagy tedd ki ideiglenesen az oldalt egy publikus címre.

4. Ezt a tíz oldalt érdemes behozni:

   ```
   index.html              identity.html           career.html
   media.html              legal-compliance.html   contact.html
   404.html                media/neuwerk-begins.html
   media/thermal-systems-milestone.html
   media/how-to-update-this-page.html
   ```

5. Az importált frame szélességét állítsd 1440 pixelre. Az oldal erre a
   szélességre van tervezve, ez a `--nw-max-width` értéke.

### A Figma-fájl beállítása a tokenekből

Az import layereket ad, de nem ad se változókat, se komponenskönyvtárat.
Ezeket kézzel érdemes felvenni, mert így marad a Figma-fájl és a kód
szinkronban. Minden érték a `css/tokens.css`-ből jön.

Színek:

| Figma-változó | Érték | Mire való |
|---|---|---|
| navy | `#1b1e52` | a fő szövegszín |
| blue-1 | `#273993` | a sötét felületek háttere |
| blue-2 | `#4e66af` | másodlagos szöveg |
| blue-3 | `#8895cb` | forma és felület, szövegnek világoson nem jó |
| blue-4 | `#afc6e7` | forma és felület, szövegnek világoson nem jó |
| sun | `#ffa500` | akcent, legfeljebb a felület 10 vagy 15 százaléka |
| canvas | `#fbfcfe` | az oldal alapja |
| surface | `#ffffff` | kártyák, kiemelt lapok |
| sunk | `#eef2fb` | süllyesztett sáv |
| deeper | `#1e2c72` | a mély felület sötétebb vége |

Betűtípusok. Mindkettő elérhető a Figmában, mert Google Fontok:

- Poppins, súlyok: 400, 500, 600, 700. Ez megy a címekre, a UI-ra és a
  törzsszövegre.
- Lora, variable, 400-től 700-ig, dőlttel együtt. Ez csak hosszú
  szövegre és idézetre való.

Betűméretek. A kódban ezek `clamp()` értékek, tehát a képernyő szélességével
változnak. Figmában a desktop, vagyis a legnagyobb értéket vedd fel:

| Stílus | Desktop méret |
|---|---|
| text-xs | 13 px |
| text-sm | 15 px |
| text-base | 17 px |
| text-lg | 22 px |
| text-xl | 28 px |
| text-2xl | 44 px |
| text-3xl | 64 px |
| text-4xl | 96 px |

Sarokkerekítés: 8, 14, 22 és 32 pixel, plusz a pill alakú elemekhez teljes
kerekítés.

### Amire figyelj a Figma-áttétellel

Az importált fájl kiindulópont, nem design system. Rétegeket kapsz, nem
komponenseket, és a plugin gyakran túl sok egymásba ágyazott framet gyárt.
Számíts arra, hogy takarítani kell utána.

Ami a legfontosabb: ettől kezdve két helyen lesz meg ugyanaz a design, a
kódban és a Figmában. Ezek elcsúsznak egymástól, ha nem döntitek el előre,
melyik az igazi. Ebben a projektben a repo az igazság, mert az megy ki az
ügyfélhez. A Figma-fájl jó vázlatozásra, prezentációra és arra, hogy
megmutassátok, mi hogyan nézne ki, de ha ott átírtok egy színt, az a
weboldalon önmagától nem változik meg. A `tokens.css` az egyetlen hely, ahol
a szín tényleg megváltozik.

Ha csak a szerkezetet akarod megmutatni valakinek, a
`docs/neuwerk-wireframe.pdf` gyorsabb, mint egy Figma-import.

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
