#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static site generator for The Moroccan Right Party.

No dependencies beyond the standard library. Run:  python3 build.py
Output lands in dist/ and can be served by any static host.

Arabic and English share every template. Only the content differs, and
direction/typography follow from the <html> element.
"""

import html
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content.site import (  # noqa: E402
    SITE, UI, NAV, HERO, WHO, NEWS_FEATURED, VISION, BUS, MONARCHY,
    ACCOUNTABILITY, FOUNDER, JOIN, DECLARATION, FOOTER, META,
)
from content.doctrines import DOCTRINES, FEATURED  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
STATIC = os.path.join(ROOT, "static")

LANGS = ("ar", "en")
DIRS = {"ar": "rtl", "en": "ltr"}


def esc(s):
    return html.escape(str(s), quote=True)


def url(lang, path=""):
    return "/{}/{}".format(lang, path)


def other(lang):
    return "en" if lang == "ar" else "ar"


# ---------------------------------------------------------------- chrome

def head(lang, title, desc, canonical, counterpart, hero=False):
    d = DIRS[lang]
    critical = (
        ["reem-kufi-700-arabic.woff2", "noto-naskh-arabic-400-arabic.woff2"]
        if lang == "ar" else
        ["fraunces-900-latin.woff2", "archivo-400-latin.woff2"]
    )
    preloads = "\n".join(
        '  <link rel="preload" href="/fonts/{}" as="font" type="font/woff2" crossorigin>'.format(f)
        for f in critical
    )
    return """<!doctype html>
<html lang="{lang}" dir="{dir}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://{domain}{canonical}">
  <link rel="alternate" hreflang="{lang}" href="https://{domain}{canonical}">
  <link rel="alternate" hreflang="{olang}" href="https://{domain}{counterpart}">
  <link rel="alternate" hreflang="x-default" href="https://{domain}/ar/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:locale" content="{locale}">
  <meta property="og:url" content="https://{domain}{canonical}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#F3EDE1">
  <link rel="icon" href="/img/party-logo.svg" type="image/svg+xml">
{preloads}
  <link rel="stylesheet" href="/css/fonts-{lang}.css">
  <link rel="stylesheet" href="/css/site.css">
</head>
<body{hero_attr}>
<a class="skip" href="#main">{skip}</a>
<div class="axis" aria-hidden="true"></div>
""".format(
        lang=lang, dir=d, title=esc(title), desc=esc(desc),
        domain=SITE["domain"], canonical=canonical, counterpart=counterpart,
        olang=other(lang), locale="ar_MA" if lang == "ar" else "en_US",
        preloads=preloads, skip=esc(UI[lang]["skip"]),
        hero_attr=' data-hero-page' if hero else '',
    )


def masthead(lang, active, counterpart):
    u = UI[lang]
    items = []
    for path, label in NAV[lang]:
        href = url(lang, path)
        cur = ' aria-current="page"' if path == active else ""
        items.append('<a class="nav__link" href="{}"{}>{}</a>'.format(href, cur, esc(label)))
    return """<header class="masthead" data-masthead>
  <div class="shell masthead__inner">
    <a class="wordmark" href="{home}">
      <img class="wordmark__mark" src="/img/party-logo.svg" alt="" width="34" height="47" loading="eager">
      <span class="wordmark__text">{name}</span>
    </a>
    <button class="burger" type="button" data-burger aria-expanded="false" aria-controls="sitenav"
            data-label-menu="{menu}" data-label-close="{close}">{menu}</button>
    <nav class="nav" id="sitenav" data-nav aria-label="{name}">
      {items}
      <a class="lang" href="{counterpart}" lang="{olang}" hreflang="{olang}" aria-label="{lang_label}">{lang_text}</a>
    </nav>
  </div>
</header>
""".format(
        home=url(lang), name=esc(UI[lang]["party_name"]),
        menu=esc(u["menu"]), close=esc(u["close"]),
        items="\n      ".join(items), counterpart=counterpart, olang=other(lang),
        lang_label=esc(u["lang_switch_label"]), lang_text=esc(u["lang_switch"]),
    )


def footer(lang):
    f = FOOTER[lang]
    u = UI[lang]
    links = "\n      ".join(
        '<a href="{}">{}</a>'.format(url(lang, p), esc(l)) for p, l in NAV[lang]
    )
    extra = [("monarchy/", {"ar": "الملكية والاستمرارية", "en": "Monarchy and continuity"}[lang]),
             ("bus/", {"ar": "حافلة المغرب", "en": "The Morocco Bus"}[lang]),
             ("accountability/", {"ar": "المساءلة والأدلة", "en": "Accountability and evidence"}[lang])]
    links += "\n      " + "\n      ".join(
        '<a href="{}">{}</a>'.format(url(lang, p), esc(l)) for p, l in extra
    )
    legal = "\n        ".join("<li>{}</li>".format(esc(x)) for x in f["legal"])
    return """<footer class="footer">
  <div class="shell">
    <div class="footer__top">
      <div>
        <img class="footer__mark" src="/img/party-logo.svg" alt="{logo_alt}" width="96" height="133" loading="lazy">
        <p class="footer__tagline">{tagline}</p>
      </div>
      <div>
        <nav class="footer__nav" aria-label="{name}">
      {links}
        </nav>
        <div class="footer__legal">
          <h2>{legal_title}</h2>
          <ul style="list-style:none;padding:0;margin:0">
        {legal}
          </ul>
        </div>
      </div>
    </div>
    <div class="footer__base">
      <span>{rights}</span>
      <a href="{yt}" rel="noopener noreferrer" target="_blank">YouTube ↗</a>
    </div>
  </div>
