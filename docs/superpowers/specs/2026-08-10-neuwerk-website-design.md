# NEUWERK weboldal — design spec

**Dátum:** 2026-08-10
**Készítette:** Hello Agency
**Státusz:** jóváhagyásra vár
**Fázis:** Build 1 — kattintható, brandelt prototípus ügyfél-jóváhagyáshoz

---

## 1. Cél és hatókör

A NEUWERK (Continental egykori Original Equipment Solutions üzletágából kivált,
független globális vállalat) publikus weboldala.

**Build 1 célja:** az ügyfél végig tudja kattintani a teljes oldalstruktúrát, és
jóváhagyja a tartalmi wireframe-et — de már a NEUWERK arculatában, valódi szöveggel,
hogy a strukturális és a hangulati jóváhagyás egy körben megtörténjen.

**Leszállítandó:** egy zip, amit az ügyfél a saját szerverére másol. Tiszta statikus
HTML/CSS/JS. Nincs build lépés, nincs npm, nincs PHP, nincs adatbázis.

**Nem hatókör (Build 1):**
- WebGL / three.js fejlesztés
- Több nyelv (a struktúra viszont felkészül rá)
- CMS vagy admin felület
- Kontakt űrlap (döntés: nincs űrlap, csak kontaktadatok)

---

## 2. Forrásanyagok

| fájl | mit ad |
|---|---|
| `Structure_and_Content_NEUWERK_Website_agi_review.pdf` | teljes EN copy és oldalstruktúra |
| `Arculat/01_neuwerk_brandbook/neuwerk_brandbook_FINAL.pdf` | **hiteles** paletta, tipográfia, logószabályok |
| `Arculat/01_neuwerk_brandbook/neuwerk_merch.pdf` | a Neuwerk pattern hivatalos szabályai |
| `Arculat/01_neuwerk_brandbook/neuwerk_building_signage.pdf` | logó clear space, színhasználat |
| `Arculat/00_neuwerk_logo/RGB/**` | hivatalos logók: navy, white, mono black, mono white (svg/ai/eps/png) |
| `Arculat/01_neuwerk_brandbook/neuwerk_brandbook_FINAL/Fonts/` | Poppins (4 súly) + Lora (variable + italic) TTF |
| `Arculat/03_neuwerk_logo_anim/neuwerk_logo_reveal.mp4` | 10 mp logó reveal, **318 KB**, 1080p |
| `Arculat/02_oesl_logo/` | jogelőd márkajel (a weboldalon nem használjuk) |
| `Arculat/03_regent_logo/` | tulajdonos logója |
| `useful visual assets/OESL_animatikv_v29.mp4` | **transparent car animatik** — a hero forrása |
| `useful visual assets/01_banners.zip` | 9 db 1920×1080 banner, aloldal-hero háttérnek |
| `useful visual assets/*.pptx` | PPT template, a világos/sötét szekcióritmus referenciája |

---

## 3. Dizájnrendszer

### 3.1 Színek (brandbook 04 — hiteles értékek)

**Elsődleges**

| név | HEX | szerep |
|---|---|---|
| Navy Blue | `#1b1e52` | elsődleges szín, nagy felületeken dominál. Pantone 2766 C |
| White | `#ffffff` | **egyenrangú** vászon a navy-vel |
| Blue tint 1 | `#273993` | a Neuwerk pattern színe |
| Blue tint 2 | `#4e66af` | tonális mélység |
| Blue tint 3 | `#8895cb` | másodlagos szöveg sötét háttéren |
| Blue tint 4 | `#afc6e7` | halvány rétegek |

**Akcent**

| név | HEX | szabály |
|---|---|---|
| Sun | `#ffa500` | **max. 10–15% a látható felületből.** Pantone 137 C |

Sun engedélyezett helyei az oldalon: logó ikon, aktív nav-jelölés, primer CTA,
fókuszgyűrű, a hero videó rendszervezetékei, szekció-számozás. **Soha nem háttér.**

**Szürkék:** `#000000` · `#333333` · `#666666` · `#999999` · `#b4b4b4` · `#cccccc` · `#e6e6e6`

**Másodlagos paletta** (Mint `#1eb78b` / Azure `#48c3cb` / Melon `#f37558` / Levander `#d18ab5`,
mindegyik 3 árnyalattal): a brandbook szerint **kizárólag** infografikán, diagramon,
illusztráción használható — fő brandfelületen nem. Az oldalon csak akkor jelenik meg,
ha adatvizualizáció kerül bele.

