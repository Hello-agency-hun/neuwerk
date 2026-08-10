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

> **Nyitott:** az „Identity" nav-címke sántít. Alternatívák: `Our story`, `About`.
> Build 1-ben `Identity`, ügyfél-visszajelzésre változtatható.

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

**Feldolgozás**

1. Vágás: **4,0–15,5 mp** (transzparens stúdió-szekvencia). Ez az egyetlen szakasz, ami
   hurkolható — semleges szürke háttér, folyamatos kameraorbit, nincs fény- vagy
   napszakváltás. Az úton játszódó részek alkonyat→nappal rámpája nem hurkolható.
2. Audiósáv eltávolítása
3. **50%-os split-tone grade**: árnyékok `#1b1e52` felé, csúcsfények hideg fehér felé,
   az eredeti fényrajz és a futómű részletessége **változatlanul megmarad**.
   A meleg (réz) pixelek maszkolva és a valódi Sun `#ffa500`-ra emelve.
4. Crossfade-hurok: az utolsó ~0,5 mp visszaúszik az elsőbe
5. Encode: H.264 + WebM, `+faststart`, poszterkép az első frame-ből

**Célméretek (mérve, nem becsülve)**

| változat | méret |
|---|---|
| orbit-szegmens, 1920, CRF 28 | **3,5 MB** |
| orbit-szegmens, 1280, CRF 28 | **1,75 MB** |
| (referencia) teljes film, 1600, CRF 30 | 3,9 MB |

Desktop: 1920-as változat. Mobil: 1280-as vagy poszterkép, hálózattól függően.

**A SPEC kártya nem kerül az oldalra** — lásd 10. pont.

---

## 7. Solutions — scroll-scrub

A three.js hero car **elvetve.** Indok: a videó már tartalmaz professzionálisan
renderelt transzparens autót, amelyben a narancs kiemelés pontosan a fluid- és
hőmenedzsment-köröket jelöli — azaz vizuálisan azt mutatja, hol van NEUWERK az autóban.
WebGL-ben ennél csak rosszabbat, lassabbat és nehezebben átadhatót lehetne építeni.

Helyette: a Solutions szekcióban ugyanaz a videó scroll-scrubbolva fut, a 4 pillér
pedig a videó idővonalára ugrik. Ugyanaz a hatás, töredék kódból, minden böngészőben.

**Fontos taxonómia-ütközés:** a videó tengelye `SAFETY / PERFORMANCE / EFFICIENCY /
COMFORT` — ezek **előnyök**. A tartalmi spec Solutions szekciója viszont
`fluid handling / thermal management / sealing & damping / multi-material` — ezek
**képességek**. Két különböző rendszer. Kezelés: a hero viszi az előnyöket
(a videóba égetve), a Solutions a képességeket. Ügyfél-egyeztetést igényel.

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

## 10. Nyitott kérdések az ügyfél felé

| # | kérdés | miért számít |
|---|---|---|
| 1 | **A SPEC élő almárka, vagy leselejtezett?** A videó utolsó harmada egy `SPEC` névre fut ki, ami sehol nincs a tartalmi specben. A forrásfájl neve `OESL_animatik` — ez a Continental-korszak anyaga, utólag ráragasztott neuwerk endcarddal. | Ha leselejtezett, a videó ezen része semmiképp nem mehet ki. Jelenlegi feltételezés: **nem használjuk.** |
| 2 | **A négy előny vs. a négy képesség** (7. pont) | Két párhuzamos taxonómia fut az anyagokban |
| 3 | **Media tartalom.** A spec csak annyit ír: „Content?" | 3 demo cikk placeholder tartalommal készül |
| 4 | **Career pozíciók forrása.** Statikus lista, vagy külső ATS? | Build 1: statikus `jobs.js` placeholder tételekkel |
| 5 | **A valódi brand font.** A brandbook Poppinst *ajánl* („a logotype karakteréhez vizuálisan legközelebb álló"), nem előír. Ha készül egyedi vágat, cserélhető. | Egyetlen `--nw-font` változóból jön minden |
| 6 | **Az „Identity" nav-címke** | Lásd 4. pont |
| 7 | **Kontakt adatok.** Milyen címek, telefonszámok, e-mailek mennek ki? | Nincs űrlap; Build 1 placeholder adatokkal |
| 8 | **Színeltérés.** A videó endcardján a slash `#c9901c`, a vektoros logóban `#ffa500`. A videó gradingje húzta el. | Az oldalon a vektoros érték megy |

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
