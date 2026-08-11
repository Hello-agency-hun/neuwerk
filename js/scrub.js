/* Solutions: scroll-scrub + pillérváltás.

   A videó a 4,0-17,0 s tartományt tartalmazza, lokálisan 0-13 s.
   A képesség -> szakasz leképezés a specben van; a gombokon a
   data-scrub-to a szakasz KÖZEPE, lokális időben.

   A fájl -g 15 kulcskocka-sűrűséggel készült, ezért a currentTime-ugrás
   simán megy. Ha akadozik, a build_video.py GOP értékét kell csökkenteni.
*/
(function () {
  "use strict";

  var section = document.querySelector("[data-scrub]");
  if (!section) return;

  var video = section.querySelector("[data-scrub-video]");
  var buttons = Array.prototype.slice.call(section.querySelectorAll("[data-scrub-to]"));
  if (!video || !buttons.length) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var duration = 0;
  var manual = false;
  var manualUntil = 0;

  video.addEventListener("loadedmetadata", function () {
    duration = video.duration || 13;
    video.pause();
    video.currentTime = 0.01;
    markActive(0.01);
  });

  function markActive(t) {
    var best = 0;
    var bestDist = Infinity;
    buttons.forEach(function (b, i) {
      var d = Math.abs(parseFloat(b.getAttribute("data-scrub-to")) - t);
      if (d < bestDist) { bestDist = d; best = i; }
    });
    buttons.forEach(function (b, i) {
      b.setAttribute("aria-pressed", String(i === best));
    });
  }

  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      var t = parseFloat(b.getAttribute("data-scrub-to"));
      video.currentTime = t;
      markActive(t);
      manual = true;
      manualUntil = Date.now() + 1200;
      b.scrollIntoView({ block: "nearest", behavior: reduced ? "auto" : "smooth" });
    });
  });

  if (reduced) return;   // reduced-motion: csak a gombok működnek, scroll nem scrubbol

  var ticking = false;

  function update() {
    ticking = false;
    if (!duration) return;
    if (manual && Date.now() < manualUntil) return;
    manual = false;

    var rect = section.getBoundingClientRect();
    var vh = window.innerHeight;
    var span = rect.height + vh;
    if (rect.bottom < 0 || rect.top > vh) return;

    var progress = Math.min(Math.max((vh - rect.top) / span, 0), 1);
    var t = progress * duration;
    if (Math.abs(video.currentTime - t) > 0.06) {
      video.currentTime = t;
      markActive(t);
    }
  }

  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }, { passive: true });
})();