</footer>
<script src="/js/nav.js" defer></script>
<script src="/js/motion.js" defer></script>
</body>
</html>
""".format(
        logo_alt=esc(u["logo_alt"]), tagline=esc(f["tagline"]), name=esc(UI[lang]["party_name"]),
        links=links, legal_title=esc(f["legal_title"]), legal=legal,
        rights=esc(f["rights"]), yt=SITE["youtube"],
    )


def page(lang, key, active, body, counterpart, hero=False):
    title, desc = META[lang][key]
    canonical = url(lang, active)
    return (head(lang, title, desc, canonical, counterpart, hero=hero)
            + masthead(lang, active, counterpart)
            + '<main id="main">\n' + body + "\n</main>\n"
            + footer(lang))


def crumbs(lang, trail):
    """trail: list of (href|None, label)"""
    parts = []
    for i, (href, label) in enumerate(trail):
        if i:
            parts.append('<span aria-hidden="true">/</span>')
        if href:
            parts.append('<a href="{}">{}</a>'.format(href, esc(label)))
        else:
            parts.append("<span>{}</span>".format(esc(label)))
    return '<nav class="crumbs" aria-label="{}">{}</nav>'.format(
        "مسار التصفح" if lang == "ar" else "Breadcrumb", "".join(parts))


def pagehead(lang, trail, label, title, standfirst=""):
    sf = '<p class="pagehead__standfirst">{}</p>'.format(esc(standfirst)) if standfirst else ""
    return """<section class="pagehead">
  <div class="shell">
    {crumbs}
    <p class="label" style="margin-block-start:1.4rem">{label}</p>
    <h1 class="pagehead__title">{title}</h1>
    {sf}
  </div>
</section>
""".format(crumbs=crumbs(lang, trail), label=esc(label), title=esc(title), sf=sf)


# ------------------------------------------------------------------ hero

def hero_block(lang):
    h = HERO[lang]
    u = UI[lang]

    def srcset(name):
        return ", ".join("/img/{}-{}.jpg {}w".format(name, w, w)
                         for w in (800, 1200, 1600, 2200, 2752))

    slogan = '<p class="hero__slogan">{}'.format(esc(h["slogan"]))
    if lang == "en":
        slogan += '<span class="hero__slogan-src" lang="ar" dir="rtl">{}</span>'.format(
            esc(h["slogan_source"]))
    slogan += "</p>"

    return """<section class="hero" data-hero>
  <div class="hero__media">
    <figure class="hero__half hero__half--left" style="margin:0">
      <img data-hero-img src="/img/hero-abdullah-ben-zakar-1600.jpg"
           srcset="{ss_left}" sizes="(max-width: 820px) 100vw, 50vw"
           width="2752" height="1536" alt="{alt_left}" fetchpriority="high" decoding="async">
    </figure>
    <figure class="hero__half hero__half--right" style="margin:0">
      <img data-hero-img src="/img/hero-moroccan-monarch-1600.jpg"
           srcset="{ss_right}" sizes="(max-width: 820px) 100vw, 50vw"
           width="2752" height="1536" alt="{alt_right}" fetchpriority="high" decoding="async">
    </figure>
    <div class="hero__wash" aria-hidden="true"></div>
    <div class="hero__seam" aria-hidden="true"></div>

    <div class="hero__content" data-hero-content>
      <div class="shell">
        <p class="hero__eyebrow">{eyebrow}</p>
        <h1 class="hero__title">{headline}</h1>
        {slogan}
        <p class="hero__declaration">{declaration}</p>
        <div class="hero__actions">
          <a class="btn btn--primary" href="{doctrines}">{cta1}</a>
          <a class="btn btn--ghost" href="{join}">{cta2}</a>
        </div>
      </div>
    </div>

    <p class="hero__scroll" aria-hidden="true">{scroll}<span></span></p>
  </div>
</section>
""".format(
        ss_left=srcset("hero-abdullah-ben-zakar"),
        ss_right=srcset("hero-moroccan-monarch"),
        alt_left=esc(u["hero_left_alt"]), alt_right=esc(u["hero_right_alt"]),
        eyebrow=esc(h["eyebrow"]),
        headline=esc(h["headline"]), slogan=slogan,
        declaration=esc(h["declaration"]),
        doctrines=url(lang, "doctrines/"), join=url(lang, "join/"),
        cta1=esc(h["cta_primary"]), cta2=esc(h["cta_secondary"]),
        scroll=esc(u["scroll"]),
    )


BUS_SVG = """<svg class="road__bus" viewBox="0 0 80 34" fill="none" aria-hidden="true" focusable="false">
  <path d="M3 26V10a4 4 0 0 1 4-4h49l18 11v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"
        fill="#F3EDE1" stroke="#A8823C" stroke-width="1.2"/>
  <path d="M10 10h13v8H10zM27 10h13v8H27zM44 10h11l9 8H44z" fill="#14503A" opacity=".85"/>
  <circle cx="20" cy="29" r="4" fill="#2A241B" stroke="#A8823C" stroke-width="1"/>
  <circle cx="60" cy="29" r="4" fill="#2A241B" stroke="#A8823C" stroke-width="1"/>
