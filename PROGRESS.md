# PROGRESS

## 2026-08-20 — Teo masodik korenek behuzasa

**Kész:**
- `8579db9` behuzva (fast-forward): szelesebb brand-sav minta
  (`assets/img/brandband-wide.svg`) az index es az identity savjaban, a tobbi
  oldal hero-mintaja valtozatlanul a regi `brandband.svg`.
- A `teo-deploy/` mappa es a wireframe-PDF ujraepitve az uj allapotra;
  zip: `work/teo-deploy-2026-08-20.zip` (79 fajl).
- Ellenorizve: check_links + check_placeholders PASS, 169 belso link a PDF-ben,
  a wireframe-reteg szelektorai (`.nw-brandband__img`) tovabbra is talalnak.

**Következő lépés:**
- nincs nyitott epitesi feladat. A `teo-deploy/` feltoltesre kesz.

**Döntések, amiket ne kérdezzünk újra:**
- A brand-sav kepe 100 px-szel tullog a dobozon mindket oldalon, mert a
  gorgetes max. ~91 px-et mozdit (`data-depth 0.35` * 260). Merve: ±91 px-nel
  meg 9 px a rahagyas. **Ha valaki a data-depth-et 0,38 fole viszi, vagy a
  pattern.js 260-as konstansat noveli, a szel-hiba visszajon.**
- A `--shift` ures marad, ha a bongeszo-panel nincs megjelenitve: a
  `pattern.js` rAF-fel utemez, az pedig `visibilityState: hidden` mellett nem
  fut. Ez meresi mutermek, NEM hiba -- ne induljunk el megint a nyomon.

## 2026-08-19 — Repo-atadas Teonak, Teo verzioja behuzva, teo-deploy mappa

**Kész:**
- `main` fast-forwarddal felzarkoztatva (57 commit volt lemaradva), a ket ag
  azota vegig szinkronban. A sima `git clone` mukodik.
- README ujrairva atadasra + `requirements.txt`; a humanizer skill lefuttatva
  rajta (0 gondolatjel, 0 felkover). Lepesrol lepesre leiras a Claude- es a
  Figma-attetelhez, ellenorzott token-ertekekkel.
- `docs/neuwerk-wireframe.pdf` bekerult a repoba referenciakent.
- Teo `3123c20` commitja behuzva: uj fejlec-szerkezet (`.nw-header__group` +
  kulon lebego `.nw-header__contact`), brand-sav SVG-re csere
  (`assets/img/brandband.svg`), terkep-klaszter, holt CSS/JS takaritas.
- `tools/wireframe.css` hozzaigazitva Teo szerkezetehez (a Contact gomb
  eltunt volt a PDF-bol, 169 -> 159 link; javitva, 169 vissza).
- `teo-deploy/` bemutato-mappa elkeszult es helyi PHP-n tesztelve;
  zip: `work/teo-deploy-2026-08-19.zip`.

**Következő lépés:**
- nincs nyitott epitesi feladat. Varunk arra, hogy Peter feltoltse a
  `teo-deploy/`-t es visszajojjenek a megjegyzesek (`round: "teo-deploy"`).

**Érintett fájlok:**
- `README.md` — Teo belepesi pontja, 8 szakasz
- `tools/wireframe.css` — a header/brand-sav szelektorok Teo osztalyaihoz
- `tools/build_review.py` — a README-FELTOLTES.txt szovege frissitve
- `.claude/launch.json` — `teo-deploy` bejegyzes (php -S, 8124)
- `.gitignore` — `/teo-deploy/` hozzaadva

**Döntések, amiket ne kérdezzünk újra:**
- **Teo stilusvaltoztatasai az iranyadok** — ha az eszkozeink regi osztalyra
  hivatkoznak, az ESZKOZT igazitjuk hozza, nem forditva.
- A terkep 8 jelolot mutat 18 helyett (7 orszag + 1 kozep-europai klaszter),
  es a 7 onallo orszag neve csak hoveren latszik — Peter megerositette, hogy
  Teo pont igy akarta.
- A generalt bemutato-mappak (`uj-neuwerk/`, `teo-deploy/`) es a `work/`
  gitignore-ban vannak; a mappanev egyben a megjegyzesek `round` mezoje.
- A wireframe-PDF egy site-oldal = egy folytonos lap (nincs A4-tordeles), es
  210 mm szeles, mert a Chrome nyomtatasi layoutja fixen ~794 px.

