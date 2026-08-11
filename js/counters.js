/* Felszámláló. A végérték a data-count attribútumban van, hogy
   JS nélkül és reduced-motion mellett is a helyes szám látsszon. */
(function () {
  "use strict";

  var els = document.querySelectorAll("[data-count]");
  if (!els.length) return;

  function format(n, sep) {
    return sep ? String(n).replace(/\B(?=(\d{3})+(?!\d))/g, sep) : String(n);
  }

  function run(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var sep = el.getAttribute("data-count-sep") || "";
    var dur = 1400;
    var t0 = null;

    function step(ts) {
      if (t0 === null) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = format(Math.round(target * eased), sep);
      if (p < 1) window.requestAnimationFrame(step);
    }
    window.requestAnimationFrame(step);
  }

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  Array.prototype.forEach.call(els, function (el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var sep = el.getAttribute("data-count-sep") || "";

    if (reduced || !("IntersectionObserver" in window)) {
      el.textContent = format(target, sep);
      return;
    }

    el.textContent = format(0, sep);
    var io = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { run(el); io.disconnect(); }
    }, { threshold: 0.5 });
    io.observe(el);
  });
})();