</svg>"""


def bus_block(lang, full=False):
    b = BUS[lang]
    stages = []
    for st in b["stages"]:
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
        '<p class="declaration__line">{}</p>'.format(esc(l)) for l in b["closing"])

    more = ""
    if not full:
        more = '<p style="margin-block-start:2.5rem"><a class="btn btn--ghost" href="{}">{}</a></p>'.format(
            url(lang, "bus/"),
            "اقرأ القصة كاملة" if lang == "ar" else "Read the full story")

    return """<section class="bay bus" data-progress>
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
""".format(label=esc(b["label"]), title=esc(b["title"]), lead=esc(b["lead"]),
           bus_svg=BUS_SVG, stages="\n      ".join(stages),
           note_title=esc(b["note_title"]), note_body=esc(b["note_body"]),
           closing=closing, more=more)


# ------------------------------------------------------------- home page

def home(lang):
    u, w = UI[lang], WHO[lang]
    n = NEWS_FEATURED[lang]
    v = VISION[lang]
    m = MONARCHY[lang]
    a = ACCOUNTABILITY[lang]
    fo = FOUNDER[lang]
    j = JOIN[lang]
    dec = DECLARATION[lang]

    rows = "\n    ".join(
        """<div class="ledger__row" data-reveal="{d}">
      <p class="ledger__term">{t}</p>
      <p class="ledger__def">{b}</p>
    </div>""".format(d=i * 70, t=esc(t), b=esc(b))
        for i, (t, b) in enumerate(w["distinctions"]))

    folios = "\n      ".join(
        """<a class="folio" href="{href}" data-reveal="{d}">
        <span class="folio__index">{idx:02d}</span>
        <span class="folio__name">{name}</span>
        <p class="folio__summary">{summary}</p>
        <span class="folio__more">{more}</span>
      </a>""".format(href=url(lang, "doctrines/{}/".format(dd["slug"])),
                     d=i * 60, idx=dd["order"], name=esc(dd[lang]["name"]),
                     summary=esc(dd[lang]["summary"]), more=esc(u["read_more"]))
        for i, dd in enumerate(FEATURED))

    roster = "\n        ".join("<li>{}</li>".format(esc(c)) for c in n["outreach"])

    pillars = "\n      ".join(
        """<div class="pillar" data-reveal="{d}">
        <h3>{t}</h3>
        <p>{b}</p>
      </div>""".format(d=i * 55, t=esc(t), b=esc(b))
        for i, (t, b) in enumerate(v["pillars"]))

    ladder = "\n      ".join(
        """<div class="ladder__step">
        <span class="ladder__rank">{r}</span>
        <p class="ladder__body">{b}</p>
      </div>""".format(r=esc(r), b=esc(b)) for r, b in a["ladder"])

    dec_lines = "\n      ".join(
        '<p class="declaration__line">{}</p>'.format(esc(l)) for l in dec["lines"])

    more_label = "اقرأ المزيد" if lang == "ar" else "Read more"

    parts = [hero_block(lang)]

    # 2 — who we are
    parts.append("""<section class="bay bay--raised bay--overlap">
  <div class="shell">
    <p class="label" data-rise="30">{label}</p>
    <h2 class="bay__title" data-rise="46">{title}</h2>
    <p class="bay__lead" data-rise="36">{lead}</p>
    <div class="ledger">
    {rows}
    </div>
  </div>
</section>""".format(label=esc(w["label"]), title=esc(w["title"]),
                     lead=esc(w["lead"]), rows=rows))

    # 3 — news: the international initiative
    parts.append("""<section class="bay">
  <div class="shell news">
    <div>
      <p class="news__kicker" data-rise="30">{kicker}</p>
      <h2 class="news__title" data-rise="48">{title}</h2>
      <p class="news__standfirst" data-rise="38">{standfirst}</p>
      <div class="status">
        <span class="status__tag">{tag}</span>
        <p>{status}</p>
      </div>
      <p><a class="btn btn--outline" href="{href}">{more}</a></p>
    </div>
    <aside class="roster" data-rise="66">
      <p class="roster__label">{roster_label}</p>
      <ul class="roster__list">
        {roster}
      </ul>
      <p class="roster__note">{roster_note}</p>
    </aside>
  </div>
</section>""".format(kicker=esc(n["kicker"]), title=esc(n["title"]),
                     standfirst=esc(n["standfirst"]),
                     tag=esc(UI[lang]["status_proposal"]), status=esc(n["status_note"]),
                     href=url(lang, "news/{}/".format(NEWS_FEATURED["slug"])),
                     more=esc(more_label), roster_label=esc(n["outreach_label"]),
                     roster=roster, roster_note=esc(n["outreach_note"])))

    # 4 — featured doctrines
    parts.append("""<section class="bay bay--recessed">
  <div class="shell">
    <p class="label" data-rise="30">{label}</p>
    <h2 class="bay__title" data-rise="46">{title}</h2>
    <p class="bay__lead" data-rise="36">{lead}</p>
    <div class="folios">
      {folios}
    </div>
    <p style="margin-block-start:2.4rem"><a class="btn btn--outline" href="{href}">{all}</a></p>
  </div>
</section>""".format(
        label="عقائدنا" if lang == "ar" else "Our doctrines",
        title=("عشر عقائد، لا عشرة شعارات" if lang == "ar"
               else "Ten doctrines, not ten slogans"),
        lead=("كل عقيدة تبدأ من مشكل مغربي محدد، وتنتهي بالتزام يمكن قياسه."
              if lang == "ar" else
              "Each doctrine begins with a specific Moroccan problem and ends with a commitment that can be measured."),
        folios=folios, href=url(lang, "doctrines/"),
        all=esc(u["back_to_doctrines"])))

    # 5 — vision
    parts.append("""<section class="bay bay--raised">
  <div class="shell">
    <p class="label" data-rise="30">{label}</p>
    <h2 class="bay__title" data-rise="46">{title}</h2>
    <p class="bay__lead" data-rise="36">{lead}</p>
    <div class="pillars">
      {pillars}
    </div>
    <p style="margin-block-start:2.6rem"><a class="btn btn--outline" href="{href}">{more}</a></p>
  </div>