**Zsákutcák:**
- Higgsfield img2video a brand-savhoz: 2 kor, mindketto bukott (tapetazott,
  es gyakorlatilag nem mozgott, 0,31/255 kockakulonbseg). Lezarva; Teo azota
  statikus SVG-vel oldotta meg.
- Three.js x-ray auto: elengedve, mert a `file://`-kovetelmennyel utkozik.
- Szelesebb `@page` a wireframe-hez nem ad desktop elrendezest: a Chrome
  fixen ~794 px-en tordel, es csak felnagyitja az eredmenyt (megmerve).

## 2026-08-17 — IRÁNYVÁLTÁS: az ügyfélnek wireframe-PDF megy, nem a kész oldal

**Döntés:** az ügyfél nem a kész, színes, animált oldalt kapja, mert akkor a
visszajelzés a színekről és a görgetéses effektekről szólna. Helyette egy
**szürke, kép nélküli, kattintható wireframe-PDF**, aminek egyetlen célja a
**tartalom** jóváhagyása: mi van a headerben, mi a footerben, mi lesz a
Mediában, milyen sorrendben jönnek a szekciók.

**Új: `tools/build_wireframe.py` + `tools/wireframe.css`**
→ `work/neuwerk-wireframe.pdf` (41 lap, 1,69 MB)

A lánc: a 13 oldal másolata a `work/wireframe/` alá → minden `<script>`
kiszedve (a PDF statikus) → minden `<video>`/`<img>`/interaktív elem
feliratozott dobozzá → `wireframe.css` ráhúzva → Chrome headless
`--print-to-pdf` oldalanként → PyMuPDF-fel egy fájlba fűzve.

**Miért a meglévő oldalakból épül, és nem kézzel írt wireframe:** így a
szöveg nem tud elcsúszni attól, ami végül kimegy. Ha a copy változik, a
szkript újrafuttatva mindig a friss állapotot adja.

**Amit menet közben meg kellett oldani:**
- **A4 FEKVŐ, nem álló.** 297 mm ≈ 1123 CSS px 96 dpi-n, ami a 900 px-es
  töréspont felett van → a desktop elrendezés renderelődik ki, a főmenüvel.
  Állón (~794 px) a mobil változat jönne, és pont a header szerkezetét nem
  lehetne jóváhagyni.
- **A lapok közti linkek nem `uri`-ként jönnek**, hanem `LINK_LAUNCH`-ként,
  `file` kulccsal — az első verzió ezért 0 linket írt át.
- **A Chrome `%23`-ként kódolja a horgonyt.** Ezért ELŐSZÖR dekódolni kell,
  csak AZUTÁN levágni a `#`-et — fordítva 63 link (`index.html#solutions`
  típusú) nem oldódott fel.
- **Halott linkek kiszedve:** az `assets/docs/*.pdf` hivatkozások nem részei
  a csomagnak. Egy halott link az ügyfél PDF-jében rosszabb, mint semmi — a
  szöveg és a placeholder-badge marad, tehát látszik, hogy ott dokumentum lesz.
- **A `.nw-hero` fixen `--nw-white` szövegszínt használ** (és két másik hely
  is), mert élesben sötét felület van alatta. Szürkében ez láthatatlan lett
  volna. A tokent nem írtuk át — az felületszínként is szerepel —, hanem
  a három helyet külön címeztük.
- **Borító** került a PDF elejére: megmondja, hogy szándékosan nyers, mi
  maradt ki és miért, és hogy mit várunk vissza. Enélkül az első reakció
  az lenne, hogy „ez nagyon nyers".

Ellenőrizve: 149 belső link átírva, mind a 9 hivatkozott oldal a saját
kezdőlapjára ugrik, halott vagy feloldatlan link nincs.

**Ötödik kör — a Media-cikkek semlegesítve (2026-08-17):**

A három Media-cikk címe **„Example article"**, törzse **lorem ipsum**.
Indok: a korábbi szövegek (egy új fejezet, egy hőszabályzási mérföldkő és
egy belső „hogyan frissítsd az oldalt" leírás) elég konkrétak voltak ahhoz,
hogy az ügyfél valódi, publikálásra szánt cikkeknek higgye őket, és azok
TARTALMÁRÓL kezdjen visszajelzést adni — pedig itt csak a cikk-SABLONT kell
jóváhagyni.

**A Media-LISTÁN is „Example article" áll**, nem csak a cikkoldalakon. Ha a
lista valódi címeket mutatna, a megnyitott cikk viszont „Example article"-t,
az ügyfél joggal nem értené, melyik az igazi. Így a lista azt mondja, amit
kell: három cikk-hely, tartalom később.

Ellenőrizve, hogy egyetlen régi cikkszöveg sem szivárog át (a címek, a
bekezdések és az `assets/docs/` hivatkozás sem szerepel sehol).

Továbbá: a „Decorative brand band — animated geometric pattern" felirat
**„Brand pattern"** lett; a fejléc menüje pedig egy sorba szorítva (794 px-en
a Contact gomb megjelenésével a „Who we are" két sorba tördelt, ami azt a
hamis látszatot adta, hogy a menüpont kétsoros lesz).

