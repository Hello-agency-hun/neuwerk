#!/usr/bin/env python3
"""Kattinthato wireframe-PDF a TARTALMI jovahagyashoz.

Miert kell: az ugyfelnek nem a kesz designt kell jovahagynia, hanem azt,
hogy MI van az oldalon -- mi kerul a headerbe, mi a footerbe, mi lesz a
Mediaban, milyen sorrendben jonnek a szekciok. Egy keszre csiszolt,
szines, animalt valtozat ilyenkor artalmas: a visszajelzes a szinekrol es
a gorgeteses effektekrol fog szolni, nem a szovegrol.

Miert a MEGLEVO oldalakbol epul, es nem kezzel irom ujra: igy a szoveg nem
tud elcsuszni attol, ami vegul kimegy. Ha a copy valtozik, ez a szkript
ujrafuttatva mindig a friss allapotot adja.

A lanc:
  1. a 13 oldal masolata a work/wireframe/ ala
  2. minden <script> kiszedve  -> a PDF statikus, nincs mit "megvarni"
  3. minden <video> es <img>   -> feliratozott doboz
  4. minden interaktiv elem    -> feliratozott doboz
  5. wireframe.css rahuzva     -> szurkearnyalat, semleges betu
  6. Chrome headless --print-to-pdf oldalankent
  7. PyMuPDF: egy fajlba fuzve, a lapok kozotti linkek ATIRVA oldalszamra,
     hogy a PDF-en belul tenyleg kattinthato legyen a navigacio

Futtatas:
    python tools/build_wireframe.py
"""
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote

import fitz  # PyMuPDF
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work" / "wireframe"

# EGY SITE-OLDAL = EGY PDF-LAP.
#
# Elobb A4-re tordeltunk (allo es fekvo valtozatban is). Mindketto ugyanazt
# a bajt termelte: a lapvegek ures foltokat vagtak a tartalomba, amiket az
# ugyfel TERVEZOI SZANDEKNAK olvasott -- "miert hagytunk itt ekkora ureset?"
# --, a szekciok paddingje pedig lapokent maskepp nezett ki. A break-inside
# szabalyok ezen nem segitettek, csak athelyeztek a hezagokat.
#
# Ezert nincs tordeles: minden site-oldal egyetlen, nagyon magas lapra megy,
# amit utana a tartalom aljara vagunk. Igy a PDF ugy gordul, mint a weboldal,
# a terkozok pontosan azok, amik a lapon lesznek, es nincs egyetlen olyan
# ures folt sem, ami ne a designbol jonne.
#
# A SZELESSEG 210 mm. Megmertuk, hogy szelesebb lapot nincs ertelme kerni:
# a Chrome nyomtatasi layoutja FIXEN ~794 px szeles (A4), fuggetlenul attol,
# mit ir elo a @page. Probaval ellenorizve -- 360 mm-es, 1360 px-es lapon a
# media query tovabbra is 700-799 px-et latott, tehat a bongeszo 794 px-en
# tordelt, majd az eredmenyt felnagyitotta 1360 px-re. Az csak nagyobb betut
# adott, nem desktop elrendezest.
#
# Ezert a lap szelessege = a layout szelessege: nincs nyujtas. A desktop
# racsokat viszont kezzel kell visszakenyszeriteni (lasd wireframe.css),
# mert 794 px-en a mobil breakpointok tuzelnenek.
#
# A magassag 4000 mm: a PDF-korlat 200 huvelyk (5080 mm), a leghosszabb
# oldalunk ennek a felet sem eri el. A vegleges magassagot a crop_to_content
# allitja be lapokent.
FORMATS = {
    "desktop": {"page": "210mm 4000mm", "margin": "0 12mm 12mm"},
}

CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

# A sorrend a PDF sorrendje: ahogy egy ember vegigjarna az oldalt.
PAGES = [
    ("index.html", "Home"),
    ("identity.html", "A new identity"),
    ("career.html", "Career"),
    ("media.html", "Media"),
    ("media/neuwerk-begins.html", "Media article 1"),
    ("media/thermal-systems-milestone.html", "Media article 2"),
    ("media/how-to-update-this-page.html", "Media article 3"),
    ("legal-compliance.html", "Legal & Compliance"),
    ("contact.html", "Contact"),
    ("404.html", "404 — not found"),
]


