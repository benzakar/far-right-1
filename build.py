#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""مولّد الموقع ديال حزب اليمين المغربي.

بلا أي تبعية خارج المكتبة القياسية ديال بايثون. للتشغيل:

    python3 build.py

المخرجات كتمشي لـ dist/ ويقدر يخدمها أي استضافة ثابتة.
الموقع بالمغربية فقط، من اليمين للشمال.
"""

import hashlib
import html
import json
import os
import shutil
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content.site import (  # noqa: E402
    SITE, UI, NAV, WHO, NEWS_FEATURED, VISION, BUS, MONARCHY,
    ACCOUNTABILITY, FOUNDER, JOIN, DECLARATION, FOOTER, META, PETITION,
    CINEMA,
)
from content.doctrines import DOCTRINES  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
STATIC = os.path.join(ROOT, "static")
EDITOR_CONFIG_PATH = os.path.join(ROOT, "content", "editor.json")


def _load_editor_config():
    try:
        with open(EDITOR_CONFIG_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


EDITOR_CONFIG = _load_editor_config()
EDITOR_SECTIONS = EDITOR_CONFIG.get("sections", {})


def section_config(section_id):
    data = EDITOR_SECTIONS.get(section_id, {})
    return data if isinstance(data, dict) else {}


def section_value(section_id, key, fallback=""):
    value = section_config(section_id).get(key, fallback)
    return fallback if value is None else value


def section_class(section_id, extra=""):
    tone = section_value(section_id, "background", "green")
    tone = tone if tone in ("green", "red") else "green"
    classes = ["bay", "bay--{}back".format(tone)]
    if extra:
        classes.extend(extra.split())
    return " ".join(classes)


def theme_style():
    theme = EDITOR_CONFIG.get("theme", {})
    if not isinstance(theme, dict):
        return ""
    colors = {
        "green": "--green-deep",
        "red": "--section-red",
        "gold": "--gold",
        "panel": "--ivory-0",
        "ink": "--ink",
    }
    declarations = []
    for key, css_var in colors.items():
        value = str(theme.get(key, "")).strip()
        if value.startswith("#") and len(value) in (4, 7):
            declarations.append("{}:{}".format(css_var, value))
    try:
        radius = max(8, min(48, int(theme.get("radius", 28))))
        declarations.append("--panel-radius:{}px".format(radius))
    except (TypeError, ValueError):
        pass
    return ":root{{{}}}".format(";".join(declarations)) if declarations else ""

# فين غادي يتقدم الموقع.
#
# BASE_PATH هو المجلد الفرعي إلا كان. الدومين الخاص كيقدم من الجذر وما
# كيحتاج والو؛ أما موقع GitHub Pages ديال مشروع فكيقدم من /<repo>/
# وخاصو BASE_PATH، وإلا كل مسار مطلق غادي يطيح.
BASE = os.environ.get("BASE_PATH", "").rstrip("/")
if BASE and not BASE.startswith("/"):
    BASE = "/" + BASE
ORIGIN = os.environ.get("SITE_ORIGIN", "https://" + SITE["domain"]).rstrip("/")


def esc(s):
    return html.escape(str(s), quote=True)


def asset(path):
    """مسار مطلق لملف ثابت، مع احترام BASE_PATH."""
    return BASE + path


_stamps = {}


def versioned(path):
    """أصل ثابت مع بصمة المحتوى.

    بلا هادي، المتصفح كيبقى كيخدم النسخة القديمة من CSS و JS من بعد كل
    نشر، حتى يمسح الكاش بيدو. البصمة كتتبدل غير ملي يتبدل الملف.
    """
    if path not in _stamps:
        src = os.path.join(STATIC, path.lstrip("/"))
        try:
            with open(src, "rb") as fh:
                _stamps[path] = hashlib.md5(fh.read()).hexdigest()[:8]
        except OSError:
            _stamps[path] = "0"
    return "{}{}?v={}".format(BASE, path, _stamps[path])


def url(path=""):
    return "{}/{}".format(BASE, path)


# ---------------------------------------------------------------- الهيكل

def head(title, desc, canonical, hero=False, noindex=False):
    critical = [
        "reem-kufi-700-arabic.woff2",
        "zain-400-arabic.woff2",
        "cairo-variable-arabic.woff2",
    ]
    preloads = "\n".join(
        '  <link rel="preload" href="{}" as="font" type="font/woff2" crossorigin>'.format(
            asset("/fonts/" + f))
        for f in critical
    )
    return """<!doctype html>
<html lang="ar" dir="rtl" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>document.documentElement.classList.remove("no-js");</script>
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{origin}{canonical}">
{robots}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:locale" content="ar_MA">
  <meta property="og:url" content="{origin}{canonical}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#F3EDE1">
  <link rel="icon" href="{favicon}" type="image/png" sizes="48x48">
{preloads}
  <link rel="stylesheet" href="{fontcss}">
  <link rel="stylesheet" href="{sitecss}">
  <style>{theme_style}</style>
</head>
<body{hero_attr}>
<a class="skip" href="#main">{skip}</a>
""".format(
        title=esc(title), desc=esc(desc), origin=ORIGIN, canonical=canonical,
        robots='  <meta name="robots" content="noindex, nofollow">\n' if noindex else "",
        favicon=asset("/img/favicon2.png"),
        fontcss=versioned("/css/fonts-ar.css"), sitecss=versioned("/css/site.css"),
        theme_style=theme_style(),
        preloads=preloads, skip=esc(UI["skip"]),
        hero_attr=' data-hero-page' if hero else '',
    )


# Inline so the icons need no extra request and inherit the current colour.
FACEBOOK_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="20" height="20">'
    '<path fill="currentColor" d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 '
    '3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12Z"/>'
    "</svg>")
X_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="18" height="18">'
    '<path fill="currentColor" d="M18.2 2H21l-6.5 7.4L22 22h-6l-4.7-6.2L5.9 22H3l7-8L2 2h6.2l4.3 5.7L18.2 2Zm-1 18h1.7L7.9 3.8H6.1L17.2 20Z"/>'
    "</svg>")
YOUTUBE_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="22" height="22">'
    '<path fill="currentColor" d="M23 12s0-3.2-.4-4.7a2.5 2.5 0 0 0-1.8-1.8C19.3 5 12 5 12 5s-7.3 '
    '0-8.8.5a2.5 2.5 0 0 0-1.8 1.8C1 8.8 1 12 1 12s0 3.2.4 4.7a2.5 2.5 0 0 0 1.8 1.8C4.7 19 12 19 12 '
    '19s7.3 0 8.8-.5a2.5 2.5 0 0 0 1.8-1.8C23 15.2 23 12 23 12ZM9.8 15.1V8.9l6 3.1-6 3.1Z"/>'
    "</svg>")
INSTAGRAM_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" width="20" height="20">'
    '<path fill="currentColor" d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 '
    '1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 '
    '.4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 '
    '15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 '
    '8.8 2.2 12 2.2Zm0 1.8c-3.1 0-3.5 0-4.7.1-.9 0-1.4.2-1.7.3-.4.2-.7.4-1 .7-.3.3-.5.6-.7 1-.1.3-.3.8-.3 1.7-.1 '
    '1.2-.1 1.6-.1 4.7s0 3.5.1 4.7c0 .9.2 1.4.3 1.7.2.4.4.7.7 1 .3.3.6.5 1 .7.3.1.8.3 1.7.3 1.2.1 1.6.1 4.7.1s3.5 '
    '0 4.7-.1c.9 0 1.4-.2 1.7-.3.4-.2.7-.4 1-.7.3-.3.5-.6.7-1 .1-.3.3-.8.3-1.7.1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c0-.9-.2-1.4-.3-1.7-.2-.4-.4-.7-.7-1-.3-.3-.6-.5-1-.7-.3-.1-.8-.3-1.7-.3-1.2-.1-1.6-.1-4.7-.1Zm0 '
    '3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8Zm0 8.1a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4Zm6.2-8.3a1.1 1.1 0 '
    '1 1-2.3 0 1.1 1.1 0 0 1 2.3 0Z"/>'
    "</svg>")


def masthead(active):
    """A landing page, not a site with a menu.

    Other pages are still built and reachable by URL, but nothing links to
    them yet, so a navigation bar would advertise unfinished work. The
    header is reduced to the mark and the tagline.
    """
    return """<header class="masthead masthead--bare" data-masthead>
  <div class="shell masthead__inner">
    <a class="wordmark" href="{home}">
      <img class="wordmark__mark" src="{logo}" alt="{name}" width="120" height="166" loading="eager">
      <span class="wordmark__tagline">{tagline}</span>
    </a>
  </div>
</header>
""".format(home=url(), logo=asset("/img/party-logo.png"),
           name=esc(UI["party_name"]), tagline=esc(SITE["tagline"]))


def footer():
    """No links to pages that are not finished.

    Listing them as plain text says what is coming without sending anyone
    to a page that is still being written.
    """
    pages = [
        "من حنا", "عقائدنا", "رؤيتنا", "الأخبار", "المقالات", "انضم لينا",
        "الملكية والاستمرارية", "حافلة المغرب", "المساءلة والأدلة",
    ]
    coming = "\n        ".join(
        "<li>{}</li>".format(esc(name)) for name in pages)
    legal = "\n        ".join("<li>{}</li>".format(esc(x)) for x in FOOTER["legal"])
    socials = [
        (SITE["facebook"], "فيسبوك", FACEBOOK_ICON),
        (SITE["instagram"], "إنستغرام", INSTAGRAM_ICON),
        (SITE["x"], "إكس", X_ICON),
        (SITE["youtube"], "يوتيوب", YOUTUBE_ICON),
    ]
    social_html = "\n        ".join(
        '<a class="social" href="{href}" rel="noopener noreferrer" target="_blank" '
        'aria-label="{label}">{icon}</a>'.format(href=href, label=esc(label), icon=icon)
        for href, label, icon in socials)

    return """<footer class="footer">
  <div class="shell">
    <div class="footer__top">
      <div class="footer__brand">
        <img class="footer__mark" src="{logo}" alt="{logo_alt}" width="96" height="133" loading="lazy">
        <p class="footer__tagline">{tagline}</p>
        <div class="footer__socials">
        {socials}
        </div>
      </div>
      <div>
        <div class="footer__coming">
          <h2>صفحات فطور التطوير</h2>
          <p class="footer__hint">هاد الصفحات مازال كنخدمو عليها، غادي تتحل وحدة بوحدة.</p>
          <ul class="footer__pages">
        {coming}
          </ul>
        </div>
        <div class="footer__legal">
          <h2>{legal_title}</h2>
          <ul>
        {legal}
          </ul>
        </div>
      </div>
    </div>
    <div class="footer__base">
      <span>{rights}</span>
      <a class="footer__z" href="{z}" aria-label="أرشيف النصوص">Z</a>
    </div>
  </div>