> **Hiba a brandbook v1.1-ben:** a 6. oldalon a *White* swatch alá a Black értékei
> csúsztak (`RGB 100 100 100 / HEX 000000`). Javítandó a v1.2-ben. A specben
> White = `#ffffff`.

### 3.2 Tipográfia

| szerep | betűtípus | súlyok |
|---|---|---|
| elsődleges — headline, UI, gomb, kiemelés | **Poppins** | Regular, Medium, SemiBold, Bold |
| másodlagos — hosszú szöveg, idézet, editorial | **Lora** | Regular, Medium, SemiBold, Italic |

Mindkettő OFL-licencű, mindkettő megvan TTF-ben a mappában.
**Kötelezően self-hosted woff2** — nincs Google Fonts CDN (német ügyfél, GDPR).

Gyakorlati elosztás az oldalon:
- **Poppins**: navigáció, minden headline, gomb, számok, rövid törzsszöveg, UI-mikroszöveg
- **Lora**: Media cikkek törzse, az „A new identity" story, pull-quote-ok

### 3.3 A Neuwerk pattern

A brandbook (merch guideline) szó szerinti szabálya:

> „A Neuwerk pattern a logó grafikai szimbólumából származik. Kizárólag **Blue Tint 01-ben,
> Navy Blue háttéren** használható. Mindig **bátran és jól láthatóan** jelenjen meg,
> lehetőleg nagyobb felületet lefedve. **A kisméretű, túl sűrű vagy pusztán dekoratív
> használat kerülendő.**"

Ebből következő megkötések:

- pattern szín: **kizárólag** `#273993` on `#1b1e52`
- **szekciónként 2–3 forma**, nem több
- minden forma legalább a viewport rövidebbik oldalának 40%-a
- nincs részecskerendszer, nincs egérparallax-mező, nincs apró ismétlődő textúra
- világos szekciókban **nincs pattern** — ott tiszta tipográfia és képanyag visz mindent

Technikailag: `border-radius: 9999px` + `transform: rotate()`, tiszta CSS.
Mozgás: scroll-vezérelt, lassú, nagy amplitúdójú eltolás.

### 3.4 Logóhasználat

- **Elsődleges:** navy háttér + fehér logotype + Sun ikon. A brandbook szerint ezt kell
  preferálni minden felületen, ahol lehet → **a header navy.**
- Világos háttéren: navy logotype + Sun ikon
- Monokróm: csak ha a felület nem enged színt
- Clear space: **1× az ikon magassága** minden oldalon
- Minimum digitális méret: **24 px**. Az alatt csak az ikon → **a favicon a slash maga**
- Tilos: forgatás, torzítás, idegen szín, árnyék/körvonal/effekt, zsúfolt háttér,
  az ikon és a szöveg közti távolság módosítása

**Módosítás a szállított SVG-ken:** a hivatalos fájlokban a slash `fill: orange`
CSS-kulcsszóval van definiálva. Átírandó `fill: var(--nw-sun, #ffa500)`-ra, hogy a
logó színe kódból vezérelhető legyen. A geometria érintetlen marad — nincs újrarajzolás.

### 3.5 Világos/sötét ritmus

Nem felhasználói kapcsoló, hanem **szekció-tulajdonság**. A brand mindkét módban létezik,
és a váltakozásuk maga a védjegy. Nincs dark mode toggle.

### 3.6 Kontraszt (WCAG 2.1, számolt értékek)

| pár | arány | AA törzs | AA nagy | AAA |
|---|---|---|---|---|
| White on Navy | 15,51:1 | ✅ | ✅ | ✅ |
| Navy on White | 15,51:1 | ✅ | ✅ | ✅ |
| Blue tint 4 on Navy | 8,90:1 | ✅ | ✅ | ✅ |
| **Sun on Navy** | **7,85:1** | ✅ | ✅ | ✅ |
| **Navy on Sun** | **7,85:1** | ✅ | ✅ | ✅ |
| Grey 02 on White | 5,74:1 | ✅ | ✅ | — |
| Blue tint 3 on Navy | 5,32:1 | ✅ | ✅ | — |
| Grey 03 on White | 2,85:1 | ❌ | ❌ | — |
| Blue tint 2 on Navy | 2,84:1 | ❌ | ❌ | — |
| **Sun on White** | **1,97:1** | ❌ | ❌ | — |
| **White on Sun** | **1,97:1** | ❌ | ❌ | — |

