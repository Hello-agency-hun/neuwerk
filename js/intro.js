/* Logó reveal intro. Egyszer fut látogatásonként (sessionStorage),
   átugorható kattintással vagy billentyűvel, és reduced-motion
   mellett meg sem jelenik. */
(function () {
  "use strict";

  var intro = document.querySelector("[data-intro]");
  if (!intro) return;

  var KEY = "nw-intro-seen";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var seen = false;
  try { seen = window.sessionStorage.getItem(KEY) === "1"; } catch (e) { seen = false; }

  if (reduced || seen) { intro.remove(); return; }

  document.documentElement.style.overflow = "hidden";

  function dismiss() {
    intro.setAttribute("data-done", "");
    document.documentElement.style.overflow = "";
    try { window.sessionStorage.setItem(KEY, "1"); } catch (e) { /* privát mód */ }
    window.setTimeout(function () { intro.remove(); }, 500);
  }

  window.setTimeout(dismiss, 1200);
  intro.addEventListener("click", dismiss);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" || e.key === "Enter" || e.key === " ") dismiss();
  }, { once: true });
})();