</footer>
<script src="{navjs}" defer></script>
<script src="{motionjs}" defer></script>
</body>
</html>
""".format(logo=asset("/img/party-logo.svg"), logo_alt=esc(UI["logo_alt"]),
           tagline=esc(FOOTER["tagline"]), coming=coming, socials=social_html,
           legal_title=esc(FOOTER["legal_title"]), legal=legal,
           rights=esc(FOOTER["rights"]), z=url("z/"),
           navjs=versioned("/js/nav.js"), motionjs=versioned("/js/motion.js"))


def page(key, active, body, hero=False, override_key=None):
    title, desc = META[key]
    body = apply_page_overrides(override_key or key, body)
    return (head(title, desc, url(active), hero=hero)
            + masthead(active)
            + '<main id="main">\n' + body + "\n</main>\n"
            + footer())


def redirect_page(target, canonical):
    """Keep an old public URL working after its content joins another page."""
    return """<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{origin}{canonical}">
  <title>المؤسس داخل صفحة من حنا — حزب اليمين المغربي</title>
</head>
<body>
  <p>قسم المؤسس ولى داخل صفحة «من حنا». <a href="{target}">دوز ليه من هنا</a>.</p>
</body>
</html>
""".format(target=target, origin=ORIGIN, canonical=canonical)


def crumbs(trail):
    parts = []
    for i, (href, label) in enumerate(trail):
        if i:
            parts.append('<span aria-hidden="true">/</span>')
        parts.append('<a href="{}">{}</a>'.format(href, esc(label)) if href
                     else "<span>{}</span>".format(esc(label)))
    return '<nav class="crumbs" aria-label="مسار التصفح">{}</nav>'.format("".join(parts))


def pagehead(trail, label, title, standfirst=""):
    sf = '<p class="pagehead__standfirst">{}</p>'.format(esc(standfirst)) if standfirst else ""
    return """<section class="pagehead bay--greenback" data-parallax-bg>
  <div class="shell">
    {crumbs}
    <p class="label" style="margin-block-start:1.4rem">{label}</p>
    <h1 class="pagehead__title">{title}</h1>
    {sf}
  </div>
</section>
""".format(crumbs=crumbs(trail), label=esc(label), title=esc(title), sf=sf)


# ------------------------------------------------------------------ الواجهة

def cinema_block():
    """The opening sequence.

    One pinned stage. Everything inside is a pure function of how far the
    stage has been scrolled, so the sequence plays identically forwards
    and backwards and can be stopped anywhere in between.
    """
    def srcset(name):
        return ", ".join(asset("/img/{}-{}.jpg".format(name, w)) + " {}w".format(w)
                         for w in (640, 960, 1280, 1920, 2560, 3840))

    return """<h1 class="vh">{page_h1}</h1>
<section class="cinema" data-cinema>
  <div class="cinema__stage">

    <img class="cinema__bg" data-cine="bg" src="{src}" srcset="{ss}" sizes="100vw"
         width="1280" height="720" alt="{hero_alt}" fetchpriority="high" decoding="async">

    <div class="cinema__dim" data-cine="dim" aria-hidden="true"></div>

    <div class="cinema__scroll-hint" data-cine="hint" aria-hidden="true">
      <span class="cinema__scroll-word">Scroll Down</span>
      <img class="cinema__scroll-arrow" src="{arrow}"
           width="500" height="500" alt="" decoding="async">
    </div>

    <p class="cinema__line" data-cine="line1">{line1}</p>

    <img class="cinema__parties" data-cine="parties" src="{parties}"
         width="1280" height="720" alt="{parties_alt}" loading="eager" decoding="async">

    <p class="cinema__line" data-cine="line2">{line2}</p>

    <img class="cinema__logo" data-cine="logo" src="{logo}"
         width="1280" height="720" alt="{logo_alt}" loading="eager" decoding="async">

    <p class="cinema__slogan" data-cine="slogan">{slogan}</p>

  </div>
</section>
""".format(page_h1=esc("{} — {}".format(UI["party_name"], CINEMA["line_2"])),
           src=asset("/img/hero9-1920.jpg"), ss=srcset("hero9"),
           arrow=asset("/img/arrow.gif"),
           hero_alt=esc(CINEMA["hero_alt"]),
           line1=esc(CINEMA["line_1"]), line2=esc(CINEMA["line_2"]),
           parties=asset("/img/darklogos.png"),
           parties_alt=esc(CINEMA["parties_alt"]),
           logo=asset("/img/party-logo.png"), logo_alt=esc(CINEMA["logo_alt"]),
           slogan=esc(CINEMA["slogan"]))


BUS_SVG = """<svg class="road__bus" viewBox="0 0 80 34" fill="none" aria-hidden="true" focusable="false">
  <path d="M3 26V10a4 4 0 0 1 4-4h49l18 11v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"
        fill="#F3EDE1" stroke="#A8823C" stroke-width="1.2"/>
  <path d="M10 10h13v8H10zM27 10h13v8H27zM44 10h11l9 8H44z" fill="#14503A" opacity=".85"/>
  <circle cx="20" cy="29" r="4" fill="#2A241B" stroke="#A8823C" stroke-width="1"/>
  <circle cx="60" cy="29" r="4" fill="#2A241B" stroke="#A8823C" stroke-width="1"/>
</svg>"""


def bus_block(full=False, backdrop=None):
    stages = []
    for st in BUS["stages"]:
        reqs = "\n        ".join("<li>{}</li>".format(esc(r)) for r in st["requirements"])
        stages.append("""<article class="stage" data-reveal>
      <h3 class="stage__role">{role}</h3>
      <p class="stage__sub">{sub}</p>
      <p>{body}</p>
      <p class="stage__req-label">{req_label}</p>
      <ul>
        {reqs}
      </ul>
    </article>""".format(role=esc(st["role"]), sub=esc(st["subtitle"]),
                         body=esc(st["body"]), req_label=esc(st["requirements_label"]),
                         reqs=reqs))

    closing = "\n      ".join(
        '<p class="declaration__line">{}</p>'.format(esc(l)) for l in BUS["closing"])

    more = ("" if full else
            '<p style="margin-block-start:2.5rem">'
            '<a class="btn btn--ghost" href="{}">قرا القصة كاملة</a></p>'.format(url("bus/")))

    backdrop_class = " bay--{}back".format(backdrop) if backdrop else ""
    backdrop_attr = " data-parallax-bg" if backdrop else ""

    return """<section class="bay bus{backdrop_class}" data-progress{backdrop_attr}>
  <div class="bus__sky" aria-hidden="true"></div>
  <div class="bus__sun" aria-hidden="true"></div>
  <div class="shell bus__inner">
    <p class="label" data-rise="34">{label}</p>
    <h2 class="bay__title" data-rise="52">{title}</h2>
    <p class="bay__lead" data-rise="40">{lead}</p>

    <div class="road" aria-hidden="true">
      <div class="road__line"></div>
      {bus_svg}
    </div>

    <div class="stages">
      {stages}
    </div>

    <div style="margin-block-start:clamp(2.5rem,6vw,4rem);border-block-start:1px solid rgba(243,237,225,.22);padding-block-start:2rem">
      <h3 style="font-size:var(--step-1);margin-block-end:.6rem">{note_title}</h3>
      <p style="color:rgba(243,237,225,.8)">{note_body}</p>
    </div>

    <div class="declaration" style="margin-block-start:clamp(2.5rem,6vw,4rem)">
      {closing}
    </div>
    {more}
  </div>