</section>""".format(label=esc(v["label"]), title=esc(v["title"]), lead=esc(v["lead"]),
                     pillars=pillars, href=url(lang, "vision/"), more=esc(more_label)))

    # 6 — the bus
    parts.append(bus_block(lang))

    # 7 — monarchy
    parts.append("""<section class="bay bay--recessed">
  <div class="shell shell--narrow">
    <p class="label" data-rise="30">{label}</p>
    <h2 class="bay__title" data-rise="46">{title}</h2>
    <p class="bay__lead" data-rise="36">{p1}</p>
    <p style="margin-block-start:1.6rem">{p2}</p>
    <p><a class="btn btn--outline" href="{href}">{more}</a></p>
  </div>
</section>""".format(label=esc(m["label"]), title=esc(m["title"]),
                     p1=esc(m["body"][0]), p2=esc(m["body"][3]),
                     href=url(lang, "monarchy/"), more=esc(more_label)))

    # 8 — accountability explainer
    parts.append("""<section class="bay bay--raised">
  <div class="shell shell--narrow">
    <p class="label" data-rise="30">{label}</p>
    <h2 class="bay__title" data-rise="46">{title}</h2>
    <p class="bay__lead" data-rise="36">{summary}</p>
    <div class="status">
      <span class="status__tag">{tag}</span>
      <p>{disclaimer}</p>
    </div>
    <h3 style="font-size:var(--step-1);margin-block-end:.4rem">{ladder_title}</h3>
    <div class="ladder">
      {ladder}
    </div>
    <p><a class="btn btn--outline" href="{href}">{more}</a></p>
  </div>
</section>""".format(label=esc(a["label"]), title=esc(a["title"]),
                     summary=esc(a["summary"]), tag=esc(u["status_explainer"]),
                     disclaimer=esc(a["disclaimer"]), ladder_title=esc(a["ladder_title"]),
                     ladder=ladder, href=url(lang, "accountability/"), more=esc(more_label)))

    # 9 — founder
    parts.append("""<section class="bay bay--recessed">
  <div class="shell shell--narrow">
    <p class="label" data-rise="30">{label}</p>
    <h2 class="bay__title" data-rise="46">{title}</h2>
    <p class="bay__lead" data-rise="36">{p1}</p>
    <p style="margin-block-start:1.6rem">{p2}</p>
    <p>{p3}</p>
    <p style="margin-block-start:2rem;display:flex;gap:.8rem;flex-wrap:wrap">
      <a class="btn btn--outline" href="{href}">{more}</a>
      <a class="btn btn--outline" href="{yt}" rel="noopener noreferrer" target="_blank">{yt_label} ↗</a>
    </p>
    <p style="font-size:var(--step--1);color:var(--ink-mute)">{yt_note}</p>
  </div>
</section>""".format(label=esc(fo["label"]), title=esc(fo["title"]),
                     p1=esc(fo["message"][0]), p2=esc(fo["message"][2]),
                     p3=esc(fo["message"][5]), href=url(lang, "founder/"),
                     more=esc(more_label), yt=SITE["youtube"],
                     yt_label=esc(fo["youtube_label"]), yt_note=esc(fo["youtube_note"])))

    # 10 — join
    paths = "\n      ".join(
        """<div class="pillar" data-reveal="{d}">
        <h3>{t}</h3>
        <p>{b}</p>
      </div>""".format(d=i * 55, t=esc(t), b=esc(b))
        for i, (t, b) in enumerate(j["paths"]))

    parts.append("""<section class="bay bay--raised">
  <div class="shell">
    <p class="label" data-rise="30">{label}</p>
    <h2 class="bay__title" data-rise="46">{title}</h2>
    <p class="bay__lead" data-rise="36">{lead}</p>
    <div class="pillars">
      {paths}
    </div>
    <p style="margin-block-start:2.6rem"><a class="btn btn--primary" href="{href}">{more}</a></p>
  </div>
</section>""".format(label=esc(j["label"]), title=esc(j["title"]), lead=esc(j["lead"]),
                     paths=paths, href=url(lang, "join/"), more=esc(j["label"])))

    # 11 — declaration
    parts.append("""<section class="bay bay--deep">
  <div class="shell declaration">
    {lines}
    <a class="btn btn--primary" href="{href}">{cta}</a>
  </div>
