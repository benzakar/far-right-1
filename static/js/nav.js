/* Mobile navigation: modal on small screens, plain list above.
 * Focus is trapped while open and restored on close. */
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
