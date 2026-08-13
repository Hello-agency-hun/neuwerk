# assets-src — a generált vizuálok eredetije

Ez **nem** része a weboldalnak. Sem a `tools/build_review.py`, sem a
`tools/make_zip.py` nem másolja be: mindkettő névre szólóan az
`assets/`, `css/`, `js/`, `data/` és `media/` mappákat viszi.

## Miért van itt

Ami itt van, azt **nem lehet újraelőállítani**. AI-generált képek, tehát
ugyanaz a prompt sem adja vissza ugyanazt a képet. Ha elvesznének, a
hírkártyák és a hozzájuk tartozó cikkfejlécek vizuálja pótolhatatlan.

A `work/` mappa ezzel szemben szándékosan nincs verziózva: az ottani
kontaktlapok, kockakivágatok és összehasonlító rácsok mind a
forrásvideóból állnak elő, `tools/build_video.py` és
`tools/build_solutions.py` futtatásával.

## news/

Higgsfield `nano_banana_pro`, 16:9, 2026-08-13.

| fájl | hol jelenik meg |
|---|---|
| `neuwerk-begins.png` | Media-kártya + `media/neuwerk-begins.html` fejléc |
| `how-to-update-this-page.png` | Media-kártya + `media/how-to-update-this-page.html` fejléc |
| `thermal-systems-milestone.png` | Media-kártya + `media/thermal-systems-milestone.html` fejléc |

A weboldalon futó változat ezekből készül: 1200 px széles, 82-es
minőségű progresszív JPEG az `assets/img/news/` alatt, 22-46 KB. Ha új
vágás kell (más képarány, más kivágat), innen indulj, ne a JPEG-ből.

A prompt mindháromnál kizárta a szöveget, a logót, az embert, az autót és
a termékfotót — az utóbbit a benchmark-elemzés TI Fluid-döntése miatt.