Kötelező szabályok ebből:

1. **Sun szöveg fehér háttéren tilos** (1,97:1). Világos szekcióban a Sun csak
   kitöltésként, vonalként vagy ikonként jelenhet meg — soha szövegként.
2. **Sun-kitöltésű gomb felirata Navy, nem fehér.** A fehér-narancs 1,97:1;
   a navy-narancs 7,85:1 (AAA).
3. **Blue tint 1 és 2 soha nem hordoz szöveget.** A tint 1 a pattern színe
   (1,55:1 navy-n) — ez szándékos, háttérelem.
4. Sötét szekcióban a másodlagos szöveg **Blue tint 3** (5,32:1) vagy
   **Blue tint 4** (8,90:1). Tint 2 nem.
5. Világos szekcióban a másodlagos szöveg **Grey 02** (5,74:1). Grey 03 nem.
6. A Sun mint fókuszgyűrű navy háttéren működik (7,85:1); fehér háttéren a
   fókuszgyűrű Navy legyen.

---

## 4. Információs architektúra

```
index.html                       Főoldal
  ├── #who-we-are
  ├── #footprint
  ├── #solutions
  └── #ambition
identity.html                    A new identity
career.html                      Career          → data/jobs.js
media.html                       Media hub       → data/news.js
  └── media/<slug>.html          cikkoldalak (3 demo)
responsibility.html              „Acting Responsibly" hub
  ├── legal/code-of-conduct.html
  ├── legal/compliance-ethics.html
  ├── legal/supplier-requirements.html
  ├── legal/privacy-policy.html
  └── legal/legal-notice.html
integrity-line.html              Whistleblower Reporting
contact.html                     Contact
404.html
```

**16 oldal.** Az 5 jogi dokumentum Build 1-ben kattintható stub „content pending"
jelöléssel — a cél, hogy az ügyfél sehol ne fusson zsákutcába.

**Navigáció (6 elem):** `Who we are · Solutions · Identity · Career · Media · Contact`
Nincs dropdown. Az első kettő főoldali anker; aloldalról `/#who-we-are` alakban működik.