**Ez mind WIREFRAME-ONLY — az éles oldalak szövege változatlan.**

**Negyedik kör — VÉGE A LAPOKRA TÖRDELÉSNEK (2026-08-17):**

A grafikus négy panasza (a jegyzet a jobb oldalon, a „Learn more" alatti
üresség, a csonka blokkok, az „összevissza padding") **ugyanarra a gyökérre
vezetett vissza: a lapokra tördelés maga gyártotta a hamis üres helyeket,
amiket az ügyfél tervezői szándéknak olvasott volna.**

Megoldás: **egy site-oldal = egy PDF-lap.** Minden oldal egyetlen, 4000 mm
magas lapra renderelődik, amit a `crop_to_content()` a tartalom aljára vág.
Nincs törés, nincs hamis üresség, a szekció-térköz pontosan a valódi
`--nw-section-y` (a korábbi kitalált 8 mm helyett). **11 lap** (borító + 10).

Ebből következett, hogy több korábbi kerülőút feleslegessé vált:
- az `unstack_who` (a törzsszöveg kiemelése a kéthasábos rácsból) **törölve**
  — most a valódi elrendezés látszik, cím balra, szöveg jobbra. A sticky
  viselkedést jelző jegyzet a CÍM alá került, ahova tartozik.
- a `break-inside` / `break-after` szabályok kikerültek.

**Mérési eredmény, amit érdemes megjegyezni:** próbáltam igazi desktop
szélességen (360 mm / 1361 px) renderelni, hogy a natív töréspontok
tüzeljenek. **Nem megy:** a Chrome nyomtatási layoutja FIXEN ~794 px széles,
bármit is ír elő a `@page`. Bináris kereséssel megmérve — 1360 px-es lapon a
media query továbbra is 700–799 px-et látott, tehát 794 px-en tördelt és az
eredményt felnagyította. Ezért a lap 210 mm (lapszélesség = layout-szélesség,
nincs nyújtás), és a desktop-rácsokat kézzel kényszerítjük vissza.

További javítások ebben a körben:
- **a lifecycle öt lépése EGY sorban** (3+2 helyett — két csoportnak látszott)
- **a térkép-doboz kérdést tesz fel az ügyfélnek:** „should the map show the
  individual cities as well, or countries only?"

**Harmadik kör — külső ügynök-review, két formátum összehasonlítva
(2026-08-17):**

A `tools/build_wireframe.py` mostantól **paraméterezhető**: `portrait` és
`landscape` ugyanabból a forrásból. A `@page` szabály a generált
`work/wireframe/page.css`-ben van, a `wireframe.css` formátumfüggetlen.

**VERDIKT: ÁLLÓ.** Az ügynök végigkattintotta mindkettőt és összevetette.
Az álló 29 lap / fekvő 39; a fekvőben több lap kétharmadában üres (egy lapon
a tartalom egyetlen negyedbe szorult), ami „elrontott renderelés" benyomást
kelt — és pont az a hibamód, amit a wireframe el akar kerülni. Az álló
sorhossza 75–90 karakter, a fekvőé 95–110, ami nem anyanyelvi olvasónak
rossz irány. A fekvő egyetlen valódi előnyét (Solutions egyben) egy
`break-inside: avoid` megoldotta az állóban is.

**Amit a review talált és javítottam:**
1. **A Contact gomb hiányzott a headerből MINDEN lapon.** A
   `components.css` 900 px alatt elrejti, álló A4 pedig 794 px — vagyis az
   ügyfél olyan headert hagyott volna jóvá, amiben nincs Contact.
2. **A Solutions szekció kettévágódott**, így az interaktív doboz csak az
   első pillér mellé került, a másik három egy üres hasáb mellé — amiből az
   olvasható ki, hogy csak az elsőhöz tartozik videó.
3. **`media/how-to-update-this-page.html` az „Acting Responsibly" oldalra
   hivatkozott**, ami az Amendment 02 óta nem létezik. **Ez éles
   tartalmi hiba volt, nem wireframe-artefakt** — a valódi oldalon is
   javítva.
4. **Az Identity-jegyzet nem létező címre hivatkozott** („beside the
   heading above"), mert ott az oldalsó hasáb eleve üres. Most más szöveget
   kap, ha nincs cím.
5. **A főoldalon a „Who we are" és a „Solutions" menüpont holt volt.** A
   Chrome a saját fájlra mutató horgonyt nevesített célként adja, ami
   összefűzéskor eltűnik. Megoldás: a fragmentum levágása — a horgony
   nélküli önhivatkozás rendes GOTO-t ad. 149 → **169 élő link.**
6. Narancs placeholder-körvonal (az egyetlen szín egy fekete-fehérnek
   ígért dokumentumban), hírkártyák 2+1 tördelése, Integrity Line
   mondat közepén vágva, árva jegyzet-doboz, badge által tördelt
   kártyacímek — mind javítva.
7. **Tartalomjegyzék a borítón**, valódi PDF-oldalszámokkal.
   **Ez több menetes buildet igényel**, és menet közben kiderült, miért:
   fekvőben a tartalomjegyzék kétlapossá tette a borítót, amitől minden
   szám eggyel elcsúszott. A build most addig ismétli, amíg az oldalszámok
   meg nem állnak (álló: 2 menet, fekvő: 3). Ellenőrizve: mindkét fájlban
   a borítón szereplő szám megegyezik a valódi oldalkezdettel.

Ellenőrizve: álló 169, fekvő 172 belső link, mind oldalkezdetre mutat,
halott link nincs, 6 külső link (Oracle, tel, 4 mailto) sértetlen.

**Második kör a grafikus-visszajelzésre (2026-08-17):**
- **ÁLLÓ A4 lett a fekvő helyett.** Fekvőn a szöveghasábok
  (`max-width: 68ch`) a lap bal felére zsúfolódtak, a jobb harmad üres
  maradt. Álló: 41 → **28 lap**, sűrűbb és olvashatóbb.
  Ára: 210 mm ≈ 794 px, ami a 900 px-es töréspont ALATT van, tehát a mobil
  breakpointok tüzelnének → a `.nw-who`, `.nw-solutions`,
  `.nw-ambition__grid`, `.nw-cards`, `.nw-stats` rácsokat kézzel
  visszakényszerítjük desktopra, mert **az elrendezés is jóváhagyandó
  tartalom**.
- **A duplikált menü kiszedve.** A hamburger-panelt kibontva mutattam
  („hadd lássák, mi van benne") — de desktopon nincs hamburger, a panel
  tartalma pedig a főmenü + a Contact, ami gombként amúgy is ott áll.
  Jogos volt a kérdés, hogy miért szerepel kétszer.
- **A Solutions vizuálja a JOBB oldalra került**, a szöveg balra —
  `.nw-solutions > .wf-box { order: 1 }`. A mobil `order: -1` szabály nem
  is talált semmit, mert a build a `.nw-solutions__stage`-et már dobozra
  cserélte.
- **A Regent-logó doboza szétesett**, mert `<div>`-et tettem egy `<p>`-be:
  az érvénytelen HTML, a böngésző kiemeli a bekezdésből. A doboz mostantól
  `<span>`. A felirata is rossz volt („neuwerk logo") — a `"brand" in src`
  ág elkapta a Regentet is, ezért a `"regent" in src` vizsgálat előbb áll.
- **Arányok:** a logó-dobozok `wf-box--inline` változatot kapnak (a valódi
  logó 132×20 px, egy 22 mm magas doboz ötszörösére duzzasztotta a headert).
  A header dupla kerete is megszűnt — a keret csak a shellen van.
- **Törésvezérlés:** `break-inside: avoid` a blokkokon, kártyákon,
  dobozokon; `break-after: avoid` a címeken. Az Origin/Capability/Focus
  most egy lapon van. Elv: inkább több lap, mint szétvágott szekció.

**A `work/neuwerk-review-2026-08-14.zip` (kész, színes verzió) marad
BELSŐ használatra** — az ügyfélhez a wireframe-PDF megy.


## 2026-08-14 — Grafikus-feedback R3, 13 pont

**Kész (12 pont, mind ellenőrizve böngészőben):**
- 2. címsor a 3 tovább-kártya fölé: „Learn more about neuwerk" (`index.html`)
- 3. Regent-lockup **függőleges** lett („PART OF" + logó egymás alatt). Az egysoros
  „A [logó] company" azért esett szét, mert három különböző dolgot próbált közös
  alapvonalra húzni, és a wordmark fölötti korona miatt a sormagasság ugrált. A
  függőleges lockupnál nincs közös alapvonal, amit el lehetne véteni.
- 4. `Together.` → „A design built to move forward." (`identity.html`)
- 6. Career: a fake pozíciólista törölve, helyette sötét CTA-szekció, ami a
  Regent Oracle HCM karrierportálra visz (új ablak). A `data/jobs.js` script-tag
  is kikerült. Indok a fájlban.
- 7. `responsibility.html` **törölve** (11 → 10 oldal). Az „Acting Responsibly"
  szöveg a `legal-compliance.html` élére került, a footer Responsibility oszlopa
  és a hamburger-sor eltűnt, a contact.html Supplier-linkje átirányítva.
- 8. hamburger **csak mobilon** (`@media (min-width: 901px)` elrejti)
- 10. „Let's talk" → „We're Here to Connect" (`contact.html`)
- 11. Contact gomb ki a mobil fejlécből (a hamburgerben ott van)
- 12. cím→szövegtörzs térköz: új `--nw-flow` token, `:is(h1,h2) + :where(...)`.
  **Figyelem:** `:where()`-rel nem működik — nulla specifikusságú, a `p { margin: 0 }`
  legyőzi. Ezért `:is()` a cím oldalán.
- 13. lifecycle-pöttyök: az első/utolsó már nem állandóan Sun, mind egyforma,
  a Sun csak hoveren/fókuszon
- 9. levegősebb: `--nw-section-y` 88 → **120 px**. Ez a harmadik beállítás
  (160 → 88 → 120). A 160 szétszakította, a 88 tömör lett.

**Folyamatban — 1. és 5. pont, a brand-sáv:**
- első kör: 9 pulzáló pill → „gagyi". Átépítve 6 nagy, nyúlánk formára,
  autoplay nélkül, **görgetésre** csúszva (`js/pattern.js` írja a `--shift`-et,
  a szelektora `[data-depth]`-re általánosítva). Ez sem tetszett.
- **Higgsfield img2video, 1. kör — BUKOTT, de tanulságos.**
  Alapkép 1920×512 (`tools/build_band_base.py`), `seedance_2_0`,
  start_image = end_image = ugyanaz a kép (ettől seamless a loop), 5 s,
  1080p, hang nélkül, 45 kredit. Job `bb2cf091-d867-4def-9e36-544268619cb2`,
  letöltve: `work/gen/band/raw.mp4`.
  - **Ami működött:** a paletta és a formanyelv tökéletesen stimmelt. Se
    ciánkék, se lila, se kitalált tárgy. A képből indítás megszüntette azt a
    hibaforrást, ami a korábbi két szöveges kört megölte.
  - **Ami elromlott:** a modell 2206×946-ra (21:9) komponálta át, és hogy
    kitöltse, **kicsinyítve tapétázta** a mintát → sűrű pasztilla-mező, ami
    sérti a brandbook „nagy lépték" szabályát. A sáv arányára vágva a
    pasztillák végei levágódtak, szögletes cikcakk maradt. Ráadásul alig
    mozgott: a 0./60./120. képkocka szinte azonos.
- **2. kör — SZINTÉN BUKOTT.** Alapkép a modell saját arányában (2208×946,
  3 sor, a középső a látható sáv, `STRIP_FRAC = 0.43`), a prompt kifejezetten
  tiltotta a tapétázást. Job `8312d43a-e58e-4d6e-ac63-72c0d7ca4a7a`,
  letöltve: `work/gen/band/raw2.mp4`.
  - a paletta megint tökéletes, és a pasztillák végei most már látszanak
  - **de a tapétázást a tiltás ellenére is megcsinálta**: apró, egymást nem
    fedő pasztillák szabályos rácsban — pont a „kisméretű, sűrű, dekoratív"
    használat, amit a brandbook tilt
  - **és gyakorlatilag NEM MOZOG.** Mérve (160×69-re skálázott szürkeárnyalat,
    átlagos kockakülönbség): 1. kör 1,69/255, 2. kör **0,31/255** — az utóbbi
    nagyjából az enkóder zaja. Első vs. utolsó képkocka: 0,63.

**ZSÁKUTCA — a generatív út lezárva.** Két kör, két külön hibaosztály, és a
második a szigorúbb prompttal ROSSZABB lett. A négy követelmény (pontos
formaszám, token-színek, nagy lépték, tökéletes loop) együtt pont az, amiben
a videómodellek a leggyengébbek: a modell a kompozíciót mindig újrarajzolja.
Ha kell a mozgás, a determinisztikus út marad: Canvas/WebGL loop vagy
AE/Remotion render ugyanebből a geometriából — ott mind a négy garantált.
Összes ráfordítás: 90 kredit.

**DÖNTVE: marad a CSS-sáv**, és kapott egy esztétikai kört (2026-08-14):

- **7 forma, mindkét szélen túlfut** a savon (−6% … 94,5%). Korábban a jobb
  szélen üresen maradt egy navy sáv.
- **A formák áttetszőek** (`--tone` + 82% alfa), nem tömörek. Ez a legnagyobb
  változás: tömör foltoknál három előre kiosztott tónus volt, és a szem
  azonnal látta, hogy generált. Áttetszően minden keresztezés saját tónust
  hoz létre — a hét formából tucatnyi árnyalat áll elő magától, ahogy a
  nyomtatott márkaanyagok rétegzett fedvényei.
- **`k*(r+1)` 1,46 → 1,77**: a formák függőleges kiterjedése a sáv
  magasságának 1,25-szöröse. Kell, mert a −45°-os átlók elvi okból nem érik
  el a jobb felső és bal alsó sarkot, ha épp csak a sávig érnek. Egyben
  nyúlánkabbak is, közelebb a logó arányaihoz.
- **`--dy` függőleges szórás** (±1,8%): enélkül mind a hét forma pontosan a
  középvonalon ül, ami vonalzóval húzottnak látszik.
- **Vízszintes osztás szándékosan egyenetlen** (16–17%): pontosan 17%-onként
  metronómnak látszott.
- **Szemcse:** `tools/build_grain.py` → `assets/img/grain.png` (96×96, 8,9 kB),
  `mix-blend-mode: overlay`, `opacity: 0.06`. A sávon már van
  `isolation: isolate`, ezért nem szivárog a szomszéd szekciókra.
  **Miért nem futásidejű SVG-szűrő:** a keringő `feTurbulence` +
  `filter: contrast(170%) brightness(1000%)` recept minden festésnél
  újraszámol, Blinkben és WebKitben máshogy néz ki, és drága. Az előre
  legyártott csempe nulla futásidejű költség és böngészőfüggetlen.

**Megfontolva, de NEM építve:** natív scroll-driven animáció
(`animation-timeline: scroll()`). Fő szálon kívül fut, tehát simább lenne a
parallax — de Firefox stable-ben 2026 júniusában (FF 152) még flag mögött
van, tehát csak `@supports`-szal, a JS-t fallbackként megtartva. Két út
párhuzamos karbantartása nem éri meg egy működő megoldásért.

Két mellékdöntés ebből a körből:
- **GIF helyett MP4** lett volna: a GIF 256 színnel sávosítaná a navy
  átmeneteket, 5–20× nagyobb, és nincs hardveres dekódolás.
- a `.nw-pill` primitív kiemelve: a contact/legal hero formái ezen futnak, hogy
  a sáv átépítése ne rántsa magával őket

**Érintett fájlok:**
- `css/tokens.css` — `--nw-section-y` 120px, új `--nw-flow`
- `css/base.css` — cím→törzs flow-szabály
- `css/components.css` — header breakpointok, Regent-lockup, `.nw-btn--lg`, `.nw-btn__ext`
- `css/sections.css` — `.nw-pill` primitív, `.nw-brandband` átépítve, `.nw-cta`,
  lifecycle-pöttyök
- `js/pattern.js` — `[data-depth]` szelektor
- `tools/build_band_base.py` — ÚJ; `tools/build_review.py`, `make_zip.py`,
  `build_subhero_images.py` — responsibility kivezetve

**Ellenőrzés:** `check_links.py` PASS (0 halott link),
`check_placeholders.py` PASS (16 placeholder — a térkép kikerült közülük).

**Review-csomag kész (2026-08-14):** `python tools/build_review.py` lefutott,
77 fájl / 12,51 MB, widget 10 oldalon. Zip:
`work/neuwerk-review-2026-08-14.zip` (12,24 MB, gitignore-ban).

Feltöltés előtt leellenőrizve helyi PHP-n (`localhost:8123`):
- mentés `POST /feedback.php` → `ok:true` · `?stat=1` → ok · `?download=1` → ok
- a mező neve **`comment`**, nem `note` — üres `comment` esetén 400
- a teszt-bejegyzés törölve, a `feedback/` csak a `.gitkeep`-et tartalmazza
- a zipben benne van a `feedback/` könyvtár és a `feedback.php`
- a buildben: 18 térkép-pont, 7 sáv-forma, 14 000 / 18 / 1 statisztika,
  `responsibility.html` nincs, `grain.png` megvan

---

## Az áttetsző autó — DÖNTVE: marad a videós verzió

2026-08-14: a Three.js út **elengedve** (a `file://` követelménnyel ütközik,
lásd lent). Build 1 a jelenlegi, animatikból vágott videós megoldással megy ki.
Az alábbi leírás dokumentáció, nem nyitott feladat.



**Hogyan készült (ez a jelenlegi állapot):**
- Forrás: `useful visual assets/OESL_animatikv_v29.mp4` — az ügyfél saját
  animatikja, 28,33 s. **Az x-ray hatás ebbe bele van renderelve**, nem mi
  csináltuk: kész képkockák, nem interaktív jelenet.
- `tools/build_video.py` — hero: 4,0–17,0 s vágás. A 20,0–20,5 s között
  összeálló SPEC betűk és a 18,0-tól jövő zászlós szakasz így kimarad.
  Grade: 50% split-tone (árnyék → navy, csúcsfény → hideg fehér), a meleg
  pixelek maszkolva és a valódi Sun `#ffa500`-ra emelve. Encode `-g 15`,
  mert a Solutions szekció scrubbolja.
- `tools/build_solutions.py` — pillérenként külön klip (C1–C4 renderekből),
  ugyanaz a grade. Miért nem egy fájl: a hero-klipbe **bele van égetve** a
  padlóra vetített SAFETY / PERFORMANCE / EFFICIENCY / COMFORT tipográfia,
  ami az EFFICIENCY szakaszban a képkocka közepén, az akkucsomagon fut át —
  vágással nem eltávolítható.

**Amiért az interaktív Three.js x-ray autót elengedtük:**

⚠️ **Ütközik a projekt egyik alapszabályával.** A `CLAUDE.md` szerint a zipnek `file://`-ből is
működnie kell, ezért nincs `fetch()`. Egy szokásos Three.js jelenet három
ponton is `fetch`-el:
1. `<script type="module">` — `file://` alatt CORS miatt blokkolt, a modern
   three.js pedig ESM-only (r160+ nem szállít UMD buildet)
2. `GLTFLoader.load()` — a `.glb`-t XHR-rel kéri le → blokkolt
3. `TextureLoader` — ugyanaz

**Megkerülhető, de ára van:**
- three.js: r159 vagy korábbi UMD build, lokálisan verziózva (nem CDN)
- OrbitControls: a klasszikus változat r147 után megszűnt — vagy kézzel
  portoljuk, vagy írunk egy ~80 soros saját orbitot (ezt javaslom, könnyebb)
- a modell: **base64 data URI-ként** egy `data/car.js`-ben, `window.NEUWERK_CAR`
  néven — pontosan az a minta, amit a projekt már használ, és a
  `GLTFLoader.parse()` ArrayBuffert is elfogad, tehát nincs hálózati kérés.
  Ára: egy használható autómodell 3–15 MB, base64-gyel +33%. A mostani négy
  pillér-videó együtt 2,4 MB.

**Ha valaha mégis előkerül (Build 2+), ezeket kell eldönteni:**
- honnan jön a modell: Sketchfab (licenc kérdéses ügyfélweben), AI-generálás
  (autóra + belső rendszerekre gyenge), vagy Blenderben épített egyszerűsített
  geometria (teljes kontroll, „általános német autó" pont így oldható meg)
- x-ray shader: Fresnel `ShaderMaterial` a karosszériára (additív blending,
  `depthWrite: false`), a belső rendszerek tömör Sun-színnel — ez egy az egyben
  ráképezhető a négy pillérre
- hotspotok: `Raycaster` a rendszer-mesheken
- **ez Build 2 tétel, nem Build 1 finomhangolás** — nagyságrendileg 1–3 nap

Aki ezt újra elővenné: a `file://` követelmény feladása nélkül nem megy.
Az `uj-neuwerk/` review-mappa PHP-n fut, tehát a review működne — a
„nyisd meg a zipet helyben" nem.

---

---

## Térkép — valós telephely-adat (2026-08-14)

Forrás: `Website_Countries_Locations_12.08.2026.xlsx`, 34 sor, 4 régió.
Új: `tools/build_locations.py` → generálja a `data/locations.js`-t.

- **36 telephely, 18 ország.** (34 sor − 1 kihagyott + 3 többvárosos cellából.)
- A vetítés képlete egy helyen van leírva, és **egyeznie kell** a
  `tools/build_map.py`-beliVel: `px=(lon+180)/360×150`, `py=(83−lat)/143×60`,
  plusz a viewBox `-0.5` eltolása. A korábbi 16 placeholder-pont kézzel volt
  belőve és pontatlan volt (a „Germany" pont a 39. szélességi fokon ült).
- **Országonként egy pont**, nem telephelyenként: 20 telephely van Európában,
  telephelyenkénti pont a 150×60-as rácson összefüggő folttá mosódna.
  A városok a tooltipben vannak, tehát nem vész el adat.
- A pont a **medoidra** kerül (a súlyponthoz legközelebbi tényleges telephely),
  nem a súlypontra. A súlypont vízbe eshet: Kína négy telephelyének átlaga a
  Sárga-tengerbe, az USA-é a Nagy-tavakra esett. Ellenőrizve: mind a 18 pont
  1,2 rácsegységen belül van a legközelebbi szárazföldi ponttól (a parti
  városoknál ennyi a rács saját felbontása).
- Mobilon a tooltip a térkép **alatt**, statikusan áll: a vászon ott csak
  ~133 px magas, a pont fölé rakott buborék a szekció címébe lógott (mérve
  77 px-ig), és tapintásnál az ujj amúgy is eltakarná. A helye akkor is le
  van foglalva, ha üres, hogy ne ugráljon a layout.
- Ellenőrizve: mind a 18 tooltip elfér a térkép dobozában desktopon és
  mobilon is.

**Eldöntve 2026-08-14:**
- a statisztika **18 countries** lett (volt 16). A számláló animáció is
  a 18-ra fut.
- **a városokat név szerint NEM mutatjuk** — a tooltip csak az országnevet
  írja ki. A `data/locations.js` továbbra is telephely-szinten tartja őket,
  mert abból jön, mely országok szerepelnek és hova kerül az ország pontja.
- `Auburn` → **Auburn Hills** megerősítve.

**Nyitva, az ügyfélnél:**
1. **`Karbel` (Germany)** — nincs ilyen nevű német település.
   Elgépelés? `Korbach` (az már szerepel a listán) vagy `Karben`?
   **Jelenleg KIHAGYVA a térképről.** Ha bekerül, 18 ország marad, csak
   eggyel több telephely.
2. Két cellában több város volt, szétbontva:
   `Sun Prairie Rochester Hills` → 2 · `Hann. Münden, Waltershausen, Hamburg` → 3
3. `San Luis Potosi (2 locations)` — egy pontként szerepel.
4. Elgépelések, amiket kijavítottam: `Wiena`→Vienna, `Renees`→Rennes,
   `Ostava`→Ostrava, `Monteremorelos`→Montemorelos, `Tanger`→Tangier,
   `Mako`→Makó, `Vac`→Vác, `Timisoara`→Timișoara, `Dolne Vestenice`→Dolné
   Vestenice, `Caluire`→Caluire-et-Cuire, `Andrézieux`→Andrézieux-Bouthéon

## Nyitott, az ügyfélnél
- v2 brandbook jóváhagyás (R1.1) · végleges Legal & Compliance kategórialista
- a grafikusoktól pontosabb visszajelzés a 9. ponthoz (levegősség)

## Zsákutcák
- Higgsfield **szövegből** a két maradék heróhoz: 2 kör, mindkettő bukott
  (gyógyszerkapszula, lila gömbök, konzekvensen ciánkék a navy helyett).
  Prompt-hangolással ne próbáld újra. A mostani kör **képből** indul, ami
  pont ezt a hibaforrást szünteti meg — ha ez is bukik, AE/Remotion render.
- `?zip=1` a `feedback.php`-ben helyben 501 (nincs ZipArchive) — nem hiba,
  rendezetten a JSON-ra irányít.

## Döntések, amiket ne kérdezzünk újra
- `contact.html` és `legal-compliance.html` hero = CSS-pattern, nem videó
- a `feltoltesre/` mappa törölve, helyette `uj-neuwerk/`
- az elv-lista nem kap 01–04 sorszámot — a számozott címke AI-slop jelzés
- `assets-src/` a gyökérben van, nem `assets/` alatt
