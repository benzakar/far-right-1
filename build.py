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
import os
import shutil
import sys

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

def head(title, desc, canonical, hero=False):
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
""".format(
        title=esc(title), desc=esc(desc), origin=ORIGIN, canonical=canonical,
        favicon=asset("/img/party-logo.svg"),
        fontcss=versioned("/css/fonts-ar.css"), sitecss=versioned("/css/site.css"),
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
            aria-label="{menu}" data-label-menu="{menu}" data-label-close="{close}">
      <span class="burger__icon" aria-hidden="true"><span></span><span></span><span></span></span>
    </button>
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
      <a href="{yt}" rel="noopener noreferrer" target="_blank">يوتيوب ↗</a>
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
           navjs=versioned("/js/nav.js"), motionjs=versioned("/js/motion.js"))


def page(key, active, body, hero=False):
    title, desc = META[key]
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

def cinema_block():
    """The opening sequence.

    One pinned stage. Everything inside is a pure function of how far the
    stage has been scrolled, so the sequence plays identically forwards
    and backwards and can be stopped anywhere in between.
    """
    def srcset(name):
        return ", ".join(asset("/img/{}-{}.jpg".format(name, w)) + " {}w".format(w)
                         for w in (640, 960, 1280))

    return """<section class="cinema" data-cinema>
  <div class="cinema__stage">

    <img class="cinema__bg" data-cine="bg" src="{src}" srcset="{ss}" sizes="100vw"
         width="1280" height="720" alt="{hero_alt}" fetchpriority="high" decoding="async">

    <div class="cinema__dim" data-cine="dim" aria-hidden="true"></div>

    <img class="cinema__scroll-hint" data-cine="hint" src="{arrow}"
         width="500" height="500" alt="" aria-hidden="true" decoding="async">

    <p class="cinema__line" data-cine="line1">{line1}</p>

    <img class="cinema__parties" data-cine="parties" src="{parties}"
         width="1280" height="720" alt="{parties_alt}" loading="eager" decoding="async">

    <p class="cinema__line" data-cine="line2">{line2}</p>

    <img class="cinema__logo" data-cine="logo" src="{logo}"
         width="1280" height="720" alt="{logo_alt}" loading="eager" decoding="async">

    <p class="cinema__slogan" data-cine="slogan">{slogan}</p>

  </div>
