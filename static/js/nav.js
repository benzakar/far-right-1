/* Mobile navigation: modal on small screens, plain list above.
 * Focus is trapped while open and restored on close. */
/* Sliders: one item at a time, arrows on both sides.
 *
 * The track is a scroll-snap container, so swipe and keyboard already work
 * without us. These handlers only nudge that scroll by one slide and keep
 * the arrows and counter honest about where we are. With JavaScript off,
 * the track is still scrollable and every slide reachable.
 */
(function () {
  "use strict";

  Array.prototype.forEach.call(document.querySelectorAll("[data-slider]"), function (slider) {
    var track = slider.querySelector("[data-slider-track]");
    var count = slider.querySelector("[data-slider-count]");
    var prev = slider.querySelector('[data-slide="prev"]');
    var next = slider.querySelector('[data-slide="next"]');
    if (!track) return;

    var slides = Array.prototype.slice.call(track.children);
    if (slides.length < 2) {
      if (prev) prev.hidden = true;
      if (next) next.hidden = true;
      if (count) count.hidden = true;
      return;
    }

    /* Which slide is nearest the centre of the track right now. Measuring
       beats tracking an index: swipe, keyboard and arrows all move the same
       scroll position, so reading it back is the one source of truth. */
    function currentIndex() {
      var middle = track.scrollLeft + track.clientWidth / 2;
      var best = 0;
      var bestGap = Infinity;
      slides.forEach(function (slide, i) {
        var centre = slide.offsetLeft + slide.offsetWidth / 2;
        var gap = Math.abs(centre - middle);
        if (gap < bestGap) { bestGap = gap; best = i; }
      });
      return best;
    }

    /* Paint the controls for a known index. Smooth scrolling means the
       scroll handler reports the new position hundreds of milliseconds
       later, so driving the UI only from it left the arrows a click behind
       — pressing next then prev found prev still disabled. */
    function paint(i) {
      if (count) count.textContent = (i + 1) + " / " + slides.length;
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === slides.length - 1;
    }

    /* Where we intend to be. Measuring on every click read a position still
       mid-animation, so pressing the arrow quickly several times kept
       resolving to the same slide and the extra presses were swallowed. */
    var wanted = 0;

    function goTo(index) {
      wanted = Math.max(0, Math.min(slides.length - 1, index));
      var slide = slides[wanted];
      paint(wanted);
      track.scrollTo({
        left: slide.offsetLeft - (track.clientWidth - slide.offsetWidth) / 2,
        behavior: "smooth"
      });
    }

    /* Re-derive from the actual scroll position, which is what a swipe or a
       trackpad gesture moves without ever calling goTo. */
    function sync() {
      wanted = currentIndex();
      paint(wanted);
    }

    if (prev) prev.onclick = function () { goTo(wanted - 1); };
    if (next) next.onclick = function () { goTo(wanted + 1); };

    track.addEventListener("keydown", function (event) {
      if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
      event.preventDefault();
      /* in RTL, ArrowLeft advances */
      var forward = event.key === "ArrowLeft";
      goTo(wanted + (forward ? 1 : -1));
    });

    var pending;
    track.addEventListener("scroll", function () {
      clearTimeout(pending);
      pending = setTimeout(sync, 90);
    }, { passive: true });
    window.addEventListener("resize", sync, { passive: true });
    sync();
  });
}());

(function () {
  "use strict";

  var burger = document.querySelector("[data-burger]");
  var nav = document.querySelector("[data-nav]");
  if (!burger || !nav) return;

  var opener = null;

  /* The toggle sits outside the panel but stays visible above it, so it
     belongs inside the trap — otherwise the panel can be opened by
     keyboard and only closed with Escape. It is listed first because it
     precedes the panel in the document. */
  function focusables() {
    var inPanel = Array.prototype.filter.call(
      nav.querySelectorAll("a[href], button:not([disabled])"),
      function (el) { return el.offsetParent !== null; }
    );
    return [burger].concat(inPanel);
  }

  function open() {
    opener = document.activeElement;
    nav.classList.add("is-open");
    burger.setAttribute("aria-expanded", "true");
    burger.setAttribute("aria-label", burger.getAttribute("data-label-close") || "Close menu");
    document.body.style.overflow = "hidden";
    var f = focusables();
    if (f.length) f[0].focus();
    document.addEventListener("keydown", onKey);
  }

  function close() {
    nav.classList.remove("is-open");
    burger.setAttribute("aria-expanded", "false");
    burger.setAttribute("aria-label", burger.getAttribute("data-label-menu") || "Menu");
    document.body.style.overflow = "";
    document.removeEventListener("keydown", onKey);
    if (opener && opener.focus) opener.focus();
  }

  function onKey(e) {
    if (e.key === "Escape") { close(); return; }
    if (e.key !== "Tab") return;
    var f = focusables();
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  burger.addEventListener("click", function () {
    if (nav.classList.contains("is-open")) close(); else open();
  });

  nav.addEventListener("click", function (e) {
    if (e.target.closest("a") && nav.classList.contains("is-open")) close();
  });

  /* If the viewport grows past the breakpoint while the panel is open,
     drop the modal state so the desktop nav is not left inert. */
  window.matchMedia("(min-width: 941px)").addEventListener("change", function (e) {
    if (e.matches && nav.classList.contains("is-open")) close();
  });
})();