</section>
""".format(backdrop_class=backdrop_class, backdrop_attr=backdrop_attr,
           label=esc(BUS["label"]), title=esc(BUS["title"]), lead=esc(BUS["lead"]),
           bus_svg=BUS_SVG, stages="\n      ".join(stages),
           note_title=esc(BUS["note_title"]), note_body=esc(BUS["note_body"]),
           closing=closing, more=more)


# ------------------------------------------------------------ الصفحة الرئيسية

def _pillar_grid(items):
    return "\n      ".join(
        """<div class="pillar" data-reveal="{d}">
        <h3>{t}</h3>
        <p>{b}</p>
      </div>""".format(d=i * 55, t=esc(t), b=esc(b))
        for i, (t, b) in enumerate(items))


# Stands in until each section gets its own artwork. Swap per section under
# `images` in content/editor.json, or upload through the editor.
DEFAULT_READER_IMAGE = "/img/from-002.png"


def _image_slot(key, label, compact=False):
    """An intentional empty image plane.

    The visible placeholder keeps the layout finished while the commissioned
    artwork is still being produced. `data-image-slot` is the stable hook used
    when the matching image is uploaded later.
    """
    # Always a real picture. The old ornamental box assumed square, hard-edged
    # artwork and fell apart the moment an image with rounded corners or its
    # own frame was dropped in. Anything without artwork yet borrows the
    # second section's, so replacing one is a straight image swap.
    image_path = EDITOR_CONFIG.get("images", {}).get(key, "") or DEFAULT_READER_IMAGE
    return """<figure class="media-slot media-slot--image{compact}" data-image-slot="{key}">
      <img src="{src}" alt="{label}" loading="lazy" decoding="async">
    </figure>""".format(
        compact=" media-slot--compact" if compact else "",
        key=esc(key), src=asset(str(image_path)), label=esc(label))


def _story_panel(key, image_label, eyebrow, title, body, actions=(), flip=False,
                 panel_id="", level=2, extra=""):
    override = EDITOR_CONFIG.get("content_overrides", {}).get(key, {})
    if isinstance(override, dict):
        eyebrow = override.get("eyebrow", eyebrow)
        title = override.get("title", title)
        body = override.get("body", body)
    if isinstance(body, str):
        body = [body]
    body_html = "\n        ".join(
        '<p class="story-panel__text">{}</p>'.format(esc(p)) for p in body)
    if extra:
        body_html += "\n        " + extra
    links = []
    for href, label, external in actions:
        attrs = ' rel="noopener noreferrer" target="_blank"' if external else ""
        arrow = " ↗" if external else ""
        links.append('<a class="btn btn--outline" href="{}"{}>{}{}</a>'.format(
            href, attrs, esc(label), arrow))
    actions_html = ("\n      <div class=\"story-panel__actions\">{}</div>".format(
        "\n          ".join(links))) if links else ""
    classes = "story-panel story-panel--flip" if flip else "story-panel"
    id_attr = ' id="{}"'.format(esc(panel_id)) if panel_id else ""
    return """<article class="{classes}"{id_attr} data-reveal>
    <div class="story-panel__visual">
      {slot}
    </div>
    <div class="story-panel__copy">
      <p class="story-panel__eyebrow">{eyebrow}</p>
      <h{level} class="story-panel__title">{title}</h{level}>
      <div class="story-panel__body">
        {body}
      </div>{actions}
    </div>
  </article>""".format(
        classes=classes, id_attr=id_attr, slot=_image_slot(key, image_label),
        eyebrow=esc(eyebrow), level=level, title=esc(title), body=body_html,
        actions=actions_html)




def policy_reader(key, image_label, blocks, aria, actions=(), tweet_id=None,
                  image=None):
    """The reading treatment used by the second section, made reusable.

    A framed visual beside a bounded, independently scrollable passage with a
    fade and live progress. This is the house style for every prose section;
    `_story_panel` remains only for short card-like blocks.

    `blocks` is a list of strings (paragraphs) or ("h3", text) pairs. When no
    artwork exists for `key` yet, the visual falls back to the same labelled
    placeholder the rest of the site uses, so the geometry is identical and
    the image can be dropped in later without touching the layout.
    """
    # Deliberately does NOT read `content_overrides`. Those entries are the
    # one-paragraph defaults snapshotted for the old story panels, and they
    # would silently truncate a reader back to a single block. Text here is
    # editable through the click editor's per-element `data-edit-id` path,
    # which covers every paragraph without a parallel copy of the content.
    parts = []
    for block in blocks:
        if isinstance(block, (list, tuple)) and len(block) == 2:
            tag, text = block
        else:
            tag, text = "p", block
        if not str(text).strip():
            continue
        parts.append("<{tag}>{text}</{tag}>".format(tag=tag, text=esc(text)))
    body_html = "\n          ".join(parts)

    # Always a real image, never the ornamental placeholder box. The box
    # assumed a square, hard-edged picture and broke as soon as artwork with
    # rounded corners or its own frame was dropped in. Sections without their
    # own artwork yet borrow the second section's, so replacing one is a
    # straight image swap with nothing else to adjust.
    configured = (image
                  or EDITOR_CONFIG.get("images", {}).get(key, "")
                  or DEFAULT_READER_IMAGE)
    visual = """<figure class="policy-reader__visual">
      <img class="policy-reader__image" src="{src}" width="1000" height="1000"
           alt="{label}" loading="lazy" decoding="async">
    </figure>""".format(src=asset(str(configured)), label=esc(image_label))

    links = []
    for href, label, external in actions:
        attrs = ' rel="noopener noreferrer" target="_blank"' if external else ""
        arrow = " ↗" if external else ""
        links.append('<a class="btn btn--outline" href="{}"{}>{}{}</a>'.format(
            href, attrs, esc(label), arrow))
    actions_html = ('\n    <div class="policy-reader__actions">{}</div>'.format(
        "\n      ".join(links))) if links else ""

    return """<div class="policy-reader" data-reveal>
    {visual}
    <div class="policy-pane" data-text-pane>
      <div class="policy-pane__window">
        <div class="policy-pane__scroll" aria-label="{aria}">
          {body}
        </div>
        <div class="policy-pane__fade" aria-hidden="true"></div>
      </div>
      <footer class="policy-pane__foot">
        <span>قرا النص</span>
        <span class="policy-pane__progress" aria-hidden="true"><i></i></span>
        <span data-pane-progress>0%</span>
      </footer>
    </div>{actions}
    {tweet}
  </div>""".format(visual=visual, aria=esc(aria), body=body_html,
                   actions=actions_html,
                   tweet=section_tweet(tweet_id) if tweet_id else "")


def section_intro(section_id, label, title, lead=""):
    label = section_value(section_id, "label", label)
    title = section_value(section_id, "title", title)
    lead = section_value(section_id, "lead", lead)
    quote = str(section_value(section_id, "quote", "")).strip()
    bits = []
    if label:
        bits.append('<p class="label" data-rise="30">{}</p>'.format(esc(label)))
    if title:
        bits.append('<h2 class="bay__title" data-rise="46">{}</h2>'.format(esc(title)))
    if lead:
        bits.append('<p class="bay__lead" data-rise="36">{}</p>'.format(esc(lead)))
    if quote:
        bits.append('<blockquote class="section-quote">{}</blockquote>'.format(esc(quote)))
    return "\n    ".join(bits).strip()


X_HANDLE = "@benzakarMorocco"
X_ACCOUNT = "https://x.com/benzakarMorocco"


def _tweet_card(tweet):
    if not isinstance(tweet, dict) or not str(tweet.get("text", "")).strip():
        return ""
    avatar = tweet.get("avatar") or "/img/ben-zakar-x-profile.jpg"
    avatar_html = ('<img class="policy-tweet__avatar" src="{}" width="96" height="96" alt="">'
                   .format(asset(str(avatar))))
    # The card always links to the account itself, never a per-post URL. A
    # status link rots the moment a post is edited or deleted, and every card
    # here is the party's own voice, so the account is the honest destination.
    return """<article class="policy-tweet section-tweet" dir="rtl" aria-label="تغريدة">
      <header class="policy-tweet__head">
        <div class="policy-tweet__identity">{avatar}<span><strong>{name}</strong>
          <span class="policy-tweet__handle">{handle}</span></span></div>
        <span class="policy-tweet__mark" aria-hidden="true">𝕏</span>
      </header>
      <p class="policy-tweet__copy">{text}</p>
      <footer class="policy-tweet__foot"><time>{date}</time>
        <a href="{account}" target="_blank" rel="noopener noreferrer">شوف الحساب على X
          <span aria-hidden="true">↗</span></a></footer>
    </article>""".format(
        avatar=avatar_html, name=esc(tweet.get("name") or "Ben Zakar"),
        handle=esc(tweet.get("handle") or X_HANDLE),
        text=esc(tweet.get("text", "")), date=esc(tweet.get("date", "")),
        account=X_ACCOUNT).strip()


def section_tweets(section_id):
    """Every card configured for a section.

    Accepts a `tweets` list, and still honours the older single `tweet`
    object so existing configuration keeps working untouched.
    """
    config = section_config(section_id)
    cards = []

    single = config.get("tweet")
    if isinstance(single, dict) and single.get("enabled"):
        cards.append(_tweet_card(single))

    listed = config.get("tweets")
    if isinstance(listed, list):
        for tweet in listed:
            if isinstance(tweet, dict) and tweet.get("enabled", True):
                cards.append(_tweet_card(tweet))

    return "\n    ".join(c for c in cards if c)


# kept so existing call sites read naturally
section_tweet = section_tweets


def clean_markup(markup):
    return "\n".join(line.rstrip() for line in markup.splitlines())


EDITABLE_TAG_RE = re.compile(r"<(h[1-3]|p|blockquote|a|img|article|section|div)\b([^>]*)>", re.I)


VOID_TAGS = {"img"}
TEXT_TAGS = {"h1", "h2", "h3", "p", "blockquote", "a"}


def _find_element(markup, edit_id):
    """Span of the whole element carrying `edit_id`, nesting included.

    Regex alone cannot do this: `div` and `section` nest inside themselves,
    so a lazy match would stop at the first inner `</div>`. Walking the tag
    stream and counting depth is the only way to get the real end.
    """
    opener = re.search(r'<([a-z0-9]+)\b[^>]*data-edit-id="{}"[^>]*>'.format(
        re.escape(edit_id)), markup, re.I)
    if not opener:
        return None
    tag = opener.group(1).lower()
    if tag in VOID_TAGS:
        return opener.start(), opener.end(), tag, opener.group(0), ""

    depth, pos = 1, opener.end()
    pattern = re.compile(r'<(/?){}\b[^>]*>'.format(re.escape(tag)), re.I)
    while depth and pos < len(markup):
        m = pattern.search(markup, pos)
        if not m:
            return None
        depth += -1 if m.group(1) else 1
        pos = m.end()
        if not depth:
            return (opener.start(), pos, tag, opener.group(0),
                    markup[opener.end():m.start()])
    return None


def _retag(open_tag, old, new):
    return re.sub(r'^<{}\b'.format(re.escape(old)), '<' + new, open_tag, flags=re.I)


def apply_page_overrides(page_key, markup):
    """Apply click-editor changes to generated markup using stable edit IDs.

    Supported per element: `text` (blank lines split it into siblings),
    `tag` (turn a paragraph into a heading or back), `removed`, plus the
    plain attribute overrides `src`, `href`, `class` and `style`.
    """
    overrides = EDITOR_CONFIG.get("page_overrides", {}).get(page_key, {})
    if not isinstance(overrides, dict):
        overrides = {}
    counters = {}

    def decorate(match):
        tag, attrs = match.group(1).lower(), match.group(2)
        counters[tag] = counters.get(tag, 0) + 1
        edit_id = "{}-{}".format(tag, counters[tag])
        op = overrides.get(edit_id, {})
        attrs = re.sub(r'\sdata-edit-id="[^"]*"', "", attrs)

        def set_attr(text, name, value):
            text = re.sub(r'\s{}="[^"]*"'.format(re.escape(name)), "", text)
            return text + ' {}="{}"'.format(name, esc(value)) if value else text

        if isinstance(op, dict):
            for name in ("src", "href", "class", "style"):
                if name in op:
                    attrs = set_attr(attrs, name, str(op[name]))
        return '<{}{} data-edit-id="{}">'.format(tag, attrs, edit_id)

    # Ids are positional, so they are assigned once, before any structural
    # rewrite. Paragraphs added by a split therefore carry derived ids and
    # never shift the numbering of anything after them.
    markup = EDITABLE_TAG_RE.sub(decorate, markup)

    for edit_id, op in overrides.items():
        if not isinstance(op, dict):
            continue
        if not any(k in op for k in ("removed", "tag", "text", "after")):
            continue
        found = _find_element(markup, edit_id)
        if not found:
            continue
        start, end, tag, open_tag, inner = found

        if op.get("removed"):
            markup = markup[:start] + markup[end:]
            continue

        new_tag = str(op.get("tag") or tag).lower()
        if new_tag not in TEXT_TAGS | {tag}:
            new_tag = tag

        pieces = []

        if "text" in op and tag in TEXT_TAGS:
            text = str(op["text"]).strip()
            if not text and not op.get("after"):
                markup = markup[:start] + markup[end:]
                continue
            if text:
                pieces.append("{}{}</{}>".format(
                    _retag(open_tag, tag, new_tag), esc(text), new_tag))
        elif new_tag != tag:
            pieces.append(_retag(open_tag, tag, new_tag) + inner + "</{}>".format(new_tag))
        elif op.get("after"):
            pieces.append(markup[start:end])
        else:
            continue

        # Blocks added underneath this one. They carry ids derived from their
        # anchor, so inserting never renumbers the positional ids that
        # everything else is addressed by.
        for i, block in enumerate(op.get("after") or []):
            if not isinstance(block, dict):
                continue
            body = str(block.get("text", "")).strip()
            if not body:
                continue
            btag = str(block.get("tag", "p")).lower()
            if btag not in TEXT_TAGS:
                btag = "p"
            style = str(block.get("style", "")).strip()
            pieces.append('<{tag}{style} data-edit-id="{eid}-add{n}">{text}</{tag}>'.format(
                tag=btag, style=' style="{}"'.format(esc(style)) if style else "",
                eid=edit_id, n=i + 1, text=esc(body)))

        markup = markup[:start] + "\n".join(pieces) + markup[end:]

    return markup


def _doctrine_cards(doctrines):
    cards = []
    for i, d_ in enumerate(doctrines):
        override = EDITOR_CONFIG.get("content_overrides", {}).get("doctrine-" + d_["slug"], {})
        title = override.get("title", d_["name"]) if isinstance(override, dict) else d_["name"]
        body = override.get("body", [d_["summary"]]) if isinstance(override, dict) else [d_["summary"]]
        if isinstance(body, str):
            body = [body]
        summary = body[0] if body else d_["summary"]
        cards.append(
        """<article class="doctrine-card" data-reveal="{delay}">
        {slot}
        <div class="doctrine-card__copy">
          <span class="doctrine-card__index">عقيدة {idx:02d}</span>
          <h3 class="doctrine-card__title">{name}</h3>
          <p class="doctrine-card__summary">{summary}</p>
          <a class="doctrine-card__link" href="{href}">{more}</a>
        </div>
      </article>""".format(
            delay=(i % 2) * 70,
            slot=_image_slot("doctrine-" + d_["slug"], d_["name"], compact=True),
            idx=d_["order"], name=esc(title), summary=esc(summary),
            href=url("doctrines/{}/".format(d_["slug"])), more=esc(UI["read_more"]))
        )
    return "\n      ".join(cards)


def _news_slider():
    """Images only — the owner designs each news card and uploads it.

    Slides come from `news_slides` in content/editor.json so they can be
    added and reordered from the editor without touching the build.
    """
    slides = EDITOR_CONFIG.get("news_slides", [])
    if not isinstance(slides, list) or not slides:
        slides = [{"image": DEFAULT_READER_IMAGE, "alt": "خبر"}]

    items = []
    for i, slide in enumerate(slides):
        if not isinstance(slide, dict):
            continue
        src = str(slide.get("image", "")).strip() or DEFAULT_READER_IMAGE
        alt = str(slide.get("alt", "")).strip() or "صورة خبر"
        link = str(slide.get("link", "")).strip()
        picture = """<img class="news-slide__image" src="{src}" alt="{alt}"
             loading="lazy" decoding="async">""".format(src=asset(src), alt=esc(alt))
        if link:
            picture = '<a href="{}" class="news-slide__link">{}</a>'.format(esc(link), picture)
        items.append("""<article class="news-slide" role="group"
             aria-roledescription="خبر" aria-label="{n} من {total}">
        {picture}
      </article>""".format(n=i + 1, total=len(slides), picture=picture))

    return """<div class="slider slider--news" data-slider>
      <button class="slider__arrow slider__arrow--prev" type="button"
              data-slide="prev" aria-label="الخبر اللي قبل">
        <span aria-hidden="true">‹</span>
      </button>
      <div class="slider__track" data-slider-track tabindex="0"
           role="region" aria-label="الأخبار">
        {items}
      </div>
      <button class="slider__arrow slider__arrow--next" type="button"
              data-slide="next" aria-label="الخبر اللي من بعد">
        <span aria-hidden="true">›</span>
      </button>
      <p class="slider__count" data-slider-count aria-live="polite">1 / {total}</p>
    </div>""".format(items="\n        ".join(items), total=len(items))


def _doctrine_slider(doctrines):
    """One doctrine at a time, with an arrow on each side.

    The track is a scroll-snap row rather than a transform carousel, so it
    still works with no JavaScript, keeps native swipe on touch, and stays
    keyboard reachable. The arrows only nudge the same scroll container.
    """
    slides = []
    for i, d_ in enumerate(doctrines):
        override = EDITOR_CONFIG.get("content_overrides", {}).get("doctrine-" + d_["slug"], {})
        name = override.get("title", d_["name"]) if isinstance(override, dict) else d_["name"]
        body = override.get("body", [d_["summary"]]) if isinstance(override, dict) else [d_["summary"]]
        if isinstance(body, str):
            body = [body]
        slides.append("""<article class="doctrine-slide" id="doctrine-slide-{n}"
             role="group" aria-roledescription="عقيدة" aria-label="{n} من {total}">
        {slot}
        <div class="doctrine-slide__copy">
          <span class="doctrine-slide__index">عقيدة {idx:02d}</span>
          <h3 class="doctrine-slide__title">{name}</h3>
          <p class="doctrine-slide__summary">{summary}</p>
          <a class="doctrine-slide__link" href="{href}">{more}</a>
        </div>
      </article>""".format(
            n=i + 1, total=len(doctrines),
            slot=_image_slot("doctrine-" + d_["slug"], d_["name"], compact=True),
            idx=d_["order"], name=esc(name),
            summary=esc(body[0] if body else d_["summary"]),
            href=url("doctrines/{}/".format(d_["slug"])), more=esc(UI["read_more"])))

    return """<div class="slider" data-slider>
      <button class="slider__arrow slider__arrow--prev" type="button"
              data-slide="prev" aria-label="العقيدة اللي قبل">
        <span aria-hidden="true">‹</span>
      </button>
      <div class="slider__track" data-slider-track tabindex="0"
           role="region" aria-label="العقائد">
        {slides}
      </div>
      <button class="slider__arrow slider__arrow--next" type="button"
              data-slide="next" aria-label="العقيدة اللي من بعد">
        <span aria-hidden="true">›</span>
      </button>
      <p class="slider__count" data-slider-count aria-live="polite">1 / {total}</p>
    </div>""".format(slides="\n        ".join(slides), total=len(doctrines))


def petition_block(compact=False, level=3):
    """The petition card.

    `compact` is the homepage variant. `level` is the heading level: on
    the homepage the card sits under a section h2 so it is an h3; on the
    join page it is the first thing after the page h1, so it is an h2.
    """
    # Same shape as every other section: a visual beside a panel, with the
    # call to action living inside the panel rather than floating under it.
    image = EDITOR_CONFIG.get("images", {}).get("petition", "") or DEFAULT_READER_IMAGE
    paras = "\n          ".join("<p>{}</p>".format(esc(p)) for p in PETITION["body"])
    return """<div class="policy-reader petition-reader" data-reveal>
    <figure class="policy-reader__visual">
      <img class="policy-reader__image" src="{image}" width="1000" height="1000"
           alt="{title}" loading="lazy" decoding="async">
    </figure>
    <div class="policy-pane">
      <div class="policy-pane__window policy-pane__window--free">
        <div class="policy-pane__scroll policy-pane__scroll--free">
          <p class="petition__kicker">{kicker} \u00b7 {host}</p>
          <h{lvl} class="petition__title">{title}</h{lvl}>
          <p class="petition__lead">{lead}</p>
          {paras}
          <p class="petition__cta">
            <a class="btn btn--primary" href="{href}" rel="noopener noreferrer" target="_blank">{cta} \u2197</a>
          </p>
          <p class="petition__note">{note}</p>
        </div>
      </div>
    </div>
  </div>""".format(lvl=level, image=asset(str(image)),
                   kicker=esc(PETITION["kicker"]), host=esc(PETITION["host"]),
                   title=esc(PETITION["title"]), lead=esc(PETITION["lead"]),
                   paras=paras, href=SITE["petition"], cta=esc(PETITION["cta"]),
                   note=esc(PETITION["note"]))


def z_page():
    """Everything the site holds, in one place, for lifting into the page.

    Reached only from a quiet link in the footer. It is a working surface,
    not a public page: no navigation points at it, it asks not to be
    indexed, and it stays out of the sitemap. Because it is generated from
    the same content modules as the site, it cannot drift out of date.
    """
    blocks = []

    def block(heading, paragraphs):
        items = [p for p in paragraphs if str(p).strip()]
        if not items:
            return
        blocks.append("""<article class="z-block">
      <h2 class="z-block__title">{heading}</h2>
      {body}
    </article>""".format(
            heading=esc(heading),
            body="\n      ".join("<p>{}</p>".format(esc(p)) for p in items)))

    block("الواجهة — الجمل", [CINEMA["line_1"], CINEMA["line_2"], CINEMA["slogan"]])
    block(WHO["title"], [WHO["lead"]] +
          ["{} — {}".format(t, b) for t, b in WHO["distinctions"]])
    block(VISION["title"], [VISION["lead"]] +
          ["{} — {}".format(t, b) for t, b in VISION["pillars"]])
    block(VISION["plan_title"], [VISION["plan_lead"]] + list(VISION["plan_body"]))
    block(VISION["example_title"], [VISION["example_body"]])
    block(NEWS_FEATURED["title"],
          [NEWS_FEATURED["standfirst"]] + list(NEWS_FEATURED["body"]) +
          [NEWS_FEATURED["status_note"]])
    block(BUS["title"], [BUS["lead"]] +
          ["{} — {} — {}".format(s["role"], s["subtitle"], s["body"])
           for s in BUS["stages"]] +
          [BUS["note_body"]] + list(BUS["closing"]))
    block(MONARCHY["title"], list(MONARCHY["body"]) +
          [MONARCHY["questions_lead"]] + list(MONARCHY["questions"]) +
          [MONARCHY["warning_lead"]] +
          ["{}: {}".format(c, n) for c, n in MONARCHY["examples"]] +
          [MONARCHY["warning_close"]])
    block(ACCOUNTABILITY["title"],
          [ACCOUNTABILITY["summary"], ACCOUNTABILITY["disclaimer"]] +
          ["{}: {}".format(r, b) for r, b in ACCOUNTABILITY["ladder"]] +
          list(ACCOUNTABILITY["body"]) +
          [ACCOUNTABILITY["framework_lead"]] +
          list(ACCOUNTABILITY["framework_questions"]) +
          list(ACCOUNTABILITY["protection_body"]) +
          [ACCOUNTABILITY["closing"]])
    block(FOUNDER["title"], [FOUNDER["standfirst"]] + list(FOUNDER["message"]))
    block(JOIN["title"], [JOIN["lead"]] +
          ["{} — {}".format(t, b) for t, b in JOIN["paths"]] +
          [JOIN["how_body"], JOIN["contact_note"]])
    block(PETITION["title"], [PETITION["lead"]] + list(PETITION["body"]))
    block("الإعلان الأخير", list(DECLARATION["lines"]))

    for d in DOCTRINES:
        block("{:02d}. {}".format(d["order"], d["name"]),
              [d["declaration"], d["summary"], d["slogan"], d["intro"],
               d["problem"], d["why_failed"], d["belief"]] +
              list(d["solution"]) + list(d["measures"]) +
              [d["citizens"], d["beyond"], d["commitment"]])

    body = """<section class="bay bay--greenback" data-parallax-bg>
  <div class="shell">
    <p class="label">الأرشيف</p>
    <h1 class="bay__title">كل النصوص فبلاصة وحدة</h1>
    <p class="bay__lead">هاد الصفحة ماشي للزوار. فيها كل النصوص ديال الموقع باش
      تقدر تقلب على شي حاجة وتنقلها للصفحة الرئيسية. ما كتبانش فحتى قائمة.</p>
    <div class="z-list">
    {blocks}
    </div>
  </div>