</section>
""".format(src=asset("/img/hero6-1280.jpg"), ss=srcset("hero6"),
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


def _image_slot(key, label, compact=False):
    """An intentional empty image plane.

    The visible placeholder keeps the layout finished while the commissioned
    artwork is still being produced. `data-image-slot` is the stable hook used
    when the matching image is uploaded later.
    """
    cls = "media-slot media-slot--compact" if compact else "media-slot"
    return """<div class="{cls}" data-image-slot="{key}" role="img" aria-label="بلاصة مخصصة لصورة {label}">
      <span class="media-slot__ornament" aria-hidden="true"></span>
      <span class="media-slot__label">بلاصة الصورة</span>
      <span class="media-slot__name">{label}</span>
    </div>""".format(cls=cls, key=esc(key), label=esc(label))


def _story_panel(key, image_label, eyebrow, title, body, actions=(), flip=False,
                 panel_id="", level=2, extra=""):
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


def _doctrine_cards(doctrines):
    return "\n      ".join(
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
            idx=d_["order"], name=esc(d_["name"]), summary=esc(d_["summary"]),
            href=url("doctrines/{}/".format(d_["slug"])), more=esc(UI["read_more"]))
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
    dec_lines = "\n      ".join(
        '<p class="declaration__line">{}</p>'.format(esc(l))
        for l in DECLARATION["lines"])

    bronx = next(d for d in DOCTRINES if d["slug"] == "bronx")
    lalla = next(d for d in DOCTRINES if d["slug"] == "lalla-khadija")
    remaining_doctrines = [
        d for d in DOCTRINES if d["slug"] not in ("bronx", "lalla-khadija")
    ]

    about_points = """<ul class="story-panel__points">
          {items}
        </ul>""".format(items="\n          ".join(
            "<li>{}</li>".format(esc(title))
            for title, _ in WHO["distinctions"]))

    example_panels = "\n".join([
        _story_panel(
            "doctrine-bronx", bronx["name"], "المثال اللول", bronx["name"],
            [bronx["summary"], bronx["slogan"]],
            actions=[(url("doctrines/bronx/"), UI["read_more"], False)],
            level=3,
        ),
        _story_panel(
            "doctrine-lalla-khadija", lalla["name"], "المثال الثاني", lalla["name"],
            [lalla["summary"], lalla["slogan"]],
            actions=[(url("doctrines/lalla-khadija/"), UI["read_more"], False)],
            flip=True, level=3,
        ),
        _story_panel(
            "project-taxis", "خطة باء ديال الطاكسيات", "المثال الثالث",
            VISION["example_title"],
            [(
                "خطة باء ديال الطاكسيات كتجمع المأذونيات المنظمة، وحماية السائقين، "
                "والتطبيقات المرخصة، والأثمنة الواضحة، والتأمين، ومراقبة الجودة فمنظومة "
                "وحدة عادلة."
            )],
            actions=[(url("vision/"), "شوف خطة ألف وخطة باء", False)], level=3,
        ),
    ])

    identity_panels = "\n".join([
        _story_panel(
            "section-monarchy", "الملكية والاستمرارية", MONARCHY["label"],
            MONARCHY["title"], [MONARCHY["body"][1]],
            actions=[(url("monarchy/"), UI["more"], False)], flip=True, level=3,
        ),
        _story_panel(
            "about-identity", "هوية الحزب", WHO["label"], WHO["title"],
            [WHO["lead"]],
            actions=[(url("about/"), "تعرف علينا بلا لف ودوران", False)], level=3,
        ),
        _story_panel(
            "about-founder", "عبدالله بن زكار", FOUNDER["label"], FOUNDER["name"],
            [FOUNDER["standfirst"], FOUNDER["message"][5]],
            actions=[
                (url("about/#founder"), "شوف المؤسس وسط قصة الحزب", False),
                (SITE["youtube"], FOUNDER["youtube_label"], True),
            ],
            flip=True, panel_id="founder", level=3,
        ),
    ])

    two_speeds_panel = """<article class="story-panel story-panel--longform" data-reveal>
    <div class="story-panel__visual">
      {slot}
    </div>
    <div class="story-panel__copy">
      <h2 class="story-panel__title">{title}</h2>
      <div class="story-panel__body">
        <p class="story-panel__text">{p1}</p>
        <p class="story-panel__text">{p2}</p>
        <p class="story-panel__text">{p3}</p>
        <h3 class="story-panel__subheading">{subtitle}</h3>
        <p class="story-panel__text">{p4}</p>
        <p class="story-panel__text">{p5}</p>
        <p class="story-panel__text">{p6}</p>
        <p class="story-panel__text story-panel__closing">{p7} <strong>{party}</strong>.</p>
      </div>
    </div>
  </article>""".format(
        slot="""<img class="story-panel__image" src="{}" width="1000" height="1000"
             alt="قصاصة خبر على إلغاء الساعة الإضافية فالمغرب من بعد صيف 2026"
             loading="lazy" decoding="async">""".format(asset("/img/from-002.png")),
        title=esc("باش نقادو مغرب السرعتين، خاصنا مغرب الخطتين"),
        p1=esc("5 سنين ديال بنكيران، و5 ديال العثماني، و5 ديال أخنوش، وفالأخير: كارثة سبتة."),
        p2=esc("دستور 2011 خرّج على البلاد، وأحسن مثال هو مطالبة المواطنين بإلغاء الساعة الإضافية. رغم الوقفات الاحتجاجية والعريضة اللي وقّعها عشرات الآلاف من المغاربة، والمشاكل الصحية اللي عاناو منها المغاربة وأطفالهم، عطى الدستور لذاك الانتهازي ديال أخنوش السلطة باش يلغي الساعة الإضافية فقط من أجل الانتخابات، ماشي من أجل المغاربة."),
        p3=esc("أملنا فـ ولد سيدنا أعزّه الله، وفالدستور اللي الحزب موجد ليه؛ الدستور اللي غادي يحل كاع المشاكل، منها: مشكل الهجرة، والصحة، والتعليم، واللي غادي يهني ولد سيدنا من بنكيران وأخنوش ديال المستقبل."),
        subtitle=esc("علاش دستور 2011 ما صالحش من بعد المونديال؟"),
        p4=esc("زيادة على أن التغيير سنة الحياة، وأن العالم غادي بواحد السرعة كبيرة خاصها دستور خاص، وزيادة على هاد الأسباب، المغاربة كلهم سمعو من بنكيران كيفاش سيدنا كان كيهدر معاه على البلوكاج الحكومي."),
        p5=esc("سيدنا عيا مع حكومات الأحزاب، وعيا ما ينبه ويوجّه فالخطابات ديالو."),
        p6=esc("حنا جايين باش ولد سيدنا يلقى حزب كيهنيه من صداع المناورات السياسية، ومن أي بلوكاج حكومي مستقبلي. الحزب هو مشروع مغربي، داعم للملكية، رأسمالي ومنتج، كيبدا من المشكل ماشي من الكرسي."),
        p7=esc("ما كنطلبوش من المغاربة يصدقونا بالسمع؛ كنطلبو منهم يشوفو بعينيهم الفرق الواضح ما بين 36 حزب ديال الهضرة، وحزب ديال الابتكار والخدمة:"),
        party=esc("حزب اليمين المغربي"),
    )

    # Concrete proposals lead the homepage. The Bus remains available later as
    # a summary metaphor, after visitors understand Plan A/B and see examples.
    parts = [cinema_block()]

    parts.append("""<section class="bay bay--greenback" id="two-speeds-plans" data-parallax-bg>
  <div class="shell">
    <div class="story-reader story-reader--flush">
      {panel}
    </div>
  </div>