</section>""".format(lines=dec_lines, href=url(lang, "join/"), cta=esc(dec["cta"])))

    return page(lang, "home", "", "\n".join(parts), url(other(lang)), hero=True)


# ------------------------------------------------------------ inner pages

def about_page(lang):
    w = WHO[lang]
    v = VISION[lang]
    rows = "\n    ".join(
        """<div class="ledger__row" data-reveal="{d}">
      <p class="ledger__term">{t}</p>
      <p class="ledger__def">{b}</p>
    </div>""".format(d=i * 70, t=esc(t), b=esc(b))
        for i, (t, b) in enumerate(w["distinctions"]))

    identity = {
        "ar": [
            "وطني مغربي: المغرب أولاً.",
            "ملكي، مع التحديث والإصلاح العملي.",
            "رأسمالي منتج، ضد الخليط المرتبك بين الرأسمالية والاشتراكية.",
            "يميني سياسياً، وغير ديني.",
            "يشتغل بالهندسة والنماذج والحلول القابلة للقياس.",
            "متصل بمغاربة العالم وبالخبرة الدولية.",
            "يركّز على الكرامة والفرص والهجرة والأمن ومغرب ما بعد 2030.",
        ],
        "en": [
            "Moroccan nationalist: Morocco First.",
            "Pro-monarchy, while advocating modernisation and practical reform.",
            "Capitalist and productive, opposed to the current confused mixture of capitalism and socialism.",
            "Politically right-wing, and not a religious party.",
            "Driven by engineering, prototypes, and measurable solutions.",
            "Connected to the Moroccan diaspora and to international experience.",
            "Focused on dignity, opportunity, immigration, security, and Morocco after 2030.",
        ],
    }[lang]

    naming = {
        "ar": ("عن الاسم",
               "الاسم الرسمي للمشروع هو «حزب اليمين المغربي». وقد استُعملت في مرحلة "
               "التعريف الإعلامي صيغ أكثر حدة، لكنها ليست التعريف الرسمي للحزب. نقدّم "
               "أنفسنا بوصفنا يميناً مغربياً وطنياً منتجاً حديثاً."),
        "en": ("On the name",
               "The project's formal name is The Moroccan Right Party. Sharper phrasing has "
               "been used in media introductions, but it is not the party's formal "
               "definition. We present ourselves as a national, productive, modern "
               "Moroccan right."),
    }[lang]

    body = pagehead(
        lang,
        [(url(lang), UI[lang]["home"]), (None, WHO[lang]["label"])],
        w["label"], w["title"], w["lead"])

    body += """<section class="bay bay--raised">
  <div class="shell shell--narrow prose">
    <h2>{ident_title}</h2>
    <ul class="marks">
      {identity}
    </ul>
    <h2>{naming_t}</h2>
    <p>{naming_b}</p>

    <figure class="emblem">
      <img src="/img/party-logo.svg" alt="{logo_alt}" width="300" height="375" loading="lazy">
      <figcaption>{emblem_cap}</figcaption>
    </figure>
  </div>
</section>
<section class="bay bay--recessed">
  <div class="shell">
    <p class="label">{diff_label}</p>
    <h2 class="bay__title">{diff_title}</h2>
    <div class="ledger">
    {rows}
    </div>
  </div>
</section>
<section class="bay bay--raised">
  <div class="shell shell--narrow prose">
    <h2>{plan_title}</h2>
    <p>{plan_lead}</p>
    {plan_body}
    <p style="margin-block-start:2rem"><a class="btn btn--outline" href="{vhref}">{vmore}</a></p>
  </div>
</section>""".format(
        ident_title="هوية الحزب" if lang == "ar" else "The party's identity",
        identity="\n      ".join("<li>{}</li>".format(esc(x)) for x in identity),
        naming_t=esc(naming[0]), naming_b=esc(naming[1]),
        logo_alt=esc(UI[lang]["logo_alt"]),
        emblem_cap=esc({
            "ar": "شعار الحزب: النافذة المغربية المفتوحة، وأمامها لوحة تحمل صورة "
                  "تاريخية. الشعار يحمل الصيغة الإعلامية للمشروع؛ أما التسمية الرسمية "
                  "فهي «حزب اليمين المغربي».",
            "en": "The party emblem: an open Moroccan window with a stand carrying a "
                  "historical portrait before it. The emblem carries the project's media "
                  "phrasing; the formal name is The Moroccan Right Party.",
        }[lang]),
        diff_label="لماذا نحن مختلفون" if lang == "ar" else "Why we are different",
        diff_title=("أربعة فروق يمكن قياسها" if lang == "ar"
                    else "Four differences you can measure"),
        rows=rows,
        plan_title=esc(v["plan_title"]), plan_lead=esc(v["plan_lead"]),
        plan_body="\n    ".join("<p>{}</p>".format(esc(p)) for p in v["plan_body"]),
        vhref=url(lang, "vision/"),
        vmore="رؤيتنا كاملة" if lang == "ar" else "Read the full vision")

    return page(lang, "about", "about/", body, url(other(lang), "about/"))


def doctrines_index(lang):
    u = UI[lang]
    items = "\n      ".join(
        """<a class="register__item" href="{href}" data-reveal="{d}">
        <span class="register__num">{idx:02d}</span>
        <span class="register__name">{name}</span>
        <p class="register__summary">{summary}</p>
        <span class="register__go">{more}</span>
      </a>""".format(href=url(lang, "doctrines/{}/".format(dd["slug"])),
                     d=min(i, 6) * 45, idx=dd["order"], name=esc(dd[lang]["name"]),
                     summary=esc(dd[lang]["summary"]), more=esc(u["read_more"]))
        for i, dd in enumerate(DOCTRINES))

    body = pagehead(
        lang,
        [(url(lang), u["home"]), (None, "عقائدنا" if lang == "ar" else "Doctrines")],
        "عقائدنا" if lang == "ar" else "Our doctrines",
        "عشر عقائد، لا عشرة شعارات" if lang == "ar" else "Ten doctrines, not ten slogans",
        ("كل عقيدة تبدأ من مشكل مغربي محدد، وتشرح لماذا لم تُحل، ثم تقترح حلاً "
         "والتزاماً يمكن قياسه." if lang == "ar" else
         "Each doctrine starts from a specific Moroccan problem, explains why it has not "
         "been solved, then proposes a solution and a commitment that can be measured."))

    body += """<section class="bay bay--recessed">
  <div class="shell">
    <div class="register">
      {items}
    </div>
  </div>
