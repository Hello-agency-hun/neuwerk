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

  var jobsHost = document.querySelector("[data-jobs]");
  if (jobsHost && window.NEUWERK_JOBS) {
    jobsHost.innerHTML = window.NEUWERK_JOBS.map(function (j) {
      var head = j.url
        ? '<a href="' + esc(j.url) + '">' + esc(j.title) + "</a>"
        : esc(j.title);
      return (
        '<li class="nw-job"' + (j.placeholder ? ' data-placeholder' : "") + ">" +
        '<h3 class="nw-job__title">' + badge(j) + head + "</h3>" +
        '<p class="nw-job__meta">' +
          esc(j.area) + " &middot; " + esc(j.location) + " &middot; " + esc(j.type) +
        "</p></li>"
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