</section>""".format(panel=two_speeds_panel))

    parts.append("""<section class="bay bay--redback" id="plan-a-b" data-parallax-bg>
  <div class="shell">
    <p class="label" data-rise="30">من هنا كتبدا الفكرة</p>
    <h2 class="bay__title" data-rise="46">خطة ألف وخطة باء</h2>
    <p class="bay__lead" data-rise="36">خطة ألف كتوجد المغرب للمسار المتوقع. خطة باء كتوجد المغرب للي ما كانش فالحساب.</p>
    <div class="story-reader">
      {panel}
    </div>
  </div>
</section>""".format(panel=_story_panel(
    "section-vision", "خطة ألف وخطة باء", VISION["label"], VISION["plan_title"],
    [VISION["plan_lead"]],
    actions=[(url("vision/"), "شوف الرؤية كاملة", False)], level=3)))

    parts.append("""<section class="bay bay--greenback" id="examples" data-parallax-bg>
  <div class="shell">
    <p class="label" data-rise="30">من الفكرة للمشروع</p>
    <h2 class="bay__title" data-rise="46">ثلاثة أمثلة كيبينو كيفاش كنفكرو</h2>
    <p class="bay__lead" data-rise="36">ماشي شعارات عامة: كل مثال كيبدا من مشكل باين، وكيقترح تصميم يمكن يتجرب ويتقاس.</p>
    <div class="story-reader">
      {panels}
    </div>
    <div class="status" data-reveal>
      <span class="status__tag">اللي جاي</span>
      <p>وهادي غير البداية. عقائد ومشاريع أخرى كيبانو لتحت، وأخرى غادي تزيد من بعد.</p>
    </div>
  </div>
</section>""".format(panels=example_panels))

    parts.append("""<section class="bay bay--redback" id="latest-news" data-parallax-bg>
  <div class="shell">
    <p class="label" data-rise="30">آخر المستجدات</p>
    <h2 class="bay__title" data-rise="46">شنو واقع دابا</h2>
    <p class="bay__lead" data-rise="36">الخبر كيتنشر ملي يتأكد. دابا هادي مبادرة فمرحلة التحضير، ماشي لقاء وقع.</p>
    <div class="story-reader">
      {panel}
    </div>
  </div>
