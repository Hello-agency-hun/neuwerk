# Handoff — állapot és nyitott tételek

Utolsó frissítés: 2026-08-12

## Állapot

**Build 1 kész, ügyfél-jóváhagyásra vár.**

10 oldal, nulla halott link, nulla külső hálózati kérés. A csomag
kicsomagolva, szerver nélkül, duplakattintásra is végigkattintható.
Leszállítható zip: `python tools/make_zip.py` -> 12,12 MB.

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
Generálva: `python tools/check_placeholders.py` — **9 tétel**

| fájl | sor | tétel |
|---|---|---|
| `contact.html` | 63 | MINDEN kontaktadat placeholder, valós adatok bekérendők |
| `index.html` | 161 | a 16 ország tényleges listája bekérendő |
| `media/neuwerk-begins.html` | 71 | valós cikkszöveg bekérendő |
| `media/thermal-systems-milestone.html` | 67 | valós cikkszöveg bekérendő |
| `responsibility.html` | 66 | az 5 jogi dokumentum valós szövege bekérendő |
| `responsibility.html` | 130 | Integrity Line csatorna és adatvédelmi nyilatkozat bekérendő |
| `data/jobs.js` | 14 | a valós nyitott pozíciók listája bekérendő |
| `data/locations.js` | 10 | a 16 ország tényleges listája bekérendő |
| `data/news.js` | 10 | a valós hírek és cikkek bekérendők |
<!-- PLACEHOLDER-INVENTORY-END -->

## Hero videó: a beégetett felirat ELFOGADOTT ÁLLAPOT

Döntés (2026-08-12, ügyféloldali jóváhagyással): a hero videóban maradnak a
padlóra vetített SAFETY / PERFORMANCE / EFFICIENCY / COMFORT feliratok.

Ez tudatos döntés, nem elmaradt munka. Ne "javítsd":

- A felirat NEM az alsó harmadban ül. Az EFFICIENCY szakaszban a képkocka
  KÖZEPÉN fut át, az akkumulátorcsomagon; a PERFORMANCE szakaszban a felső
  éle a képmagasság ~57%-át éri el. 3D-s padlóvetület, a kamera pedig kering,
  tehát a felirat függőlegesen és vízszintesen is mozog. Nincs olyan fix
  vágás, ami a teljes szakaszon eltüntetné.
- A négy Solutions-klip ettől függetlenül feliratmentes: azokat külön
  vágtuk és generáltuk (tools/build_solutions.py).
- A végleges megoldás nem vágás, hanem egy felirat nélküli renderelés az
  ügyfél projektfájljából. Ez a "Kérések az ügyfél felé" alatt szerepel.

## Design-segédlet grafikusnak

`design-system.html` — élő stílusgyűjtemény. Ugyanazt a CSS-t tölti be, mint a
weboldal, ezért nem tud elavulni. Élő színszerkesztőkkel, valós időben számolt
kontraszt-táblázattal, komponensdemókkal és egy „mit hol találsz" listával.
A módosított tokeneket a lap alján kimásolható `tokens.css` blokként adja vissza.

Nyisd meg helyben: `python tools/serve.py`, majd `/design-system.html`.
A leszállított zipben szándékosan NINCS benne — fejlesztői eszköz.

## Asset pipeline

Egyik sem fut a felhasználónál. Csak akkor futtasd, ha a forrás változik.

    python tools/build_fonts.py           # TTF -> woff2, assets/fonts/
    python tools/build_video.py           # hero, ffmpeg + grade, assets/video/
    python tools/build_solutions.py       # 4 pillérklip + poszter, assets/video/
    python tools/build_subhero_images.py  # aloldal-hero JPEG-ek, assets/img/subhero/
    python tools/build_docs.py            # placeholder PDF-ek, assets/docs/
    python tools/build_map.py             # pont-rácsos világtérkép, assets/img/
    python tools/make_zip.py              # leszállítható csomag, work/

A `build_solutions.py` és a `build_subhero_images.py` forrása a `work/gen/`
alatt van, ami git-ignorált. A véglegesített assetek viszont verziókövetettek,
tehát a két szkriptet csak akkor kell futtatni, ha a nyers forrás cserélődik.

### Beégetett felirat az animatikban — figyelmeztetés

Az `OESL_animatikv_v29.mp4` padlójára rá van vetítve a SAFETY / PERFORMANCE /
EFFICIENCY / COMFORT felirat, és **nem csak az alsó harmadban**: az EFFICIENCY
szakaszban (kb. 12,5-14,0 s) a képkocka közepén, az akkumulátorcsomagon fut át.
Vágással egyik szakaszban sem távolítható el. A Solutions szekció emiatt már
nem ebből a fájlból dolgozik. A `hero-1920/1280.mp4` viszont **továbbra is
tartalmazza a feliratot** (forrás 4,0-17,0 s); a hero szekcióban a `object-fit:
cover` levágása viewport-arány függvényében kitakarja vagy nem. Ha a feliratnak
sehol nem szabad látszania, a heróhoz feliratmentes forrásrender kell az
ügyféltől — vágással ez sem oldható meg.

## Hogyan frissíti az ügyfél a tartalmat

Media: `data/news.js`. Career: `data/jobs.js`. Mindkettő egyszerű JS lista, kommentelve.
Új cikkhez a listába egy új objektum **és** egy új `media/<slug>.html` kell — a meglévő
cikkoldal másolásával. Ez a folyamat magán az oldalon is dokumentálva van, a
"How to update this page" című demó cikkben.
