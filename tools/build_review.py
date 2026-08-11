#!/usr/bin/env python3
"""Review-build: a `feltoltesre/` mappa összeállítása.

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
    python tools/build_review.py
"""
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "feltoltesre"

INCLUDE_DIRS = ["assets", "css", "js", "data", "media"]
INCLUDE_FILES = [
    "index.html", "identity.html", "career.html", "media.html",
    "responsibility.html", "contact.html", "404.html",
]

MEDIA_PAGES = ["how-to-update-this-page", "neuwerk-begins", "thermal-systems-milestone"]

# A widget beszúrása közvetlenül a </body> elé.
INJECT = (
    '<!-- review widget: CSAK a bemutató-változatban. Az éles csomagban nincs. -->\n'
    '<link rel="stylesheet" href="{r}review.css">\n'
    '<script src="{r}review.js"></script>\n'
)

README = """neuwerk — bemutató változat
============================

Mi ez
-----
A neuwerk weboldal jelenlegi állapota, végigkattintható formában, plusz egy
megjegyzés-gyűjtő. Nem a végleges csomag: abban nincs PHP és nincs widget.

Feltöltés
---------
1. Másold fel a mappa TELJES tartalmát a webtárhelyre, egy almappába
   (pl. /neuwerk-preview/). A mappaszerkezetet tartsd meg.
2. A `feedback` mappára adj ÍRÁSI jogot (755 vagy 775; ha nem megy, 777).
   Ha nem létezik, a PHP megpróbálja létrehozni.
3. Nyisd meg a böngészőben: https://a-domained.hu/neuwerk-preview/

Hogyan használják a véleményezők
--------------------------------
Jobb alul egy narancs gomb. Fölé húzva kinyílik, rákattintva megnyílik a
megjegyzés-panel. Automatikusan rögzíti, melyik oldalon és melyik szekciónál
járnak, tehát csak a véleményt kell beírni. A név mezőt a böngésző megjegyzi.

A megjegyzések letöltése
------------------------
A panel alján az "Összes letöltése" link, vagy közvetlenül:
    https://a-domained.hu/neuwerk-preview/feedback.php?download=1
Ez adja vissza a teljes JSON-t. Ezt küldd vissza a fejlesztésnek.

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
    html = html.replace("</body>", INJECT.format(r=prefix) + "</body>", 1)
    path.write_text(html, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

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
