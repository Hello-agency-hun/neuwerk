# neuwerk weboldal — átadási dokumentum

> Ez a dokumentum megegyezik a Slack canvas tartalmával:
> https://agencyhello.slack.com/docs/T0P5KL5PC/F0BPQD98A2Y
>
> Azért van a repóban is, hogy a grafikus a kóddal együtt megkapja.
> Technikai részletek: `docs/HANDOFF.md`, `CLAUDE.md`, `design-system.html`.

## Rövid összefoglaló

A neuwerk weboldal első buildje elkészült. **Ez már nem wireframe.** Az eredeti
terv egy kattintható tartalmi váz volt, de menet közben áttoltuk vizuális
irányba, hogy az elfogadási folyamat gyorsuljon: az ügyfél ne egy szürke
dobozrendszert lásson, hanem egy kb. félkész oldalt, amire konkrétan meg tudja
mondani, mi kell, mi nem, és mit gyártsunk újra.

**Kezeljék félkész oldalként, ne vázlatként.** Jelentős art direction munkaóra
van benne: a teljes vizuális rendszer, a videóvágás, a generált assetek és a
mozgásterv.

**A fő ajánlatunk:** ezekkel a képekkel és ezzel a vizuális rendszerrel menjünk
tovább. Minden a frissített brandbook alapján készült — szín, tipográfia,
pattern-szabály, logóhasználat és copy tekintetében egyaránt. Ami ettől eltér,
az visszalépés lenne.

## Mi készült el

10 oldal, végigkattintható, nulla halott linkkel: főoldal, A new identity,
Career, Media hub + 3 cikkoldal, Acting Responsibly, Contact, 404.

## Stack, és miért ez

Tiszta statikus HTML / CSS / JS. Nincs build lépés, nincs npm, nincs CMS.

- **Nincs `fetch()` sehol.** A csomag akkor is működik, ha valaki kicsomagolja
  és duplán kattint az `index.html`-en.
- **Nulla külső hálózati kérés.** A fontok self-hosted woff2-ként vannak benne,
  nincs Google Fonts CDN — német ipari ügyfélnél az GDPR-kockázat.
- **A változó tartalom** (hírek, állások, térképpontok) egyszerű JS adatfájl,
  amit szövegszerkesztővel is lehet frissíteni.
- **PHP csak a bemutató-változatban van**, a megjegyzés-gyűjtő miatt.
  Az éles csomagban nincs.

## Miből dolgoztunk

A **brandbook v1.1** a hiteles forrás, nem becslés:

| | |
|---|---|
| Navy Blue | `#1b1e52` — Pantone 2766 C, nagy felületeken dominál |
| White | `#ffffff` — egyenrangú vászon a navy-vel |
| Blue tint 1 | `#273993` — a Neuwerk pattern színe |
| **Sun** | `#ffa500` — Pantone 137 C, **max. a felület 10–15%-a**, soha nem háttér |
| Tipográfia | **Poppins** (headline, UI, gomb) + **Lora** (hosszú szöveg, idézet) |

A **tartalmi spec** adta a teljes szöveget, szó szerint.
Az **OESL animatik** adta a hero videót és a Solutions vizuálokat.

## A fő döntések

Mindegyik változtatható. **Mindegyiknél azt ajánljuk, hogy ne változtassanak.**

### 1. A márkanév mindig kisbetűs

`neuwerk`, mondatkezdő helyzetben is. Ez felülírja a tartalmi spec PDF-jét,
ami végig `NEUWERK`-et írt. A logó wordmark is kisbetűs, tehát a szöveg most
már követi a jelet. Egyetlen kivétel a `NEU` / `WERK` szótagbontás az Identity
oldalon, ahol a szó felbontása maga a mondanivaló.

### 2. Loading screen egy statikus oldalon

Az oldal kap egy logó reveal introt, pedig statikus. Nem technikai szükség,
hanem márkaélmény: a hivatalos logóanimáció 1,2 másodpercig fut, egyszer
látogatásonként, és átugorható.

Két védőháló van benne, mert egy teljes képernyős overlay veszélyes:
`<noscript>` esetén meg sem jelenik, és egy tisztán CSS-es kivezető 4 másodperc
után akkor is eltünteti, ha a JS bármiért nem fut le. Enélkül egy
script-blokkoló képes lenne örökre elrejteni a teljes oldalt — ezt élőben
demonstráltuk, mielőtt megjavítottuk.

### 3. A Solutions négy külön klip, keresztúsztatással

Ez a legösszetettebb rész. A négy pillérhez külön videóklipet gyártottunk,
és kattintásra keresztúsztatással váltanak.

