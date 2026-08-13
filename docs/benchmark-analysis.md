# Benchmark-elemzés és implementációs csomag

**Dátum:** 2026-08-13
**Bemenet:** az ügyfél saját benchmark-listája, 11 URL-lel, 10 vállalattal (a Continentalhoz
nem adtak URL-t)
**Kapcsolódik:** `docs/brandbook-web-v2-draft.md`, `docs/superpowers/specs/2026-08-10-neuwerk-website-design.md`,
`docs/superpowers/specs/2026-08-11-amendment-01.md`, `docs/HANDOFF.md`, `css/tokens.css`

---

## 1. Összefoglaló

Az ügyfél lényegében azt kéri, hogy a neuwerk ugyanazt a fegyelmet mutassa, amit az Aptiv,
a Bosch Mobility és a Magna oldalán lát (letisztult felület, kevés elrendezés-család, gyors
eljutás a tartalomhoz), miközben a Rivian és a Tesla dinamizmusát, valamint a Porsche és a
Netflix érzelmi ütőerejét is szeretné, és mindeközben explicit módon el akar távolodni a
Lufthansa-hatástól és a mesterségesen generált, monoton szerkezetű oldalak benyomásától.
Ezek a kérések nem mind konzisztensek egymással: a „no scrolling required” (Aptiv, Bosch) és
a „short videos, TikTok-style” (Rivian) más médiumlogikát követel, a „avoid product photos”
(TI Fluid) és a „rotating images to target different audiences” (Tesla) egyszerre nem
tartható, a Mercedes „fashion or lifestyle brand” megjegyzése pedig szemben áll a neuwerk
mérnöki-ipari pozicionálásával. A jó hír az, hogy a projekt saját v2 fordulata (világos
alapfelület, lebegő navigáció, szűkített Sun-arány, szerkezeti AI-slop-tisztítás, lásd
`css/tokens.css` és a `4ae0764` / `2f9192f` commitok) már ma, a benchmark-csomag
megérkezése előtt lefedi a kérések nagy részének lényegét, és jelenleg csak formális
ügyfél-jóváhagyásra vár (`docs/brandbook-web-v2-draft.md` státusza még „vázlat”, holott a
kód már ezt futtatja). Amit ténylegesen hozzá kell tenni: egy szekció-szintű „egy
pillantásra érthető” fegyelem a jelenlegi hosszú főoldali görgetésen belül, egy fotó
nélküli, generált vizuál a Who-we-are placeholder helyére, és egy karrier-oldal
adatmodell, ami készen áll a Netflix- és Mercedes-szintű lokáció- és munkacsalád-szervezésre,
mihelyt valós pozíciólista érkezik. Amit nem érdemes átvenni: a Mercedes-féle
életmódmárka-esztétika a fő oldalakon, a Tesla-féle célközönség szerint forgó képgaléria
(nincs hozzá se közönségszegmens, se fotókészlet), és a Continental-féle sűrű,
sok-célközönséges főoldal, mert pontosan az ellenkezője annak, amit az Amendment 01
lapszám-csökkentése (16 helyett 10 oldal) el akart érni.

---

## 2. Site-onkénti elemzés

**Módszertani megjegyzés.** A `WebFetch` a HTML-t markdown-ra alakítja és egy kisebb
modellel összefoglaltatja, tehát a szín, a pontos térköz és a mozgás csak közvetve,
benyomásszerűen ítélhető meg belőle, nem mérve. Ahol a `WebFetch` blokkolva volt (Tesla,
Mercedes-Benz Group Careers) vagy túl kevés tartalmat adott vissza (Rivian), ott a
`firecrawl scrape` eszközzel közvetlenül lekért, nyers markdow-t olvastam el magam, ami
megbízhatóbb a szerkezetre és a tartalomra nézve. Ez a három site ettől még **verified**,
csak más eszközzel.

### Aptiv - solutions
**verified on the live site** (WebFetch, teljes tartalom visszajött)