**Footer:** Responsibility hub + 5 dokumentum, Integrity Line, kontakt,
footer claim (*„NEUWERK turns expertise into impact"*), Regent tulajdonosi sor.

> **Eldöntve (2026-08-10):** a nav-címke marad **`Identity`**. Ha az ügyfél átírja,
> egyetlen `partials/header.html` sor és a 16 oldal keresés-cseréje.

---

## 5. Főoldal — szekciók

| # | szekció | mód | tartalom | mozgás |
|---|---|---|---|---|
| 0 | Intro | navy | logó reveal | 1,2 mp, átugorható, `sessionStorage`, egyszer/látogatás |
| 1 | **Hero** | videó | *NEUWERK / Turning Expertise into Impact* + 2 CTA | orbit-loop videó |
| 2 | Who we are | fehér | *Built on Expertise. Driven by Progress.* + 3 blokk | lépcsőzetes reveal |
| 3 | Global Footprint | fehér→navy | világtérkép, 16 pont | pulzálás + felszámláló 14 000 / 16 / 1 |
| 4 | **Solutions** | navy | 4 pillér | **scroll-scrub a hero videón** |
| 5 | Our ambition | navy | 4 elv | pattern tagolja |
| 6 | Explore more | fehér | kártyák: Identity / Career / Media | hover-lift |
| 7 | Footer | navy | claim + navigáció + Regent | — |

A copy szó szerint a tartalmi specből jön, változtatás nélkül.

---

## 6. Hero videó

**Forrás:** `OESL_animatikv_v29.mp4` — 1920×1080, 30 fps, 28,33 mp, 850 frame,
H.264 + AAC, 35,9 MB. **Vágás nincs benne**, végig egy folyamatos kameramozgás
átúszásokkal. Az audiósáv **digitális csend** (−91 dB) → eldobandó.

**Tartalmi idővonal**

| idő | tartalom |
|---|---|
| 0,0–1,5 | fekete → felúszás, út alkonyatban |
| 1,5–4,0 | az autó közeledik, nappalra vált a fény |
| **4,0–15,5** | **transzparens stúdió-szekvencia** — `SAFETY` → `PERFORMANCE` → `EFFICIENCY` → `COMFORT` a padlóra vetítve |
| 15,5–18,0 | visszakapja a lime fényezést, vissza az útra |
| 18,0–20,0 | elhajt, zászlók a négy szóval |
| 20,0–22,0 | narancs **SPEC** betűk, kifehéredés |
| 22,0–26,0 | **SPEC** címkártya |
| 26,0–28,3 | neuwerk endcard — *„Built on expertise. Driven by progress."* |

**A SPEC nem kerül sehova.** Ügyfél-visszajelzés (2026-08-10): a `SPEC` szó itt egyszerűen
a *specification* rövidítése, nem márkanév. **Semmilyen formában nem használjuk** —
sem címkártyaként, sem szövegként, sem a jelenetbe komponált narancs betűkként.

Vágási pont ebből: a narancs SPEC betűk **20,0 és 20,5 mp között** állnak össze, a zászlós
szakasz **18,0 mp-től** jön. A felhasználható anyag felső határa ezért **17,0 mp** —
két és fél másodperc ráhagyással.

**Feldolgozás**

1. Vágás: **4,0–17,0 mp**. Egyetlen fájl szolgálja ki a herót és a Solutions scrubot is:
   - a hero a **4,0–15,5** tartományt pörgeti (transzparens stúdió-szekvencia — semleges
     szürke háttér, folyamatos kameraorbit, nincs napszakváltás, ezért ez az egyetlen
     hurkolható szakasz),
   - a Solutions a teljes **4,0–17,0** tartományt scrubbolja, mert a multi-material
     leképezéshez kell a 15,5–17,0 közötti visszafényezés is.
2. Audiósáv eltávolítása (digitális csend)
3. **50%-os split-tone grade**: árnyékok `#1b1e52` felé, csúcsfények hideg fehér felé,
   az eredeti fényrajz és a futómű részletessége **változatlanul megmarad**.
   A meleg (réz) pixelek maszkolva és a valódi Sun `#ffa500`-ra emelve.
4. **A hurokvágás nem égetődik bele.** A hero böngészőben old crossfade-et: ~15,3 mp-nél
   visszaugrik 4,0-ra egy rövid (kb. 200 ms) opacitás-átúszással. Így ugyanaz a fájl
   scrubbolható a Solutionsnél anélkül, hogy egy beégetett átúszás átvillanna rajta.
5. Encode: H.264 + WebM, `+faststart`, poszterkép a 4,0 mp-es frame-ből

**Célméretek (mérve, nem becsülve)**

| változat | méret |
|---|---|
| **4,0–17,0 mp (13 s), 1920, CRF 28** | **4,36 MB** ← a szállítandó desktop asset |
| **4,0–17,0 mp (13 s), 1280, CRF 28** | **2,16 MB** ← mobil |
| (referencia) 4,0–15,5 mp, 1920 | 3,50 MB |
| (referencia) teljes film, 1600, CRF 30 | 3,90 MB |

Minden érték `-preset slow`, `-crf 28`, hang nélkül, `+faststart` mellett mérve.
Eredeti: 35,9 MB → **4,36 MB**, nyolcadára.

Desktop: 1920-as változat. Mobil: 1280-as vagy poszterkép, hálózattól függően.
Egy fájl → egy letöltés → egy cache, két funkcióra.

A grade (3. lépés) még nincs benne ezekben a számokban, de nem növeli érdemben a
bitrátát — split-tone művelet, nem ad új részletet a képhez.

---

## 7. Solutions — scroll-scrub

A three.js hero car **elvetve.** Indok: a videó már tartalmaz professzionálisan
renderelt transzparens autót, amelyben a narancs kiemelés pontosan a fluid- és
hőmenedzsment-köröket jelöli — azaz vizuálisan azt mutatja, hol van NEUWERK az autóban.
WebGL-ben ennél csak rosszabbat, lassabbat és nehezebben átadhatót lehetne építeni.

Helyette: a Solutions szekcióban ugyanaz a videó scroll-scrubbolva fut, a 4 pillér
pedig a videó idővonalára ugrik. Ugyanaz a hatás, töredék kódból, minden böngészőben.

**Taxonómia — feloldva.** A videó tengelye `SAFETY / PERFORMANCE / EFFICIENCY / COMFORT`
(**előnyök**, a képbe égetve), a Solutions szekcióé `fluid handling / thermal management /
sealing & damping / multi-material` (**képességek**). Nem ugyanaz, de nem is kell, hogy az
legyen: a videó minden képességhez tartalmaz egy olyan szakaszt, ami vizuálisan pontosan
azt mutatja. Ügyfél-döntés (2026-08-10): használjuk a legjobban illeszkedő szegmenseket.

**Képesség → videószakasz leképezés**

| képesség | szakasz | mi látszik |
|---|---|---|
| Fluid handling systems | **9,5–11,0 mp** | a teljes narancs cső- és vezetékhálózat kigyulladva, végig az alvázon |
| Thermal management | **11,5–13,0 mp** | alsó kameraállás a battery pack hűtőlemezére |
| Sealing and damping | **14,0–15,5 mp** | szórt, diszkrét narancs elemek: bakok, szilentek, csillapítók |
| Multi-material applications | **15,5–17,0 mp** | a visszafényezés: karosszéria, alváz és komponensek egyszerre, külön anyagként |

A padlóra vetített `SAFETY` / `PERFORMANCE` / stb. feliratok ezekben a szakaszokban
láthatók. Mivel más taxonómiát jelölnek, mint a fölöttük megjelenő pillércímke, két
kezelési mód lehetséges — implementációkor eldöntendő:

- **a)** a scrub-nézetben a videó alsó sávja levágva (a feliratok a padlón vannak,
  tehát a képkocka alsó harmadában) — egyszerű, nem kell utómunka
