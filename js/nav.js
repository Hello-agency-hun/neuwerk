/* Header: mobilmenü, scroll-állapot, aktív oldal jelölése. */
(function () {
  "use strict";

  var header = document.querySelector("[data-nav]");
  if (!header) return;

  var toggle = header.querySelector("[data-nav-toggle]");
  var nav = header.querySelector(".nw-header__nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.hasAttribute("data-open");
      if (open) {
        nav.removeAttribute("data-open");
      } else {
        nav.setAttribute("data-open", "");
      }
      toggle.setAttribute("aria-expanded", String(!open));
    });

    // Esc zárja, és a fókusz visszakerül a gombra
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.hasAttribute("data-open")) {
        nav.removeAttribute("data-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  // Scroll-állapot: a header átlátszóból navy-ra vált
  var onScroll = function () {
    if (window.scrollY > 24) {
      header.setAttribute("data-scrolled", "");
    } else {
      header.removeAttribute("data-scrolled");
    }
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // --- Aktív állapot ------------------------------------------------
  // Két külön eset, és korábban ez volt a hiba: a fájlnév-hasonlítás
  // az index.html#who-we-are és az index.html#solutions linket EGYARÁNT
  // index.html-re egyszerűsítette, ezért a főoldalon mindkettő aktív lett.
  //
  // 1. Más oldalra mutató link  -> fájlnév egyezés.
  // 2. Ugyanerre az oldalra mutató horgony -> scroll-spy: az számít
  //    aktívnak, amelyik szekció épp a nézetben van.

  var here = window.location.pathname.split("/").pop() || "index.html";
  var links = Array.prototype.slice.call(header.querySelectorAll(".nw-header__nav a[href]"));
  var anchors = [];   // { link, section }

  links.forEach(function (a) {
    var href = a.getAttribute("href");
    var hash = href.indexOf("#") >= 0 ? href.slice(href.indexOf("#") + 1) : "";
    var file = href.split("#")[0].split("/").pop();
    var samePage = !file || file === here;

    if (hash && samePage) {
      var section = document.getElementById(hash);
      if (section) anchors.push({ link: a, section: section });
    } else if (file === here && !hash) {
      a.setAttribute("aria-current", "page");
    }
  });

  if (!anchors.length) return;

  function clearAnchors() {
    anchors.forEach(function (x) { x.link.removeAttribute("aria-current"); });
  }

  if (!("IntersectionObserver" in window)) return;

  var visible = Object.create(null);

  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      visible[e.target.id] = e.isIntersecting ? e.intersectionRatio : 0;
    });

    var bestId = null;
    var bestRatio = 0;
    anchors.forEach(function (x) {
      var r = visible[x.section.id] || 0;
      if (r > bestRatio) { bestRatio = r; bestId = x.section.id; }
    });

    clearAnchors();
    if (!bestId) return;
    anchors.forEach(function (x) {
      if (x.section.id === bestId) x.link.setAttribute("aria-current", "true");
    });
  }, {
    // A header magasságát levonjuk, különben a fixed header alatti sáv
    // is "látszónak" számítana.
    rootMargin: "-" + (parseInt(getComputedStyle(document.documentElement)
      .getPropertyValue("--nw-header-h"), 10) || 72) + "px 0px -45% 0px",
    threshold: [0, 0.15, 0.35, 0.6, 0.9],
  });

  anchors.forEach(function (x) { spy.observe(x.section); });
})();