Sticky fejléc mega-menüvel (Industries, Insights, Solutions, Careers, About), kb. 70-90 px.
Nincs klasszikus képi hero: a „End-to-End Solutions” cím szöveg-vezérelt, alig van rajta
vizuális hangsúly. Szekció-ritmus: cím + bevezető → 2 oszlopos üzletág-kártya → 9 elemes
termékrács → kontakt CTA → „Mobility Decoded” videósor teaser → 3 cikk → hírlevél → lábléc.
Kb. 3-4 elrendezés-család. Domináns fehér/világos alap, kék akcent, bőséges fehér tér.
Fotográfia szinte nincs, ikon- és szövegvezérelt. Kattintási mélység a részletekig
2-3 kattintás. **Az ügyfél kommentje ("no scrolling required, most important info at a
glance") részben túlzó**: az oldal valójában többszekciós, görgetős lap, csak nagyon
fegyelmezett a tipográfia és a térköz miatt tűnik tömörnek.

### TI Fluid Systems
**verified on the live site** (WebFetch, teljes tartalom visszajött, a felvásárlási
hír-sáv is valós, jelenleg is aktuális)

Sticky vízszintes navigáció legördülőkkel. Hero szöveg-vezérelt tagline-nal
("Fluid Thinking, Thermal Innovation"), kép nélkül. Szekció-ritmus: navigáció → hero →
ügyfél-logó sáv → 10 elemes termékrács → 4 tematikus blokk (Sustainability, Innovation,
Industrial Products, News) → CTA-k → lábléc. Kb. 3 elrendezés-család. Minimál paletta,
B2B-jelleg, kb. 60/40 tartalom/légtér arány. **A kép valóban technikai illusztráció, nem
lifestyle-fotó** - ez alátámasztja az ügyfél „avoid product photos” kommentjét, azzal a
pontosítással, hogy nem a fotózás teljes hiányáról van szó, hanem a lifestyle-jellegű
termékfotózás kerüléséről.

### Tesla
**verified on the live site** (firecrawl scrape, nyers markdown-ból olvasva, mert a
WebFetch 403-at kapott)

Minimál vízszintes nav (Vehicles, Energy, Charging, Discover, Shop) mega-menüvel,
kép-alapú almenü-kártyákkal. **Nincs egyetlen nagy hero**: a főoldal egy hosszan görgetett,
azonos mintázatú kártyák sorozata (kép + eyebrow + cím + alcím + 2 CTA), kb. 12-14
egymás utáni ilyen blokk (Model Y L Premium, Model 3, Model Y, FSD-statisztika, majd
ugyanez még egyszer más árazással, Current Offers, Inventory, Solar Panels, Powerwall,
Megapack, Solar Roof). Ez ténylegesen **egyetlen elrendezés-család sokszori ismétlése**,
nem elrendezés-változatosság. A „rotating images” valójában szezonális/regionális
promóciós rotáció, nem célközönség szerinti tartalmi elágazás. Lábléc minimális, egysoros.
**Az ügyfél „clean and well organized” kommentje helytálló a tipográfiára és a térközre,
de az oldal facto hosszan görgetett**, ami ellentmond az Aptiv/Bosch „no scrolling”
kommentjének, lásd 4. fejezet, 1. konfliktus.

### Porsche - stories
**verified on the live site** (WebFetch, teljes tartalom visszajött)

Kompakt sticky fejléc (Experience, Mobility, Design, Dreams, Innovation, Culture),
kb. 60-80 px. Hero: egy nagy, érzelmi automotive fotó (két 993/996 kabrió), headline
"Stories from the world of Porsche". Szekció-ritmus rendkívül konzisztens: kategória-fejléc
→ 6 kártyás rács (kép + cím + 1-2 soros leírás) → "More" link, kategóriánként ismétlődve.
Gyakorlatilag **2 elrendezés-család** (hero + kártyarács), tudatos fegyelemmel. Fotográfia
70%+ arányban dominál, a márkajelenlét visszafogott, a képek viszik a hangulatot. Sekély
kattintási mélység (max. 3 szint). **Heritage/modern egyensúly valóban jelen van**: klasszikus
911-es fotók modern rácsrendszerben, editorial hangvétel, nem termékkommunikáció.

### Bosch Mobility
**verified on the live site** (WebFetch, teljes tartalom visszajött, a Dr. Markus Heyn
idézet valós)

Perzisztens vízszintes fejléc mega-menüvel, vizuális kategória-kártyákkal, kb. 60-80 px.
Hero nagy háttérképpel és üzenettel ("Software-driven Mobility"), vezetői idézettel és
portréval. Szekció-ritmus: nav → hero → idézet → 6 fókuszterület-kártya → 9 elemes
hír/esemény-rács → lábléc. Kb. 3 elrendezés-család. Domináns fehér háttér, bőséges légtér,
kategória-specifikus akcentszínek csak a navigációs kártyákon. Van portré- és
lifestyle-fotó. **Az „1-2 kattintás” állítás a fő témákra igaz, de a Solutions-menü
3+ szintre mélyül** (Powertrain → Fuel cell electric → komponens) - tehát a mélyebb
tartalom nem mindig 1-2 kattintás, csak a belépési pont.

### Rivian
**verified on the live site** (firecrawl scrape, nyers markdown-ból olvasva, mert a
WebFetch csak a meta-leírást kapta el)

A `docs/brandbook-web-v2-draft.md` már korábban dokumentálta a fejléc valódi kódját
(`rounded-micro`, `shadow-nav`, height:0px animálva) - ez a lebegő, kinyíláskor
helyben növő nav-konténer, amit a projekt már át is vett (lásd 5. fejezet, R1.1). A
homepage maga **hosszú és sokféle elrendezésű**: ajánlati banner → videó-hero ("R2 is
here") → konfigurátor-teaser kép → 3 jármű-kártya rétegzett képekkel (shadow+base layer,
valószínűleg hover/scroll-animációhoz) → fület-váltós tartalom (Technology/Performance/
Design tabok) → parallax "Award-winning safety" szekció (külön előtér/háttér réteg) →
fotógaléria a fizikai showroomokról → helyszín-infó → hírlevél-form → videós CTA →
parallax töltés-szekció → újabb videó ("Designed to get better with time") → gyorslinkek →
feliratkozás → záró videós szekció. **Legalább 7-8 elrendezés-család egy oldalon**, több
beágyazott videóval és egy külön `stories.rivian.com` alosztállyal - ez valóban alátámasztja
az ügyfél „short videos, dynamic” kommentjét, és pont az ellenkezője az AI-slop-monotóniának.

### Mercedes-Benz Group Careers - Graduates
**verified on the live site** (firecrawl scrape, nyers markdown-ból olvasva, mert a
WebFetch 403-at kapott)

A globális `group.mercedes-benz.com` navigáció **rendkívül mély**: 9 fő kategória
(Company, Technology, Sustainability, Careers, Investors, Press...), mindegyik alatt
4-9 alpont, minden alpontnak saját almenüje. Ez konkrét, mért bizonyíték az ügyfél saját
kritikájára ("too many subpages, navigating back often requires returning to the start of
the section"): a Graduates lap alatt is 3 további alszint van (Inspire, Doctorates,
Direct entry), és nincs a lapon breadcrumb, csak a teljes mega-menü nyitja vissza az utat.
Maga a **Graduates lap tartalma viszont valóban tiszta**: nagy portré-hero ("Becoming... a
Pioneer"), rövid mondat, 4 kártya (Inspire / Doctorates / Direct entry / Management
Consulting), 3 aktuális állásajánlat kártyaként, "Further job offers" link, majd egy rövid
céginfo blokk és egy nagy lábléc-sitemap. A képi kezelés (cutout portré, fiatal,
sokszínű szereplők) valóban **életmódmárka-jellegű**, ez alátámasztja a "resembles a
fashion or lifestyle brand" kommentet, kifejezetten a karrier-vertikálon.

### Netflix About
**verified on the live site** (WebFetch, tartalom visszajött, bár a markdown-konverzió
miatt a színek/tipográfia csak közvetve ítélhetők meg)

Hero egyetlen erős mondat: "We are here to entertain the world, one fan at a time" /
"Thrilling everyone again and again" - nagyon rövid, nagyon konkrét purpose-statement.
Szekció-ritmus: 3 pillér (Reach, Recommendations, Fandom), egységes kártya-elrendezésben
ismétlődve. Gyakorlatilag **1 elrendezés-család**, tudatos ismétléssel, nem monotóniaként
hat, mert a tartalom minden kártyánál más súlyú állítás. Kattintási mélység sekély.
A Careers-alszekció szervezettsége (lokáció, job family, lehetőségek) a fetchelt
tartalomban nem látszott közvetlenül, ezt az ügyfél saját kommentjéből vettem át
tényként.

### Continental
**verified on the live site** (WebFetch, `continental.com/en` - az ügyfél nem adott
konkrét URL-t ehhez a tételhez, ezt feltételeztem; a "ContiTech eladva a Lone Star
Fundsnak" hír valós, tehát a tartalom friss és hiteles)

Mega-menü, 3-4 szintre mélyülő alnavigáció (pl. Press → Press Releases → Corporate
Topics). Hero moduláris: legfrissebb hír (Q2 eredmények) + nagy stratégiai bejelentés
(ContiTech eladás) egymás mellett. Szekció-ritmus: hero → köszöntő → kiemelt anyagok →
karrier-üzenet → fenntarthatósági metrikák → befektetői anyagok → médiagaléria → lábléc.
**Legalább 4-5 elrendezés-család**, közepesen-magas információsűrűség. Minimál
paletta (fekete/szürke/fehér, szórt akcentek). Kattintási mélység a konkrét tartalomig
2-3 kattintás. **Az ügyfél kritikája pontos**: a navigáció ismétlődik és mélyül, a
homepage sok különböző célközönséget (sajtó, befektető, karrier, termék) szolgál ki
egyetlen lapon, ami éppen az információ-túlterhelést okozza, amit kritizáltak.

### Magna
**verified on the live site** (WebFetch, teljes tartalom visszajött, a "155k+, 28, 321"
statisztikák valósnak tűnnek)

Mega-menü 8 fő kategóriával (Innovation, Products, Company, Careers, Stories, Newsroom,
Contact, Search), nyelvválasztóval. **Nincs klasszikus képi hero**: a lap közvetlenül
webcast- és hírkártyákkal nyit, tartalom-elsőbbségi megközelítés. Szekció-ritmus: hírek →
innováció-blokk → statisztika-rács → kártyapárok (kép+szöveg, váltakozó oldal) → globális
jelenlét → ESG/emberek → hírlevél → lábléc. Kb. 4-5 elrendezés-család. Domináns fehér
alap, sötét navy akcent, minimál paletta, professzionális fotográfia. Kattintási mélység
sekély (1-2 kattintás a fő tartalomig). **A "menu design, overall layout very well
executed" komment inkább a fegyelmezett rácsrendszerre és a tipográfiai hierarchiára
vonatkozhat, nem a navigáció egyszerűségére** - Magna navigációja valójában mega-menüs,
nem minimál, szemben azzal, amit a neuwerk jelenleg csinál (6 elemű, dropdown nélküli nav).

---

## 3. Implementálható tételek

| # | Mit kértek | Konkrétan mit jelent nálunk | Megvalósíthatóság | Adaptáció / indoklás | Effort | Hatás (Lufthansa / AI-feel) |
|---|---|---|---|---|---|---|
| 1 | Aptiv, Bosch: "no scrolling required, everything at a glance" | Minden `index.html` szekció legyen egy pillantásra értelmezhető: rövidebb bekezdések, azonnal látható CTA | `adapted` | Nem dobjuk el a hosszú, videó-vezérelt görgetős felépítést (ez a hero-asset lényege), de szekciónként alkalmazzuk a "glance" fegyelmet: első viewportban a lényeg álljon | S | helps mindkettőt |
| 2 | Aptiv: "Solutions statement on the left stands out, simple yet strong" | Egy önálló, nagyméretű, egysoros állítás-blokk, NEM a tiltott split-header mintázat (cím+bekezdés kettéosztva) | `adapted` | Egyetlen helyen (pl. hero alatt, "Our ambition" előtt) egy nagy, önálló mondat, szöveg nélküli kísérőbekezdés nélkül | M | helps AI-feel, ha max. 1x szerepel |
| 3 | Aptiv, Netflix: "Careers page excellent / clear info about locations, job families, opportunities" | `data/jobs.js` séma bővítése `location` és `jobFamily` mezőkkel, `career.html` csoportosított/listázott megjelenítés | `direct` | A séma és a renderelő logika ma is buildelhető, mielőtt valós pozíciólista érkezik | M | neutral / helps percepciót |
| 4 | TI Fluid (2 visszajelző): "avoid product photos, clean and professional" | Nincs lifestyle-jellegű termékfotó a fő oldalakon; a Who-we-are placeholder generált, absztrakt vizuál legyen fotó helyett | `direct` | Ma sincs termékfotó-asset, a brandbook is minta/tipográfia-vezérelt irányt ír elő | M (asset generálás) | helps mindkettőt |
| 5 | Tesla: "rotating images target different audiences" | Célközönség szerint váltakozó képek/videók | `not possible` | Nincs több célközönség-szegmens (B2B, egy iparági közönség) és nincs hozzá fotó/videó-készlet | - | n/a, lásd 4. fejezet, 2. konfliktus |
| 6 | Tesla: "easy and simple navigation" | Egyszerű, dropdown nélküli, 6 elemű fejléc-nav | `direct` (már kész) | A `js/nav.js` + `css/tokens.css` `--nw-nav-*` tokenek már ezt adják | - | already done |
| 7 | Porsche: "classic, modern, with heritage" | Az Identity oldal ("A new identity", NEU/WERK, Continental-eredet) editorial hangsúlya | `adapted` | Erősebb Lora dőlt kiemelés a pull-quote-okon, a `--nw-font-editorial` tokent már használjuk erre | S | helps AI-feel |
| 8 | Bosch: "well-balanced, plenty of white space" | A v2 világos-domináns rendszer (`~75% világos / 25% sötét`) | `direct` (már kész) | `css/tokens.css` v2 blokkja már ezt implementálja | - | already done, helps Lufthansa-távolságot |
| 9 | Bosch: "information accessible within one or two clicks" | Lapos IA, max. 2 kattintás bármi eléréséhez | `direct` (már kész) | Amendment 01 óta 10 oldal, nincs mega-menü; ellenőrzés `tools/check_links.py`-jal | S (audit) | already largely done |
| 10 | Rivian: "floating, rounded nav container" | Lebegő, kerekített, animált nav-konténer | `direct` (már kész) | `css/tokens.css` `--nw-nav-h/--nw-nav-radius*` + `js/nav.js` már implementálja | - | already done, helps Lufthansa-távolságot |
| 11 | Rivian: "short videos, TikTok-style, dynamic" | Rövid, néma, hurkolt klipek több szekcióban | `adapted` | A 4 Solutions-klip (`assets/video/solution-*.mp4`) ma is ezt csinálja; kiterjesztés Identity/Career hero-ra új vágás nélkül nem megy | M-L | helps, de asset-függő, lásd 6. fejezet |
| 12 | Mercedes: "clean, simple, elegant, everything a few clicks away" | Lapos IA, letisztult megjelenés | `direct` (már kész) | Ugyanaz mint 9. tétel | - | already done |
| 13 | Mercedes: "career page clear, aspirational" | Aspirációs hangvétel a career.html-en | `adapted` | Szövegi szinten igen (copy-tone), fotográfiai szinten nem (lásd 15. tétel és 4. fejezet, 3. konfliktus) | S | helps, ha csak copy-szinten |
| 14 | Mercedes (kritika): "too many subpages, navigating back often requires returning to the start" | Ne kövessük a mély mega-menü mintát | `direct` (már elkerülve) | A neuwerk 6-elemű nav, dropdown nélkül; ez már eleve nem ismétli meg a hibát | - | already avoided |
| 15 | Mercedes: "resembles a fashion or lifestyle brand" | Editorial, portré-vezérelt esztétika | `not possible` a fő márkaoldalakon, `adapted` a Career oldalon | Ütközik az ipari-mérnöki pozicionálással; Career oldalon szűk körben elfogadható, ha valaha lesz hozzá valós fotó | - | hurts, ha a fő oldalakra kerül; lásd 4. fejezet, 3. konfliktus |
| 16 | Netflix: "strong purpose statement" | Rövid, ütős hero-mondat minden aloldalon, nem csak a főoldalon | `direct` | A hero lead ma 15 szó (`Built on decades of engineering excellence...`), a v2 20 szavas szabály alatt van; ezt kell auditálni a többi aloldal hero-jára is | S | helps AI-feel |
| 17 | Continental: "visually strong, professionally executed" | Tipográfiai/fotográfiai minőségi mérce | `direct` | Nincs konkrét tennivaló, a v2 tipográfiai rendszer már erre törekszik | - | referencia-mérce, nem tétel |
| 18 | Continental (kritika): "content repetitive, too much information at once" | Ne kövessük a sok-célközönséges, sűrű homepage mintát | `direct` (már elkerülve) | A neuwerk homepage 6 tartalmi szekció + lábléc, egy célközönségnek | - | already avoided, lásd 4. fejezet, 5. konfliktus |
| 19 | Magna: "menu design, overall layout, visual style well executed" | Fegyelmezett rácsrendszer és tipográfiai hierarchia | `adapted` | A vizuális fegyelmet átvesszük, a mega-menüt NEM (az ellentétes irányba megyünk, minimál nav) | - | helps, a navigáció részét kizárva |

---

## 4. Konfliktusok és döntések

### 1. "No scrolling, at a glance" (Aptiv, Bosch) vs. "short videos, dynamic" (Rivian) vs. a jelenlegi hosszú főoldal

Aptiv és Bosch dicsérete kifejezetten a görgetés hiányára és az azonnali áttekinthetőségre
vonatkozik. Rivian dicsérete pont az ellenkezőjére: hosszú, videó-gazdag, sok
elrendezés-családos oldal. A saját Tesla-elemzésünk (2. fejezet) azt is megmutatta, hogy
maga a Tesla-főoldal is hosszan görgetett, csak fegyelmezett tipográfiával tűnik
tömörnek - tehát az ügyfél saját benchmarkjai belül sem konzisztensek ebben a kérdésben.

**Döntés: a Rivian-modell nyer, szekció-szintű Aptiv-fegyelemmel.** A neuwerk hero-videó a
legerősebb leszállított asset (spec 6-7. fejezet, a three.js hero explicit elvetve pont
azért, mert a videó jobb). Egy "at a glance" dashboard-ra való lecsupaszítás eldobná ezt az
assetet, és ellentmond a spec 12. pontjának (motion: nagy pill-formák + videó). A helyes
válasz nem a hosszúság csökkentése, hanem az, hogy minden egyes szekció önmagában
követi az Aptiv/Bosch-fegyelmet (1. implementálható tétel).

### 2. "Avoid product photos" (TI Fluid) vs. "rotating images by audience" (Tesla) vs. a négy transzparens autó-klip

TI Fluid dicsérete a termékfotózás teljes kerülése. Tesla dicsérete a célközönség szerint
váltakozó képanyag. A neuwerk négy Solutions-klipje (`assets/video/solution-*.mp4`)
technikailag képanyag, de nem termékfotó és nem közönség szerint rotál, hanem
képesség szerint.

**Döntés: TI Fluid nyer a fő oldalakon, Tesla mintázata nem alkalmazható.** A neuwerknek
nincs fotókészlete és nincs több célközönség-szegmense (egy B2B, ipari közönség van, nem
lakossági szegmensek autótípusonként). A négy klip nem sérti a TI Fluid-elvet, mert
technikai vizualizáció, nem lifestyle-fotó. Ha valaha bővül a videókészlet, az a
képesség szerinti logikát kövesse tovább, ne közönség szerintit.

### 3. "Resembles a fashion or lifestyle brand, prestige" (Mercedes) vs. mérnöki-ipari hitelesség (a neuwerk pozicionálása)

Mercedes komment kifejezetten pozitívként említi az életmódmárka-hatást. A neuwerk teljes
tartalmi spec ("engineering excellence, industrial expertise", "As an independent global
company... deep industrial capabilities") és a v2 fordulat célja pont az, hogy az oldal
ne tűnjön légitársaság- vagy divatmárka-jellegűnek, hanem mérnöki cégnek.

**Döntés: elutasítva a fő márkaoldalakon (hero, Who we are, Solutions, Ambition),
elfogadva szűk körben csak a Career oldalon.** A Career oldal célja emberek toborzása,
ott az aspirációs, portré-vezérelt hangvétel legitim cél (ahogy a Mercedes Graduates
oldal is csinálja) - de csak ott, és csak ha valaha lesz hozzá valós, engedélyezett
fotóanyag. Ma nincs ilyen asset (lásd 7. fejezet).

### 4. "Information within one or two clicks, few subpages" (Bosch, és Mercedes saját kritikája) vs. a 10 oldalas struktúra

Ez nem valódi konfliktus a neuwerk számára, mert **ezt már lezártuk Amendment 01-ben**,
mielőtt a benchmark-csomag megérkezett: 16 oldalról 10-re csökkentettünk, az 5 jogi
dokumentum egyetlen oldalra (`responsibility.html`) került, a fejléc nem használ
mega-menüt. A saját Mercedes-Benz Group-fetchelésünk (2. fejezet) konkrétan megmutatta,
milyen az, amikor ez NEM sikerül: 9 fő navigációs ág, mindegyik 4-9 alponttal, mély
almenükkel, breadcrumb nélkül.

**Döntés: tartsuk a jelenlegi lapos struktúrát, ne bővítsük.** Egyetlen tennivaló: formális
ellenőrzés `tools/check_links.py`-jal, hogy minden tartalom valóban 2 kattításon belül
elérhető-e (9. implementálható tétel).

### 5. Continental mint pozitív referencia, de kritizálva ismétlődésért és túlterhelésért, és a neuwerk a Continentalból vált ki

A Continental-fetchelésünk (2. fejezet) igazolta mindkét felet: a tipográfia és a
fotográfia professzionális, de a homepage tényleg legalább 4-5 elrendezés-családot zsúfol
egy lapra, sajtó, befektető, karrier és termék-tartalmat vegyítve. A neuwerk pont a
Continental egykori OES-üzletágából vált ki független céggé - minél jobban hasonlít rá
szerkezetileg, annál kevésbé olvasható önálló márkaként, ami direkt ellentmond a
`docs/brandbook-web-v2-draft.md` teljes céljának (RGB-távolság mérése a Lufthansától,
ugyanaz a logika alkalmazható a Continentalra strukturálisan).

**Döntés: a Continental fotográfiai/tipográfiai minőségi szintje mérce, az információs
architektúrája NEM.** A neuwerk egy célközönségnek szóló, 10 oldalas, lapos struktúrát
tart, nem a Continental sokcélközönséges, sűrű modelljét.

---

## 5. Build order

### Round 1 - nagy hatás, alacsony-közepes effort

| # | Tétel | Fájlok | Miért itt | Effort |
|---|---|---|---|---|
| R1.1 | A v2 fordulat (világos alap, lebegő nav, szűkített Sun, szerkezeti tisztítás) formális ügyfél-jóváhagyása; `docs/brandbook-web-v2-draft.md` státusz frissítése "vázlat"-ról "elfogadva"-ra | `docs/brandbook-web-v2-draft.md` | Már megépült (`4ae0764`, `2f9192f` commitok), csak a papír maradt le a kódtól. Ez a legnagyobb egyetlen lépés mindkét probléma ellen, és most csak adminisztratív | S |
| R1.2 | Szekció-szintű "glance"-audit a főoldalon: minden szekció első viewportja legyen önmagában érthető, hero-lead marad 20 szó alatt (ma 15) | `index.html`, `css/sections.css` | Feloldja az 1. konfliktust anélkül, hogy a hosszú, videó-vezérelt struktúrát fel kellene adni | S |
| R1.3 | A Who-we-are `TODO(asset)` placeholder cseréje generált, absztrakt vizuálra (nem termékfotó) | `index.html` 142. sor, új asset a `tools/` pipeline-ból | TI Fluid-elv nyer (4. tétel), és ma is TODO, tehát ütemezett munka egyébként is | M |
| R1.4 | `data/jobs.js` séma bővítése `location` + `jobFamily` mezőkkel, `career.html` csoportosított megjelenítés | `data/jobs.js`, `career.html`, `js/lists.js` | Netflix/Mercedes-mintát előkészíti, valós adat nélkül is buildelhető | M |
| R1.5 | Formális 2-kattintás audit: `tools/check_links.py` + kézi bejárás | `tools/check_links.py` | Bosch/Mercedes-mérce, olcsó ellenőrzés, ami már ma is valószínűleg teljesül | S |
| R1.6 | Hero-lead és a többi aloldal hero-copy 20 szavas szabályának auditja (nem csak index.html) | `identity.html`, `career.html`, `media.html`, `responsibility.html`, `contact.html` | Netflix-mérce ("strong purpose statement"), olcsó szövegaudit | S |

### Round 2 - érdemes, de Round 1 után

| # | Tétel | Fájlok | Miért itt | Effort |
|---|---|---|---|---|
| R2.1 | Egy önálló, nagyméretű "statement" blokk (Aptiv-mintára), NEM a tiltott split-header formában | `index.html`, `css/sections.css` (új `nw-statement` osztály) | Vizuális változatosság + AI-feel csökkentés, de új CSS-komponenst igényel | M |
| R2.2 | Rövid, néma videoklip-minta kiterjesztése Identity/Career hero-ra | `identity.html`, `career.html`, új videoasset | Rivian-mintát erősíti, de ügyfél-döntést és új vágást igényel (lásd 6. fejezet) | M-L |
| R2.3 | Editorial polírozás az Identity oldalon: erősebb Lora dőlt kiemelés a pull-quote-okon | `identity.html`, `css/sections.css` | Porsche/heritage-hatás, olcsó, de nem sürgős | S-M |

### Later or drop

| Tétel | Indok |
|---|---|
| Tesla-féle célközönség szerint forgó képanyag | Nincs hozzá közönségszegmens, se fotókészlet; lásd 2. konfliktus |
| Mercedes-féle életmódmárka-fotózás a fő oldalakon | Ütközik a mérnöki-ipari pozicionálással; lásd 3. konfliktus |
| Continental-féle sűrű, sok-célközönséges homepage-modell | Ellentmond az Amendment 01 lapszám-csökkentésének; lásd 5. konfliktus |
| Mercedes Group-szintű mély IA / mega-menü bővítés | A neuwerk tudatosan a lapos struktúrát választotta; lásd 4. konfliktus |

---

## 6. Ügyfél-döntést igénylő kérdések

1. **Vágható-e tovább a hero-videó a jelenlegi 17,0 mp-es határon túl** (R2.2-höz), hogy
   legyen forrásanyag több rövid, feliratmentes klipphez az Identity/Career hero-hoz? A
   `docs/HANDOFF.md` már figyelmeztet, hogy a SAFETY/PERFORMANCE/EFFICIENCY/COMFORT
   feliratok vágással nem távolíthatók el egyik szakaszból sem, tehát ehhez új,
   feliratmentes render kellene az ügyfél projektfájljából.
2. **Van-e büdzsé aspirációs, portré-jellegű fotózásra a Career oldalhoz** (3. konfliktus,
   szűk körű Mercedes-adaptáció), vagy marad a jelenlegi zéró-termékfotó irányvonal
   mindenhol?
3. **Formális jóváhagyás a `docs/brandbook-web-v2-draft.md` egészére** (R1.1) - a kód már
   fut v2-ben, de a dokumentum "vázlat" státusza miatt ez technikailag nincs lezárva.
4. **Valós pozíciólista, lokáció- és munkacsalád-adatokkal** (R1.4-hez) - enélkül a
   Netflix/Mercedes-szintű karrieroldal-szervezés csak üres séma marad.

---

## 7. Hiányzó assetek

- **Generált, absztrakt Who-we-are vizuál** (R1.3): ma egy `TODO(asset)` megjegyzés jelzi
  a helyét `index.html` 142. sorában, jelenleg egy videó-screenshot a helykitöltő.
- **Új, feliratmentes videórender** (R2.2, ha az ügyfél jóváhagyja a 6. fejezet 1.
  kérdését): a meglévő `OESL_animatikv_v29.mp4` egyik szakaszából sem vágható ki a
  padlóra vetített felirat, tehát ez nem vágási, hanem forrás-kérdés.
- **Valós karrier-, média- és lokáció-adat**: ezek már a `docs/HANDOFF.md` blokkoló
  listáján szerepelnek (kontaktadatok, 16 ország, Media cikkek, Career pozíciók, 5 jogi
  dokumentum szövege), és most azért is relevánsak, mert a Netflix/Mercedes-mintájú
  szervezettség (lokáció, munkacsalád) enélkül nem mutatható be értelmesen, csak
  szerkezetileg előkészíthető (R1.4).
- **Alkalmazotti/telephelyi fotográfia**, ha valaha megnyílik a Career oldal aspirációs
  irányba (6. fejezet, 2. kérdés): ma egyáltalán nincs ember- vagy telephely-fotó az
  `assets/` alatt.