- **b)** a feliratok meghagyva, mert előnyként olvasva erősítik a képességet

Alapértelmezés: **a)**. Ha az ügyfél a feliratokat is látni akarja, b)-re váltunk.

**Ha egy szegmens nem elég jó**, a hiányzó vizuál Higgsfielddel újragenerálható —
statikus renderként, a fenti szakasz helyett. Ez tartalék, nem alapterv.

---

## 8. Technikai architektúra

**Zero-build, önhordó oldalak.** Nincs build lépés, nincs npm, nincs `dist/`.
A zip kicsomagolva azonnal működik, akkor is, ha csak duplakattintanak az `index.html`-en.

A header/footer markup ismétlődik minden fájlban, `<!-- @partial:header -->` /
`<!-- /@partial:header -->` jelölőkkel keretezve. A duplikáció karbantartása egy
agentnek vagy fejlesztőnek egyetlen keresés-csere.

**Kritikus megkötés — `file://` kompatibilitás:** a `fetch()` CORS miatt nem működik
lokálisan megnyitott fájlból. Ezért a változó tartalom nem JSON, hanem JS értékadás:

```js
// data/news.js
window.NEUWERK_NEWS = [ /* … */ ];
```

Az ügyfélnek ugyanúgy egy szerkeszthető szöveges lista, viszont a prototípus szerver
nélkül is végigkattintható. Ugyanez `data/jobs.js`.

**i18n-felkészítés:** a copy külön adatrétegben, a URL-struktúra `/en/` gyökérre
bővíthető. Build 1 egynyelvű (EN).

### Fájlstruktúra

```
neuwerk-web/
├── index.html … contact.html
├── legal/            5 jogi stub oldal
├── media/            3 demo cikkoldal
├── assets/
│   ├── brand/        logó SVG-k (--nw-sun változóra írva), favicon
│   ├── video/        hero-loop.mp4 · .webm · poster.jpg · intro.mp4
│   ├── fonts/        Poppins 4 súly + Lora 4 súly, woff2
│   └── img/
├── css/
│   ├── tokens.css    a teljes brandbook egyetlen fájlban
│   ├── base.css
│   ├── components.css
│   └── sections.css
├── js/
│   ├── nav.js
│   ├── pattern.js
│   ├── reveal.js
│   ├── counters.js
│   └── scrub.js
├── data/             news.js · jobs.js
├── partials/         referencia header/head/footer
├── docs/             HANDOFF.md · CHANGELOG.md · specs/
├── CLAUDE.md
└── README.md
```

### 8.1 Media és Career tartalommodell

Mindkettő ugyanazt a mintát követi: **egy szerkeszthető lista + egy renderelő szkript.**
Nincs CMS, nincs build, nincs admin felület.

