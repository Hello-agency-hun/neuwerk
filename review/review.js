/* Visszajelzés-gyűjtő widget a review-buildhez.

   CSAK a bemutató-változat része. Az éles csomagban nincs benne -- ott
   a site tiszta statikus HTML/CSS/JS, szerveroldal nélkül.

   Amit tud: lebegő gomb, hoverre kinyíló panel, oldalanként és
   szekciónként rögzített megjegyzés, kategóriával és névvel. A bejegyzést
   a feedback.php fűzi hozzá a feedback/comments.json fájlhoz.

   A "melyik szekcióról van szó" mezőt automatikusan kitölti azzal, ami
   épp a képernyő közepén van -- így a véleményező nem gépeli be újra.
*/
(function () {
  "use strict";

  var ENDPOINT = "feedback.php";
  var STORE_AUTHOR = "nw-review-author";

  var CATEGORIES = [
    "Oldalstruktúra",
    "Szöveg / copy",
    "Kép, videó, vizuál",
    "Elrendezés, tipográfia",
    "Interakció, animáció",
    "Overall benyomás",
    "Egyéb"
  ];

  /* --- panel felépítése -------------------------------------------
     Az innerHTML itt konstans literál: nincs benne egyetlen behelyettesített
     érték sem. A kategórialista createElement + textContent, az oldalnév és
     a szekciócím szintén textContent. Külső adat soha nem kerül HTML-ként
     a DOM-ba, tehát nincs XSS-felület. Ne írd át interpolációra. */
  var root = document.createElement("div");
  root.className = "nwr";
  root.setAttribute("data-nwr", "");
  root.innerHTML =
    '<button class="nwr__fab" type="button" aria-expanded="false" aria-controls="nwr-panel">' +
      '<span class="nwr__fab-icon" aria-hidden="true"></span>' +
      '<span class="nwr__fab-label">Megjegyzés</span>' +
    '</button>' +
    '<form class="nwr__panel" id="nwr-panel" hidden>' +
      '<p class="nwr__head">Megjegyzés ehhez az oldalhoz</p>' +
      '<p class="nwr__where"><span data-nwr-page></span><span data-nwr-section></span></p>' +
      '<label class="nwr__label">Miről szól<select class="nwr__input" data-nwr-cat></select></label>' +
      '<label class="nwr__label">Megjegyzés' +
        '<textarea class="nwr__input nwr__area" data-nwr-comment rows="5" required ' +
        'placeholder="Mit változtatnál? Legyél konkrét: melyik elem, mit helyette."></textarea></label>' +
      '<label class="nwr__label">Név<input class="nwr__input" data-nwr-author type="text" placeholder="pl. Ági"></label>' +
      '<div class="nwr__row">' +
        '<button class="nwr__send" type="submit">Küldés</button>' +
        '<span class="nwr__dls">' +
          '<a class="nwr__dl" href="' + ENDPOINT + '?download=1">JSON</a>' +
          '<a class="nwr__dl" href="' + ENDPOINT + '?zip=1">ZIP</a>' +
          '<a class="nwr__dl" href="' + ENDPOINT + '?stat=1" target="_blank" rel="noopener">Összesítő</a>' +
        '</span>' +
      '</div>' +
      '<p class="nwr__msg" data-nwr-msg role="status" aria-live="polite"></p>' +
    '</form>';
  document.body.appendChild(root);

  var fab = root.querySelector(".nwr__fab");
  var panel = root.querySelector(".nwr__panel");
  var catSel = root.querySelector("[data-nwr-cat]");
  var commentEl = root.querySelector("[data-nwr-comment]");
  var authorEl = root.querySelector("[data-nwr-author]");
  var pageEl = root.querySelector("[data-nwr-page]");
  var sectionEl = root.querySelector("[data-nwr-section]");
  var msgEl = root.querySelector("[data-nwr-msg]");

  CATEGORIES.forEach(function (c) {
    var o = document.createElement("option");
    o.value = c; o.textContent = c;
    catSel.appendChild(o);
  });

  var pageName = window.location.pathname.split("/").pop() || "index.html";
  pageEl.textContent = pageName;

  try {
    var saved = window.localStorage.getItem(STORE_AUTHOR);
    if (saved) authorEl.value = saved;
  } catch (e) { /* privát mód */ }

  /* --- melyik szekció van épp a képernyő közepén? ------------------ */
  function currentSection() {
    var mid = window.innerHeight / 2;
    var best = null, bestDist = Infinity;
    Array.prototype.forEach.call(
      document.querySelectorAll("main section, main article, main > div > section"),
      function (s) {
        var r = s.getBoundingClientRect();
        if (r.bottom < 0 || r.top > window.innerHeight) return;
        var d = Math.abs(r.top + r.height / 2 - mid);
        if (d < bestDist) { bestDist = d; best = s; }
      }
    );
    if (!best) return "";
    var h = best.querySelector("h1, h2");
    return (h ? h.textContent : best.id || "").trim().replace(/\s+/g, " ").slice(0, 80);
  }

  function refreshWhere() {
    var s = currentSection();
    sectionEl.textContent = s ? " · " + s : "";
  }

  /* --- nyitás / zárás ---------------------------------------------- */
  function open() {
    refreshWhere();
    panel.hidden = false;
    root.setAttribute("data-open", "");
    fab.setAttribute("aria-expanded", "true");
    commentEl.focus();
  }
  function close() {
    panel.hidden = true;
    root.removeAttribute("data-open");
    fab.setAttribute("aria-expanded", "false");
  }

  fab.addEventListener("click", function () {
    if (root.hasAttribute("data-open")) close(); else open();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && root.hasAttribute("data-open")) { close(); fab.focus(); }
  });

  /* --- küldés ------------------------------------------------------- */
  panel.addEventListener("submit", function (e) {
    e.preventDefault();
    var comment = commentEl.value.trim();
    if (!comment) return;

    var payload = {
      page: pageName,
      title: document.title,
      section: sectionEl.textContent.replace(/^ · /, ""),
      category: catSel.value,
      author: authorEl.value.trim(),
      comment: comment,
      viewport: window.innerWidth + "x" + window.innerHeight
    };

    try { window.localStorage.setItem(STORE_AUTHOR, payload.author); } catch (err) { /* privát mód */ }

    msgEl.textContent = "Küldés…";
    msgEl.removeAttribute("data-error");

    fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (!res.ok || !res.j.ok) throw new Error(res.j && res.j.error ? res.j.error : "Ismeretlen hiba");
        commentEl.value = "";
        msgEl.textContent = "Mentve (" + res.j.count + ". megjegyzés).";
        window.setTimeout(function () { msgEl.textContent = ""; }, 4000);
      })
      .catch(function (err) {
        msgEl.textContent = "Nem sikerült: " + err.message;
        msgEl.setAttribute("data-error", "");
      });
  });

  window.addEventListener("scroll", function () {
    if (root.hasAttribute("data-open")) refreshWhere();
  }, { passive: true });
})();
