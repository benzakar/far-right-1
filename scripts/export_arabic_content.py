#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يصدر كل النص العربي ديال الموقع لملف واحد سهل القراية، للأرشيف.

بلا HTML، بلا كود، غير العناوين والفقرات بالترتيب اللي كتبان بيه فالموقع.

    python3 scripts/export_arabic_content.py > site-content-archive.txt
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from content.site import (  # noqa: E402
    SITE, UI, NAV, CINEMA, WHO, NEWS_FEATURED, VISION, BUS, MONARCHY,
    ACCOUNTABILITY, FOUNDER, JOIN, PETITION, DECLARATION, FOOTER, META,
)
from content.doctrines import DOCTRINES  # noqa: E402

OUT = []


def h(title, level=1):
    OUT.append("")
    OUT.append("=" * 70 if level == 1 else "-" * 70)
    OUT.append(title)
    OUT.append("=" * 70 if level == 1 else "-" * 70)


def p(*lines):
    for l in lines:
        if isinstance(l, (list, tuple)):
            for x in l:
                OUT.append("- " + str(x))
        else:
            OUT.append(str(l))
        OUT.append("")


def kv(label, value):
    OUT.append("[{}] {}".format(label, value))
    OUT.append("")


# ---------------------------------------------------------------- الغلاف

OUT.append("أرشيف محتوى موقع {}".format(UI["party_name"]))
OUT.append("الدومين: {}".format(SITE["domain"]))
OUT.append("قناة يوتيوب: {}".format(SITE["youtube"]))
OUT.append("رابط العريضة: {}".format(SITE["petition"]))
OUT.append("")
OUT.append("هاد الملف فيه كل النص العربي اللي كاين فالموقع: العناوين، الفقرات،")
OUT.append("العقائد، والنصوص القانونية. ماشي كود، وماشي HTML.")

# ---------------------------------------------------------------- المينيو

h("المينيو الرئيسي")
p([label for _, label in NAV])

# ---------------------------------------------------------------- الواجهة السينمائية

h("الواجهة السينمائية (الصفحة الرئيسية)")
kv("الجملة الأولى", CINEMA["line_1"])
kv("الجملة الثانية", CINEMA["line_2"])
kv("الشعار", CINEMA["slogan"])

# ---------------------------------------------------------------- شكون حنا

h("شكون حنا")
kv("العنوان", WHO["title"])
p(WHO["lead"])
h("علاش حنا مختلفين", level=2)
for title, body in WHO["distinctions"]:
    OUT.append("• " + title)
    OUT.append("  " + body)
    OUT.append("")

# ---------------------------------------------------------------- الأخبار

h("الخبر الرئيسي")
kv("التصنيف", NEWS_FEATURED["kicker"])
kv("العنوان", NEWS_FEATURED["title"])
p(NEWS_FEATURED["standfirst"])
kv("حالة الملف", NEWS_FEATURED["status_note"])
p(NEWS_FEATURED["body"])
h("الجهات اللي الحزب كيعتزم يراسلها", level=2)
p(NEWS_FEATURED["outreach"])
p(NEWS_FEATURED["outreach_note"])

# ---------------------------------------------------------------- الرؤية

h("مغرب ما بعد 2030")
kv("العنوان", VISION["title"])
p(VISION["lead"])
h("ركائز الرؤية", level=2)
for title, body in VISION["pillars"]:
    OUT.append("• " + title)
    OUT.append("  " + body)
    OUT.append("")
h(VISION["plan_title"], level=2)
p(VISION["plan_lead"])
p(VISION["plan_body"])
h(VISION["example_title"], level=2)
p(VISION["example_body"])

# ---------------------------------------------------------------- حافلة المغرب

h("حافلة المغرب")
kv("العنوان", BUS["title"])
p(BUS["lead"])
for stage in BUS["stages"]:
    h(stage["role"] + " — " + stage["subtitle"], level=2)
    p(stage["body"])
    OUT.append(stage["requirements_label"] + ":")
    p(stage["requirements"])
h(BUS["note_title"], level=2)
p(BUS["note_body"])
h("الإعلان الأخير", level=2)
p(BUS["closing"])

