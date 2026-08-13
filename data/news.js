/* HÍREK ÉS CIKKEK
   ================================================================
   Új cikk hozzáadása két lépés:
     1. Vegyél fel egy új objektumot EBBE a listába, legfelülre.
     2. Másold le a media/ mappában egy meglévő cikk .html fájlját,
        nevezd át a slug szerint, és írd át benne a szöveget.

   A slug a fájlnév kiterjesztés nélkül: slug "my-story" -> media/my-story.html

   Az "image" EGY helyen van megadva, de KÉT helyen jelenik meg: a Media
   lista kártyáján és a cikkoldal fejlécében. A cikkoldalon a kép útvonala
   ../assets/... alakban szerepel, mert az a fájl a media/ mappában van.
   16:9-re vágva add meg (1200x675), mert mindkét helyen így jelenik meg.
   Ha kihagyod a mezőt, a kártya kép nélkül jelenik meg -- nem törik el.

   TODO(client): a valós hírek és cikkek bekérendők -->
*/
window.NEUWERK_NEWS = [
  {
    slug: "how-to-update-this-page",
    image: "assets/img/news/how-to-update-this-page.jpg",
    date: "2026-08-10",
    title: "How to update this page",
    excerpt: "A short guide for the neuwerk team: how to add, edit and remove news articles and open positions without a CMS.",
    placeholder: true
  },
  {
    slug: "neuwerk-begins",
    image: "assets/img/news/neuwerk-begins.jpg",
    date: "2026-08-01",
    title: "A new chapter begins",
    excerpt: "neuwerk starts operating as an independent global company, building on decades of automotive engineering expertise.",
    placeholder: true
  },
  {
    slug: "thermal-systems-milestone",
    image: "assets/img/news/thermal-systems-milestone.jpg",
    date: "2026-07-15",
    title: "Thermal systems milestone",
    excerpt: "A look at how integrated thermal management supports battery performance across demanding applications.",
    placeholder: true
  }
];
