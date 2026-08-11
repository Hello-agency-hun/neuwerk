/* Dekoratív világtérkép: 16 pulzáló pont a data/locations.js alapján.
   Nincs kereső és nincs interakció -- a spec szerint ez stat-vizuál. */
(function () {
  "use strict";

  var host = document.querySelector("[data-map]");
  if (!host || !window.NEUWERK_LOCATIONS) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  window.NEUWERK_LOCATIONS.forEach(function (loc, i) {
    var dot = document.createElement("span");
    dot.className = "nw-map__dot";
    dot.style.left = loc.x + "%";
    dot.style.top = loc.y + "%";
    if (!reduced) dot.style.animationDelay = (i * 180) + "ms";
    dot.setAttribute("title", loc.name);
    host.appendChild(dot);
  });
})();