</section>""".format(blocks="\n    ".join(blocks))

    return (head("الأرشيف — كل النصوص", "أرشيف داخلي لنصوص الموقع.",
                 url("z/"), noindex=True)
            + masthead("")
            + '<main id="main">\n' + body + "\n</main>\n"
            + footer())


def home():
    dec_lines = "\n      ".join(
        '<p class="declaration__line">{}</p>'.format(esc(l))
        for l in DECLARATION["lines"])

    bronx = next(d for d in DOCTRINES if d["slug"] == "bronx")
    lalla = next(d for d in DOCTRINES if d["slug"] == "lalla-khadija")
    remaining_doctrines = [
        d for d in DOCTRINES if d["slug"] not in ("bronx", "lalla-khadija")
    ]




    two_speeds_reader = """<div class="policy-reader" data-reveal>
    <figure class="policy-reader__visual">
      <img class="policy-reader__image" src="{image}" width="1000" height="1000"
           alt="قصاصة خبر على إلغاء الساعة الإضافية فالمغرب من بعد صيف 2026"
           loading="lazy" decoding="async">
    </figure>
    <div class="policy-pane" data-text-pane>
      <div class="policy-pane__window">
        <div class="policy-pane__scroll" aria-label="علاش المغرب محتاج دستور جديد">
          <p>{p2}</p>
          <p>{p3}</p>
          <h3>{subtitle}</h3>
          <p>{p4}</p>
          <p>{p5}</p>
          <p>{p6}</p>
        </div>
        <div class="policy-pane__fade" aria-hidden="true"></div>
      </div>
      <footer class="policy-pane__foot">
        <span>قرا النص</span>
        <span class="policy-pane__progress" aria-hidden="true"><i></i></span>
        <span data-pane-progress>0%</span>
      </footer>
    </div>
    {tweet}
  </div>""".format(
        image=asset(str(section_value("two-speeds-plans", "image", "/img/from-002.png"))),
        p2=esc("دستور 2011 خرّج على البلاد، وأحسن مثال هو مطالبة المواطنين بإلغاء الساعة الإضافية. رغم الوقفات الاحتجاجية والعريضة اللي وقّعها عشرات الآلاف من المغاربة، والمشاكل الصحية اللي عاناو منها المغاربة وأطفالهم، عطى الدستور لذاك الانتهازي ديال أخنوش السلطة باش يلغي الساعة الإضافية فقط من أجل الانتخابات، ماشي من أجل المغاربة."),
        p3=esc("أملنا فـ ولد سيدنا أعزّه الله، وفالدستور اللي الحزب موجد ليه؛ الدستور اللي غادي يحل كاع المشاكل، منها: مشكل الهجرة، والصحة، والتعليم، واللي غادي يهني ولد سيدنا من بنكيران وأخنوش ديال المستقبل."),
        subtitle=esc("علاش دستور 2011 ما صالحش من بعد المونديال؟"),
        p4=esc("زيادة على أن التغيير سنة الحياة، وأن العالم غادي بواحد السرعة كبيرة خاصها دستور خاص، وزيادة على هاد الأسباب، المغاربة كلهم سمعو من بنكيران كيفاش سيدنا كان كيهدر معاه على البلوكاج الحكومي."),
        p5=esc("سيدنا عيا مع حكومات الأحزاب، وعيا ما ينبه ويوجّه فالخطابات ديالو."),
        p6=esc("حنا جايين باش ولد سيدنا يلقى حزب كيهنيه من صداع المناورات السياسية، ومن أي بلوكاج حكومي مستقبلي. الحزب هو مشروع مغربي، داعم للملكية، رأسمالي ومنتج، كيبدا من الحل، ماشي من المنصب؛ بمعنى كنبينو للمغاربة الحل قبل ما نطلبو منهم المنصب."),
        tweet=section_tweet("two-speeds-plans"),
    )

    # Concrete proposals lead the homepage. The Bus remains available later as
    # a summary metaphor, after visitors understand Plan A/B and see examples.
    parts = [cinema_block()]

    parts.append("""<section class="{classes}" id="two-speeds-plans" data-parallax-bg>
  <div class="shell">
    {intro}
    {reader}
  </div>
