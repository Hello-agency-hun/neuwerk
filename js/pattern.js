/* neuwerk pattern: nagy formák lassú, scroll-vezérelt eltolása.

   Szándékosan NEM részecskerendszer. A brandbook tiltja a kisméretű,
   sűrű, pusztán dekoratív pattern-használatot, ezért szekciónként
   legfeljebb három nagy forma mozog.

   Markup:
   <div class="nw-pattern" data-pattern>
     <span class="nw-pattern__shape" data-depth="0.12"
           style="left:-10%;top:8%;width:64vmin;height:30vmin"></span>
   </div>

   A szelektor szandekosan [data-depth], nem .nw-pattern__shape: a brand-sav
   (.nw-brandband) sajat osztalyu formakat hasznal, de ugyanezt a
   scroll-vezerlest kapja. Az egyetlen szerzodes az, hogy a [data-pattern]
   kontenerben a mozgatando elemeken legyen data-depth, es a CSS-uk hasznalja
   a --shift valtozot.
*/
(function () {
  "use strict";

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var groups = Array.prototype.map.call(
    document.querySelectorAll("[data-pattern]"),
    function (el) {
      return {
        el: el,
        shapes: Array.prototype.slice.call(el.querySelectorAll("[data-depth]")),
      };
    }
  );
  if (!groups.length) return;

  var ticking = false;

  function update() {
    ticking = false;
    var vh = window.innerHeight;

    groups.forEach(function (g) {
      var rect = g.el.getBoundingClientRect();
      if (rect.bottom < -vh || rect.top > vh * 2) return;   // kívül: ne számolj

      // -1 .. 1 tartomány, 0 amikor a szekció közepe a viewport közepén van
      var progress = (rect.top + rect.height / 2 - vh / 2) / vh;

      g.shapes.forEach(function (s) {
        var depth = parseFloat(s.getAttribute("data-depth")) || 0.1;
        s.style.setProperty("--shift", (progress * depth * -260).toFixed(1) + "px");
      });
    });
  }

  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  update();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
})();
