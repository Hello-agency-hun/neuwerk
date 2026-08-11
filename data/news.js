/* HÍREK ÉS CIKKEK
   ================================================================
   Új cikk hozzáadása két lépés:
     1. Vegyél fel egy új objektumot EBBE a listába, legfelülre.
     2. Másold le a media/ mappában egy meglévő cikk .html fájlját,
        nevezd át a slug szerint, és írd át benne a szöveget.

   A slug a fájlnév kiterjesztés nélkül: slug "my-story" -> media/my-story.html

   TODO(client): a valós hírek és cikkek bekérendők -->
*/
window.NEUWERK_NEWS = [
  {
    slug: "how-to-update-this-page",
    date: "2026-08-10",
    title: "How to update this page",
    excerpt: "A short guide for the neuwerk team: how to add, edit and remove news articles and open positions without a CMS.",
    placeholder: true
  },
  {
    slug: "neuwerk-begins",
    date: "2026-08-01",
    title: "A new chapter begins",
    excerpt: "neuwerk starts operating as an independent global company, building on decades of automotive engineering expertise.",
    placeholder: true
  },
  {
    slug: "thermal-systems-milestone",
    date: "2026-07-15",
    title: "Thermal systems milestone",
    excerpt: "A look at how integrated thermal management supports battery performance across demanding applications.",
    placeholder: true
  }
];