</section>""".format(
        classes=section_class("two-speeds-plans"),
        intro=section_intro("two-speeds-plans", "5 سنين ديال بنكيران، و5 ديال العثماني، و5 ديال أخنوش، وفالأخير: كارثة سبتة.", "باش نقادو مغرب السرعتين، خاصنا مغرب الخطتين"),
        reader=two_speeds_reader,
    ))

    parts.append("""<section class="{classes}" id="plan-a-b" data-parallax-bg>
  <div class="shell">
    {intro}
    {reader}
  </div>
</section>""".format(
        classes=section_class("plan-a-b"),
        intro=section_intro("plan-a-b", "من هنا كتبدا الفكرة", "خطة ألف وخطة باء", "خطة ألف كتوجد المغرب للمسار المتوقع. خطة باء كتوجد المغرب للي ما كانش فالحساب."),
        reader=policy_reader(
            "section-vision", "خطة ألف وخطة باء",
            [VISION["plan_lead"]] + list(VISION["plan_body"]) + [
                ("h3", VISION["example_title"]),
                VISION["example_body"],
            ],
            aria="خطة ألف وخطة باء",
            actions=[(url("vision/"), "شوف الرؤية كاملة", False)],
            tweet_id="plan-a-b")))

    parts.append("""<section class="{classes}" id="examples" data-parallax-bg>
  <div class="shell">
    {intro}
    {reader}
    <div class="status" data-reveal>
      <span class="status__tag">اللي جاي</span>
      <p>وهادي غير البداية. عقائد ومشاريع أخرى كيبانو لتحت، وأخرى غادي تزيد من بعد.</p>
    </div>
  </div>
</section>""".format(
        classes=section_class("examples"),
        intro=section_intro("examples", "من الفكرة للمشروع", "ثلاثة أمثلة كيبينو كيفاش كنفكرو", "ماشي شعارات عامة: كل مثال كيبدا من مشكل باين، وكيقترح تصميم يمكن يتجرب ويتقاس."),
        reader=policy_reader(
            "section-bus", "حافلة المغرب",
            [item for stage in BUS["stages"] for item in (
                ("h3", stage["role"] + " — " + stage["subtitle"]),
                stage["body"],
            )] + [("h3", BUS["note_title"]), BUS["note_body"]],
            aria=BUS["title"],
            tweet_id="examples")))

    parts.append("""<section class="{classes}" id="latest-news" data-parallax-bg>
  <div class="shell">
    {intro}
    {reader}
  </div>
</section>""".format(
        classes=section_class("latest-news"),
        intro=section_intro("latest-news", "آخر المستجدات", "شنو واقع دابا", "كل خبر مصمم بوحدو. زيد ولا بدّل الصور من المحرر."),
        reader=_news_slider() + section_tweet("latest-news")))

    parts.append("""<section class="{classes}" id="about" data-parallax-bg>
  <div class="shell">
    {intro}
    {reader}
  </div>
</section>""".format(
        classes=section_class("about"),
        intro=section_intro("about", "الموقف والهوية", "حنا شكون، وشنو كيميزنا", "البراركية، هوية الحزب، والمؤسس مجموعين هنا بلا ما يتفرّقو على الزائر."),
        reader=policy_reader(
            "about-identity", "هوية الحزب",
            [
                ("h3", WHO["title"]), WHO["lead"],
                ("h3", MONARCHY["title"]), MONARCHY["body"][1], MONARCHY["body"][3],
                ("h3", FOUNDER["name"]), FOUNDER["standfirst"], FOUNDER["message"][5],
            ],
            aria="حنا شكون، وشنو كيميزنا",
            actions=[
                (url("about/"), "تعرف علينا بلا لف ودوران", False),
                (url("monarchy/"), UI["more"], False),
                (SITE["youtube"], FOUNDER["youtube_label"], True),
            ],
            tweet_id="about")))

    parts.append("""<section class="{classes}" id="doctrines" data-parallax-bg>
  <div class="shell">
    {intro}
    {slider}
    {tweet}
  </div>
