/* Hero videó.

   A forrásfájl a 4,0-17,0 s tartományt tartalmazza (lokálisan 0-13 s).
   A hero ebből a 0-11,5 s-ot pörgeti -- ez felel meg az eredeti
   4,0-15,5 s transzparens stúdió-szekvenciájának, ami az egyetlen
   hurkolható szakasz. A 11,5-13 s (visszafényezés) csak a Solutions
   scrubhoz kell, a hero nem játssza le.

   A hurokvágás NINCS beleégetve a fájlba: itt oldjuk meg rövid
   opacitás-átúszással, hogy ugyanez a fájl scrubbolható maradjon.
*/
(function () {
  "use strict";

  var video = document.querySelector("[data-hero-video]");
  if (!video) return;

  var LOOP_END = 11.5;
  var FADE_MS = 200;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    video.removeAttribute("autoplay");
    video.pause();
    return;   // a poster attribútum állóképként marad
  }

  function tryPlay() {
    var p = video.play();
    if (p && typeof p.catch === "function") {
      // Autoplay-tiltás esetén a poszter marad. Nem hiba, nem kell UI.
      p.catch(function () {});
    }
  }

  // A script a body vegen fut, a video pedig -- gyors (pl. helyi) szerveren --
  // addigra mar tuljutott a loadeddata-n, tehat readyState >= 2. Ilyenkor az
  // esemenyre varakozas soha nem sul el, a video allokepen ragad.
  if (video.readyState >= 2) {
    tryPlay();
  } else {
    video.addEventListener("loadeddata", tryPlay);
  }

  video.addEventListener("timeupdate", function () {
    if (video.currentTime < LOOP_END) return;
    video.style.opacity = "0";
    window.setTimeout(function () {
      video.currentTime = 0;
      video.style.opacity = "1";
    }, FADE_MS);
  });
})();
