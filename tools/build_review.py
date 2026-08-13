#!/usr/bin/env python3
"""Review-build: a feltölthető bemutató-mappa összeállítása.

Ez NEM a végleges csomag. Ez a bemutató-változat, amit shared hostingra
lehet másolni, hogy a döntéshozók végigkattintsák és megjegyzést hagyjanak.

Különbség az éles csomaghoz képest:
  + review/ widget (lebegő megjegyzés-gomb)
  + feedback.php (a megjegyzéseket JSON-be fűzi)
  + feedback/ mappa a comments.json-nak
  + README-FELTOLTES.txt a feltöltési tudnivalókkal

Az éles csomagban (tools/make_zip.py) EGYIK SINCS benne -- ott a site
tiszta statikus HTML/CSS/JS, szerveroldal nélkül.

Futtatás:
    python tools/build_review.py                # -> uj-neuwerk/
    python tools/build_review.py masik-mappa    # -> masik-mappa/

A kimeneti mappa neve egyben a bemutató-kör azonosítója is: minden
megjegyzés megkapja `round` mezőként, tehát ha két kör anyaga ugyanarra
a tárhelyre kerül, a visszaérkező JSON-okból látszik, melyik melyik.
"""
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "uj-neuwerk")

INCLUDE_DIRS = ["assets", "css", "js", "data", "media"]
INCLUDE_FILES = [
    "index.html", "identity.html", "career.html", "media.html",
    "responsibility.html", "legal-compliance.html", "contact.html", "404.html",
]

MEDIA_PAGES = ["how-to-update-this-page", "neuwerk-begins", "thermal-systems-milestone"]

# A widget beszúrása közvetlenül a </body> elé.
INJECT = (
    '<!-- review widget: CSAK a bemutató-változatban. Az éles csomagban nincs. -->\n'
    '<link rel="stylesheet" href="{r}review.css">\n'
    '<script>window.NWR_ROUND = "{round}";</script>\n'
    '<script src="{r}review.js"></script>\n'
)

README = """neuwerk — bemutató változat
============================

Mi ez
-----
A neuwerk weboldal jelenlegi állapota, végigkattintható formában, plusz egy
megjegyzés-gyűjtő. Nem a végleges csomag: abban nincs PHP és nincs widget.

11 oldal van benne, köztük az új Legal & Compliance aloldal. A főoldalon a
brand-sáv formái mozognak, az aloldalak fejlécében rövid klip vagy animált
minta fut — ha valakinél ezek állnak, az a gép „csökkentett mozgás"
beállítása, nem hiba.

Fontos: ez KÜLÖN mappa az előző körtől. Ha a régi is fent van a tárhelyen,
töltsd EZT egy másik almappába, különben a két kör megjegyzései egy
könyvtárba keverednek. (Minden megjegyzés kap egy `round` mezőt is, tehát
utólag akkor is szét lehet válogatni őket.)

Feltöltés
---------
1. Másold fel a mappa TELJES tartalmát a webtárhelyre, egy almappába
   (pl. /neuwerk-uj/). A mappaszerkezetet tartsd meg.
2. A `feedback` mappára adj ÍRÁSI jogot (755 vagy 775; ha nem megy, 777).
   Ha nem létezik, a PHP megpróbálja létrehozni.
3. Nyisd meg a böngészőben: https://a-domained.hu/neuwerk-uj/

Hogyan használják a véleményezők
--------------------------------
Jobb alul egy kis narancs gomb. RÁKATTINTVA kipattan a megjegyzés-panel,
újra rákattintva (vagy az X-szel, vagy Esc-cel) eltűnik. Zárt állapotban
csak a gomb látszik, az oldalból semmit nem takar.

A panel automatikusan rögzíti, melyik oldalon és melyik szekciónál járnak,
tehát csak a véleményt kell beírni. A név mezőt a böngésző megjegyzi.

A megjegyzések letöltése
------------------------
Minden megjegyzés KÜLÖN JSON fájlba kerül a feedback mappában, beszédes
fájlnévvel (időbélyeg + oldal + azonosító). A panel alján három link:

  JSON       - minden megjegyzés egy összesített fájlban
  ZIP        - a külön fájlok egy csomagban (ha a tárhely tudja)
  Összesítő  - oldalankénti, kategóriánkénti és szerzőnkénti darabszám

Vagy közvetlenül:
    .../feedback.php?download=1     összesített JSON
    .../feedback.php?zip=1          ZIP
    .../feedback.php?stat=1         összesítő

Az összesített JSON-t küldd vissza a fejlesztésnek.

Ha nem működik a mentés
-----------------------
Szinte mindig jogosultsági kérdés: a `feedback` mappára kell írási jog.
A hibaüzenet a panelen megjelenik, és megmondja, mi hiányzik.
Ha a tárhelyen nincs PHP, a megjegyzés-gomb nem fog menteni -- ilyenkor
szólj, és csinálunk egy PHP nélküli változatot.
"""


def inject(path: Path, prefix: str) -> None:
    html = path.read_text(encoding="utf-8")
    if "review.js" in html:
        return
    html = html.replace("</body>",
                        INJECT.format(r=prefix, round=OUT.name) + "</body>", 1)
    path.write_text(html, encoding="utf-8")


def clear_dir(d: Path) -> None:
    """A mappa TARTALMÁT üríti, magát a mappát nem törli.

    Windowson a shutil.rmtree(OUT) rendszeresen elhasal a záró rmdir-en,
    ha bármi fogja a mappát -- egy nyitott terminál, a Fájlkezelő, egy
    futó szerver. A tartalom addigra viszont már törlődött, tehát a
    hívó egy üres mappát kap és azt hiszi, minden rendben. Ezért nem
    töröljük a mappát: csak kiürítjük."""
    if not d.exists():
        return
    for item in d.iterdir():
        try:
            if item.is_dir() and not item.is_symlink():
                shutil.rmtree(item)
            else:
                item.unlink()
        except PermissionError as e:
            print(f"  figyelem: nem tudom törölni ({item.name}): {e}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    clear_dir(OUT)

    missing = [n for n in INCLUDE_FILES if not (ROOT / n).exists()]
    missing += [d for d in INCLUDE_DIRS if not (ROOT / d).is_dir()]
    if missing:
        print("FAIL — hiányzik:")
        for m in missing:
            print(f"    {m}")
        return 1

    for name in INCLUDE_FILES:
        shutil.copy2(ROOT / name, OUT / name)
    for d in INCLUDE_DIRS:
        shutil.copytree(ROOT / d, OUT / d,
                        ignore=shutil.ignore_patterns(".gitkeep"))

    # review widget
    for f in ["review.css", "review.js", "feedback.php"]:
        shutil.copy2(ROOT / "review" / f, OUT / f)
    (OUT / "feedback").mkdir(exist_ok=True)
    (OUT / "feedback" / ".gitkeep").write_text("", encoding="utf-8")
    (OUT / "README-FELTOLTES.txt").write_text(README, encoding="utf-8")

    # A widget beszúrása minden oldalra
    n = 0
    for name in INCLUDE_FILES:
        inject(OUT / name, "")
        n += 1
    for slug in MEDIA_PAGES:
        p = OUT / "media" / f"{slug}.html"
        if p.exists():
            inject(p, "../")
            n += 1

    files = [p for p in OUT.rglob("*") if p.is_file()]
    size = sum(p.stat().st_size for p in files)
    print(f"build_review: {len(files)} fájl, {size / 1048576:.2f} MB")
    print(f"  widget beszúrva {n} oldalra")
    print(f"  {OUT.relative_to(ROOT).as_posix()}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