</section>""".format(classes=section_class("doctrines"), intro=section_intro("doctrines", "باقي العقائد", "الفكرة فالخلاصة، والتفاصيل اختيارية", "شفتي البرونكس ولالة خديجة. هنا باقي العقائد وحدة وحدة."), slider=_doctrine_slider(remaining_doctrines), tweet=section_tweet("doctrines")))

    # The Night/Day driver passage now lives in the examples section above,
    # so this section would only repeat it.

    parts.append("""<section class="{classes}" id="accountability" data-parallax-bg>
  <div class="shell">
    {intro}
    {reader}
  </div>
</section>""".format(
        classes=section_class("accountability"),
        intro=section_intro("accountability", "كيفاش غادي تحاسبونا", "القياس قبل الثقة", "الفرق ماشي فالنوايا. الفرق فالحل، والتجربة، والنتيجة اللي كتتنشر."),
        reader=policy_reader(
            "section-accountability", "المساءلة والنتائج",
            [
                ("h3", ACCOUNTABILITY["title"]), ACCOUNTABILITY["summary"],
                ("h3", "شنو كيميزنا"),
            ] + [t for t, _ in WHO["distinctions"]] + [
                ("h3", ACCOUNTABILITY["ladder_title"]),
            ] + ["{}: {}".format(rank, body)
                 for rank, body in ACCOUNTABILITY["ladder"]] + [
                ACCOUNTABILITY["disclaimer"],
            ],
            aria=ACCOUNTABILITY["title"],
            actions=[(url("accountability/"), UI["more"], False)],
            tweet_id="accountability")))

    parts.append("""<section class="{classes}" id="join" data-parallax-bg>
  <div class="shell">
    {intro}
    {reader}
    {petition}
  </div>
</section>""".format(
        classes=section_class("join"),
        intro=section_intro("join", JOIN["label"], JOIN["title"], JOIN["lead"]),
        reader=policy_reader(
            "section-join", "الحركة والبنّايين",
            [
                ("h3", "طرق المساهمة"),
                "الانضمام كيبدا من الخدمة، ماشي من الورق. هاك الطرق اللي يقدر أي مغربي "
                "يساهم بيها من دابا.",
            ] + [
                "{} — {}".format(title, body) for title, body in JOIN["paths"]
            ] + [
                ("h3", "المجموعة ديالنا فـ فيسبوك"),
                "حتى فاش ما تحلاتش العضوية الرسمية، المجموعة فـ فيسبوك هي البلاصة اللي "
                "كيتلاقاو فيها اللي باغين يساهمو: تطرح فكرة، تناقش مشكل، ولا تلقى ناس "
                "خدامين على نفس الملف. هادي هي العضوية الافتراضية دابا.",
                ("h3", JOIN["how_title"]), JOIN["how_body"],
                ("h3", JOIN["contact_title"]), JOIN["contact_note"],
            ],
            aria=JOIN["title"],
            actions=[(SITE["facebook"], "دخل للمجموعة ديال فيسبوك", True)],
            tweet_id="join"),
        petition=petition_block(compact=True)))

    parts.append("""<section class="{classes}" id="declaration" data-parallax-bg>
  <div class="shell declaration">
    {intro}
    {lines}
    <a class="btn btn--primary" href="{href}">{cta}</a>
    {tweet}
  </div>
</section>""".format(classes=section_class("declaration", "bay--deep"), intro=section_intro("declaration", "", "", ""), lines=dec_lines, href=url("join/"),
                     cta=esc(DECLARATION["cta"]), tweet=section_tweet("declaration")))

    return page("home", "", clean_markup("\n".join(parts)), hero=True)


# ------------------------------------------------------------ باقي الصفحات

IDENTITY = [
    "وطني مغربي: المغرب أولاً.",
    "ملكي، مع التحديث والإصلاح العملي.",
    "رأسمالي منتج، ضد الخليط المخربق بين الرأسمالية والاشتراكية.",
    "يميني سياسياً، وغير ديني.",
    "كيخدم بالهندسة والنماذج والحلول اللي كتقاس.",
    "متصل بمغاربة العالم وبالخبرة الدولية.",
    "كيركز على الكرامة والفرص والهجرة والأمن ومغرب ما بعد 2030.",
]

NAMING_NOTE = (
    "الاسم الرسمي ديال المشروع هو «حزب اليمين المغربي». فمرحلة التعريف الإعلامي "
    "تستعملو صيغ أكثر حدة، ولكن هادوك ماشي هما التعريف الرسمي ديال الحزب. حنا "
    "كنقدمو راسنا بحال يمين مغربي وطني منتج حديث."
)

def about_page():
    rows = "\n    ".join(
        """<div class="ledger__row" data-reveal="{d}">
      <p class="ledger__term">{t}</p>
      <p class="ledger__def">{b}</p>
    </div>""".format(d=i * 70, t=esc(t), b=esc(b))
        for i, (t, b) in enumerate(WHO["distinctions"]))

    body = pagehead([(url(), UI["home"]), (None, WHO["label"])],
                    WHO["label"], WHO["title"], WHO["lead"])

    identity = """<ul class="story-panel__points story-panel__points--roomy">
          {items}
        </ul>""".format(items="\n          ".join(
            "<li>{}</li>".format(esc(item)) for item in IDENTITY))

    about_story = "\n".join([
        _story_panel(
            "about-identity", "هوية حزب اليمين المغربي", "هوية الحزب",
            "يمين مغربي وطني منتج حديث", [NAMING_NOTE], extra=identity,
        ),
        _story_panel(
            "about-founder", "عبدالله بن زكار", FOUNDER["label"], FOUNDER["name"],
            [FOUNDER["message"][0], FOUNDER["message"][1], FOUNDER["message"][2],
             FOUNDER["message"][5]],
            actions=[(SITE["youtube"], FOUNDER["youtube_label"], True)],
            flip=True, panel_id="founder",
        ),
    ])

    vision_story = _story_panel(
        "section-vision", "خطة ألف وخطة باء", VISION["label"], VISION["plan_title"],
        [VISION["plan_lead"]],
        actions=[(url("vision/"), "الرؤية كاملة", False)],
    )

    body += """<section class="bay bay--greenback">
  <div class="shell">
    <div class="story-reader">
      {about_story}
    </div>
  </div>
</section>
<section class="bay bay--redback">
  <div class="shell">
    <p class="label">علاش حنا مختلفين</p>
    <h2 class="bay__title">أربع فروق كتقاس</h2>
    <div class="ledger">
    {rows}
    </div>
  </div>
</section>
<section class="bay bay--greenback">
  <div class="shell">
    <div class="story-reader">
      {vision_story}
    </div>
  </div>
</section>""".format(
        about_story=about_story, rows=rows, vision_story=vision_story)

    return page("about", "about/", body)


def doctrines_index():
    body = pagehead([(url(), UI["home"]), (None, "عقائدنا")],
                    "عقائدنا", "عشر عقائد، ماشي عشر شعارات",
                    "كل عقيدة كتبدا من مشكل مغربي محدد، وكتشرح علاش ما تحلاش، ومن بعد "
                    "كتقترح حل والتزام يمكن يتقاس.")

    body += """<section class="bay bay--redback">
  <div class="shell">
    <h2 class="vh">لائحة العقائد</h2>
    <div class="doctrine-cards doctrine-cards--index">
      {cards}
    </div>
  </div>
</section>""".format(cards=_doctrine_cards(DOCTRINES))

    return page("doctrines", "doctrines/", body)


DOCTRINE_LABELS = ("المشكل", "علاش ما تحلاش", "شنو كنؤمنو بيه", "الحل اللي كنقترحو",
                   "كيفاش كنقيسو النجاح", "شنو كيعني هادشي للمواطن",
                   "مغرب ما بعد 2030", "الالتزام ديالنا")


def doctrine_page(d):
    body = pagehead([(url(), UI["home"]),
                     (url("doctrines/"), "عقائدنا"),
                     (None, d["name"])],
                    "عقيدة {:02d}".format(d["order"]), d["name"], d["declaration"])

    body += """<section class="bay bay--greenback">
  <div class="shell shell--narrow prose">
    <p>{intro}</p>

    <h2>{l0}</h2>
    <p>{problem}</p>

    <h2>{l1}</h2>
    <p>{why}</p>

    <h2>{l2}</h2>
    <p>{belief}</p>

    <h2>{l3}</h2>
    <ul class="marks">
      {solution}
    </ul>

    <h2>{l4}</h2>
    <ul class="marks">
      {measures}
    </ul>

    <h2>{l5}</h2>
    <p>{citizens}</p>

    <h2>{l6}</h2>
    <p>{beyond}</p>

    <h2>{l7}</h2>
    <p style="font-family:var(--display);font-size:var(--step-1);color:var(--ink)">{commitment}</p>

    <p class="label" style="margin-block-start:3rem">الشعار</p>
    <p style="font-family:var(--display);font-size:var(--step-2);color:var(--green)">{slogan}</p>
  </div>
</section>
<section class="bay bay--redback">
  <div class="shell">
    <p><a class="btn btn--outline" href="{index}">{back}</a></p>
  </div>