</section>""".format(items=items)

    return page(lang, "doctrines", "doctrines/", body, url(other(lang), "doctrines/"))


def doctrine_page(lang, d):
    c = d[lang]
    u = UI[lang]
    labels = {
        "ar": ("المشكل", "لماذا لم تُحل", "ما نؤمن به", "الحل الذي نقترحه",
               "كيف نقيس النجاح", "ماذا يعني هذا للمواطن", "مغرب ما بعد 2030", "التزامنا"),
        "en": ("The problem", "Why it has not been solved", "What we believe",
               "Our solution", "How success is measured", "What this means for citizens",
               "Morocco beyond 2030", "Our commitment"),
    }[lang]

    body = pagehead(
        lang,
        [(url(lang), u["home"]),
         (url(lang, "doctrines/"), "عقائدنا" if lang == "ar" else "Doctrines"),
         (None, c["name"])],
        "عقيدة {:02d}".format(d["order"]) if lang == "ar" else "Doctrine {:02d}".format(d["order"]),
        c["name"], c["declaration"])

    body += """<section class="bay bay--raised">
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

    <p class="label" style="margin-block-start:3rem">{slogan_label}</p>
    <p style="font-family:var(--display);font-size:var(--step-2);color:var(--green)">{slogan}</p>
  </div>
</section>
<section class="bay bay--recessed">
  <div class="shell">
    <p><a class="btn btn--outline" href="{index}">{back}</a></p>
  </div>
</section>""".format(
        intro=esc(c["intro"]),
        l0=labels[0], l1=labels[1], l2=labels[2], l3=labels[3],
        l4=labels[4], l5=labels[5], l6=labels[6], l7=labels[7],
        problem=esc(c["problem"]), why=esc(c["why_failed"]), belief=esc(c["belief"]),
        solution="\n      ".join("<li>{}</li>".format(esc(x)) for x in c["solution"]),
        measures="\n      ".join("<li>{}</li>".format(esc(x)) for x in c["measures"]),
        citizens=esc(c["citizens"]), beyond=esc(c["beyond"]),
        commitment=esc(c["commitment"]),
        slogan_label="الشعار" if lang == "ar" else "Slogan",
        slogan=esc(c["slogan"]),
        index=url(lang, "doctrines/"), back=esc(u["back_to_doctrines"]))

    title = "{} — {}".format(c["name"], UI[lang]["party_name"])
    desc = c["summary"]
    canonical = url(lang, "doctrines/{}/".format(d["slug"]))
    counterpart = url(other(lang), "doctrines/{}/".format(d["slug"]))
    return (head(lang, title, desc, canonical, counterpart)
            + masthead(lang, "doctrines/", counterpart)
            + '<main id="main">\n' + body + "\n</main>\n"
            + footer(lang))


def vision_page(lang):
    v = VISION[lang]
    u = UI[lang]
    pillars = "\n      ".join(
        """<div class="pillar" data-reveal="{d}">
        <h3>{t}</h3>
        <p>{b}</p>
      </div>""".format(d=i * 55, t=esc(t), b=esc(b))
        for i, (t, b) in enumerate(v["pillars"]))

    body = pagehead(lang,
                    [(url(lang), u["home"]), (None, v["label"])],
                    v["label"], v["title"], v["lead"])

    body += """<section class="bay bay--raised" aria-labelledby="pillars-h">
  <div class="shell">
    <h2 class="vh" id="pillars-h">{pillars_h}</h2>
    <div class="pillars" style="margin-block-start:0">
      {pillars}
    </div>
  </div>
</section>
<section class="bay bay--recessed">
  <div class="shell shell--narrow prose">
    <h2>{plan_title}</h2>
    <p>{plan_lead}</p>
    {plan_body}
    <h2>{ex_title}</h2>
    <p>{ex_body}</p>
  </div>
</section>""".format(
        pillars=pillars,
        pillars_h="ركائز الرؤية" if lang == "ar" else "The pillars of the vision",
        plan_title=esc(v["plan_title"]), plan_lead=esc(v["plan_lead"]),
        plan_body="\n    ".join("<p>{}</p>".format(esc(p)) for p in v["plan_body"]),
        ex_title=esc(v["example_title"]), ex_body=esc(v["example_body"]))

    return page(lang, "vision", "vision/", body, url(other(lang), "vision/"))


def news_index(lang):
    n = NEWS_FEATURED[lang]
    u = UI[lang]
    body = pagehead(lang,
                    [(url(lang), u["home"]), (None, "الأخبار" if lang == "ar" else "News")],
                    "الأخبار" if lang == "ar" else "News",
                    "مستجدات الحزب" if lang == "ar" else "Party updates",
                    ("نعلن هنا المبادرات والمواقف. ما لم يُؤكَّد بعد يُنشر بوصفه اقتراحاً، "
                     "لا بوصفه أمراً واقعاً." if lang == "ar" else
                     "Initiatives and positions are announced here. Anything not yet confirmed "
                     "is published as a proposal, not as an accomplished fact."))

    body += """<section class="bay bay--raised">
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
</section>""".format(
        kicker=esc(n["kicker"]), href=url(lang, "news/{}/".format(NEWS_FEATURED["slug"])),
        title=esc(n["title"]), standfirst=esc(n["standfirst"]),
        tag=esc(u["status_proposal"]), status=esc(n["status_note"]),
        more="اقرأ المزيد" if lang == "ar" else "Read more",
        roster_label=esc(n["outreach_label"]), roster="\n          ".join(
            "<li>{}</li>".format(esc(c)) for c in n["outreach"]),
        roster_note=esc(n["outreach_note"]))

    return page(lang, "news", "news/", body, url(other(lang), "news/"))


def news_article(lang):
    n = NEWS_FEATURED[lang]
    u = UI[lang]
    canonical = url(lang, "news/{}/".format(NEWS_FEATURED["slug"]))
    counterpart = url(other(lang), "news/{}/".format(NEWS_FEATURED["slug"]))

    body = pagehead(
        lang,
        [(url(lang), u["home"]),
         (url(lang, "news/"), "الأخبار" if lang == "ar" else "News"),
         (None, n["kicker"])],
        n["kicker"], n["title"], n["standfirst"])

    body += """<section class="bay bay--raised">
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
    <p style="margin-block-start:2.4rem"><a class="btn btn--outline" href="{dhref}">{dmore}</a></p>
  </div>