def box(soup, kind, label, extra=""):
    """Feliratozott helyorzo doboz. Ez helyettesit minden kepet es interakciot.

    SPAN, nem DIV. A footerben a Regent-logo egy <p> belsejeben all, es a
    <p><div>...</div></p> ervenytelen HTML: a bongeszo kiemeli a div-et a
    bekezdesbol, amitol a lockup szetesik. A .wf-box amugy is display: flex,
    tehat a span ugyanugy viselkedik.
    """
    d = soup.new_tag("span")
    d["class"] = "wf-box " + extra if extra else "wf-box"
    d["data-kind"] = kind
    k = soup.new_tag("span")
    k["class"] = "wf-box__kind"
    k.string = kind
    t = soup.new_tag("span")
    t["class"] = "wf-box__label"
    t.string = label
    d.append(k)
    d.append(t)
    return d


def strip_scripts(soup):
    for s in soup.find_all("script"):
        s.decompose()


def replace_media(soup, page):
    """Minden <video> es <img> feliratozott dobozza."""
    for v in soup.find_all("video"):
        src = ""
        srcs = v.find_all("source")
        if srcs:
            src = srcs[0].get("src", "")
        hero = "nw-hero__video" in (v.get("class") or [])
        label = (
            "Full-width background video, silent, looped. "
            "Source: the existing neuwerk animatic. "
            f"({Path(src).name})"
        )
        v.replace_with(box(soup, "video", label, "wf-box--hero" if hero else ""))

    for img in soup.find_all("img"):
        cls = img.get("class") or []
        src = img.get("src", "")
        alt = (img.get("alt") or "").strip()

        # A Regent-logot ELOBB kell vizsgalni, mint az altalanos "brand"
        # utvonalat -- kulonben az is "neuwerk logo" feliratot kapna.
        inline = ""
        if "regent" in src.lower():
            label = "Regent logo — parent company endorsement"
            kind = "image"
            inline = "wf-box--inline"
        elif "nw-header__logo" in (img.parent.get("class") or []) or "brand" in src:
            label = "neuwerk logo"
            kind = "image"
            inline = "wf-box--inline"
        elif "nw-map__base" in cls:
            continue  # a terkepet kulon kezeljuk, a szekcioval egyutt
        elif "nw-news__media" in (img.parent.get("class") or []):
            label = f"News card image — {alt or 'article thumbnail'}"
            kind = "image"
        elif "nw-subhero__bg" in cls:
            label = "Sub-page header background image"
            kind = "image"
        else:
            label = f"Image — {alt}" if alt else f"Image ({Path(src).name})"
            kind = "image"
        img.replace_with(box(soup, kind, label, inline))


def fix_self_anchors(soup, rel):
    """Az AZONOS oldalra mutato horgonyokat horgony nelkuli linkke teszi.

    Miert: a Chrome a "masik fajl + horgony" hivatkozast LINK_LAUNCH-kent
    adja (azt a merge atirja), a "sajat fajl + horgony" valtozatot viszont
    nevesitett celkent -- ami az osszefuzeskor egyszeruen ELTUNIK. Emiatt a
    fooldalon a "Who we are" es a "Solutions" menupont holt volt, holott a
    borito azt igeri, hogy a menu kattinthato.

    A horgony nelkuli onhivatkozas (mint a logo href="index.html") viszont
    rendes GOTO-t ad, amit az osszefuzes helyesen atszamoz. Ezert a
    fragmentumot levagjuk: az ugras az oldal elejere visz, ami tobb lapos
    szekcional nem tokeletes, de mukodik -- szemben azzal, hogy semmi.
    """
    own = rel.split("/")[-1]
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "#" not in href:
            continue
        base, _, _frag = href.partition("#")
        # "#valami" (tiszta fragmentum) vagy "sajatfajl.html#valami"
        if base == "" or base.split("/")[-1] == own:
            a["href"] = own


def sticky_note(soup):
    """Jegyzet a cim ala: a cim helyben marad, a szoveg elgordul mellette.

    Korabban a hosszu torzsszoveget kiemeltuk a ket-hasabos racsbol, mert a
    lapokra tordelesnel a folytatolapokon URESEN maradt a bal hasab. Most,
    hogy egy site-oldal egy PDF-lap, nincs mit tordelni -- a racs egyben
    marad, es azt latja az ugyfel, ami a valosag: cim balra, szoveg jobbra.

    A jegyzet ezert a CIM ALA kerul, nem a szoveg ala: a viselkedes
    (position: sticky) a cimre vonatkozik.
    """
    for aside in soup.select(".nw-who__aside"):
        if not aside.get_text(strip=True):
            continue          # Identity: ott nincs cim, nincs mit jelezni
        note = soup.new_tag("p")
        note["class"] = "wf-box wf-box--strip wf-box--note"
        note["data-kind"] = "motion"
        note.string = ("This heading stays in place while the text on the "
                       "right scrolls past it.")
        aside.append(note)


