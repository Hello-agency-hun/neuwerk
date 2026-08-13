# NEUWERK weboldal — belépési pont

Ha most veszed át a projektet, ezt olvasd el elsőként. Utána:
`docs/superpowers/specs/2026-08-10-neuwerk-website-design.md` (a design spec, minden
szám és szabály onnan jön) és `docs/HANDOFF.md` (mi nyitott).

## Mi ez

A NEUWERK statikus weboldala. Build 1 célja: az ügyfél végig tudja kattintani a
struktúrát és jóváhagyja. Leszállítás: egy zip, amit a saját szerverükre másolnak.

## Alapszabályok

1. **Nincs build lépés.** Nincs npm, nincs bundler, nincs PHP. A `tools/` alatti Python
   szkriptek csak assetet állítanak elő (videó, font) — a weboldal futásához nem kellenek.
2. **A zip `file://`-ből is működik.** Ezért nincs `fetch()`. A változó tartalom
   `window.NEUWERK_*` értékadás a `data/*.js`-ben. Ha `fetch()`-et írsz, eltörik az
   ügyfél-review.
3. **Nincs külső hálózati kérés.** Font, ikon, szkript mind lokális. Német ipari ügyfél,
   GDPR. Ne rakj be CDN-t.
4. **A header/footer minden oldalon duplikálva van**, `<!-- @partial:header -->` és
   `<!-- /@partial:header -->` jelölők között. Ha módosítod, mind a 10 oldalon módosítsd.
   A `partials/` alatti fájlok referencia-másolatok.

## Amendment 01 (2026-08-11)

A `docs/superpowers/specs/2026-08-11-amendment-01.md` **felülírja** az eredeti specet:

- a márkanév **mindig kisbetűs**: `neuwerk`, mondatkezdő helyzetben is
- nincs `legal/` könyvtár és nincs `integrity-line.html` — a jogi dokumentumok
  letölthető PDF-ek a `responsibility.html`-en, a whistleblower pedig annak
  `#integrity-line` szekciója
- ezért **10 oldal**, nem 16

## Amendment 02 (2026-08-13)

A `docs/superpowers/specs/2026-08-13-amendment-02.md` felülírja az Amendment 01-et
a jogi dokumentumok elhelyezésében:

- új, 11. oldal: `legal-compliance.html` (**Legal & Compliance**), kategóriákba
  sorolt dokumentumokkal
- a footerben **egy** link vezet ide, a korábbi két PDF-link helyett
- az Integrity Line ide költözött, a `responsibility.html`-ről
- a végleges kategórialistát az ügyfél küldi — a mostani három ideiglenes

## Design system

Minden szín, méret és betűtípus a `css/tokens.css`-ben van, és a brandbook v1.1-ből jön
(`Arculat/01_neuwerk_brandbook/neuwerk_brandbook_FINAL.pdf`). Ne írj hardcode hex értéket.

Három szabály, amit a brandbook kikényszerít:

- **Sun (`#ffa500`) max. a látható felület 10–15%-a.** Soha nem háttér.
- **Sun szöveg fehér háttéren tilos** (kontraszt 1,97:1). Sun-kitöltésű gomb felirata
  **navy**, nem fehér. Erre vannak szemantikus tokenek: `--nw-on-sun`.
- **A Neuwerk pattern csak Blue tint 1 navy háttéren**, nagy léptékben. Kisméretű, sűrű
  vagy pusztán dekoratív használat tilos. Csak sötét szekciókban.

## Ellenőrzés minden változtatás után

    python tools/check_links.py
    python tools/check_placeholders.py

Az első halott linket keres mind a 10 oldalon, a második leltározza a placeholdereket
és frissíti a `docs/HANDOFF.md` nyitott listáját.

## Mi placeholder és mi végleges

**Végleges:** a teljes copy (a tartalmi specből, szó szerint), a színek, a tipográfia,
a logók, a hero videó.

**Placeholder, jelölve:** minden kontaktadat, a Media cikkek, a Career pozíciók,
a térkép 16 pontja, az 5 jogi dokumentum szövege.

Minden placeholder `<!-- TODO(client): … -->` megjegyzést **és** látható badge-et kap.
A badge-eket egyetlen osztály kapcsolja ki: a `<body>`-ról vedd le a `is-wireframe`-et.