</section>""".format(
        tag=esc(u["status_proposal"]), status=esc(n["status_note"]),
        paras="\n    ".join("<p>{}</p>".format(esc(p)) for p in n["body"]),
        roster_label=esc(n["outreach_label"]),
        roster="\n        ".join("<li>{}</li>".format(esc(c)) for c in n["outreach"]),
        roster_note=esc(n["outreach_note"]),
        dhref=url(lang, "doctrines/dignified-immigration/"),
        dmore=("عقيدة الهجرة والكرامة" if lang == "ar"
               else "The Dignified Immigration Doctrine"))

    title = "{} — {}".format(n["title"], UI[lang]["party_name"])
    return (head(lang, title, n["standfirst"], canonical, counterpart)
            + masthead(lang, "news/", counterpart)
            + '<main id="main">\n' + body + "\n</main>\n"
            + footer(lang))


def founder_page(lang):
    f = FOUNDER[lang]
    u = UI[lang]
    body = pagehead(lang,
                    [(url(lang), u["home"]), (None, f["label"])],
                    f["label"], f["title"], f["standfirst"])

    body += """<section class="bay bay--raised">
  <div class="shell shell--narrow prose">
    {paras}
    <p style="margin-block-start:2.4rem">
      <a class="btn btn--outline" href="{yt}" rel="noopener noreferrer" target="_blank">{yt_label} ↗</a>
    </p>
    <p style="font-size:var(--step--1);color:var(--ink-mute)">{yt_note}</p>
  </div>
</section>
<section class="bay bay--recessed">
  <div class="shell shell--narrow prose">
    <h2>{role_t}</h2>
    <p>{role_b}</p>
    <p><a class="btn btn--outline" href="{bus}">{bus_label}</a></p>
  </div>
</section>""".format(
        paras="\n    ".join("<p>{}</p>".format(esc(p)) for p in f["message"]),
        yt=SITE["youtube"], yt_label=esc(f["youtube_label"]), yt_note=esc(f["youtube_note"]),
        role_t="دوره في الحزب" if lang == "ar" else "His role in the party",
        role_b=esc(BUS[lang]["stages"][1]["body"]),
        bus=url(lang, "bus/"),
        bus_label="حافلة المغرب" if lang == "ar" else "The Morocco Bus")

    return page(lang, "founder", "founder/", body, url(other(lang), "founder/"))


def join_page(lang):
    j = JOIN[lang]
    u = UI[lang]
    paths = "\n      ".join(
        """<div class="pillar" data-reveal="{d}">
        <h3>{t}</h3>
        <p>{b}</p>
      </div>""".format(d=i * 55, t=esc(t), b=esc(b))
        for i, (t, b) in enumerate(j["paths"]))

    body = pagehead(lang,
                    [(url(lang), u["home"]), (None, j["label"])],
                    j["label"], j["title"], j["lead"])

    body += """<section class="bay bay--raised" aria-labelledby="paths-h">
  <div class="shell">
    <h2 class="vh" id="paths-h">{paths_h}</h2>
    <div class="pillars" style="margin-block-start:0">
      {paths}
    </div>
  </div>
</section>
<section class="bay bay--recessed">
  <div class="shell shell--narrow prose">
    <h2>{how_t}</h2>
    <p>{how_b}</p>
    <h2>{contact_t}</h2>
    <div class="status">
      <span class="status__tag">{tag}</span>
      <p>{contact_n}</p>
    </div>
    <p><a class="btn btn--outline" href="{yt}" rel="noopener noreferrer" target="_blank">YouTube ↗</a></p>
  </div>
</section>""".format(
        paths=paths,
        paths_h="طرق المساهمة" if lang == "ar" else "Ways to contribute",
        how_t=esc(j["how_title"]), how_b=esc(j["how_body"]),
        contact_t=esc(j["contact_title"]), tag=esc(u["status_explainer"]),
        contact_n=esc(j["contact_note"]), yt=SITE["youtube"])

    return page(lang, "join", "join/", body, url(other(lang), "join/"))


def monarchy_page(lang):
    m = MONARCHY[lang]
    u = UI[lang]
    body = pagehead(lang,
                    [(url(lang), u["home"]), (None, m["label"])],
                    m["label"], m["title"])

    examples = "\n      ".join(
        "<li><strong>{}</strong> — {}</li>".format(esc(t), esc(b)) for t, b in m["examples"])

    body += """<section class="bay bay--raised">
  <div class="shell shell--narrow prose">
    {paras}

    <h2>{q_title}</h2>
    <p>{q_lead}</p>
    <ul class="marks">
      {questions}
    </ul>

    <h2>{w_title}</h2>
    <p>{w_lead}</p>
    <ul class="marks">
      {examples}
    </ul>
    <p>{w_close}</p>

    <p style="margin-block-start:2.4rem"><a class="btn btn--outline" href="{bus}">{bus_label}</a></p>
  </div>
