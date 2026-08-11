/* Solutions: kattintásra a kiválasztott pillér saját klipje úszik be és
   játszik le egyszer, majd megáll az utolsó képkockán.

   Miért négy külön fájl és nem egy scrubbolt: a közös fájl a hero volt, amibe
   bele van égetve a padlóra vetített SAFETY / PERFORMANCE / EFFICIENCY /
   COMFORT tipográfia. Az a felirat nem az alsó harmadban ül -- az EFFICIENCY
   szakaszban a képkocka közepén, az akkumulátorcsomagon fut át --, tehát sem
   `object-position`-nel, sem vágással nem tüntethető el. A négy pillér ezért
   saját, feliratmentes vágóképet kapott (tools/build_solutions.py).

   Miért nem sima vágás: mind a négy klip ugyanabban a stúdióban, ugyanazon az
   autón készült, és ugyanazt a split-tone gradinget kapta. Keresztúsztatásban
   ezért nem jelenetváltásnak látszik, hanem annak, hogy ugyanaz az autó vált
   át egy másik rendszer átvilágítására. A kimenő réteg az úsztatás alatt
   átlátszatlan marad a bejövő alatt, így nem villan át a háttér.
*/
(function () {
  "use strict";

  var root = document.querySelector("[data-solutions]");
  if (!root) return;

  var stage = root.querySelector(".nw-solutions__stage");
  var caption = root.querySelector("[data-solutions-caption]");
  var progress = root.querySelector("[data-solutions-progress]");
  var items = Array.prototype.slice.call(root.querySelectorAll(".nw-solutions__item"));
  var videos = Array.prototype.slice.call(root.querySelectorAll(".nw-solutions__video"));
  if (!items.length || !videos.length) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var byName = {};
  videos.forEach(function (v) { byName[v.getAttribute("data-solution")] = v; });

  var active = root.querySelector(".nw-solutions__video.is-active") || videos[0];
  var rafId = 0;
  var prevTimer = 0;

  function setProgress(p) {
    if (progress) progress.style.setProperty("--p", Math.max(0, Math.min(1, p)));
  }

  function stop() {
    if (rafId) { window.cancelAnimationFrame(rafId); rafId = 0; }
    root.removeAttribute("data-playing");
  }

  function watch() {
    rafId = window.requestAnimationFrame(watch);
    var d = active.duration;
    if (!d || !isFinite(d)) return;
    setProgress(active.currentTime / d);
    if (active.ended || active.currentTime >= d - 0.02) {
      stop();
      setProgress(1);
    }
  }

  function mark(item) {
    items.forEach(function (b) { b.setAttribute("aria-pressed", String(b === item)); });
    if (caption) caption.textContent = item.querySelector(".nw-solutions__title").textContent;
  }

  /* A leváltott réteg .is-prev-ként átlátszatlan marad, amíg a bejövő
     beúszik, utána kerül vissza a sor végére. */
  function swap(next) {
    if (next === active) return;
    var prev = active;
    active = next;

    window.clearTimeout(prevTimer);
    videos.forEach(function (v) {
      if (v !== prev && v !== next) v.classList.remove("is-prev", "is-active");
    });
    prev.classList.remove("is-active");
    prev.classList.add("is-prev");
    next.classList.add("is-active");

    var hold = reduced ? 0 : 700;
    prevTimer = window.setTimeout(function () {
      prev.classList.remove("is-prev");
      prev.pause();
      try { prev.currentTime = 0; } catch (e) { /* metaadat még nincs */ }
    }, hold);
  }

  function select(item, play) {
    var name = item.getAttribute("data-solution");
    var video = byName[name];
    if (!video) return;

    stop();
    mark(item);
    setProgress(0);
    swap(video);

    // A szomszédos klipeket csak akkor húzzuk be, ha a szekcióhoz tényleg
    // hozzáért a felhasználó -- így az oldalbetöltés nem visz el 2,3 MB-ot.
    warm();

    try { video.currentTime = 0; } catch (e) { /* metaadat még nincs */ }

    if (!play || reduced) {
      // Reduced motion: nincs lejátszás, a klip első képkockája marad állva.
      video.pause();
      setProgress(1);
      return;
    }

    root.setAttribute("data-playing", "");
    var p = video.play();
    if (p && typeof p.catch === "function") {
      // Autoplay-tiltás esetén a poszter marad. Nem hiba, nem kell UI.
      p.catch(function () { stop(); setProgress(1); });
    }
    rafId = window.requestAnimationFrame(watch);
  }

  var warmed = false;
  function warm() {
    if (warmed) return;
    warmed = true;
    videos.forEach(function (v) {
      if (v.getAttribute("preload") !== "auto") {
        v.setAttribute("preload", "auto");
        v.load();
      }
    });
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

  // Ha a szekció képbe ér, előtöltjük a többi klipet, hogy az első
  // kattintás már ne várjon a hálózatra.
  if (stage && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        warm();
        io.disconnect();
      });
    }, { rootMargin: "200px" });
    io.observe(stage);
  }

  videos.forEach(function (v) { v.pause(); });
  mark(items[0]);
  setProgress(reduced ? 1 : 0);
})();