</section>""".format(panel=_story_panel(
    "news-immigration-equality", "المساواة فالهجرة", "آخر المستجدات · 10 غشت 2026",
    NEWS_FEATURED["title"], [NEWS_FEATURED["standfirst"], NEWS_FEATURED["status_note"]],
    actions=[(url("news/{}/".format(NEWS_FEATURED["slug"])), UI["more"], False)],
    flip=True, level=3)))

    parts.append("""<section class="bay bay--greenback" id="about" data-parallax-bg>
  <div class="shell">
    <p class="label" data-rise="30">الموقف والهوية</p>
    <h2 class="bay__title" data-rise="46">حنا شكون، وشنو كيميزنا</h2>
    <p class="bay__lead" data-rise="36">البراركية، هوية الحزب، والمؤسس مجموعين هنا بلا ما يتفرّقو على الزائر.</p>
    <div class="story-reader">
      {panels}
    </div>
  </div>
</section>""".format(panels=identity_panels))

    parts.append("""<section class="bay bay--redback" id="doctrines" data-parallax-bg>
  <div class="shell">
    <p class="label" data-rise="30">باقي العقائد</p>
    <h2 class="bay__title" data-rise="46">الفكرة فالخلاصة، والتفاصيل اختيارية</h2>
    <p class="bay__lead" data-rise="36">شفتي البرونكس ولالة خديجة. هنا باقي العقائد فبطاقات قصيرة.</p>
    <p class="doctrine-cards__hint">جرّ البطاقات باش تشوف الباقي</p>
    <div class="doctrine-cards">
      {cards}
    </div>
  </div>
</section>""".format(cards=_doctrine_cards(remaining_doctrines)))

    parts.append("""<section class="bay bay--greenback" id="bus-summary" data-parallax-bg>
  <div class="shell">
    <div class="story-reader">
      {panel}
    </div>
  </div>
</section>""".format(panel=_story_panel(
    "section-bus", "حافلة المغرب", BUS["label"], BUS["title"], [BUS["lead"]],
    actions=[(url("bus/"), "شوف حافلة المغرب", False)], flip=True)))

    parts.append("""<section class="bay bay--redback" id="accountability" data-parallax-bg>
  <div class="shell">
    <p class="label" data-rise="30">كيفاش غادي تحاسبونا</p>
    <h2 class="bay__title" data-rise="46">القياس قبل الثقة</h2>
    <p class="bay__lead" data-rise="36">الفرق ماشي فالنوايا. الفرق فالحل، والتجربة، والنتيجة اللي كتتنشر.</p>
    <div class="story-reader">
      {panel}
    </div>
  </div>
</section>""".format(panel=_story_panel(
    "section-accountability", "المساءلة والنتائج", ACCOUNTABILITY["label"],
    ACCOUNTABILITY["title"], [ACCOUNTABILITY["summary"]],
    actions=[(url("accountability/"), UI["more"], False)],
    extra=about_points, level=3)))

    parts.append("""<section class="bay bay--greenback" data-parallax-bg>
  <div class="shell">
    <div class="story-reader">
      {panel}
    </div>
    {petition}
  </div>
</section>""".format(panel=_story_panel(
    "section-join", "الحركة والبنّايين", JOIN["label"], JOIN["title"], [JOIN["lead"]],
    actions=[(url("join/"), JOIN["label"], False)]),
    petition=petition_block(compact=True)))

    parts.append("""<section class="bay bay--deep bay--greenback" data-parallax-bg>
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

    body += """<section class="bay bay--raised">
  <div class="shell">
    <div class="story-reader">
      {about_story}
    </div>
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

    body += """<section class="bay bay--recessed">
  <div class="shell">
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
        ("founder/index.html", redirect_page(url("about/#founder"), url("about/"))),
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
             "news/{}/".format(NEWS_FEATURED["slug"]), "join/",
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