</section>""".format(
        paras="\n    ".join("<p>{}</p>".format(esc(p)) for p in m["body"]),
        q_title=esc(m["questions_title"]), q_lead=esc(m["questions_lead"]),
        questions="\n      ".join("<li>{}</li>".format(esc(q)) for q in m["questions"]),
        w_title="دروس موثقة" if lang == "ar" else "Documented lessons",
        w_lead=esc(m["warning_lead"]), examples=examples, w_close=esc(m["warning_close"]),
        bus=url(lang, "bus/"),
        bus_label="حافلة المغرب" if lang == "ar" else "The Morocco Bus")

    return page(lang, "monarchy", "monarchy/", body, url(other(lang), "monarchy/"))


def bus_page(lang):
    u = UI[lang]
    b = BUS[lang]
    body = pagehead(lang,
                    [(url(lang), u["home"]), (None, b["label"])],
                    b["label"], b["title"])
    body += bus_block(lang, full=True)
    return page(lang, "bus", "bus/", body, url(other(lang), "bus/"))


def accountability_page(lang):
    a = ACCOUNTABILITY[lang]
    u = UI[lang]
    ladder = "\n      ".join(
        """<div class="ladder__step">
        <span class="ladder__rank">{r}</span>
        <p class="ladder__body">{b}</p>
      </div>""".format(r=esc(r), b=esc(bb)) for r, bb in a["ladder"])

    body = pagehead(lang,
                    [(url(lang), u["home"]), (None, a["label"])],
                    a["label"], a["title"], a["summary"])

    body += """<section class="bay bay--raised">
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

    <p class="label" style="margin-block-start:3rem">{closing_label}</p>
    <p style="font-family:var(--display);font-size:var(--step-2);color:var(--green)">{closing}</p>
  </div>
</section>""".format(
        tag=esc(u["status_explainer"]), disclaimer=esc(a["disclaimer"]),
        ladder_title=esc(a["ladder_title"]), ladder=ladder,
        paras="\n    ".join("<p>{}</p>".format(esc(p)) for p in a["body"]),
        fw_title=esc(a["framework_title"]), fw_lead=esc(a["framework_lead"]),
        fw_questions="\n      ".join("<li>{}</li>".format(esc(q)) for q in a["framework_questions"]),
        pr_title=esc(a["protection_title"]),
        pr_body="\n    ".join("<p>{}</p>".format(esc(p)) for p in a["protection_body"]),
        closing_label="خلاصة" if lang == "ar" else "In short",
        closing=esc(a["closing"]))

    return page(lang, "accountability", "accountability/", body,
                url(other(lang), "accountability/"))


# ---------------------------------------------------------------- writing

def write(path, content):
    full = os.path.join(DIST, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    return full


def build():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    for sub in ("css", "js", "img", "fonts"):
        src = os.path.join(STATIC, sub)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(DIST, sub))

    count = 0
    for lang in LANGS:
        write("{}/index.html".format(lang), home(lang)); count += 1
        write("{}/about/index.html".format(lang), about_page(lang)); count += 1
        write("{}/doctrines/index.html".format(lang), doctrines_index(lang)); count += 1
        for d in DOCTRINES:
            write("{}/doctrines/{}/index.html".format(lang, d["slug"]),
                  doctrine_page(lang, d)); count += 1
        write("{}/vision/index.html".format(lang), vision_page(lang)); count += 1
        write("{}/news/index.html".format(lang), news_index(lang)); count += 1
        write("{}/news/{}/index.html".format(lang, NEWS_FEATURED["slug"]),
              news_article(lang)); count += 1
        write("{}/founder/index.html".format(lang), founder_page(lang)); count += 1
        write("{}/join/index.html".format(lang), join_page(lang)); count += 1
        write("{}/monarchy/index.html".format(lang), monarchy_page(lang)); count += 1
        write("{}/bus/index.html".format(lang), bus_page(lang)); count += 1
        write("{}/accountability/index.html".format(lang), accountability_page(lang)); count += 1

    # Root: send visitors to Arabic, the primary experience.
    write("index.html", """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>حزب اليمين المغربي — The Moroccan Right Party</title>
<meta http-equiv="refresh" content="0; url=/ar/">
<link rel="canonical" href="https://{d}/ar/">
<meta name="robots" content="noindex">
</head>
<body>
<p><a href="/ar/">العربية</a> · <a href="/en/">English</a></p>
<script>location.replace("/ar/");</script>
</body>
</html>
""".format(d=SITE["domain"]))
    count += 1

    # sitemap + robots
    urls = []
    for lang in LANGS:
        paths = ["", "about/", "doctrines/", "vision/", "news/",
                 "news/{}/".format(NEWS_FEATURED["slug"]), "founder/", "join/",
                 "monarchy/", "bus/", "accountability/"]
        paths += ["doctrines/{}/".format(d["slug"]) for d in DOCTRINES]
        urls += [url(lang, p) for p in paths]

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u_ in sorted(urls):
        sitemap.append("  <url><loc>https://{}{}</loc></url>".format(SITE["domain"], u_))
    sitemap.append("</urlset>")
    write("sitemap.xml", "\n".join(sitemap) + "\n")

    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: https://{}/sitemap.xml\n".format(
        SITE["domain"]))

    print("built {} pages + {} urls in sitemap".format(count, len(urls)))


if __name__ == "__main__":
    build()