def fix_self_anchors(soup, rel):
    """Az AZONOS oldalra mutato horgonyokat horgony nelkuli linkke teszi.

    Miert: a Chrome a "masik fajl + horgony" hivatkozast LINK_LAUNCH-kent
    adja (azt a merge atirja), a "sajat fajl + horgony" valtozatot viszont
    nevesitett celkent -- ami az osszefuzeskor egyszeruen ELTUNIK. Emiatt a
    fooldalon a "Who we are" es a "Solutions" menupont holt volt, holott a
    borito azt igeri, hogy a menu kattinthato.

    A horgony nelkuli onhivatkozas (mint a logo href="index.html") viszont
    rendes GOTO-t ad, amit az osszefuzes helyesen atszamoz. Ezert a
    fragmentumot levagjuk: az ugras az oldal elejere visz, ami tobb lapos
    szekcional nem tokeletes, de mukodik -- szemben azzal, hogy semmi.
    """
    own = rel.split("/")[-1]
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "#" not in href:
            continue
        base, _, _frag = href.partition("#")
        # "#valami" (tiszta fragmentum) vagy "sajatfajl.html#valami"
        if base == "" or base.split("/")[-1] == own:
            a["href"] = own


def unstack_who(soup):
    """A hosszu torzsszoveget kiemeli a ket-hasabos racsbol.

    Miert: a .nw-who racs bal hasabjaban a cim all, a jobb hasabban a
    szoveg. A szoveg viszont harom hosszu blokk, tehat tobb lapra fut --
    es a folytatolapokon a bal hasab URESEN marad, mintha hianyozna
    valami.

    Ezert a racsban csak a cim es a bevezeto marad (ott latszik a valodi,
    ket-hasabos elrendezes), a harom blokk pedig TELJES SZELESSEGBEN
    folytatodik alatta. Ala kerul egy jegyzet, ami elmondja, hogy elesben
    ez a szoveg a cim melletti hasabban all, es a cim helyben marad,
    amig a szoveg elgordul mellette (position: sticky).
    """
    for who in soup.select(".nw-who"):
        blocks = who.select_one(".nw-who__blocks")
        if not blocks:
            continue

        who.insert_after(blocks.extract())

        # Ha a racsban semmi tartalom nem maradt (az Identity oldalon az
        # oldalso hasab eleve ures), akkor az ures racs csak hezagot adna.
        # A jegyzet szovege ilyenkor MAS: nincs "a fenti cim", amire
        # hivatkozhatna -- azzal a valtozattal az ugyfel egy nem letezo
        # cimet keresne.
        has_heading = bool(who.get_text(strip=True))
        if not has_heading:
            who.decompose()

        note = soup.new_tag("p")
        note["class"] = "wf-box wf-box--strip wf-box--note"
        note["data-kind"] = "motion"
        note.string = (
            "In the live page this text sits in the right-hand column, beside "
            "the heading above: the heading stays in place while this text "
            "scrolls past it. It runs full width here so that the wireframe "
            "does not leave an empty column."
        ) if has_heading else (
            "In the live page this text sits in a narrower column, not full "
            "width. It runs full width here so that the wireframe does not "
            "leave an empty column."
        )
        blocks.insert_after(note)