Miért nem egy videó scrubbolása, ahogy először terveztük:

- Az eredeti animatikba **bele van égetve** a padlóra vetített `SAFETY` /
  `PERFORMANCE` / `EFFICIENCY` / `COMFORT` felirat. Nem az alsó harmadban ül:
  az EFFICIENCY szakaszban a képkocka **közepén** fut át, az akkumulátor-
  csomagon. 3D-s padlóvetület mozgó kamerával, tehát nincs olyan vágás, ami
  eltüntetné.
- Ezért a négy pillér saját, **feliratmentes** vágóképet kapott.
- Mind a négy klip ugyanabban a stúdióban, ugyanazon az autón készült, és
  ugyanazt a split-tone gradinget kapta. Keresztúsztatásban ezért nem
  jelenetváltásnak látszik, hanem annak, hogy **ugyanaz az autó vált át egy
  másik rendszer átvilágítására.**
- A négy klip négy különböző kameraállást használ — szemből, felülről, alsó
  háromnegyedből, oldalról —, hogy a pillérek első ránézésre elkülönüljenek.

A klipeket referenciakép-alapú generálással állítottuk elő az animatikból,
több körben, majd **képkockánként átnéztük** őket. Két generált változatot el
is dobtunk: az egyikben az autó identitása változott menet közben, egy másikban
pedig a modell **fényből vetített betűt rajzolt a padlóra** — pont azt, amit
tiltottunk. Ezt csak sűrű, kézi átnézéssel lehetett kiszűrni; automatikus
detektorral próbálkoztunk, de az hamis negatívot adott, ezért nem
támaszkodtunk rá.

### 4. A hero videóban maradnak a feliratok

Tudatos, elfogadott döntés. Ugyanaz az ok, ami fent: nem vágható ki.
A végleges megoldás egy felirat nélküli renderelés az ügyfél projektfájljából.

### 5. A pattern használata szigorú

A brandbook merch-guideline-ja szó szerint: a Neuwerk pattern **kizárólag
Blue Tint 01-ben, Navy Blue háttéren**, mindig bátran és nagy felületen.
A kisméretű, sűrű, pusztán dekoratív használat tiltott.

Ezért szekciónként legfeljebb három nagy forma mozog, és világos szekcióban
egyáltalán nincs pattern. Az első tervünk egy sodródó, sűrű pill-mező volt —
azt kihúztuk, mert pontosan az, amit a brandbook tilt.

### 6. A Sun szigorúan korlátozott

A narancs a felület 10–15%-át nem lépheti túl, és soha nem háttér. Ezen felül
két kemény szabály jött ki a kontraszt-számításból:

- **Narancs szöveg fehér háttéren tilos** — 1,97:1, olvashatatlan.
- **A Sun-gomb felirata navy, nem fehér** — a fehér-narancs szintén 1,97:1,
  a navy-narancs viszont 7,85:1 (AAA).

Ez utóbbi ellentmond az ösztönnek, ezért szemantikus tokenekbe van
kényszerítve. Egyszer így is átcsúszott a header Contact gombján; méréssel
fogtuk meg, nem szemmel.

### 7. Világos és sötét szekciók váltakozása

Nem felhasználói dark mode kapcsoló, hanem **szekció-tulajdonság**. A brand
mindkét módban létezik, és a ritmusuk váltakozása maga a védjegy.

### 8. Egyoldalas Acting Responsibly

Az öt jogi dokumentum nem kapott külön aloldalt. Egy oldalon vannak, letölthető
PDF-ként, rövid leírással, és a whistleblower is ide került.

Jelenleg placeholder PDF-ek vannak bent, arculatosan. Amikor jön a valós
szöveg, **csak a PDF-et kell cserélni** azonos fájlnévvel — a HTML nem
változik, link nem törik.

## Ami placeholder, és bekérendő

| # | tétel | jelenlegi állapot |
|---|---|---|
| 1 | **Valós kontaktadatok** | felismerhető `example.com` placeholderek |
| 2 | **A 16 ország megnevezése** — sehol nincs a forrásanyagban | jelölt placeholder-pozíciók a térképen |
| 3 | Media cikkek tartalma | 3 placeholder cikk |
| 4 | Career pozíciók | 3 placeholder pozíció |
| 5 | Az 5 jogi dokumentum szövege | arculatos placeholder PDF-ek |

Minden ilyen elem látható jelöléssel szerepel az oldalon, és egyetlen CSS
osztály levételével tüntethető el. A kontaktadatokra gép is vigyáz: egy
ellenőrző szkript hibával leáll, ha bármelyik e-mail nem `example` domainre
végződik.

