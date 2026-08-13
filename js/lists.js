/* Lista-renderelés a data/*.js fájlokból.

   Szándékosan nincs fetch(): a zip file://-ből is működik, és ott a
   fetch CORS-ba fut. A data/*.js sima értékadás, amit az ügyfél
   szövegszerkesztővel is tud szerkeszteni.
*/
(function () {
  "use strict";

  function badge(item) {
    return item.placeholder ? '<span class="nw-ph">Placeholder</span> ' : "";
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  /* A poziciok munkacsalad (jobFamily) szerint csoportosulnak.

     Miert: az ugyfel sajat benchmarkjai (Netflix About, Mercedes-Benz
     Group Careers) pontosan igy szervezik a karrieroldalt, es a
     benchmark-elemzes ezt Round 1 tetelkent hozta. Sima lapos lista
     nem mutatja meg, milyen terulete van a cegnek. */
  var jobsHost = document.querySelector("[data-jobs]");
  if (jobsHost && window.NEUWERK_JOBS) {
    var groups = [];
    var byFamily = {};
    window.NEUWERK_JOBS.forEach(function (j) {
      var fam = j.jobFamily || "Other";
      if (!byFamily[fam]) { byFamily[fam] = []; groups.push(fam); }
      byFamily[fam].push(j);
    });

    jobsHost.innerHTML = groups.map(function (fam) {
      var rows = byFamily[fam].map(function (j) {
        var head = j.url
          ? '<a href="' + esc(j.url) + '">' + esc(j.title) + "</a>"
          : esc(j.title);
        var meta = [j.location, j.type].filter(Boolean).map(esc).join(" &middot; ");
        return (
          '<li class="nw-job"' + (j.placeholder ? " data-placeholder" : "") + ">" +
          '<h4 class="nw-job__title">' + badge(j) + head + "</h4>" +
          '<p class="nw-job__meta">' + meta + "</p></li>"
        );
      }).join("");
      return (
        '<li class="nw-jobgroup">' +
        '<h3 class="nw-jobgroup__title">' + esc(fam) +
        '<span class="nw-jobgroup__count">' + byFamily[fam].length + "</span></h3>" +
        '<ul class="nw-jobgroup__list">' + rows + "</ul></li>"
      );
    }).join("");
  }

  var newsHost = document.querySelector("[data-news]");
  if (newsHost && window.NEUWERK_NEWS) {
    newsHost.innerHTML = window.NEUWERK_NEWS.map(function (n) {
      return (
        '<li class="nw-news"' + (n.placeholder ? ' data-placeholder' : "") + ">" +
        '<a href="media/' + esc(n.slug) + '.html">' +
        '<time datetime="' + esc(n.date) + '">' + esc(n.date) + "</time>" +
        "<h3>" + badge(n) + esc(n.title) + "</h3>" +
        "<p>" + esc(n.excerpt) + "</p>" +
        "</a></li>"
      );
    }).join("");
  }
})();
