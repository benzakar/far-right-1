#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""مولّد الموقع ديال حزب اليمين المغربي.

بلا أي تبعية خارج المكتبة القياسية ديال بايثون. للتشغيل:

    python3 build.py

المخرجات كتمشي لـ dist/ ويقدر يخدمها أي استضافة ثابتة.
الموقع بالمغربية فقط، من اليمين للشمال.
"""

import html
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content.site import (  # noqa: E402
    SITE, UI, NAV, HERO, WHO, NEWS_FEATURED, VISION, BUS, MONARCHY,
    ACCOUNTABILITY, FOUNDER, JOIN, DECLARATION, FOOTER, META, PETITION,
)
from content.doctrines import DOCTRINES, FEATURED  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
STATIC = os.path.join(ROOT, "static")

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


def url(path=""):
    return "{}/{}".format(BASE, path)


# ---------------------------------------------------------------- الهيكل

def head(title, desc, canonical, hero=False):
    critical = ["reem-kufi-700-arabic.woff2", "ibm-plex-sans-arabic-400-arabic.woff2"]
    preloads = "\n".join(
        '  <link rel="preload" href="{}" as="font" type="font/woff2" crossorigin>'.format(
            asset("/fonts/" + f))
        for f in critical
    )
    return """<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{origin}{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:locale" content="ar_MA">
  <meta property="og:url" content="{origin}{canonical}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#F3EDE1">
  <link rel="icon" href="{favicon}" type="image/svg+xml">
{preloads}
  <link rel="stylesheet" href="{fontcss}">
  <link rel="stylesheet" href="{sitecss}">
</head>
<body{hero_attr}>
<a class="skip" href="#main">{skip}</a>
<div class="axis" aria-hidden="true"></div>
""".format(
        title=esc(title), desc=esc(desc), origin=ORIGIN, canonical=canonical,
        favicon=asset("/img/party-logo.svg"),
        fontcss=asset("/css/fonts-ar.css"), sitecss=asset("/css/site.css"),
        preloads=preloads, skip=esc(UI["skip"]),
        hero_attr=' data-hero-page' if hero else '',
    )


def masthead(active):
    items = []
    for path, label in NAV:
        cur = ' aria-current="page"' if path == active else ""
        items.append('<a class="nav__link" href="{}"{}>{}</a>'.format(
            url(path), cur, esc(label)))
    return """<header class="masthead" data-masthead>
  <div class="shell masthead__inner">
    <a class="wordmark" href="{home}">
      <img class="wordmark__mark" src="{logo}" alt="" width="34" height="47" loading="eager">
      <span class="wordmark__text">{name}</span>
    </a>
    <button class="burger" type="button" data-burger aria-expanded="false" aria-controls="sitenav"
            data-label-menu="{menu}" data-label-close="{close}">{menu}</button>
    <nav class="nav" id="sitenav" data-nav aria-label="{name}">
      {items}
    </nav>
  </div>
</header>
""".format(home=url(), logo=asset("/img/party-logo.svg"),
           name=esc(UI["party_name"]), menu=esc(UI["menu"]), close=esc(UI["close"]),
           items="\n      ".join(items))


def footer():
    links = [(p, l) for p, l in NAV] + [
        ("monarchy/", "الملكية والاستمرارية"),
        ("bus/", "حافلة المغرب"),
        ("accountability/", "المساءلة والأدلة"),
    ]
    nav_html = "\n      ".join(
        '<a href="{}">{}</a>'.format(url(p), esc(l)) for p, l in links)
    legal = "\n        ".join("<li>{}</li>".format(esc(x)) for x in FOOTER["legal"])
    return """<footer class="footer">
  <div class="shell">
    <div class="footer__top">
      <div>
        <img class="footer__mark" src="{logo}" alt="{logo_alt}" width="96" height="133" loading="lazy">
        <p class="footer__tagline">{tagline}</p>
      </div>
      <div>
        <nav class="footer__nav" aria-label="{name}">
      {nav}
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
<script src="{navjs}" defer></script>
<script src="{motionjs}" defer></script>
</body>
</html>
""".format(logo=asset("/img/party-logo.svg"), logo_alt=esc(UI["logo_alt"]),
           tagline=esc(FOOTER["tagline"]), name=esc(UI["party_name"]), nav=nav_html,
           legal_title=esc(FOOTER["legal_title"]), legal=legal,
           rights=esc(FOOTER["rights"]), yt=SITE["youtube"],
           navjs=asset("/js/nav.js"), motionjs=asset("/js/motion.js"))


def page(key, active, body, hero=False):
    title, desc = META[key]
    return (head(title, desc, url(active), hero=hero)
            + masthead(active)
            + '<main id="main">\n' + body + "\n</main>\n"
            + footer())


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
    return """<section class="pagehead">
  <div class="shell">
    {crumbs}
    <p class="label" style="margin-block-start:1.4rem">{label}</p>
    <h1 class="pagehead__title">{title}</h1>
    {sf}
  </div>
</section>
""".format(crumbs=crumbs(trail), label=esc(label), title=esc(title), sf=sf)


# ------------------------------------------------------------------ الواجهة

def hero_block():
    def srcset(name):
        return ", ".join(asset("/img/{}-{}.jpg".format(name, w)) + " {}w".format(w)
                         for w in (800, 1200, 1600, 2200, 2752))

    return """<section class="hero" data-hero>
  <div class="hero__media">
    <figure class="hero__half hero__half--left" style="margin:0">
      <img data-hero-img src="{src_left}"
           srcset="{ss_left}" sizes="(max-width: 820px) 100vw, 50vw"
           width="2752" height="1536" alt="{alt_left}" fetchpriority="high" decoding="async">
    </figure>
    <figure class="hero__half hero__half--right" style="margin:0">
      <img data-hero-img src="{src_right}"
           srcset="{ss_right}" sizes="(max-width: 820px) 100vw, 50vw"
           width="2752" height="1536" alt="{alt_right}" fetchpriority="high" decoding="async">
    </figure>
    <div class="hero__wash" aria-hidden="true"></div>
    <div class="hero__seam" aria-hidden="true"></div>

    <div class="hero__content" data-hero-content>
      <div class="shell">
        <p class="hero__eyebrow">{eyebrow}</p>
        <h1 class="hero__title">{headline}</h1>
        <p class="hero__slogan">{slogan}</p>
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
""".format(src_left=asset("/img/hero-abdullah-ben-zakar-1600.jpg"),
           src_right=asset("/img/hero-moroccan-monarch-1600.jpg"),
           ss_left=srcset("hero-abdullah-ben-zakar"),
           ss_right=srcset("hero-moroccan-monarch"),
           alt_left=esc(UI["hero_left_alt"]), alt_right=esc(UI["hero_right_alt"]),
           eyebrow=esc(HERO["eyebrow"]), headline=esc(HERO["headline"]),
           slogan=esc(HERO["slogan"]), declaration=esc(HERO["declaration"]),
           doctrines=url("doctrines/"), join=url("join/"),
           cta1=esc(HERO["cta_primary"]), cta2=esc(HERO["cta_secondary"]),
           scroll=esc(UI["scroll"]))


BUS_SVG = """<svg class="road__bus" viewBox="0 0 80 34" fill="none" aria-hidden="true" focusable="false">
  <path d="M3 26V10a4 4 0 0 1 4-4h49l18 11v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"
        fill="#F3EDE1" stroke="#A8823C" stroke-width="1.2"/>
  <path d="M10 10h13v8H10zM27 10h13v8H27zM44 10h11l9 8H44z" fill="#14503A" opacity=".85"/>
  <circle cx="20" cy="29" r="4" fill="#2A241B" stroke="#A8823C" stroke-width="1"/>
  <circle cx="60" cy="29" r="4" fill="#2A241B" stroke="#A8823C" stroke-width="1"/>
</svg>"""


def bus_block(full=False):
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
""".format(label=esc(BUS["label"]), title=esc(BUS["title"]), lead=esc(BUS["lead"]),
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


def _folio_grid(doctrines):
    return "\n      ".join(
        """<a class="folio" href="{href}" data-reveal="{d}">
        <span class="folio__index">{idx:02d}</span>
        <span class="folio__name">{name}</span>
        <p class="folio__summary">{summary}</p>
        <span class="folio__more">{more}</span>
      </a>""".format(href=url("doctrines/{}/".format(d_["slug"])), d=i * 60,
                     idx=d_["order"], name=esc(d_["name"]),
                     summary=esc(d_["summary"]), more=esc(UI["read_more"]))
        for i, d_ in enumerate(doctrines))


def petition_block(compact=False, level=3):
    """The petition card.

    `compact` is the homepage variant. `level` is the heading level: on
    the homepage the card sits under a section h2 so it is an h3; on the
    join page it is the first thing after the page h1, so it is an h2.
    """
    paras = "" if compact else "\n    ".join(
        "<p>{}</p>".format(esc(p)) for p in PETITION["body"])
    return """<div class="petition" data-reveal>
    <p class="petition__kicker">{kicker} · {host}</p>
    <h{lvl} class="petition__title">{title}</h{lvl}>
    <p class="petition__lead">{lead}</p>
    {paras}
    <div class="petition__actions">
      <a class="btn btn--primary" href="{href}" rel="noopener noreferrer" target="_blank">{cta} \u2197</a>
      <p class="petition__note">{note}</p>
    </div>
  </div>""".format(lvl=level, kicker=esc(PETITION["kicker"]), host=esc(PETITION["host"]),
                   title=esc(PETITION["title"]), lead=esc(PETITION["lead"]),
                   paras=paras, href=SITE["petition"], cta=esc(PETITION["cta"]),
                   note=esc(PETITION["note"]))


def home():
    rows = "\n    ".join(
        """<div class="ledger__row" data-reveal="{d}">
      <p class="ledger__term">{t}</p>
      <p class="ledger__def">{b}</p>
    </div>""".format(d=i * 70, t=esc(t), b=esc(b))
        for i, (t, b) in enumerate(WHO["distinctions"]))

    roster = "\n        ".join("<li>{}</li>".format(esc(c))
                              for c in NEWS_FEATURED["outreach"])

    ladder = "\n      ".join(
        """<div class="ladder__step">
        <span class="ladder__rank">{r}</span>
        <p class="ladder__body">{b}</p>
      </div>""".format(r=esc(r), b=esc(b)) for r, b in ACCOUNTABILITY["ladder"])

    dec_lines = "\n      ".join(
        '<p class="declaration__line">{}</p>'.format(esc(l))
        for l in DECLARATION["lines"])

    parts = [hero_block()]

    parts.append("""<section class="bay bay--raised bay--overlap">
  <div class="shell">
    <p class="label" data-rise="30">{label}</p>
    <h2 class="bay__title" data-rise="46">{title}</h2>
    <p class="bay__lead" data-rise="36">{lead}</p>
    <div class="ledger">
    {rows}
    </div>
  </div>
</section>""".format(label=esc(WHO["label"]), title=esc(WHO["title"]),
                     lead=esc(WHO["lead"]), rows=rows))

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
</section>""".format(kicker=esc(NEWS_FEATURED["kicker"]),
                     title=esc(NEWS_FEATURED["title"]),
                     standfirst=esc(NEWS_FEATURED["standfirst"]),
                     tag=esc(UI["status_proposal"]),
                     status=esc(NEWS_FEATURED["status_note"]),
                     href=url("news/{}/".format(NEWS_FEATURED["slug"])),
                     more=esc(UI["more"]),
                     roster_label=esc(NEWS_FEATURED["outreach_label"]),
                     roster=roster,
                     roster_note=esc(NEWS_FEATURED["outreach_note"])))

    parts.append("""<section class="bay bay--recessed">
  <div class="shell">
    <p class="label" data-rise="30">عقائدنا</p>
    <h2 class="bay__title" data-rise="46">عشر عقائد، ماشي عشر شعارات</h2>
    <p class="bay__lead" data-rise="36">كل عقيدة كتبدا من مشكل مغربي محدد، وكتسالي بالتزام يمكن يتقاس.</p>
    <div class="folios">
      {folios}
    </div>
    <p style="margin-block-start:2.4rem"><a class="btn btn--outline" href="{href}">{all}</a></p>
  </div>
</section>""".format(folios=_folio_grid(FEATURED), href=url("doctrines/"),
                     all=esc(UI["back_to_doctrines"])))

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
</section>""".format(label=esc(VISION["label"]), title=esc(VISION["title"]),
                     lead=esc(VISION["lead"]), pillars=_pillar_grid(VISION["pillars"]),
                     href=url("vision/"), more=esc(UI["more"])))

    parts.append(bus_block())

    parts.append("""<section class="bay bay--recessed">
  <div class="shell shell--narrow">
    <p class="label" data-rise="30">{label}</p>
    <h2 class="bay__title" data-rise="46">{title}</h2>
    <p class="bay__lead" data-rise="36">{p1}</p>
    <p style="margin-block-start:1.6rem">{p2}</p>
    <p><a class="btn btn--outline" href="{href}">{more}</a></p>
  </div>
</section>""".format(label=esc(MONARCHY["label"]), title=esc(MONARCHY["title"]),
                     p1=esc(MONARCHY["body"][0]), p2=esc(MONARCHY["body"][3]),
                     href=url("monarchy/"), more=esc(UI["more"])))

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
</section>""".format(label=esc(ACCOUNTABILITY["label"]),
                     title=esc(ACCOUNTABILITY["title"]),
                     summary=esc(ACCOUNTABILITY["summary"]),
                     tag=esc(UI["status_explainer"]),
                     disclaimer=esc(ACCOUNTABILITY["disclaimer"]),
                     ladder_title=esc(ACCOUNTABILITY["ladder_title"]),
                     ladder=ladder, href=url("accountability/"), more=esc(UI["more"])))

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
</section>""".format(label=esc(FOUNDER["label"]), title=esc(FOUNDER["title"]),
                     p1=esc(FOUNDER["message"][0]), p2=esc(FOUNDER["message"][2]),
                     p3=esc(FOUNDER["message"][5]), href=url("founder/"),
                     more=esc(UI["more"]), yt=SITE["youtube"],
                     yt_label=esc(FOUNDER["youtube_label"]),
                     yt_note=esc(FOUNDER["youtube_note"])))

    parts.append("""<section class="bay bay--raised">
  <div class="shell">
    <p class="label" data-rise="30">{label}</p>
    <h2 class="bay__title" data-rise="46">{title}</h2>
    <p class="bay__lead" data-rise="36">{lead}</p>
    {petition}
    <div class="pillars" style="margin-block-start:clamp(2.4rem,5vw,3.5rem)">
      {paths}
    </div>
    <p style="margin-block-start:2.6rem"><a class="btn btn--outline" href="{href}">{label}</a></p>
  </div>
</section>""".format(label=esc(JOIN["label"]), title=esc(JOIN["title"]),
                     lead=esc(JOIN["lead"]), petition=petition_block(compact=True),
                     paths=_pillar_grid(JOIN["paths"]), href=url("join/")))

    parts.append("""<section class="bay bay--deep">
  <div class="shell declaration">
    {lines}
    <a class="btn btn--primary" href="{href}">{cta}</a>
  </div>
</section>""".format(lines=dec_lines, href=url("join/"),
                     cta=esc(DECLARATION["cta"])))

    return page("home", "", "\n".join(parts), hero=True)


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