def annotate(soup, page):
    """Az interaktiv elemek helyere feliratozott doboz kerul.

    Nem elrejtjuk oket, hanem MEGNEVEZZUK: az ugyfelnek tudnia kell, hogy
    ott valami tortenni fog, csak most nem arrol kerdezunk.
    """
    # Solutions: a negy pillert vezerlo videovalto. A pillerek listaja
    # tartalom, tehat marad -- csak a videoszinpad lesz doboz.
    stage = soup.select_one(".nw-solutions__stage")
    if stage:
        stage.replace_with(box(
            soup, "interactive",
            "Interactive looped car animatic, based on the main animatic video. "
            "Selecting one of the four solution pillars on the left plays the "
            "matching clip here, showing that system highlighted on the vehicle.",
            "wf-box--hero"))

    # Brand-sav: dekoracio, nem tartalom.
    for band in soup.select(".nw-brandband"):
        band.replace_with(box(
            soup, "motion",
            "Decorative brand band — animated geometric pattern.",
            "wf-box--strip"))

    # A contact/legal hero mintaja.
    for sh in soup.select(".nw-subhero__shapes"):
        sh.replace_with(box(
            soup, "motion",
            "Sub-page header — animated brand pattern background.",
            "wf-box--hero"))

    # Terkep: a pontok a locations.js-bol jonnek, tehat JS nelkul uresek.
    # Az ORSZAGLISTA viszont tartalom, ezert kiirjuk.
    canvas = soup.select_one("[data-map]")
    if canvas:
        countries = read_countries()
        canvas.replace_with(box(
            soup, "map",
            "World map — dotted grid, one marker per country. "
            f"Currently {len(countries)} countries: " + ", ".join(countries) + ". "
            "Hovering or focusing a marker shows the country name. "
            "QUESTION FOR YOU: should the map show the individual cities as "
            "well, or countries only?",
            "wf-box--hero"))

    # Kinetikus szoveg es gorgetesre kiemelt elvek: a szoveg marad,
    # csak megjegyezzuk, mi tortenik veluk.
    for el in soup.select("[data-kinetic], [data-kinetic-lines]"):
        note = soup.new_tag("p")
        note["class"] = "wf-box wf-box--strip"
        note["data-kind"] = "motion"
        note.string = "The sentence above fades in word by word as it scrolls into view."
        el.insert_after(note)

    principles = soup.select_one("[data-principles]")
    if principles:
        note = soup.new_tag("p")
        note["class"] = "wf-box wf-box--strip"
        note["data-kind"] = "motion"
        note.string = "Scrolling highlights the principle currently in view."
        principles.insert_after(note)

    # Szamlalok: JS nelkul a HTML-ben allo vegertek latszik, az jo.
    for c in soup.select("[data-count]"):
        del c["data-count"]


def read_countries():
    """Az orszaglista a generalt data/locations.js-bol, hogy ne ketszer alljon."""
    txt = (ROOT / "data" / "locations.js").read_text(encoding="utf-8")
    seen = []
    for m in re.finditer(r'country:\s*"([^"]+)"', txt):
        if m.group(1) not in seen:
            seen.append(m.group(1))
    return seen


def pagehead(soup, filename, title):
    """Azonosito sav a lap tetejen: melyik fajl, melyik oldal."""
    head = soup.new_tag("div")
    head["class"] = "wf-pagehead"
    f = soup.new_tag("div")
    f["class"] = "wf-pagehead__file"
    f.string = filename
    n = soup.new_tag("div")
    n["class"] = "wf-pagehead__name"
    n.string = title
    head.append(f)
    head.append(n)
    return head


COVER = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>neuwerk — content wireframe</title>
<link rel="stylesheet" href="wireframe.css">
<link rel="stylesheet" href="page.css"></head>
<body class="wf-cover">
<h1>neuwerk website — content wireframe</h1>
<p class="wf-cover__sub">Draft for content review · {date}</p>

<h2>What this is</h2>
<p>A deliberately rough, black-and-white outline of every page on the new
neuwerk website. Its only purpose is to agree on <strong>content</strong>:
what each page says, what goes in the header and the footer, what the Media
section contains, and in what order the sections appear.</p>

<h2>What has been left out on purpose</h2>
<p>Colours, brand typography, photography, video and all scrolling and hover
effects have been removed. They are designed and working already — they are
simply not what we are asking about at this stage, and showing them here
would pull the discussion away from the text.</p>
<p>Wherever an image, a video or an interactive element belongs, you will
find a <strong>dashed box describing what will be there</strong>.</p>

<h2>How to use it</h2>
<p>The navigation is live: clicking a menu item, a card or a footer link
jumps to that page inside this PDF. Each page starts with its file name and
title, so you can refer to them precisely in your comments.</p>
<p>Anything still marked <span class="nw-ph">Placeholder</span> is content we
are waiting on from your side.</p>

