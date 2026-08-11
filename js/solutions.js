/* Solutions: kattintásra a transzparens autó lejátssza az adott
   képességhez tartozó szakaszt, majd megáll.

   Miért nem scroll-scrub: az előző változat a görgetéshez kötötte a
   videó idejét, de a szekció végigfutása alatt gyakorlatilag egy
   állóképnek látszott, és kattintásra sem történt semmi látható.
   Kattintásra lejátszani egyértelműbb: az autó fordul egyet, aztán
   megáll azon a rendszeren, amit a felirat mond.

   A fájl a forrás 4,0-17,0 s tartományát tartalmazza, tehát lokálisan
   0-13 s. A szakaszhatárok a data-from / data-to attribútumokban vannak.
*/
(function () {
  "use strict";

  var root = document.querySelector("[data-solutions]");
  if (!root) return;

  var video = root.querySelector("[data-solutions-video]");
  var caption = root.querySelector("[data-solutions-caption]");
  var progress = root.querySelector("[data-solutions-progress]");
  var items = Array.prototype.slice.call(root.querySelectorAll(".nw-solutions__item"));
  if (!video || !items.length) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var current = null;   // { from, to, item }
  var rafId = 0;

  function segmentOf(item) {
    return {
      from: parseFloat(item.getAttribute("data-from")),
      to: parseFloat(item.getAttribute("data-to")),
      item: item,
    };
  }

  function mark(item) {
    items.forEach(function (b) { b.setAttribute("aria-pressed", String(b === item)); });
    if (caption) caption.textContent = item.querySelector(".nw-solutions__title").textContent;
  }

  function setProgress(p) {
    if (progress) progress.style.setProperty("--p", Math.max(0, Math.min(1, p)));
  }

  function stop() {
    if (rafId) { window.cancelAnimationFrame(rafId); rafId = 0; }
    video.pause();
    root.removeAttribute("data-playing");
  }

  function watch() {
    rafId = window.requestAnimationFrame(watch);
    if (!current) return;
    var span = current.to - current.from;
    setProgress(span > 0 ? (video.currentTime - current.from) / span : 1);
    if (video.currentTime >= current.to) {
      stop();
      video.currentTime = current.to;
      setProgress(1);
    }
  }

  function select(item, play) {
    var seg = segmentOf(item);
    current = seg;
    mark(item);
    stop();
    setProgress(0);

    try { video.currentTime = seg.from; } catch (e) { /* metadata még nincs */ }

    if (!play || reduced) {
      // Reduced motion: nincs lejátszás, csak a szakasz első képkockája.
      setProgress(1);
      return;
    }

    root.setAttribute("data-playing", "");
    var p = video.play();
    if (p && typeof p.catch === "function") {
      p.catch(function () { stop(); setProgress(1); });
    }
    rafId = window.requestAnimationFrame(watch);
  }

  items.forEach(function (item) {
    item.addEventListener("click", function () { select(item, true); });
  });

  // Nyílbillentyűs léptetés a listán belül -- gombcsoportnál ez elvárt.
  root.querySelector(".nw-solutions__list").addEventListener("keydown", function (e) {
    var i = items.indexOf(document.activeElement);
    if (i < 0) return;
    var next = null;
    if (e.key === "ArrowDown" || e.key === "ArrowRight") next = items[(i + 1) % items.length];
    if (e.key === "ArrowUp" || e.key === "ArrowLeft") next = items[(i - 1 + items.length) % items.length];
    if (!next) return;
    e.preventDefault();
    next.focus();
    select(next, true);
  });

  function init() {
    video.pause();
    select(items[0], false);
  }

  if (video.readyState >= 1) init();
  else video.addEventListener("loadedmetadata", init, { once: true });
})();
