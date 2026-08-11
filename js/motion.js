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

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  var fine = window.matchMedia("(pointer: fine)");
  var narrow = window.matchMedia("(max-width: 820px)");

  var root = document.documentElement;
  var hero = document.querySelector("[data-hero]");
  var heroContent = document.querySelector("[data-hero-content]");
  var heroImages = Array.prototype.slice.call(document.querySelectorAll("[data-hero-img]"));
  var risers = Array.prototype.slice.call(document.querySelectorAll("[data-rise]"));
  var progressors = Array.prototype.slice.call(document.querySelectorAll("[data-progress]"));

  var live = [];       // risers currently in view
  var liveProg = [];   // progress sections currently in view
  var ticking = false;

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }

  /* ---- reveal on entry (independent of the rise engine) ---- */

  var reveals = document.querySelectorAll("[data-reveal]");
  if (reveals.length) {
    if (reduced.matches || !("IntersectionObserver" in window)) {
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

  if (reduced.matches) return;

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

  /* ---- the frame ---- */

  function frame() {
    ticking = false;
    var vh = window.innerHeight || root.clientHeight;

    /* page progress drives the carved axis traveller */
    var doc = document.documentElement;
    var max = doc.scrollHeight - vh;
    root.style.setProperty("--scroll", max > 0 ? clamp(window.scrollY / max).toFixed(4) : "0");

    /* hero: images hold, content lifts away */
    if (hero && !narrow.matches) {
      var span = hero.offsetHeight - vh;
      var hp = span > 0 ? clamp(window.scrollY / span) : 0;

      if (heroContent) {
        heroContent.style.setProperty("--rise", (hp * 210).toFixed(1));
        /* gone before it can collide with the masthead */
        heroContent.style.setProperty("--fade", (1 - clamp(hp / 0.72)).toFixed(3));
      }
      heroImages.forEach(function (img, n) {
        /* the two halves drift at slightly different rates so the
           diptych gains depth without either portrait sliding away */
        img.style.setProperty("--rise", (hp * (n === 0 ? 34 : 46)).toFixed(1));
        img.style.setProperty("--zoom", (1 + hp * 0.038).toFixed(4));
      });
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
  }

  function request() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(frame);
  }

  window.addEventListener("scroll", request, { passive: true });
  window.addEventListener("resize", request, { passive: true });
  frame();

  /* ---- restrained pointer depth, fine pointers only ----
     A few pixels of counter-movement on the hero copy. The portraits
     themselves never move with the pointer: sculpture should not wobble. */

  if (fine.matches && heroContent && !narrow.matches) {
    var px = 0, py = 0, pending = false;
    window.addEventListener("mousemove", function (e) {
      px = (e.clientX / window.innerWidth - 0.5) * 2;
      py = (e.clientY / window.innerHeight - 0.5) * 2;
      if (pending) return;
      pending = true;
      requestAnimationFrame(function () {
        pending = false;
        heroContent.style.setProperty("--tilt-x", (px * -5).toFixed(2) + "px");
        heroContent.style.setProperty("--tilt-y", (py * -3).toFixed(2) + "px");
      });
    }, { passive: true });
  }

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
