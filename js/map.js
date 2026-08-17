/* Világtérkép a neuwerk telephelyekkel.

   ORSZÁGONKÉNT egy pont, nem telephelyenként. A data/locations.js 36
   telephelyet tartalmaz, de azok közül 20 Európában van, több egymástól
   1-2 fokra: telephelyenként egy pont a 150x60-as rácson összefüggő
   folttá mosódna Közép-Európa fölött, és pont az ellenkezőjét mutatná
   annak, amit a szekció állít.

   Az adat viszont nem vész el: a pont az ország telephelyeinek súlypontján
   ül, a tooltip pedig felsorolja a városokat.

   A spec szerint ez stat-vizuál, nem kereső -- ezért a pontok nem linkek,
   csak a nevet mutatják meg.

   Billentyűvel is elérhető: minden pont fókuszálható, mert egérrel
   megszerezhető információt billentyűvel is meg kell tudni szerezni.
*/
(function () {
  "use strict";

  var host = document.querySelector("[data-map]");
  if (!host || !window.NEUWERK_LOCATIONS) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Országonként csoportosítás. A sorrendet az adat sorrendje adja, tehát
     régió szerint halad -- a pontok megjelenési késleltetése így nyugatról
     keletre fut végig, nem összevissza. */
  var order = [];
  var byCountry = {};
  window.NEUWERK_LOCATIONS.forEach(function (loc) {
    if (!byCountry[loc.country]) {
      byCountry[loc.country] = {
        country: loc.country, area: loc.area, cities: [], pts: [], x: 0, y: 0
      };
      order.push(loc.country);
    }
    var g = byCountry[loc.country];
    g.cities.push(loc.city);
    g.pts.push({ x: loc.x, y: loc.y });
    g.x += loc.x;
    g.y += loc.y;
  });

  var groups = order.map(function (name) {
    var g = byCountry[name];

    /* A pont a súlyponthoz legközelebbi TÉNYLEGES telephelyre kerül, nem
       magára a súlypontra.

       Miért: a súlypont vízbe eshet. Kína négy telephelye közül három a
       partvidéken van, egy pedig Changchunnál, északkeleten -- a négy átlaga
       a Sárga-tengerbe esik. Az USA négy telephelyének átlaga a Nagy-tavakra.
       Egy tengerre kitett gyártelep-jelölő azonnal feltűnik, és pont a
       szekció hitelességét rontja.

       A legközelebbi telephely viszont definíció szerint szárazföldön van,
       és az ország telephelyeit ugyanúgy reprezentálja. */
    var cx = g.x / g.pts.length;
    var cy = g.y / g.pts.length;
    var best = g.pts[0];
    var bestD = Infinity;
    g.pts.forEach(function (p) {
      var d = (p.x - cx) * (p.x - cx) + (p.y - cy) * (p.y - cy);
      if (d < bestD) { bestD = d; best = p; }
    });
    g.x = best.x;
    g.y = best.y;
    return g;
  });

  /* A tooltip a .nw-map dobozba kerül, nem a térkép-vászonba.

     Miért: mobilon a vászon mindössze ~133 px magas, tehát a pont fölé
     rakott buborék a szekció címébe lógna bele (méréssel 77 px-ig). Ott
     ezért a térkép ALATT, statikus helyen jelenik meg -- ez egyben a
     tapintásos használatot is megoldja, ahol nincs hover, és ahol az ujj
     amúgy is eltakarná a pont fölötti buborékot.

     A pozíciót emiatt pixelben számoljuk, nem százalékban: a százalék a
     szülőhöz szólna, a .nw-map viszont a vászonnál magasabb (alatta van a
     megjegyzés is), tehát a százalék elcsúszna. */
  var wrap = host.parentNode;
  var tip = document.createElement("span");
  tip.className = "nw-map__tip";
  tip.setAttribute("role", "status");
  tip.setAttribute("aria-live", "polite");
  // Közvetlenül a vászon után, a megjegyzés elé -- mobilon ez a sorrend
  // olvasható: térkép, a kiválasztott ország, majd a használati útmutató.
  wrap.insertBefore(tip, host.nextSibling);

  var active = null;

  function show(dot, g) {
    active = dot;
    /* Csak az ORSZÁG neve. A városokat az ügyfél kérésére nem tüntetjük fel
       név szerint -- a data/locations.js továbbra is telephely-szinten tartja
       őket, mert abból jön az, hogy mely országok szerepelnek, és hova kerül
       az ország pontja. */
    tip.textContent = g.country;

    /* A tooltip a pont fölött, középen ül. A szélső országoknál (USA,
       Japán) a hosszú városlista kilógna a térkép dobozából, ezért a
       vízszintes igazítás a pozíciótól függ.

       Custom property, nem közvetlen left/top: mobilon a CSS statikusra
       váltja a buborékot, és ott ezeket egyszerűen figyelmen kívül hagyja.
       Inline left/top esetén ehhez !important kellene. */
    tip.style.setProperty("--tip-x", (host.offsetLeft + dot.offsetLeft) + "px");
    tip.style.setProperty("--tip-y", (host.offsetTop + dot.offsetTop) + "px");
    tip.setAttribute("data-align", g.x < 25 ? "start" : g.x > 75 ? "end" : "center");
    tip.setAttribute("data-visible", "");
    dot.setAttribute("data-active", "");
  }

  function hide(dot) {
    if (active !== dot) return;
    active = null;
    tip.removeAttribute("data-visible");
    dot.removeAttribute("data-active");
  }

  groups.forEach(function (g, i) {
    var dot = document.createElement("button");
    dot.type = "button";
    dot.className = "nw-map__dot";
    dot.style.left = g.x + "%";
    dot.style.top = g.y + "%";
    if (!reduced) dot.style.animationDelay = (i * 180) + "ms";
    dot.setAttribute("aria-label", g.country);

    dot.addEventListener("pointerenter", function () { show(dot, g); });
    dot.addEventListener("pointerleave", function () { hide(dot); });
    dot.addEventListener("focus", function () { show(dot, g); });
    dot.addEventListener("blur", function () { hide(dot); });

    host.appendChild(dot);
  });
})();
