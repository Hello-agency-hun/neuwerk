/* Kinetikus tipográfia: a bekezdés szavanként világosodik be, ahogy
   a szekció áthalad a nézeten.

   Nem dísz: a vezérmondat így kap súlyt anélkül, hogy nagyobb betűvel
   vagy színnel kellene kiabálnia -- a brandbook a Sunt 10-15%-ban
   maximálja, tehát a kiemelésre nem használhatunk narancsot.

   Progresszív: JS nélkül a szöveg simán olvasható marad, mert a
   kiinduló állapotot is a JS teszi rá (data-kinetic-ready).
*/
(function () {
  "use strict";

  var nodes = Array.prototype.slice.call(document.querySelectorAll("[data-kinetic]"));
  if (!nodes.length) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var blocks = nodes.map(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = "";
    var spans = words.map(function (w, i) {
      var span = document.createElement("span");
      span.className = "nw-kinetic__w";
      span.textContent = w;
      el.appendChild(span);
      if (i < words.length - 1) el.appendChild(document.createTextNode(" "));
      return span;
    });
    el.setAttribute("data-kinetic-ready", "");
    return { el: el, spans: spans };
  });

  if (reduced) {
    // Nincs mozgás: minden szó azonnal a végállapotban.
    blocks.forEach(function (b) {
      b.spans.forEach(function (s) { s.setAttribute("data-on", ""); });
    });
    return;
  }

  var ticking = false;

  function update() {
    ticking = false;
    var vh = window.innerHeight;

    blocks.forEach(function (b) {
      var r = b.el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;

      // 0 -> a blokk alja épp belép alulról; 1 -> a teteje a viewport
      // felső harmadánál jár. Ebben a sávban fut végig a bevilágítás.
      var startY = vh * 0.85;
      var endY = vh * 0.35;
      var p = (startY - r.top) / (startY - endY);
      p = Math.max(0, Math.min(1, p));

      var lit = Math.round(p * b.spans.length);
      b.spans.forEach(function (s, i) {
        if (i < lit) s.setAttribute("data-on", "");
        else s.removeAttribute("data-on");
      });
    });
  }

  function onScroll() {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }

  update();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
})();
