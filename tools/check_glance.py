#!/usr/bin/env python3
"""Glance-, kattintasmelyseg- es hero-copy audit.

Harom mercet ellenoriz, mindharom az ugyfel sajat benchmarkjaibol jon
(docs/benchmark-analysis.md):

1. HERO-COPY (Netflix-merce: "strong purpose statement")
   Minden oldal elso bekezdese legyen legfeljebb 20 szo. Ennel hosszabb
   lead nem fer ki az elso viewportba, es hosszu bekezdeskent olvasodik,
   nem allitaskent.

2. GLANCE (Aptiv / Bosch-merce: "most important info at a glance")
   Egy szekcioban ne legyen 3-nal tobb egymast koveto bekezdes cim,
   lista vagy vizual nelkul. A tomor szovegfal pont az, amit az Aptiv es
   a Bosch dicseretenek ellentete.

3. KATTINTASMELYSEG (Bosch-merce: "within one or two clicks")
   Az index.html-bol indulva minden oldal legyen legfeljebb 2 kattintasra.

Futtatas:
    python tools/check_glance.py
"""
import re
import sys
from collections import deque
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SKIP = {".git", "work", "Arculat", "useful visual assets", "docs", "tools",
        "partials", "feltoltesre", "vendor", "review"}

MAX_HERO_WORDS = 20
MAX_RUN_OF_PARAGRAPHS = 3
MAX_CLICKS = 2


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT)
        if any(part in SKIP for part in rel.parts):
            continue
        if rel.name == "design-system.html":      # belso segedlet, nem publikus
            continue
        yield p


def strip_tags(html):
    html = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", " ", html, flags=re.S)
    return re.sub(r"<[^>]+>", " ", html)


def words(html):
    return len(strip_tags(html).split())


def main():
    fails = 0

    # --- 1. hero-copy -------------------------------------------------
    print("HERO-COPY (max %d szo)" % MAX_HERO_WORDS)
    for p in pages():
        s = p.read_text(encoding="utf-8")
        m = re.search(r'class="[^"]*nw-(?:hero__lead|lead|kinetic)[^"]*"[^>]*>(.*?)</p>', s, re.S)
        if not m:
            continue
        w = words(m.group(1))
        ok = w <= MAX_HERO_WORDS
        fails += not ok
        print(f"  {str(p.relative_to(ROOT)):<40}{w:>4} szo  {'ok' if ok else 'FAIL'}")

    # --- 2. glance ----------------------------------------------------
    print("\nGLANCE (max %d egymast koveto bekezdes tagolas nelkul)" % MAX_RUN_OF_PARAGRAPHS)
    for p in pages():
        s = p.read_text(encoding="utf-8")
        for sec in re.findall(r"<section\b.*?</section>", s, re.S):
            sid = re.search(r'id="([^"]+)"', sec)
            name = sid.group(1) if sid else "(nevtelen)"
            # A cimke-bekezdes (pl. nw-who__label, nw-eyebrow) NEM szovegfal:
            # vizualisan tagol, sajat hairline-nal es kiskapitalis felirattal.
            # Ezert elvalasztonak szamit, nem torzsszovegnek.
            run, longest = 0, 0
            for m in re.finditer(r"<(p|h2|h3|h4|ul|ol|figure|img|video|dl)\b([^>]*)>", sec):
                tag, attrs = m.group(1), m.group(2)
                is_label = "__label" in attrs or "nw-eyebrow" in attrs
                if tag == "p" and not is_label:
                    run += 1
                    longest = max(longest, run)
                else:
                    run = 0
            if longest > MAX_RUN_OF_PARAGRAPHS:
                fails += 1
                print(f"  {str(p.relative_to(ROOT)):<30}#{name:<16}{longest} bekezdes egymas utan  FAIL")

    # --- 3. kattintasmelyseg ------------------------------------------
    print("\nKATTINTASMELYSEG (max %d kattintas az index.html-bol)" % MAX_CLICKS)
    start = ROOT / "index.html"
    depth = {start.resolve(): 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        d = depth[cur.resolve()]
        html = cur.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith(("#", "http", "mailto:", "tel:", "data:")):
                continue
            tgt = (cur.parent / href.split("#")[0]).resolve()
            if not tgt.exists() or tgt.suffix != ".html":
                continue
            if tgt not in depth or depth[tgt] > d + 1:
                depth[tgt] = d + 1
                q.append(tgt)

    for p in pages():
        if p.name == "404.html":
            # Szandekosan nincs linkelve: a szerver szolgalja ki hibanal.
            print(f"  {str(p.relative_to(ROOT)):<40}nincs linkelve (szandekos)")
            continue
        d = depth.get(p.resolve())
        if d is None:
            fails += 1
            print(f"  {str(p.relative_to(ROOT)):<40}ELERHETETLEN  FAIL")
        else:
            ok = d <= MAX_CLICKS
            fails += not ok
            print(f"  {str(p.relative_to(ROOT)):<40}{d} kattintas  {'ok' if ok else 'FAIL'}")

    print()
    if fails:
        print(f"FAIL - {fails} tetel nem felel meg")
        return 1
    print("PASS - minden merce teljesul")
    return 0


if __name__ == "__main__":
    sys.exit(main())
