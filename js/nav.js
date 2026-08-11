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

  // Aktív oldal. A fájlnevet hasonlítjuk, mert nincs szerveroldali routing.
  var here = window.location.pathname.split("/").pop() || "index.html";
  Array.prototype.forEach.call(header.querySelectorAll("a[href]"), function (a) {
    var target = a.getAttribute("href").split("#")[0].split("/").pop();
    if (target && target === here) a.setAttribute("aria-current", "page");
  });
})();