# ---------------------------------------------------------------- الملكية

h("الملكية والاستمرارية")
kv("العنوان", MONARCHY["title"])
p(MONARCHY["body"])
h(MONARCHY["questions_title"], level=2)
p(MONARCHY["questions_lead"])
p(MONARCHY["questions"])
h("دروس موثقة", level=2)
p(MONARCHY["warning_lead"])
for country, note in MONARCHY["examples"]:
    OUT.append("• {}: {}".format(country, note))
OUT.append("")
p(MONARCHY["warning_close"])

# ---------------------------------------------------------------- المساءلة

h("المساءلة والأدلة")
kv("العنوان", ACCOUNTABILITY["title"])
p(ACCOUNTABILITY["summary"])
kv("تنبيه", ACCOUNTABILITY["disclaimer"])
h(ACCOUNTABILITY["ladder_title"], level=2)
for rank, body in ACCOUNTABILITY["ladder"]:
    OUT.append("• {}: {}".format(rank, body))
OUT.append("")
p(ACCOUNTABILITY["body"])
h(ACCOUNTABILITY["framework_title"], level=2)
p(ACCOUNTABILITY["framework_lead"])
p(ACCOUNTABILITY["framework_questions"])
h(ACCOUNTABILITY["protection_title"], level=2)
p(ACCOUNTABILITY["protection_body"])
kv("خلاصة", ACCOUNTABILITY["closing"])

# ---------------------------------------------------------------- المؤسس

h("رسالة المؤسس — " + FOUNDER["name"])
p(FOUNDER["standfirst"])
p(FOUNDER["message"])

# ---------------------------------------------------------------- العريضة

h("العريضة")
kv("العنوان", PETITION["title"])
p(PETITION["lead"])
p(PETITION["body"])
kv("الرابط", SITE["petition"])

# ---------------------------------------------------------------- انضم لينا

h("انضم لينا")
kv("العنوان", JOIN["title"])
p(JOIN["lead"])
h("طرق المساهمة", level=2)
for title, body in JOIN["paths"]:
    OUT.append("• " + title)
    OUT.append("  " + body)
    OUT.append("")
h(JOIN["how_title"], level=2)
p(JOIN["how_body"])
h(JOIN["contact_title"], level=2)
p(JOIN["contact_note"])

# ---------------------------------------------------------------- الإعلان

h("الإعلان الأخير")
p(DECLARATION["lines"])

# ---------------------------------------------------------------- العقائد

h("العقائد العشرة", level=1)
for d in DOCTRINES:
    h("{:02d}. {}".format(d["order"], d["name"]), level=2)
    kv("الإعلان", d["declaration"])
    kv("الملخص", d["summary"])
    kv("الشعار", d["slogan"])
    OUT.append("المقدمة:")
    p(d["intro"])
    OUT.append("المشكل:")
    p(d["problem"])
    OUT.append("علاش ما تحلاش:")
    p(d["why_failed"])
    OUT.append("شنو كنؤمنو بيه:")
    p(d["belief"])
    OUT.append("الحل اللي كنقترحو:")
    p(d["solution"])
    OUT.append("كيفاش كنقيسو النجاح:")
    p(d["measures"])
    OUT.append("شنو كيعني هادشي للمواطن:")
    p(d["citizens"])
    OUT.append("مغرب ما بعد 2030:")
    p(d["beyond"])
    OUT.append("الالتزام ديالنا:")
    p(d["commitment"])

# ---------------------------------------------------------------- الفوتر

h("الفوتر", level=1)
p(FOOTER["tagline"])
h(FOOTER["legal_title"], level=2)
p(FOOTER["legal"])
kv("الحقوق", FOOTER["rights"])

# ---------------------------------------------------------------- عناوين الصفحات ومواصفاتها

h("عناوين الصفحات والوصف (meta)", level=1)
for key, (title, desc) in META.items():
    OUT.append("[{}]".format(key))
    OUT.append("العنوان: " + title)
    OUT.append("الوصف: " + desc)
    OUT.append("")

print("\n".join(OUT))
