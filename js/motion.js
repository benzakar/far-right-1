/* Scroll choreography.
 *
 * One engine. It writes two custom properties and never touches a
 * layout-triggering property:
 *   --rise  px the element has drifted upward
 *   --fade  opacity
 * Sections that need their own progress get --p (0 to 1).
 *
 * Native scrolling is never intercepted: there is no wheel or touch
 * handler here, and nothing is pinned that the browser does not pin
 * with position: sticky.
 */
(function () {
  "use strict";

  var narrow = window.matchMedia("(max-width: 820px)");

  var root = document.documentElement;
  var cinema = document.querySelector("[data-cinema]");
  var risers = Array.prototype.slice.call(document.querySelectorAll("[data-rise]"));
  var progressors = Array.prototype.slice.call(document.querySelectorAll("[data-progress]"));
  var backdrops = Array.prototype.slice.call(document.querySelectorAll("[data-parallax-bg]"));

  var live = [];       // risers currently in view
  var liveProg = [];   // progress sections currently in view
  var liveBackdrops = []; // leather layers currently near the viewport
  var ticking = false;

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }

  /* Progress through the window [a,b] of an overall 0..1 timeline. */
  function seg(p, a, b) { return clamp((p - a) / (b - a)); }

  /* Ease so layers arrive and leave without a mechanical linear feel.
     Symmetric, so scrubbing backwards mirrors scrubbing forwards. */
  function ease(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function lerp(a, b, t) { return a + (b - a) * t; }

  /* ---- the opening sequence ----
   *
   * One pinned stage, one timeline. Each layer is a pure function of p,
   * which is why the whole thing scrubs cleanly in both directions and
   * can rest at any point.
   *
   *   0.00 .. 0.05   the image alone
   *   0.05 .. 0.35   first line and rival marks share the right-hand slide
   *   0.36 .. 0.68   second line enters and holds on the left
   *   0.69 .. 0.88   party mark rises into the centre
   *   0.88 .. 1.00   centred slogan appears beneath it
   */
  var cine = {};
  if (cinema) {
    ["bg", "dim", "hint", "line1", "parties", "line2", "logo", "slogan"].forEach(function (k) {
      cine[k] = cinema.querySelector('[data-cine="' + k + '"]');
    });
  }

  function set(el, prop, val) { if (el) el.style.setProperty(prop, val); }

  function playCinema(p) {
    /* The background travels on a slower plane than the foreground beats.
       The previous 46px drift across 460vh was effectively imperceptible on
       desktop; the extra overscan keeps this stronger parallax edge-free. */
    /* Mobile scales the visible 16:9 plate itself, so a stronger zoom reads
       clearly even across a short thumb-scroll. */
    var bgTravel = narrow.matches ? 18 : 116;
    var bgZoom = narrow.matches ? 0.22 : 0.12;
    set(cine.bg, "--bg-scale", (1 + p * bgZoom).toFixed(4));

    /* Travel strongly through the sequence, then settle before the stage
       releases. The previous linear finish left the image 116px above its
       own bottom edge and exposed an ivory strip before the green section. */
    var bgPhase = p < 0.82
      ? p / 0.82
      : lerp(1, 0.20, ease(seg(p, 0.82, 1)));
    set(cine.bg, "--bg-rise", (bgPhase * bgTravel).toFixed(1));

    /* The mobile cue fills the quiet space under the image, then clears as
       soon as the visitor starts the scroll story. */
    var hintOut = ease(seg(p, 0.005, 0.075));
    set(cine.hint, "--hint-o", (1 - hintOut).toFixed(3));
    set(cine.hint, "--hint-y", lerp(0, -18, hintOut).toFixed(1));

    /* line one and the rival marks form one right-hand title slide */
    var in1 = ease(seg(p, 0.05, 0.13));
    var out1 = ease(seg(p, 0.29, 0.35));
    set(cine.line1, "--o", (in1 * (1 - out1)).toFixed(3));
    set(cine.line1, "--x", lerp(28, 0, ease(seg(p, 0.05, 0.14))).toFixed(1));
    set(cine.line1, "--y", lerp(34, -24, ease(seg(p, 0.05, 0.35))).toFixed(1));

    /* the pale contrast wash that lets the dark uploaded marks read */
    var dimIn = ease(seg(p, 0.05, 0.12));
    var dimOut = ease(seg(p, 0.29, 0.35));
    set(cine.dim, "--dim", (dimIn * (1 - dimOut)).toFixed(3));

    /* rival marks share the first line's entrance, hold and exit */
    var pIn = ease(seg(p, 0.06, 0.14));
    var pOut = ease(seg(p, 0.29, 0.35));
    var travel = ease(seg(p, 0.06, 0.35));
    set(cine.parties, "--o", (pIn * (1 - pOut)).toFixed(3));
    set(cine.parties, "--x", lerp(24, 0, ease(seg(p, 0.06, 0.15))).toFixed(2));
    set(cine.parties, "--y", lerp(24, -18, travel).toFixed(1));

    /* line two has a clean, separate left-hand title slide */
    var in2 = ease(seg(p, 0.36, 0.45));
    var out2 = ease(seg(p, 0.61, 0.68));
    set(cine.line2, "--o", (in2 * (1 - out2)).toFixed(3));
    set(cine.line2, "--x", lerp(-28, 0, ease(seg(p, 0.36, 0.46))).toFixed(1));
    set(cine.line2, "--y", lerp(34, -24, ease(seg(p, 0.36, 0.68))).toFixed(1));

    /* the party mark rises from below the frame and settles in the middle */
    var rise = ease(seg(p, 0.69, 0.79));
    set(cine.logo, "--o", ease(seg(p, 0.69, 0.76)).toFixed(3));
    set(cine.logo, "--y", lerp(62, 0, rise).toFixed(2));
    set(cine.logo, "--s", lerp(0.92, 1, rise).toFixed(4));

    /* and only then, the slogan */
    var sl = ease(seg(p, 0.88, 0.97));
    set(cine.slogan, "--o", sl.toFixed(3));
    set(cine.slogan, "--y", lerp(26, 0, sl).toFixed(1));
  }

  /* ---- bounded reading panes ----
   *
   * Mirrors the GenioPolicy reader: the passage scrolls inside a fixed-height
   * window, reports progress, and removes its bottom fade at the end. We do
   * not contain overscroll, so the wheel naturally returns to the page once
   * the passage reaches either boundary.
   */
  Array.prototype.forEach.call(document.querySelectorAll("[data-text-pane]"), function (pane) {
    var scroller = pane.querySelector(".policy-pane__scroll");
    var bar = pane.querySelector(".policy-pane__progress i");
    var label = pane.querySelector("[data-pane-progress]");
    if (!scroller) return;

    function updatePane() {
      var max = scroller.scrollHeight - scroller.clientHeight;
      var pct = max > 4 ? Math.min(100, Math.round((scroller.scrollTop / max) * 100)) : 100;
      if (bar) bar.style.width = pct + "%";
      if (label) label.textContent = pct + "%";
      pane.setAttribute("data-at-end", String(pct >= 99));
    }

    scroller.addEventListener("scroll", updatePane, { passive: true });
    window.addEventListener("resize", updatePane, { passive: true });
    if (scroller.scrollHeight > scroller.clientHeight + 4) {
      scroller.setAttribute("tabindex", "0");
      scroller.setAttribute("role", "region");
    }
    updatePane();
  });

  /* ---- reveal on entry (independent of the rise engine) ---- */

  var reveals = document.querySelectorAll("[data-reveal]");
  if (reveals.length) {
    if (!("IntersectionObserver" in window)) {
      for (var r = 0; r < reveals.length; r++) reveals[r].classList.add("is-in");
    } else {
      var revealObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          var delay = parseInt(e.target.getAttribute("data-reveal"), 10) || 0;
          setTimeout(function () { e.target.classList.add("is-in"); }, delay);
          revealObs.unobserve(e.target);
        });
      }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });
      for (var i = 0; i < reveals.length; i++) revealObs.observe(reveals[i]);
    }
  }

  /* ---- only animate what is on screen ---- */

  function membership(list, bucket) {
    if (!("IntersectionObserver" in window)) {
      bucket.push.apply(bucket, list);
      return;
    }
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var at = bucket.indexOf(e.target);
        if (e.isIntersecting && at === -1) bucket.push(e.target);
        else if (!e.isIntersecting && at !== -1) bucket.splice(at, 1);
      });
      request();
    }, { rootMargin: "18% 0px 18% 0px" });
    list.forEach(function (el) { obs.observe(el); });
  }

  membership(risers, live);
  membership(progressors, liveProg);
  membership(backdrops, liveBackdrops);

  /* ---- the frame ---- */

  function frame() {
    ticking = false;
    var vh = window.innerHeight || root.clientHeight;

    /* the opening sequence */
    if (cinema) {
      var span = cinema.offsetHeight - vh;
      var top = cinema.getBoundingClientRect().top;
      playCinema(span > 0 ? clamp(-top / span) : 0);
    }

    /* generic risers */
    for (var i = 0; i < live.length; i++) {
      var el = live[i];
      var rect = el.getBoundingClientRect();
      var p = clamp((vh - rect.top) / (vh + rect.height));
      var amount = parseFloat(el.getAttribute("data-rise")) || 60;
      el.style.setProperty("--rise", (p * amount).toFixed(1));
    }

    /* sections that colour themselves by progress (the bus) */
    for (var j = 0; j < liveProg.length; j++) {
      var sec = liveProg[j];
      var sr = sec.getBoundingClientRect();
      var sp = clamp((vh - sr.top) / (vh + sr.height * 0.6));
      sec.style.setProperty("--p", sp.toFixed(4));
    }

    /* Independent leather planes. Each image crosses half the available
       overscan while its section passes the viewport, so the movement is
       visible without making the copy feel detached from its section. */
    for (var k = 0; k < liveBackdrops.length; k++) {
      var backdrop = liveBackdrops[k];
      var br = backdrop.getBoundingClientRect();
      var bp = clamp((vh - br.top) / (vh + br.height));
      var travel = narrow.matches ? 56 : 120;
      backdrop.style.setProperty("--backdrop-y", ((0.5 - bp) * travel).toFixed(1) + "px");
    }
  }

  function request() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(frame);
  }

  window.addEventListener("scroll", request, { passive: true });
  window.addEventListener("resize", request, { passive: true });
  frame();

  /* ---- masthead surface after the first scroll threshold ---- */

  var masthead = document.querySelector("[data-masthead]");
  if (masthead) {
    var sentinel = document.createElement("div");
    sentinel.setAttribute("aria-hidden", "true");
    sentinel.style.cssText = "position:absolute;top:0;left:0;width:1px;height:80px;pointer-events:none;";
    document.body.prepend(sentinel);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        masthead.classList.toggle("is-stuck", !entries[0].isIntersecting);
      }).observe(sentinel);
    }
  }
})();