</section>""".format(
        intro=esc(d["intro"]),
        l0=DOCTRINE_LABELS[0], l1=DOCTRINE_LABELS[1], l2=DOCTRINE_LABELS[2],
        l3=DOCTRINE_LABELS[3], l4=DOCTRINE_LABELS[4], l5=DOCTRINE_LABELS[5],
        l6=DOCTRINE_LABELS[6], l7=DOCTRINE_LABELS[7],
        problem=esc(d["problem"]), why=esc(d["why_failed"]), belief=esc(d["belief"]),
        solution="\n      ".join("<li>{}</li>".format(esc(x)) for x in d["solution"]),
        measures="\n      ".join("<li>{}</li>".format(esc(x)) for x in d["measures"]),
        citizens=esc(d["citizens"]), beyond=esc(d["beyond"]),
        commitment=esc(d["commitment"]), slogan=esc(d["slogan"]),
        index=url("doctrines/"), back=esc(UI["back_to_doctrines"]))

    title = "{} — {}".format(d["name"], UI["party_name"])
    canonical = url("doctrines/{}/".format(d["slug"]))
    body = apply_page_overrides("doctrine-" + d["slug"], body)
    return (head(title, d["summary"], canonical)
            + masthead("doctrines/")
            + '<main id="main">\n' + body + "\n</main>\n"
            + footer())


def vision_page():
    body = pagehead([(url(), UI["home"]), (None, VISION["label"])],
                    VISION["label"], VISION["title"], VISION["lead"])

    body += """<section class="bay bay--greenback" aria-labelledby="pillars-h">
  <div class="shell">
    <h2 class="vh" id="pillars-h">ركائز الرؤية</h2>
    <div class="pillars" style="margin-block-start:0">
      {pillars}
    </div>
  </div>
</section>
<section class="bay bay--redback">
  <div class="shell shell--narrow prose">
    <h2>{plan_title}</h2>
    <p>{plan_lead}</p>
    {plan_body}
    <h2>{ex_title}</h2>
    <p>{ex_body}</p>
  </div>
</section>""".format(pillars=_pillar_grid(VISION["pillars"]),
                     plan_title=esc(VISION["plan_title"]),
                     plan_lead=esc(VISION["plan_lead"]),
                     plan_body="\n    ".join("<p>{}</p>".format(esc(p))
                                             for p in VISION["plan_body"]),
                     ex_title=esc(VISION["example_title"]),
                     ex_body=esc(VISION["example_body"]))

    return page("vision", "vision/", body)


def news_index():
    body = pagehead([(url(), UI["home"]), (None, "الأخبار")],
                    "الأخبار", "مستجدات الحزب",
                    "كنعلنو هنا المبادرات والمواقف. اللي ما تأكدش بعد كينشر بحال اقتراح، "
                    "ماشي بحال أمر واقع.")

    body += """<section class="bay bay--greenback">
  <div class="shell">
    <article class="news">
      <div>
        <p class="news__kicker">{kicker}</p>
        <h2 class="news__title"><a href="{href}" style="text-decoration:none">{title}</a></h2>
        <p class="news__standfirst">{standfirst}</p>
        <div class="status">
          <span class="status__tag">{tag}</span>
          <p>{status}</p>
        </div>
        <p><a class="btn btn--outline" href="{href}">{more}</a></p>
      </div>
      <aside class="roster">
        <p class="roster__label">{roster_label}</p>
        <ul class="roster__list">
          {roster}
        </ul>
        <p class="roster__note">{roster_note}</p>
      </aside>
    </article>
  </div>
</section>""".format(kicker=esc(NEWS_FEATURED["kicker"]),
                     href=url("news/{}/".format(NEWS_FEATURED["slug"])),
                     title=esc(NEWS_FEATURED["title"]),
                     standfirst=esc(NEWS_FEATURED["standfirst"]),
                     tag=esc(UI["status_proposal"]),
                     status=esc(NEWS_FEATURED["status_note"]), more=esc(UI["more"]),
                     roster_label=esc(NEWS_FEATURED["outreach_label"]),
                     roster="\n          ".join("<li>{}</li>".format(esc(c))
                                                for c in NEWS_FEATURED["outreach"]),
                     roster_note=esc(NEWS_FEATURED["outreach_note"]))

    return page("news", "news/", body)


def news_article():
    body = pagehead([(url(), UI["home"]),
                     (url("news/"), "الأخبار"),
                     (None, NEWS_FEATURED["kicker"])],
                    NEWS_FEATURED["kicker"], NEWS_FEATURED["title"],
                    NEWS_FEATURED["standfirst"])

    body += """<section class="bay bay--greenback">
  <div class="shell shell--narrow prose">
    <div class="status">
      <span class="status__tag">{tag}</span>
      <p>{status}</p>
    </div>
    {paras}
    <div class="roster" style="margin-block-start:2.6rem">
      <p class="roster__label">{roster_label}</p>
      <ul class="roster__list">
        {roster}
      </ul>
      <p class="roster__note">{roster_note}</p>
    </div>
    <p style="margin-block-start:2.4rem"><a class="btn btn--outline" href="{dhref}">عقيدة الهجرة والكرامة</a></p>
  </div>
</section>""".format(tag=esc(UI["status_proposal"]),
                     status=esc(NEWS_FEATURED["status_note"]),
                     paras="\n    ".join("<p>{}</p>".format(esc(p))
                                         for p in NEWS_FEATURED["body"]),
                     roster_label=esc(NEWS_FEATURED["outreach_label"]),
                     roster="\n        ".join("<li>{}</li>".format(esc(c))
                                              for c in NEWS_FEATURED["outreach"]),
                     roster_note=esc(NEWS_FEATURED["outreach_note"]),
                     dhref=url("doctrines/dignified-immigration/"))

    title = "{} — {}".format(NEWS_FEATURED["title"], UI["party_name"])
    canonical = url("news/{}/".format(NEWS_FEATURED["slug"]))
    body = apply_page_overrides("news-article", body)
    return (head(title, NEWS_FEATURED["standfirst"], canonical)
            + masthead("news/")
            + '<main id="main">\n' + body + "\n</main>\n"
            + footer())


def join_page():
    body = pagehead([(url(), UI["home"]), (None, JOIN["label"])],
                    JOIN["label"], JOIN["title"], JOIN["lead"])

    body += """<section class="bay bay--greenback">
  <div class="shell shell--narrow">
    {petition}
  </div>
</section>
<section class="bay bay--redback" aria-labelledby="paths-h">
  <div class="shell">
    <h2 class="vh" id="paths-h">طرق المساهمة</h2>
    <div class="pillars" style="margin-block-start:0">
      {paths}
    </div>
  </div>
</section>
<section class="bay bay--greenback">
  <div class="shell shell--narrow prose">
    <h2>{how_t}</h2>
    <p>{how_b}</p>
    <h2>{contact_t}</h2>
    <div class="status">
      <span class="status__tag">{tag}</span>
      <p>{contact_n}</p>
    </div>
    <p><a class="btn btn--outline" href="{yt}" rel="noopener noreferrer" target="_blank">يوتيوب ↗</a></p>
  </div>
</section>""".format(petition=petition_block(level=2),
                     paths=_pillar_grid(JOIN["paths"]),
                     how_t=esc(JOIN["how_title"]), how_b=esc(JOIN["how_body"]),
                     contact_t=esc(JOIN["contact_title"]),
                     tag=esc(UI["status_explainer"]),
                     contact_n=esc(JOIN["contact_note"]), yt=SITE["youtube"])

    return page("join", "join/", body)


def monarchy_page():
    body = pagehead([(url(), UI["home"]), (None, MONARCHY["label"])],
                    MONARCHY["label"], MONARCHY["title"])

    examples = "\n      ".join("<li><strong>{}</strong> — {}</li>".format(esc(t), esc(b))
                              for t, b in MONARCHY["examples"])

    body += """<section class="bay bay--greenback">
  <div class="shell shell--narrow prose">
    {paras}

    <h2>{q_title}</h2>
    <p>{q_lead}</p>
    <ul class="marks">
      {questions}
    </ul>

    <h2>دروس موثقة</h2>
    <p>{w_lead}</p>
    <ul class="marks">
      {examples}
    </ul>
    <p>{w_close}</p>

    <p style="margin-block-start:2.4rem"><a class="btn btn--outline" href="{bus}">حافلة المغرب</a></p>
  </div>
</section>""".format(paras="\n    ".join("<p>{}</p>".format(esc(p))
                                        for p in MONARCHY["body"]),
                     q_title=esc(MONARCHY["questions_title"]),
                     q_lead=esc(MONARCHY["questions_lead"]),
                     questions="\n      ".join("<li>{}</li>".format(esc(q))
                                               for q in MONARCHY["questions"]),
                     w_lead=esc(MONARCHY["warning_lead"]), examples=examples,
                     w_close=esc(MONARCHY["warning_close"]), bus=url("bus/"))

    return page("monarchy", "monarchy/", body)


def bus_page():
    body = pagehead([(url(), UI["home"]), (None, BUS["label"])],
                    BUS["label"], BUS["title"])
    body += bus_block(full=True)
    return page("bus", "bus/", body)


def accountability_page():
    ladder = "\n      ".join(
        """<div class="ladder__step">
        <span class="ladder__rank">{r}</span>
        <p class="ladder__body">{b}</p>
      </div>""".format(r=esc(r), b=esc(bb))
        for r, bb in ACCOUNTABILITY["ladder"])

    body = pagehead([(url(), UI["home"]), (None, ACCOUNTABILITY["label"])],
                    ACCOUNTABILITY["label"], ACCOUNTABILITY["title"],
                    ACCOUNTABILITY["summary"])

    body += """<section class="bay bay--greenback">
  <div class="shell shell--narrow prose">
    <div class="status">
      <span class="status__tag">{tag}</span>
      <p>{disclaimer}</p>
    </div>

    <h2>{ladder_title}</h2>
    <div class="ladder">
      {ladder}
    </div>

    {paras}

    <h2>{fw_title}</h2>
    <p>{fw_lead}</p>
    <ul class="marks">
      {fw_questions}
    </ul>

    <h2>{pr_title}</h2>
    {pr_body}

    <p class="label" style="margin-block-start:3rem">خلاصة</p>
    <p style="font-family:var(--display);font-size:var(--step-2);color:var(--green)">{closing}</p>
  </div>