EMBLEM_CAPTION = (
    "شعار الحزب: النافذة المغربية المحلولة، وقدامها لوحة فيها صورة تاريخية. الشعار "
    "حامل الصيغة الإعلامية ديال المشروع؛ أما التسمية الرسمية فهي «حزب اليمين المغربي»."
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

    body += """<section class="bay bay--raised">
  <div class="shell shell--narrow prose">
    <h2>هوية الحزب</h2>
    <ul class="marks">
      {identity}
    </ul>
    <h2>على الاسم</h2>
    <p>{naming}</p>

    <figure class="emblem">
      <img src="{logo}" alt="{logo_alt}" width="300" height="375" loading="lazy">
      <figcaption>{cap}</figcaption>
    </figure>
  </div>
</section>
<section class="bay bay--recessed">
  <div class="shell">
    <p class="label">علاش حنا مختلفين</p>
    <h2 class="bay__title">أربع فروق كتقاس</h2>
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
    <p style="margin-block-start:2rem"><a class="btn btn--outline" href="{vhref}">الرؤية كاملة</a></p>
  </div>
</section>""".format(
        identity="\n      ".join("<li>{}</li>".format(esc(x)) for x in IDENTITY),
        naming=esc(NAMING_NOTE), logo=asset("/img/party-logo.svg"),
        logo_alt=esc(UI["logo_alt"]), cap=esc(EMBLEM_CAPTION), rows=rows,
        plan_title=esc(VISION["plan_title"]), plan_lead=esc(VISION["plan_lead"]),
        plan_body="\n    ".join("<p>{}</p>".format(esc(p)) for p in VISION["plan_body"]),
        vhref=url("vision/"))

    return page("about", "about/", body)


def doctrines_index():
    items = "\n      ".join(
        """<a class="register__item" href="{href}" data-reveal="{d}">
        <span class="register__num">{idx:02d}</span>
        <span class="register__name">{name}</span>
        <p class="register__summary">{summary}</p>
        <span class="register__go">{more}</span>
      </a>""".format(href=url("doctrines/{}/".format(d_["slug"])),
                     d=min(i, 6) * 45, idx=d_["order"], name=esc(d_["name"]),
                     summary=esc(d_["summary"]), more=esc(UI["read_more"]))
        for i, d_ in enumerate(DOCTRINES))

    body = pagehead([(url(), UI["home"]), (None, "عقائدنا")],
                    "عقائدنا", "عشر عقائد، ماشي عشر شعارات",
                    "كل عقيدة كتبدا من مشكل مغربي محدد، وكتشرح علاش ما تحلاش، ومن بعد "
                    "كتقترح حل والتزام يمكن يتقاس.")

    body += """<section class="bay bay--recessed">
  <div class="shell">
    <div class="register">
      {items}
    </div>
  </div>
</section>""".format(items=items)

    return page("doctrines", "doctrines/", body)


DOCTRINE_LABELS = ("المشكل", "علاش ما تحلاش", "شنو كنؤمنو بيه", "الحل اللي كنقترحو",
                   "كيفاش كنقيسو النجاح", "شنو كيعني هادشي للمواطن",
                   "مغرب ما بعد 2030", "الالتزام ديالنا")


def doctrine_page(d):
    body = pagehead([(url(), UI["home"]),
                     (url("doctrines/"), "عقائدنا"),
                     (None, d["name"])],
                    "عقيدة {:02d}".format(d["order"]), d["name"], d["declaration"])

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

    <p class="label" style="margin-block-start:3rem">الشعار</p>
    <p style="font-family:var(--display);font-size:var(--step-2);color:var(--green)">{slogan}</p>
  </div>
</section>
<section class="bay bay--recessed">
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
    return (head(title, d["summary"], canonical)
            + masthead("doctrines/")
            + '<main id="main">\n' + body + "\n</main>\n"
            + footer())


def vision_page():
    body = pagehead([(url(), UI["home"]), (None, VISION["label"])],
                    VISION["label"], VISION["title"], VISION["lead"])

    body += """<section class="bay bay--raised" aria-labelledby="pillars-h">
  <div class="shell">
    <h2 class="vh" id="pillars-h">ركائز الرؤية</h2>
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
    return (head(title, NEWS_FEATURED["standfirst"], canonical)
            + masthead("news/")
            + '<main id="main">\n' + body + "\n</main>\n"
            + footer())


def founder_page():
    body = pagehead([(url(), UI["home"]), (None, FOUNDER["label"])],
                    FOUNDER["label"], FOUNDER["title"], FOUNDER["standfirst"])

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
    <h2>الدور ديالو فالحزب</h2>
    <p>{role}</p>
    <p><a class="btn btn--outline" href="{bus}">حافلة المغرب</a></p>
  </div>
</section>""".format(paras="\n    ".join("<p>{}</p>".format(esc(p))
                                        for p in FOUNDER["message"]),
                     yt=SITE["youtube"], yt_label=esc(FOUNDER["youtube_label"]),
                     yt_note=esc(FOUNDER["youtube_note"]),
                     role=esc(BUS["stages"][1]["body"]), bus=url("bus/"))

    return page("founder", "founder/", body)


def join_page():
    body = pagehead([(url(), UI["home"]), (None, JOIN["label"])],
                    JOIN["label"], JOIN["title"], JOIN["lead"])

    body += """<section class="bay bay--raised">
  <div class="shell shell--narrow">
    {petition}
  </div>
</section>
<section class="bay bay--recessed" aria-labelledby="paths-h">
  <div class="shell">
    <h2 class="vh" id="paths-h">طرق المساهمة</h2>
    <div class="pillars" style="margin-block-start:0">
      {paths}
    </div>
  </div>
</section>
<section class="bay bay--raised">
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

    body += """<section class="bay bay--raised">
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
        ("founder/index.html", founder_page()),
        ("join/index.html", join_page()),
        ("monarchy/index.html", monarchy_page()),
        ("bus/index.html", bus_page()),
        ("accountability/index.html", accountability_page()),
    ]
    for d in DOCTRINES:
        routes.append(("doctrines/{}/index.html".format(d["slug"]), doctrine_page(d)))

    for path, content in routes:
        write(path, content)

    paths = ["", "about/", "doctrines/", "vision/", "news/",
             "news/{}/".format(NEWS_FEATURED["slug"]), "founder/", "join/",
             "monarchy/", "bus/", "accountability/"]
    paths += ["doctrines/{}/".format(d["slug"]) for d in DOCTRINES]

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
