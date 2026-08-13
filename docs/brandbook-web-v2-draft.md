# neuwerk — web brandbook v2 (VÁZLAT, jóváhagyásra)

**Státusz:** vázlat. Ez a dokumentum a web-alapú arculatot javasolja, nem hagyja jóvá.
Készült: 2026-08-12.

**Miért kell:** két független visszajelzés futott össze.

1. A grafikusok szerint az oldal **túl közel van a Lufthansához**. Mérve: az akcentünk
   `#ffa500`, a Lufthansáé `#FFAD00` — RGB-távolság **8,0**, azaz szabad szemmel
   megkülönböztethetetlen. A sötét alap `#1b1e52` vs `#05164D`, távolság **23,9**.
   Mindkét rendszer *navy + meleg akcent + fehér*, és mindkét akcent megbukik fehéren
   (1,97:1 vs 1,87:1), tehát mindkettő kénytelen sötét alapra menni. Nem másolás:
   ugyanaz a bevett ipari sablon. De a piaci megkülönböztetéshez kevés.
2. Az oldal **"AI-osnak" hat**. Ez viszont NEM színkérdés — lásd a 4. fejezetet.

---

## 1. Mi marad

A v1.1 brandbook nem dobható el, és nem is kell. Ezek maradnak:

| elem | érték | miért marad |
|---|---|---|
| Navy Blue | `#1b1e52` | Pantone 2766 C, nyomdai referencia, a logó része |
| Sun | `#ffa500` | Pantone 137 C, a logó ikonja |
| White | `#ffffff` | |
| Poppins | headline, UI | a logotype karakteréhez legközelebbi |
| Lora | editorial | |
| neuwerk pattern | a logó szimbólumából | a márka egyetlen saját formanyelve |

**A logó nem változik.** Se szín, se geometria.

---

## 2. Mi változik: az ARÁNYOK, nem a színek

A Lufthansa-hasonlóság nem abból jön, hogy melyik színeket használjuk, hanem abból,
**mennyit** használunk belőlük. A Lufthansa navy-domináns. Ha mi is az vagyunk,
ugyanúgy nézünk ki.

### 2.1 Az alapfelület világos lesz

| | v1 (jelenlegi) | v2 (javaslat) |
|---|---|---|
| domináns felület | navy | **fehér / világos** |
| navy szerepe | alap | **kiemelés, tagolás, egy-két szekció** |
| felületarány (becsült) | ~60% navy / 40% világos | **~25% navy / 75% világos** |

Ez a legnagyobb egyetlen lépés a Lufthansától való elszakadásban, és pont egybeesik
azzal, amit a grafikusok az új, világos PPT-sablonban szerettek.

A brandbook ezt megengedi: *"White carries equal weight as a foundation color:
large-format surfaces can be built on white just as confidently as on Navy Blue."*
Tehát nem szabályt sértünk, hanem egy eddig kihasználatlan felét használjuk ki.

### 2.2 A blue tintek kapnak valódi szerepet

Eddig a négy tintből gyakorlatilag csak a Blue tint 1 és 3 élt, azok is technikai
szerepben (pattern, másodlagos szöveg). A v2-ben mindegyiknek dolga lesz:

| token | HEX | v1 szerepe | **v2 szerepe** |
|---|---|---|---|
| Blue tint 1 | `#273993` | pattern navy-n | pattern navy-n + primer link világos alapon |
| Blue tint 2 | `#4e66af` | gyakorlatilag semmi | interaktív állapotok, ikonszín |
| Blue tint 3 | `#8895cb` | másodlagos szöveg sötéten | **lágy formák világos alapon** |
| Blue tint 4 | `#afc6e7` | semmi | **lágy formák világos alapon, halvány felületek** |

A "lágy bigyók" a világos sablonból pontosan ezek: **Blue tint 4 fehéren**, nagy
léptékben, alacsony kontraszttal. A pattern eddig csak sötétben létezett; a v2-ben
világos változata is lesz, ugyanazzal a geometriával.

> **Ehhez brandbook-módosítás kell.** A v1.1 merch-guideline azt írja, a pattern
> *"kizárólag Blue Tint 01-ben, Navy Blue háttéren"*. A világos variáns ezt kibővíti:
> Blue tint 3 vagy 4, fehér háttéren, ugyanazzal a nagy léptékkel és ugyanazzal
> a "kisméretű, sűrű, dekoratív használat tilos" megkötéssel.
> **Ezt jóvá kell hagyatni.**

### 2.3 A Sun aránya tovább csökken