{toc}
<h2>What we would like back</h2>
<p>Corrections to the wording, anything missing, anything that should not be
there, and whether the page order and the menu structure make sense.</p>
</body></html>"""


def build_toc(starts):
    """Tartalomjegyzek a boritora, vegleges PDF-oldalszamokkal.

    Nyomtatva es annotalva olvassak: enelkul a lapozas talalgatas. A
    _cover.html sajat maga nem szerepel benne.
    """
    rows = []
    for rel, title in PAGES:
        if rel not in starts:
            continue
        rows.append(f"<li><span>{title}</span><span>{starts[rel] + 1}</span></li>")
    return '<h2>Contents</h2>\n<ol class="wf-toc">\n' + "\n".join(rows) + "\n</ol>"


def prepare(fmt, toc=""):
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    (WORK / "media").mkdir()

    # A CSS-ek kellenek, mert a wireframe.css RAJUK epul (felulir, nem
    # helyettesit). Kepet, videot, fontot nem masolunk: nincs ra szukseg.
    shutil.copytree(ROOT / "css", WORK / "css")
    shutil.copy(ROOT / "tools" / "wireframe.css", WORK / "wireframe.css")

    # A lapmeret sajat fajlba kerul, hogy a wireframe.css formatumfuggetlen
    # maradjon es a ket valtozat kozott csak ez az egy dolog terjen el.
    f = FORMATS[fmt]
    (WORK / "page.css").write_text(
        f'@page {{ size: {f["page"]}; margin: {f["margin"]}; }}\n',
        encoding="utf-8")

    for rel, title in PAGES:
        src = ROOT / rel
        soup = BeautifulSoup(src.read_text(encoding="utf-8"), "lxml")

        strip_scripts(soup)
        fix_self_anchors(soup, rel)
        sticky_note(soup)
        annotate(soup, rel)
        replace_media(soup, rel)

        depth = "../" if "/" in rel else ""
        soup.head.append(soup.new_tag("link", rel="stylesheet",
                                     href=f"{depth}wireframe.css"))
        soup.head.append(soup.new_tag("link", rel="stylesheet",
                                     href=f"{depth}page.css"))

        body = soup.body
        body.insert(0, pagehead(soup, rel, title))

        (WORK / rel).write_text(str(soup), encoding="utf-8")

    # Borito. Enelkul az ugyfel elso reakcioja az lenne, hogy "ez nagyon
    # nyers" -- a lap megmondja, hogy szandekosan az, es mit kerdezunk.
    (WORK / "_cover.html").write_text(
        COVER.replace("{date}", date.today().isoformat()).replace("{toc}", toc),
        encoding="utf-8")

    print(f"  {len(PAGES)} oldal + borito elokeszitve: "
          f"{WORK.relative_to(ROOT).as_posix()}/")


def render():
    pdfs = []
    for i, (rel, _title) in enumerate([("_cover.html", "Cover")] + PAGES):
        out = WORK / f"_{i:02d}.pdf"
        url = (WORK / rel).resolve().as_uri()
        subprocess.run(
            [str(CHROME), "--headless", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={out}", "--virtual-time-budget=4000", url],
            check=True, capture_output=True,
        )
        crop_to_content(out)
        d = fitz.open(out)
        h_mm = d[0].rect.height / 72 * 25.4
        print(f"    {rel:42} -> {d.page_count} lap, {h_mm:.0f} mm magas")
        pdfs.append(out)
    return pdfs


def crop_to_content(pdf_path):
    """A tulmeretezett lapot a tartalom aljara vagja.

    A renderelt lap 4000 mm magas, a tartalom viszont ennek toredeke. Vagas
    nelkul minden oldal utan ezer millimeternyi ures papir jonne -- pont az
    a hatas, amit el akarunk kerulni.

    A hatarolo dobozt a szoveg- es rajzelemek uniojabol szamoljuk. A
    hattersavok (sotet szekciok) is rajzelemek, tehat beleszamitanak: ez jo,
    mert a szekcio hattere a tartalom resze.
    """
    doc = fitz.open(pdf_path)
    for page in doc:
        limit = page.rect.height * 0.9
        bottom = 0.0
        for blk in page.get_text("dict")["blocks"]:
            bottom = max(bottom, blk["bbox"][3])
        for drw in page.get_drawings():
            r = drw["rect"]
            # A body hatteret a Chrome egy TELJES LAPOT lefedo teglalapkent
            # festi. Ha ezt beleszamolnank, a hatarolo doboz mindig a lap
            # aljaig erne, es a vagas nem csinalna semmit. Ezert a lap
            # magassaganak 90%-anal nagyobb rajzelemeket kihagyjuk -- valodi
            # tartalom (szekcio-hatter, keret) sosem ekkora.
            if r.height >= limit:
                continue
            bottom = max(bottom, r.y1)

        if bottom <= 0:
            continue
        # Also margo, hogy a tartalom ne erjen a lap szelehez.
        bottom = min(page.rect.y1, bottom + 34)
        page.set_cropbox(fitz.Rect(page.rect.x0, page.rect.y0,
                                   page.rect.x1, bottom))
    doc.saveIncr()
    doc.close()


def merge(pdfs, out_pdf):
    """Osszefuzes + a lapok kozotti linkek atirasa PDF-belso ugrasokra.

    Enelkul a "Career" link a PDF-ben egy nem letezo career.html fajlra
    mutatna, tehat a kattinthatosag -- a feladat lenyege -- nem mukodne.
    """
    doc = fitz.open()
    starts = {}
    for (rel, _t), p in zip([("_cover.html", "Cover")] + PAGES, pdfs):
        starts[rel] = doc.page_count
        doc.insert_pdf(fitz.open(p))

    rewritten = dead = 0
    for pno in range(doc.page_count):
        page = doc[pno]
        for lnk in page.get_links():
            # A Chrome a lapok kozotti hivatkozast NEM uri-kent adja, hanem
            # LINK_LAUNCH-kent, 'file' kulccsal -- abszolut, URL-kodolt uttal.
            # (Az azonos lapon beluli #horgony viszont LINK_NAMED, azt az
            # insert_pdf mar helyesen atszamozta, ahhoz nem nyulunk.)
            target = lnk.get("file") or lnk.get("uri") or ""
            if not target:
                continue

            # ELOSZOR dekodolunk, AZUTAN vagjuk le a horgonyt: a Chrome a
            # '#'-et %23-kent kodolja, tehat a forditott sorrendben az
            # "index.html%23solutions" nem oldodna fel index.html-re.
            path = unquote(target).split("#")[0].replace("\\", "/")

            # A kulso hivatkozasok (http, mailto, tel) mukodnek a PDF-bol is,
            # azokhoz nem nyulunk.
            if "/wireframe/" not in path:
                continue
            name = path.split("/wireframe/")[-1]

            if name in starts:
                page.delete_link(lnk)
                page.insert_link({
                    "kind": fitz.LINK_GOTO,
                    "from": lnk["from"],
                    "page": starts[name],
                    "to": fitz.Point(0, 0),
                })
                rewritten += 1
            else:
                # Nem a csomag resze (pl. assets/docs/*.pdf, a jogi
                # dokumentumok helyorzoi). A hivatkozast KISZEDJUK: egy
                # halott link az ugyfel PDF-jeben rosszabb, mint semmi.
                # A szoveg es a placeholder-badge marad, tehat latszik,
                # hogy ott egy letoltheto dokumentum lesz.
                page.delete_link(lnk)
                dead += 1

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_pdf, deflate=True, garbage=4)
    mb = out_pdf.stat().st_size / 1024 / 1024
    print(f"  {out_pdf.relative_to(ROOT).as_posix()}  "
          f"{doc.page_count} lap, {mb:.2f} MB")
    print(f"  belso link atirva: {rewritten}"
          + (f", csomagon kivulire mutato kiszedve: {dead}" if dead else ""))
    return starts, doc.page_count


def main():
    if not CHROME.exists():
        print(f"FAIL — nincs meg a Chrome: {CHROME}")
        return 1

    wanted = [a for a in sys.argv[1:] if a in FORMATS] or list(FORMATS)
    for fmt in wanted:
        print(f"=== {fmt} ===")
        out = ROOT / "work" / f"neuwerk-wireframe-{fmt}.pdf"

        # TOBB MENET, amig az oldalszamok meg nem allnak.
        #
        # A boritora keruo tartalomjegyzekhez ismerni kell a vegleges
        # oldalszamokat, azok viszont csak az osszefuzes utan allnak elo.
        # Ket menet nem mindig eleg: fekvo formatumban a tartalomjegyzek
        # ketlaposra novelte a boritot, amitol MINDEN oldalszam eggyel
        # elcsuszott -- vagyis a kinyomtatott szamok hibasak lettek.
        # Ezert addig ismeteljuk, amig a ket egymast koveto menet ugyanazt
        # adja. Gyakorlatban ez 2-3 kor.
        toc = ""
        starts = None
        for attempt in range(1, 5):
            prepare(fmt, toc=toc)
            print(f"  renderels ({attempt}.):")
            pdfs = render()
            new_starts, pages = merge(pdfs, out)
            if new_starts == starts:
                break
            starts = new_starts
            toc = build_toc(starts)
        else:
            print("  FIGYELEM: az oldalszamok nem alltak meg 4 menet alatt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
