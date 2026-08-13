/* Gorgetett elv-index.

   A negy elv a bekezdesek mellett all, es az olvasas utemere vilagosodik
   be egyesevel: mindig az az egy sor aktiv, amelyik a nezet kozepehez
   legkozelebb van. Igy a jobb oszlop nem statikus lista, hanem koveti,
   hol tartasz -- ez adja a szekcio mozgasat, uj elem nelkul.

   Az aktiv allapot pontosan ugyanaz a stilus, mint a hover, tehat
   egyszerre mindig csak EGY narancs csik latszik: az akcent igy sem
   lepi tul a brandbook 10-15%-os keretet.

   JS nelkul: minden sor alapallapotban marad es hoverre mukodik. */
(function () {
  "use strict";

  var list = document.querySelector("[data-principles]");
  if (!list) return;

  // Reduced motion eseten nem kotjuk gorgeteshez -- marad a hover.
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var items = Array.prototype.slice.call(list.children);
  if (items.length < 2) return;

  var ticking = false;
  var current = null;

  function update() {
    ticking = false;

    var vh = window.innerHeight;
    var box = list.getBoundingClientRect();
    // A lista teljesen kivul: nincs aktiv sor.
    if (box.bottom < 0 || box.top > vh) {
      if (current) { current.removeAttribute("data-active"); current = null; }
      return;
    }

    var mid = vh * 0.5;
    var best = null;
    var bestDist = Infinity;

    items.forEach(function (li) {
      var r = li.getBoundingClientRect();
      var d = Math.abs((r.top + r.bottom) / 2 - mid);
      if (d < bestDist) { bestDist = d; best = li; }
    });

    if (best === current) return;
    if (current) current.removeAttribute("data-active");
    if (best) best.setAttribute("data-active", "");
    current = best;
  }

  function onScroll() {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }

  update();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
})();