## Hogyan veszi át egy grafikus

### A legegyszerűbb: a git repo

`Hello-agency-hun/neuwerk`, `build/1-clickable-prototype` ág. Minden benne van:
a forrásassetek, a brandbook, a fontok, az eredeti animatik, a generáló
szkriptek és a teljes döntésnapló. A gyökérben lévő `CLAUDE.md` az első
olvasmány.

### One-click csomag Claude Designhoz vagy Lovable-höz

Ha nem akar gittel bajlódni, becsomagoljuk egyetlen fájlba, amit beejt a saját
Claude Code-jába vagy Claude Designjába. Ehhez minden oldal **önhordó**: nincs
build lépés, nincs komponens-fordítás, nincs függőség. Egy oldal HTML-je
önmagában teljes, tehát bármelyik eszköz be tudja olvasni és tovább tudja vinni.

### Az élő design-segédlet

A repóban van egy **`design-system.html`**. Ez nem statikus dokumentáció, hanem
ugyanazt a CSS-t tölti be, mint a weboldal, ezért nem tud elavulni.

- Élő színszerkesztők — állítod a színt, és az egész oldal együtt változik
- **Valós időben újraszámolt kontraszt-táblázat** — ha egy színváltás elbuktat
  egy párost, azonnal látszik
- Tipográfiai és térközskála, komponensdemók mindkét szekciótémában
- Pattern-szabályok, „mit hol találsz" lista
- A végén kimásolható `tokens.css` blokk

### Mit hol talál

| ha ezt akarja változtatni | ezt szerkessze |
|---|---|
| szín, méret, betűtípus, időzítés | `css/tokens.css` — az egyetlen fájl hex értékekkel |
| reset, tipográfiai alapok, layout | `css/base.css` |
| header, footer, gomb, badge, pattern | `css/components.css` |
| szekció-elrendezések | `css/sections.css` |
| navigáció, footer linkek | a `@partial:header` / `@partial:footer` jelölők között |
| hírek, cikkek | `data/news.js` + új fájl a `media/` alatt |
| állásajánlatok | `data/jobs.js` |
| térképpontok | `data/locations.js` |
| jogi dokumentumok | a PDF cseréje azonos fájlnévvel |
| hero videó | `tools/build_video.py` |
| Solutions klipek | `tools/build_solutions.py` |
| világtérkép | `tools/build_map.py` |

### Három szabály, amit érdemes megtartani

1. **Nincs build lépés.** Aki átveszi, ne vezessen be bundlert.
2. **Nincs `fetch()`.** A csomagnak `file://`-ből is működnie kell.
3. **Nincs külső hálózati kérés.** Se CDN font, se CDN script.

## Bemutató-változat visszajelzés-gyűjtővel

A `tools/build_review.py` előállítja a `feltoltesre/` mappát: a teljes site plusz
egy lebegő megjegyzés-gomb. A véleményező oldalanként és szekciónként tud
kommentelni, a rendszer automatikusan rögzíti, hol jár.

**Minden megjegyzés külön JSON fájlba kerül** a `feedback/` mappában, beszédes
fájlnévvel (időbélyeg + oldal + azonosító), így bulk letölthető és elemezhető,
hogy többen ugyanazt mondják-e.

Végpontok:

- `feedback.php?download=1` — összesített JSON
- `feedback.php?zip=1` — az összes külön fájl ZIP-ben, ha a tárhelyen van
  ZipArchive; ha nincs, tiszta hibaüzenettel átirányít a JSON-ra
- `feedback.php?stat=1` — oldalankénti, kategóriánkénti és szerzőnkénti
  összesítő

Ez a változat tartalmaz PHP-t. Az éles csomag nem.

## Kérések az ügyfél felé

**A legfontosabb:** jó lenne, ha szét tudnánk szedni az animatikot, vagy
kapnánk inputot arról, hogy az egyes solutionökhöz milyen vizualizációt
szeretnének — és akkor legyártjuk.

- **Felirat nélküli renderelés az animatikból.** A padlóra vetített tipográfia
  külön réteg a projektfájlban, tehát nekik ez egy exportálás. Ezzel a hero és
  a Solutions is teljes fidelitásban, felirat nélkül működne.
- **Vagy: mit szeretnének látni pillérenként.** Ha megmondják, hogy a fluid
  handling, a thermal management, a sealing and damping és a multi-material
  esetében pontosan milyen vizualizációt képzelnek el, azt legyártjuk.
- A fenti öt placeholder tétel adatai.

Amíg ezek nem érkeznek meg, az oldal a jelenlegi generált és vágott assetekkel
teljes értékűen bemutatható.
