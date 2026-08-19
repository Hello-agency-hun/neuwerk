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

  /* Kozep-Europaban 11 orszag zsufolodik ~13x8 szazalekponton -- ennyi
     pont a 150x60-as vasznon egymast fedne. A doboz-hatarok a tenyleges
     adatbol vannak kimerve (Nemetorszagtol Romaniaig, Portugaliatol a
     legkeletibb pontig), Marokko (y~34) mar kivul esik, tehat marad
     onallo pontkent a fo terkepen.

     Megoldas: a klaszteren beluli orszagok EGY jelolot kapnak a fo
     terkepen ("Europe, 11 countries"), a tenyleges 11 pont pedig egy
     kulon, mindig lathato listaban jelenik meg alatta -- nem hover-fuggo
     tooltipben, mert pont a zsufoltsag miatt nincs ott hely a neveknek. */
  var EU_BBOX = { x0: 46, x1: 59, y0: 20, y1: 32 };
  function inEuropeCluster(g) {
    return g.x >= EU_BBOX.x0 && g.x <= EU_BBOX.x1 && g.y >= EU_BBOX.y0 && g.y <= EU_BBOX.y1;
  }

  var euGroups = groups.filter(inEuropeCluster);
  var restGroups = groups.filter(function (g) { return !inEuropeCluster(g); });

  function makeDot(g, i, extraLabel) {
    var dot = document.createElement("button");
    dot.type = "button";
    dot.className = "nw-map__dot";
    dot.style.left = g.x + "%";
    dot.style.top = g.y + "%";
    if (!reduced) dot.style.animationDelay = (i * 180) + "ms";
    dot.setAttribute("aria-label", extraLabel || g.country);

    dot.addEventListener("pointerenter", function () { show(dot, { country: extraLabel || g.country }); });
    dot.addEventListener("pointerleave", function () { hide(dot); });
    dot.addEventListener("focus", function () { show(dot, { country: extraLabel || g.country }); });
    dot.addEventListener("blur", function () { hide(dot); });

    host.appendChild(dot);
    return dot;
  }

  restGroups.forEach(function (g, i) { makeDot(g, i); });

  if (euGroups.length) {
    /* A klaszter-jelolo a csoport sulypontjan all -- nem egy tenyleges
       orszagot jelol, csak azt mutatja meg, HOL van a zsufolt terulet. */
    var cx = 0, cy = 0;
    euGroups.forEach(function (g) { cx += g.x; cy += g.y; });
    cx /= euGroups.length; cy /= euGroups.length;

    var clusterDot = makeDot(
      { x: cx, y: cy },
      restGroups.length,
      "Europe, " + euGroups.length + " countries — see list below"
    );
    clusterDot.classList.add("nw-map__dot--cluster");

    var detail = document.querySelector("[data-map-detail]");
    var list = document.querySelector("[data-map-detail-list]");
    if (detail && list) {
      document.querySelector(".nw-map__detail-label").textContent =
        "Europe, " + euGroups.length + " countries";
      euGroups.forEach(function (g) {
        var li = document.createElement("li");
        li.className = "nw-map__detail-item";
        var dot = document.createElement("span");
        dot.className = "nw-map__detail-dot";
        dot.setAttribute("aria-hidden", "true");
        li.appendChild(dot);
        li.appendChild(document.createTextNode(g.country));
        list.appendChild(li);
      });
      detail.hidden = false;
    }
  }
})();
