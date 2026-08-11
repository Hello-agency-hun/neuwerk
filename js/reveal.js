/* Belépő animáció: IntersectionObserver, egyszer fut elemenként. */
(function () {
  "use strict";

  var items = document.querySelectorAll("[data-reveal]");
  if (!items.length) return;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
      !("IntersectionObserver" in window)) {
    Array.prototype.forEach.call(items, function (el) { el.setAttribute("data-revealed", ""); });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      var delay = parseInt(el.getAttribute("data-reveal-delay") || "0", 10);
      window.setTimeout(function () { el.setAttribute("data-revealed", ""); }, delay);
      io.unobserve(el);
    });
  }, { rootMargin: "0px 0px -12% 0px", threshold: 0.12 });

  Array.prototype.forEach.call(items, function (el) { io.observe(el); });
})();