```js
// data/news.js
window.NEUWERK_NEWS = [
  {
    slug:     "how-to-update-this-page",
    date:     "2026-08-10",
    title:    "…",
    excerpt:  "…",
    image:    "assets/img/news/…",
    placeholder: true            // → látható badge a kártyán
  },
];
```

A `media.html` és a `career.html` ebből rendereli a listát. A cikkeknek külön statikus
HTML oldaluk van a `media/<slug>.html` alatt, hogy a linkek megoszthatók és
indexelhetők legyenek.

**Build 1 tartalma**

- **3 placeholder cikk**, mindegyik látható badge-dzsel.
  Az egyik cikk címe és tartalma **arról szól, hogyan tudják maguk frissíteni és bővíteni
  a cikklistát**: melyik fájlt kell szerkeszteni, milyen mezők vannak, hogyan kell új
  oldalt hozzáadni, mekkora legyen a kép. Így a placeholder egyben a felhasználói
  dokumentáció, és nem vész el egy külön PDF-ben, amit senki nem nyit meg.
- **Placeholder pozíciólista** a Careeren, ugyanezzel a logikával.

Ugyanez a leírás bekerül a `docs/HANDOFF.md`-be is, fejlesztői nyelven.

---

## 9. Átadhatóság

A projekt egy ponton átkerül másik fejlesztőhöz, másik Claude-hoz vagy agenthez, és
esetleg Claude Designbe. Ezt a struktúra explicit módon támogatja:

- **`CLAUDE.md`** a gyökérben: tokenek, konvenciók, mi hol van, **mi placeholder és
  mi végleges**. Ez az átvevő első olvasmánya.
- **`docs/CHANGELOG.md`**: minden változás naplózva, dátummal.
- **`docs/HANDOFF.md`**: aktuális állapot, nyitott ügyfélkérdések, jóváhagyásra várók.
- Minden ideiglenes tartalom `<!-- TODO(client): … -->` jelöléssel **és** látható
  badge-dzsel, amit egyetlen CSS osztály kikapcsol build 1 után.
- Conventional commit üzenetek.
- Minden oldal önhordó → Claude Designba vitelhez nem kell build környezetet reprodukálni.

**Repo:** https://github.com/Hello-agency-hun/neuwerk.git

---

## 10. Ügyfélkérdések — státusz

### 10.1 Lezárva (2026-08-10)

| # | kérdés | döntés |
|---|---|---|
| 1 | A SPEC élő almárka? | **Nem.** A `SPEC` itt a *specification* rövidítése, nem márkanév. Semmilyen formában nem használjuk — sem címkártyaként, sem sehogy. Vágási pont: 17,0 mp. |
| 2 | Négy előny vs. négy képesség | Használjuk a legjobban illeszkedő videószakaszt képességenként. Leképezés a 7. pontban. Ha egy szakasz nem elég jó, Higgsfielddel újragenerálható. |
| 3 | Media tartalom | Placeholder cikkek, láthatóan jelölve. **Az egyik cikk arról szól, hogyan tudják majd frissíteni és bővíteni a cikklistát** — a placeholder egyben dokumentáció. |
| 4 | Career pozíciók | Ugyanaz a minta: statikus lista, a `data/jobs.js` szerkesztésével frissül. |
| 5 | Betűtípus | **A brandbookot követjük**: Poppins + Lora. |
| 6 | „Identity" nav-címke | Marad. Az ügyfél átírhatja. |
| 8 | Színeltérés (videó `#c9901c` vs. vektor `#ffa500`) | **A vektoros logó a mérvadó** → `#ffa500` mindenhol. |

### 10.2 Nyitva — bekérendő az ügyféltől

| # | kérdés | Build 1 kezelése |
|---|---|---|
| 7 | **KONTAKT ADATOK.** Milyen címek, telefonszámok, e-mail címek, cégadatok mennek ki? | Szándékosan hamis, felismerhető placeholderek: `info@example.com`, `+00 000 000 0000`, `Example Street 1, 00000 Example City`. Automatikusan ellenőrizve — lásd lent. |
| 9 | **A 16 ORSZÁG MEGNEVEZÉSE.** Sem a tartalmi spec, sem a brandbook nem sorolja fel őket, a Global Footprint térképhez viszont 16 konkrét pont kell. | `data/locations.js` 16 jelölt placeholder-pozícióval, látható badge-dzsel a térkép alatt. |
| 10 | **Media cikkek valós tartalma.** | 3 placeholder cikk, jelölve. Az egyik a frissítés módját dokumentálja — ez marad élesben is. |
| 11 | **Career pozíciók valós listája.** | 3 placeholder pozíció a `data/jobs.js`-ben, jelölve. |
| 12 | **Az 5 jogi dokumentum szövege** (Code of Conduct, Compliance & Ethics, Supplier Requirements, Privacy Policy, Legal Notice). | 5 kattintható stub oldal „content pending" jelöléssel. |