</section>""".format(tag=esc(UI["status_explainer"]),
                     disclaimer=esc(ACCOUNTABILITY["disclaimer"]),
                     ladder_title=esc(ACCOUNTABILITY["ladder_title"]), ladder=ladder,
                     paras="\n    ".join("<p>{}</p>".format(esc(p))
                                         for p in ACCOUNTABILITY["body"]),
                     fw_title=esc(ACCOUNTABILITY["framework_title"]),
                     fw_lead=esc(ACCOUNTABILITY["framework_lead"]),
                     fw_questions="\n      ".join(
                         "<li>{}</li>".format(esc(q))
                         for q in ACCOUNTABILITY["framework_questions"]),
                     pr_title=esc(ACCOUNTABILITY["protection_title"]),
                     pr_body="\n    ".join("<p>{}</p>".format(esc(p))
                                           for p in ACCOUNTABILITY["protection_body"]),
                     closing=esc(ACCOUNTABILITY["closing"]))

    return page("accountability", "accountability/", body)


# ---------------------------------------------------------------- المقالات

ARTICLES_PATH = os.path.join(ROOT, "content", "articles.json")


def load_articles():
    """Articles, newest first. Missing or broken file yields an empty list."""
    try:
        with open(ARTICLES_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return []
    items = data.get("articles") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return []
    clean = [a for a in items if isinstance(a, dict) and a.get("slug") and a.get("title")]
    return sorted(clean, key=lambda a: str(a.get("date", "")), reverse=True)


# Only these hosts can be embedded. Anything else is rendered as a plain
# link, so a typo or a hostile paste cannot inject a third-party frame.
EMBED_HOSTS = {
    "youtube": ("youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com"),
    "x": ("twitter.com", "www.twitter.com", "x.com", "www.x.com"),
    "instagram": ("instagram.com", "www.instagram.com"),
    "tiktok": ("tiktok.com", "www.tiktok.com"),
}

EMBED_NAMES = {
    "youtube": "يوتيوب",
    "x": "X",
    "instagram": "إنستغرام",
    "tiktok": "تيك توك",
}


def _youtube_id(parsed):
    if parsed.netloc.endswith("youtu.be"):
        return parsed.path.strip("/").split("/")[0]
    qs = dict(pair.split("=", 1) for pair in parsed.query.split("&") if "=" in pair)
    if qs.get("v"):
        return qs["v"]
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) >= 2 and parts[0] in ("embed", "shorts", "live"):
        return parts[1]
    return ""


def embed_block(url_, caption=""):
    """A social or video embed that loads nothing until asked.

    Every one of these providers ships tracking with its player. Loading them
    on page view would put a third-party profile cookie on every reader of a
    political site, which is exactly the reason the fonts here are
    self-hosted. So the article ships a still card plus a real link, and the
    provider's own code is fetched only when the reader presses play.
    """
    from urllib.parse import urlparse

    raw = str(url_ or "").strip()
    parsed = urlparse(raw)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return ""

    host = parsed.netloc.lower()
    provider = next((p for p, hosts in EMBED_HOSTS.items() if host in hosts), "")
    if not provider:
        return '<p class="article__link"><a href="{u}" rel="noopener noreferrer" target="_blank">{u} ↗</a></p>'.format(
            u=esc(raw))

    frame = ""
    if provider == "youtube":
        vid = _youtube_id(parsed)
        if not vid:
            return ""
        # nocookie host, and still only fetched on demand
        frame = "https://www.youtube-nocookie.com/embed/{}?rel=0".format(esc(vid))

    label = EMBED_NAMES.get(provider, provider)
    return """<figure class="embed" data-embed="{provider}" data-url="{url}"{frame_attr}>
      <button class="embed__load" type="button">
        <span class="embed__provider">{label}</span>
        <span class="embed__play" aria-hidden="true">▶</span>
        <span class="embed__hint">اضغط باش تشغّل — {label} غادي يحمّل الكود ديالو دابا</span>
      </button>
      <figcaption class="embed__caption">
        <a href="{url}" rel="noopener noreferrer" target="_blank">{caption} ↗</a>
      </figcaption>
    </figure>""".format(
        provider=esc(provider), url=esc(raw), label=esc(label),
        frame_attr=' data-frame="{}"'.format(frame) if frame else "",
        caption=esc(caption or "شوف على {}".format(label)))


def article_blocks(blocks):
    out = []
    for block in blocks or []:
        if not isinstance(block, dict):
            continue
        kind = block.get("type", "p")
        text = str(block.get("text", "")).strip()
        if kind == "h3" and text:
            out.append("<h3>{}</h3>".format(esc(text)))
        elif kind == "p" and text:
            out.append("<p>{}</p>".format(esc(text)))
        elif kind == "quote" and text:
            out.append('<blockquote class="article__quote">{}</blockquote>'.format(esc(text)))
        elif kind == "note" and text:
            out.append("""<div class="status">
      <span class="status__tag">{tag}</span>
      <p>{text}</p>
    </div>""".format(tag=esc(block.get("tag", "ملاحظة")), text=esc(text)))
        elif kind == "image" and block.get("src"):
            out.append("""<figure class="article__figure">
      <img src="{src}" alt="{alt}" loading="lazy" decoding="async">{cap}
    </figure>""".format(
                src=asset(str(block["src"])), alt=esc(block.get("alt", "")),
                cap="\n      <figcaption>{}</figcaption>".format(esc(block["caption"]))
                    if block.get("caption") else ""))
        elif kind == "embed" and block.get("url"):
            out.append(embed_block(block["url"], block.get("caption", "")))
    return "\n    ".join(out)


def _keywords(article):
    words = [str(k).strip() for k in article.get("keywords", []) if str(k).strip()]
    if not words:
        return ""
    tags = "\n        ".join(
        '<li lang="en" dir="ltr">{}</li>'.format(esc(w)) for w in words)
    return """<div class="article__keys">
      <h2 class="article__keys-title">Keywords</h2>
      <ul class="article__keys-list">
        {tags}
      </ul>
    </div>""".format(tags=tags)


def articles_index():
    items = load_articles()
    body = pagehead([(url(), UI["home"]), (None, "مقالات")],
                    "مقالات", "مقالات وتحاليل",
                    "كتابات على السياسة، الاقتصاد، والهجرة. كل مقال فيه "
                    "الكلمات المفتاحية بالإنجليزية باش يتلقى بسهولة.")

    if not items:
        cards = """<p class="articles__empty">مازال ما كاين حتى مقال منشور.
      زيد واحد من صفحة التحرير المحلية.</p>"""
    else:
        cards = "\n      ".join(
            """<article class="article-card" data-reveal="{delay}">
        <a class="article-card__link" href="{href}">
          <img class="article-card__image" src="{img}" alt="{alt}" loading="lazy" decoding="async">
          <div class="article-card__copy">
            <time class="article-card__date" datetime="{date}">{date}</time>
            <h3 class="article-card__title">{title}</h3>
            <p class="article-card__summary">{summary}</p>
            <span class="article-card__more">قرا المقال</span>
          </div>
        </a>
      </article>""".format(
                delay=(i % 3) * 60, href=url("articles/{}/".format(a["slug"])),
                img=asset(str(a.get("image") or DEFAULT_READER_IMAGE)),
                alt=esc(a.get("image_alt", "")), date=esc(a.get("date", "")),
                title=esc(a["title"]), summary=esc(a.get("summary", "")))
            for i, a in enumerate(items))

    body += """<section class="bay bay--redback" data-parallax-bg>
  <div class="shell">
    <h2 class="vh">لائحة المقالات</h2>
    <div class="articles">
      {cards}
    </div>
  </div>
</section>""".format(cards=cards)

    return page("articles", "articles/", body)


def article_page(article):
    body = pagehead([(url(), UI["home"]),
                     (url("articles/"), "مقالات"),
                     (None, article["title"])],
                    esc(article.get("date", "")), article["title"],
                    article.get("summary", ""))

    body += """<section class="bay bay--greenback" data-parallax-bg>
  <div class="shell shell--narrow">
    <figure class="article__lead">
      <img src="{img}" alt="{alt}" width="1000" height="1000" loading="eager" decoding="async">
    </figure>
    <h2 class="vh">نص المقال</h2>
    <div class="prose article__body">
    {blocks}
    </div>
    {keys}
    <p style="margin-block-start:2.4rem">
      <a class="btn btn--outline" href="{back}">كل المقالات</a>
    </p>
  </div>
</section>""".format(
        img=asset(str(article.get("image") or DEFAULT_READER_IMAGE)),
        alt=esc(article.get("image_alt", "")),
        blocks=article_blocks(article.get("blocks")),
        keys=_keywords(article), back=url("articles/"))

    title = "{} — {}".format(article["title"], UI["party_name"])
    canonical = url("articles/{}/".format(article["slug"]))
    markup = apply_page_overrides("article-" + article["slug"], body)
    return (head(title, article.get("summary", ""), canonical)
            + masthead("articles/")
            + '<main id="main">\n' + markup + "\n</main>\n"
            + footer())


# ---------------------------------------------------------------- الكتابة

def write(path, content):
    full = os.path.join(DIST, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)


def build():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    for sub in ("css", "js", "img", "fonts"):
        src = os.path.join(STATIC, sub)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(DIST, sub))

    routes = [
        ("index.html", home()),
        ("about/index.html", about_page()),
        ("doctrines/index.html", doctrines_index()),
        ("vision/index.html", vision_page()),
        ("news/index.html", news_index()),
        ("news/{}/index.html".format(NEWS_FEATURED["slug"]), news_article()),
        ("founder/index.html", redirect_page(url("about/#founder"), url("about/"))),
        ("join/index.html", join_page()),
        ("monarchy/index.html", monarchy_page()),
        ("articles/index.html", articles_index()),
        ("bus/index.html", bus_page()),
        ("accountability/index.html", accountability_page()),
        ("z/index.html", z_page()),
    ]
    for d in DOCTRINES:
        routes.append(("doctrines/{}/index.html".format(d["slug"]), doctrine_page(d)))

    for a in load_articles():
        routes.append(("articles/{}/index.html".format(a["slug"]), article_page(a)))

    for path, content in routes:
        write(path, content)

    paths = ["", "about/", "doctrines/", "vision/", "news/",
             "news/{}/".format(NEWS_FEATURED["slug"]), "join/",
             "monarchy/", "bus/", "accountability/"]
    paths += ["doctrines/{}/".format(d["slug"]) for d in DOCTRINES]
    paths += ["articles/"] + ["articles/{}/".format(a["slug"]) for a in load_articles()]

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in sorted(url(x) for x in paths):
        sitemap.append("  <url><loc>{}{}</loc></url>".format(ORIGIN, p))
    sitemap.append("</urlset>")
    write("sitemap.xml", "\n".join(sitemap) + "\n")

    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: {}{}/sitemap.xml\n".format(
        ORIGIN, BASE))

    print("built {} pages + {} urls in sitemap".format(len(routes), len(paths)))


if __name__ == "__main__":
    build()
