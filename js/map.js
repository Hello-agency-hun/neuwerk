/* Dekoratív világtérkép: 16 pont a data/locations.js alapján, hoverre
   és fókuszra megjelenő országnévvel.

   A spec szerint ez stat-vizuál, nem kereső -- ezért a pontok nem
   linkek, csak a nevet mutatják meg.

   Billentyűvel is elérhető: minden pont fókuszálható, mert egérrel
   megszerezhető információt billentyűvel is meg kell tudni szerezni.
*/
(function () {
  "use strict";

  var host = document.querySelector("[data-map]");
  if (!host || !window.NEUWERK_LOCATIONS) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var tip = document.createElement("span");
  tip.className = "nw-map__tip";
  tip.setAttribute("role", "status");
  tip.setAttribute("aria-live", "polite");
  host.appendChild(tip);

  var active = null;

  function show(dot, loc) {
    active = dot;
    tip.textContent = loc.name;
    // A placeholder-jelölés a tooltipben is ott van: ha valaki képernyőképet
    // készít a térképről, azon is látszania kell, hogy ez nem valós adat.
    tip.setAttribute("data-placeholder-label", loc.placeholder ? "placeholder" : "");
    tip.style.left = loc.x + "%";
    tip.style.top = loc.y + "%";
    tip.setAttribute("data-visible", "");
    dot.setAttribute("data-active", "");
  }

  function hide(dot) {
    if (active !== dot) return;
    active = null;
    tip.removeAttribute("data-visible");
    dot.removeAttribute("data-active");
  }

  window.NEUWERK_LOCATIONS.forEach(function (loc, i) {
    var dot = document.createElement("button");
    dot.type = "button";
    dot.className = "nw-map__dot";
    dot.style.left = loc.x + "%";
    dot.style.top = loc.y + "%";
    if (!reduced) dot.style.animationDelay = (i * 180) + "ms";
    dot.setAttribute("aria-label", loc.name + (loc.placeholder ? " (placeholder)" : ""));

    dot.addEventListener("pointerenter", function () { show(dot, loc); });
    dot.addEventListener("pointerleave", function () { hide(dot); });
    dot.addEventListener("focus", function () { show(dot, loc); });
    dot.addEventListener("blur", function () { hide(dot); });

    host.appendChild(dot);
  });
})();