Világos alapon a Sun úgyis tilos szövegként (1,97:1). A v2-ben a Sun szerepe:

- a logó ikonja
- **egyetlen** primer CTA oldalanként
- az aktív állapot jelölése
- a videóban a rendszervezetékek

Ennyi. A jelenlegi oldalon a narancs sorszámok, hairline-ok és jelölővonalak
összeadódnak — ez az, ami "Lufthansa-sárgás" összbenyomást ad.

---

## 3. Navigáció: el a sávtól

A jelenlegi fejléc teljes szélességű navy sáv, jobbra igazított linkekkel és egy
kitöltött CTA-gombbal. Ez a Lufthansa-minta.

**Referencia (az ügyfél saját benchmarkja): rivian.com.** Lemérve a jelenlegi kódjukat:

```
<header data-open="false" style="height:0px"
        class="rounded-micro border-[0.1px] border-border/50 bg-background
               overflow-hidden shadow-nav
               transition-[border-radius] duration-300 ease-shift-magnetic">
```

Amit ebből átveszünk:

- **A nav önálló, lekerekített, lebegő konténer**, nem teljes szélességű sáv.
- **Kinyíláskor ugyanaz a konténer nő meg**, nem alatta jelenik meg dropdown.
- A sarokkerekítés animálódik a nyitás közben.
- Világos alap, hajszálvékony keret, finom árnyék. Nincs kitöltött színes gomb.

Amit NEM veszünk át: a Rivian palettáját és fontját. Az az ő arculatuk.

---

## 4. Az "AI-os" benyomás — és ez nem szín, hanem szerkezet

Lemérve a jelenlegi oldalon:

| tell | mért | megengedett |
|---|---|---|
| eyebrow-címke (`KISKAPITÁLIS` a cím fölött) | **21** | 10 |
| em-dash a látható szövegben | **22** | 0 |
| `01` / `02` / `03` sorszámcímke | **10** | 0 |
| split-header (bal nagy cím + jobb kis bekezdés) | **2** | 0 |
| hero subtext hossza | **25 szó** | 20 |

Az index.html **6 szekcióra 7 eyebrow-t** használ. Minden szekció ugyanazzal a
`címke → nagy cím → bekezdés` ritmussal indul. Ez az, amit a grafikusok éreznek.
A színek javításától ez NEM fog megszűnni.

**Szerkezeti szabályok a v2-re:**

1. **Eyebrow maximum három szekciónként egy.** A cím önmagában elég.
2. **Nulla em-dash a látható szövegben.** Pont vagy vessző.
3. **Nincs sorszámcímke.** A tartalom a címke.
4. **Nincs split-header.** Cím és bekezdés egymás alatt.
5. **Egy layout-család legfeljebb egyszer** szerepel egy oldalon. Nyolc szekció
   legalább négy különböző elrendezést használ.
6. **Hero subtext max 20 szó.**

---

## 5. Tipográfia

Marad **Poppins + Lora**. Egy megkötés kerül be:

- **Kiemelés a címen belül ugyanannak a fontnak a dőlt vagy félkövér vágatával
  történik**, nem másik betűcsaláddal. A Poppins-cím közé beszúrt Lora-szó amatőr.

---

## 6. Amit jóvá kell hagyni

| # | tétel | döntés kell |
|---|---|---|
| 1 | A világos alapfelület dominanciája (~75/25) | igen |
| 2 | A pattern világos variánsa (Blue tint 3/4 fehéren) | **igen, ez brandbook-módosítás** |
| 3 | A blue tintek kibővített szerepe | igen |
| 4 | A Sun szerepének szűkítése | igen |
| 5 | A nav átalakítása lebegő, morfoló konténerré | igen |
| 6 | A szerkezeti szabályok (4. fejezet) | fejlesztői oldalról kötelező |

---

## 7. Amit ez NEM old meg

Őszintén: a **Sun `#ffa500` és a Lufthansa `#FFAD00` továbbra is 8 RGB-egységre lesz
egymástól.** Ha a cél az, hogy egy német nézőnek se jusson eszébe a Lufthansa,
akkor az akcentszínhez kell nyúlni — az viszont Pantone 137 C, a logó része, és
nyomdai referencia. Ez már nem webes, hanem arculati döntés.

A világos alap + a szűkített Sun-arány + a más navigáció együtt **jelentősen** csökkenti
a hasonlóságot, mert a Lufthansa-benyomás a navy-dominanciából jön. De a színpárt
magát nem szünteti meg.