> ⚠️ **Az 5 tétel egyike sem zárható le fejlesztői oldalról** — mind ügyfél-adatszolgáltatást
> igényel. Minden placeholder `<!-- TODO(client): … -->` megjegyzéssel **és** látható
> badge-dzsel szerepel, és a `tools/check_placeholders.py` leltározza őket a
> `docs/HANDOFF.md`-be.
>
> A kontaktadatokra külön gép is vigyáz: a `check_placeholders.py` **hibával leáll**,
> ha bármelyik e-mail cím nem `example.com` / `example.org` / `example.net` végű.
> Így valós kontaktadat nem hiányozhat észrevétlenül, és kitalált „hihető" adat nem
> csúszhat élesbe.

---

## 11. Kész-kritériumok (Build 1)

1. Minden nav-elem és minden link működik, **nulla zsákutca**
2. A zip kicsomagolva, `index.html`-re duplakattintva, **szerver nélkül** végigkattintható
3. Törésmentes 375 / 768 / 1280 / 1920 px-en
4. `prefers-reduced-motion: reduce` mellett semmi nem törik: hero → poszterkép,
   scrub → statikus képsor
5. A Sun sehol nem lép 15% fölé
6. A pattern sehol nem kicsi, sűrű vagy pusztán dekoratív; csak navy szekciókban
7. Egyetlen külső hálózati kérés sincs (font, ikon, script mind lokális)
8. Lighthouse zöld a főoldalon
9. Minden placeholder látható badge-dzsel jelölve
10. Minden szöveg-háttér pár megfelel a 3.6 táblázatnak. Külön ellenőrizendő:
    sehol nincs Sun szöveg világos háttéren, és egyetlen Sun-kitöltésű gombon
    sincs fehér felirat
11. A `SPEC` szó **sehol nem jelenik meg** — sem a videóban, sem szövegben, sem
    fájlnévben. A videó 17,0 mp-nél vágva.
12. Minden kontaktadat felismerhetően placeholder (`example@example.com` mintázat),
    látható badge-dzsel és `TODO(client)` megjegyzéssel. **Éles indulás előtt ez
    blokkoló tétel** — a `docs/HANDOFF.md` nyitott listáján marad, amíg az ügyfél
    nem szolgáltatja az adatokat.

---

## 12. Rögzített döntések

| # | döntés | választott |
|---|---|---|
| 1 | Build 1 készültsége | brandelt prototípus (nem szürke wireframe) |
| 2 | Térkép | csak dekoratív stat-vizuál, nincs Locations aloldal |
| 3 | Nyelv | EN only, i18n-re felkészítve |
| 4 | Változó tartalom | JS adatfájl (`window.NEUWERK_*`), nem JSON+fetch |
| 5 | Kontakt form | nincs űrlap, csak kontaktadatok → nem kell PHP |
| 6 | Motion | nagy pill-formák + videó; **three.js elvetve** |
| 7 | Architektúra | zero-build, önhordó oldalak |
| 8 | Hero videó | orbit-loop 4,0–15,5 mp + scroll-scrub a Solutions-nél |
| 9 | Hero grade | 50% split-tone navy, Sun `#ffa500`-ra emelve |
| 10 | Regent logó | footerben, diszkréten |
| 11 | OESL logó | **nem** használjuk, csak szövegben említjük |
| 12 | SPEC | semmilyen formában nem használjuk; a videó 17,0 mp-nél vágva |
| 13 | Videófájlok száma | **egy** fájl (4,0–17,0 mp) szolgálja ki a herót és a scrubot is |
| 14 | Képesség → videószakasz | leképezve (7. pont); Higgsfield csak tartalék |
| 15 | Media / Career tartalom | placeholder, láthatóan jelölve; egy cikk a frissítés módját dokumentálja |
| 16 | Betűtípus | brandbook szerint: Poppins + Lora |
| 17 | Kontaktadatok | felismerhető `example@example.com` placeholderek; bekérés kötelező lépés |
