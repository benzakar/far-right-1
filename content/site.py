# -*- coding: utf-8 -*-
"""Bilingual site content.

Arabic is the primary experience. English is an authored international
adaptation, not a mechanical translation.

Editorial rules enforced throughout this file:
  * Invitations are labelled as invitations, proposals as proposals.
  * No named third party is presented as having accepted, endorsed, or
    joined the party. Roles in the Morocco Bus are described by what the
    role requires; the party names no invitee it has not publicly
    confirmed. The founder is named because he names himself.
  * The accountability framework is explanatory. It describes how
    allegations should be handled and names no subject of any allegation.
  * No invented statistics, endorsements, meetings, or memberships.
"""

SITE = {
    "domain": "fromparty.com",
    "youtube": "https://www.youtube.com/@BenZakarMinus",
    "founder_ar": "عبدالله بن زكار",
    "founder_en": "Abdullah Ben Zakar",
}

# --- Interface strings -------------------------------------------------

UI = {
    "ar": {
        "party_name": "حزب اليمين المغربي",
        "party_short": "اليمين المغربي",
        "skip": "تخطَّ إلى المحتوى",
        "menu": "القائمة",
        "close": "إغلاق",
        "lang_switch": "English",
        "lang_switch_label": "التبديل إلى الإنجليزية",
        "read_more": "اقرأ العقيدة كاملة",
        "back_to_doctrines": "كل العقائد",
        "home": "الرئيسية",
        "scroll": "تابع النزول",
        "on_this_page": "في هذه الصفحة",
        "status_proposal": "اقتراح",
        "status_invitation": "دعوة معلنة",
        "status_position": "موقف الحزب",
        "status_explainer": "شرح",
        "published": "نُشر",
        "logo_alt": (
            "شعار الحزب: نافذة مغربية حمراء مفتوحة تحمل اسم الحزب وعنوان "
            "fromparty.com، وأمامها لوحة خشبية صغيرة تحمل صورة تاريخية."
        ),
        "hero_left_alt": (
            "منحوتة عاجية ثلاثية الأبعاد لعبدالله بن زكار بالبذلة أمام جدار "
            "مغربي منقوش يحمل شعار المملكة والأسدين والتاج."
        ),
        "hero_right_alt": (
            "منحوتة عاجية ثلاثية الأبعاد تصور العاهل المغربي أمام شعار المملكة "
            "المنحوت بالأسد والتاج والنجمة الخضراء."
        ),
    },
    "en": {
        "party_name": "The Moroccan Right Party",
        "party_short": "Moroccan Right",
        "skip": "Skip to content",
        "menu": "Menu",
        "close": "Close",
        "lang_switch": "العربية",
        "lang_switch_label": "Switch to Arabic",
        "read_more": "Explore the doctrine",
        "back_to_doctrines": "All doctrines",
        "home": "Home",
        "scroll": "Scroll",
        "on_this_page": "On this page",
        "status_proposal": "Proposal",
        "status_invitation": "Public invitation",
        "status_position": "Party position",
        "status_explainer": "Explainer",
        "published": "Published",
        "logo_alt": (
            "Party emblem: an open red Moroccan window carrying the party name and "
            "the address fromparty.com, with a small wooden stand holding a "
            "historical portrait in front of it."
        ),
        "hero_left_alt": (
            "Three-dimensional ivory sculpture of Abdullah Ben Zakar in a suit before "
            "a carved Moroccan wall bearing the royal coat of arms with two lions and a crown."
        ),
        "hero_right_alt": (
            "Three-dimensional ivory sculpture depicting the Moroccan monarch before the "
            "carved royal coat of arms with its lion, crown and green star."
        ),
    },
}

NAV = {
    "ar": [
        ("", "الرئيسية"),
        ("about/", "من نحن"),
        ("doctrines/", "عقائدنا"),
        ("vision/", "رؤيتنا"),
        ("news/", "الأخبار"),
        ("founder/", "المؤسس"),
        ("join/", "انضم إلينا"),
    ],
    "en": [
        ("", "Home"),
        ("about/", "About"),
        ("doctrines/", "Doctrines"),
        ("vision/", "Vision"),
        ("news/", "News"),
        ("founder/", "Founder"),
        ("join/", "Join"),
    ],
}

# --- Homepage ----------------------------------------------------------

HERO = {
    "ar": {
        "eyebrow": "المغرب أولاً، الفعل أولاً، المستقبل أولاً.",
        "headline": "حزب الفعل، لا حزب الهضرة",
        "slogan": "الا خيابت، دابا تزيان",
        "declaration": (
            "مشروع وطني مغربي جديد: ملكي، منتج، عملي، غير ديني — يحوّل المشكلات "
            "الوطنية إلى نماذج تُختبر وتُقاس وتُنشر نتائجها."
        ),
        "cta_primary": "اكتشف عقائدنا",
        "cta_secondary": "انضم إلى الحركة",
    },
    "en": {
        "eyebrow": "Morocco First. Action First. The Future First.",
        "headline": "A party of action, not of speeches",
        "slogan": "We took a hit, but soon we'll bounce back.",
        "slogan_source": "الا خيابت، دابا تزيان",
        "declaration": (
            "A new Moroccan national project — monarchist, productive, practical and "
            "non-religious — turning national problems into prototypes that are tested, "
            "measured, and published."
        ),
        "cta_primary": "Explore our doctrines",
        "cta_secondary": "Join the movement",
    },
}

WHO = {
    "ar": {
        "label": "من نحن",
        "title": "مشروع سياسي يبدأ من المشكل، لا من الكرسي",
        "lead": (
            "حزب اليمين المغربي مشروع سياسي جديد قائم على المسؤولية الوطنية، "
            "والرأسمالية المنتجة، واستقرار المؤسسات، والابتكار، والنتائج القابلة للقياس. "
            "لا نطلب من المغاربة أن يصدقونا، بل أن يقيسونا."
        ),
        "distinctions": [
            ("نقدم حلولاً، لا شعارات",
             "كل موقف نتبناه يصاحبه تصميم مفصل: من يفعل ماذا، بأي كلفة، في أي أجل."),
            ("نبني نماذج أولية قبل إطلاق الوعود",
             "الوعد الذي لم يُختبر على نطاق صغير ليس وعداً، بل رهاناً بمال المغاربة."),
            ("نقيس النتائج ونعلنها",
             "ننشر ما نجح وما فشل. تقرير الفشل التزام، لا اعتراف اضطراري."),
            ("نضع مصلحة المغرب فوق الصراع الإيديولوجي",
             "حين تتعارض مصلحة الحزب مع مصلحة الوطن، تسقط مصلحة الحزب."),
        ],
    },
    "en": {
        "label": "Who we are",
        "title": "A political project that starts from the problem, not the seat",
        "lead": (
            "The Moroccan Right Party is a new political project built on national "
            "responsibility, productive capitalism, institutional stability, innovation, and "
            "measurable results. We are not asking Moroccans to believe us. We are asking "
            "them to measure us."
        ),
        "distinctions": [
            ("Solutions before slogans",
             "Every position we adopt comes with a detailed design: who does what, at what cost, by when."),
            ("Prototypes before promises",
             "A promise never tested at small scale is not a promise. It is a wager with public money."),
            ("Results citizens can measure",
             "We publish what worked and what failed. The failure report is a commitment, not a forced confession."),
            ("Morocco above ideological conflict",
             "Where party advantage conflicts with the national interest, party advantage loses."),
        ],
    },
}

NEWS_FEATURED = {
    "slug": "immigration-equality",
    "date": "2026-08-10",
    "ar": {
        "kicker": "مبادرة دولية — مقترح",
        "title": "«المساواة في الهجرة»: مبادرة عالمية يقترحها الحزب",
        "standfirst": (
            "يعتزم الحزب طلب لقاءات مع أحزاب اليمين في أوروبا وكندا والولايات المتحدة "
            "لعرض مبادرة «المساواة في الهجرة»، وهي إطار مقترح لمعالجة الهجرة معالجة "
            "مستدامة بدل إدارتها كأزمة متكررة."
        ),
        "status_note": (
            "حالة الملف: اقتراح في مرحلة التحضير. لم يُحدَّد أي موعد، ولم يُتَّصل بأي "
            "حزب، ولم توافق أي جهة على المشاركة. أي إعلان عن لقاء سيصدر فقط بعد تأكيده "
            "من الطرفين."
        ),
        "body": [
            "تقوم المبادرة على ملاحظة يمكن للجميع التحقق منها: النظام الدولي للجوء صُمّم "
            "بعد الحرب العالمية الثانية لحماية من يفرّ من الاضطهاد، ثم أصبح اليوم "
            "المسار الوحيد المتاح عملياً أمام من يبحث عن فرصة اقتصادية. حين يُستعمل "
            "مسار مصمم للحماية لغرض اقتصادي، يدفع الثمن طرفان: اللاجئ الحقيقي الذي "
            "يضيع ملفه في الازدحام، والمهاجر الاقتصادي الذي يقضي سنوات في وضع معلّق "
            "بلا حقوق واضحة.",
            "يقترح الحزب إعادة النظر في طريقة تطبيق المادة الرابعة عشرة من الإعلان "
            "العالمي لحقوق الإنسان — لا في المبدأ الذي تحميه. الهدف هو الفصل الصريح "
            "بين مسار الحماية ومسار الهجرة الاقتصادية النظامية، وإنشاء المسار الثاني "
            "بشكل حقيقي بدل تركه فراغاً يملؤه التهريب.",
            "ولأن المغرب بلد مصدر وعبور ومقصد في آن واحد، فإن موقعه يسمح له بأن يقترح "
            "هذا الإطار بمصداقية لا تملكها الأطراف التي ترى الملف من جهة واحدة فقط. "
            "وهذا هو الامتداد العملي لعقيدة الهجرة والكرامة.",
        ],
        "outreach_label": "الجهات التي يعتزم الحزب مراسلتها",
        "outreach_note": "قائمة نوايا اتصال — لا تعني أي التزام أو موافقة من أي طرف.",
        "outreach": [
            "المملكة المتحدة", "ألمانيا", "فرنسا", "إيطاليا",
            "إسبانيا", "كندا", "الولايات المتحدة",
        ],
    },
    "en": {
        "kicker": "International initiative — proposed",
        "title": "Immigration Equality: a global initiative proposed by the party",
        "standfirst": (
            "The party intends to seek meetings with right-of-centre parties in Europe, "
            "Canada and the United States to present Immigration Equality — a proposed "
            "framework for addressing migration sustainably rather than managing it as a "
            "recurring crisis."
        ),
        "status_note": (
            "File status: a proposal in preparation. No date has been set, no party has been "
            "contacted, and no organisation has agreed to participate. Any meeting will be "
            "announced only after both sides confirm it."
        ),
        "body": [
            "The initiative rests on an observation anyone can verify: the international asylum "
            "system was designed after the Second World War to protect people fleeing "
            "persecution, and has since become the only route practically available to people "
            "seeking economic opportunity. When a channel built for protection is used for an "
            "economic purpose, two parties pay: the genuine refugee whose case is lost in the "
            "congestion, and the economic migrant who spends years suspended without clear rights.",
            "The party proposes revisiting how Article 14 of the Universal Declaration of Human "
            "Rights is applied — not the principle it protects. The objective is an explicit "
            "separation between the protection route and a regular economic migration route, and "
            "building the second one properly instead of leaving a vacuum that smuggling fills.",
            "Because Morocco is simultaneously a country of origin, transit and destination, it is "
            "positioned to propose this framework with a credibility unavailable to parties who "
            "see the file from one side only. This is the practical extension of the Dignified "
            "Immigration Doctrine.",
        ],
        "outreach_label": "Where the party intends to write",
        "outreach_note": "A list of intended contacts. It implies no commitment or agreement by any party.",
        "outreach": [
            "United Kingdom", "Germany", "France", "Italy",
            "Spain", "Canada", "United States",
        ],
    },
}

VISION = {
    "ar": {
        "label": "رؤيتنا",
        "title": "مغرب ما بعد 2030",
        "lead": (
            "مونديال 2030 موعد، وليس مشروعاً. المشروع هو ما يبقى بعد أن تنطفئ الأضواء: "
            "اقتصاد منتج، وقدرة تكنولوجية، وأمن، ومؤسسات مستقرة، وأسباب تجعل الشاب "
            "المغربي يبقى ويعود ويستثمر ويبني."
        ),
        "pillars": [
            ("اقتصاد ينتج",
             "قاعدة صناعية وخدمية تخلق القيمة داخل المغرب، لا تكتفي بتجميع ما صُنع في مكان آخر."),
            ("قدرة تكنولوجية",
             "هندسة وبحث وتصنيع دقيق: أن نملك المعرفة، لا أن نستوردها جاهزة في كل دورة."),
            ("كرامة وأمن",
             "أمن يُبنى بكلفة معقولة، وكرامة تُقاس بوجود خيار حقيقي أمام المواطن."),
            ("مؤسسات مستقرة",
             "إدارة وقضاء وتعليم لا تتوقف خدماتهم كلما تغيّرت حكومة."),
            ("خبرة مغاربة العالم",
             "خمسة ملايين مغربي في الخارج بوصفهم شبكة معرفية، لا مصدر تحويلات."),
            ("سبب للبقاء",
             "مسار واضح بين التكوين والشغل الأول، وسكن يمكن بلوغه، ومسطرة لا تستهلك السنوات."),
        ],
        "plan_title": "خطة ألف وخطة باء",
        "plan_lead": (
            "خطة ألف هي التحضير الوطني للاستحقاقات الكبرى: البنية التحتية، الاستثمار، "
            "التنظيم، والتحول الاقتصادي والاجتماعي. أما خطة باء فهي ما يقترحه الحزب "
            "للتعامل مع أسوأ السيناريوهات."
        ),
        "plan_body": [
            "ماذا لو وقع اضطراب كبير في التجارة العالمية وسلاسل التوريد وصناعة الرقائق "
            "الإلكترونية والنقل البحري؟ وماذا لو كان أثر أزمة كبرى في شرق آسيا على "
            "الاقتصاد العالمي أوسع مما اعتدنا توقعه؟ هل يبقى الاستحقاق بالصورة التي "
            "ننتظرها؟ وهل لدينا سيناريو بديل، واحتياطي، وخطة لحماية المشاريع وفرص الشغل؟",
            "دراسة أسوأ السيناريوهات ليست تشاؤماً. حتى صاحب محل صغير يدرس احتمال أن "
            "يفتح منافس بابه في الشارع نفسه. فما بالك بدولة فيها أكثر من سبعة وثلاثين "
            "مليون مواطن، وأمن قومي، واستثمارات بمليارات الدراهم، والتزامات دولية.",
            "الدول المتقدمة تعطي إدارة المخاطر الأهمية نفسها التي تعطيها لقانون المالية. "
            "السياسة الجدية ليست توقع أن كل شيء سيمر بخير، بل الأمل في أفضل النتائج مع "
            "الاستعداد لأسوأ الاحتمالات.",
        ],
        "example_title": "مثال: ملف النقل",
        "example_body": (
            "خطة ألف تحضّر قطاع النقل للاستحقاق الدولي، بما في ذلك تكوين سائقي سيارات "
            "الأجرة في اللغة والاستقبال. خطوة مفيدة، لكنها لا تحل وحدها المشكلات البنيوية "
            "للقطاع. خطة باء تقترح إصلاحاً متكاملاً: مأذونيات منظمة، وسائقون محميون، "
            "وتطبيقات مرخصة، وأسعار واضحة، وتأمين، ومراقبة جودة، ونظام رقمي يحدد الحقوق "
            "والمسؤوليات. الهدف ليس إلغاء سيارات الأجرة لصالح التطبيقات، ولا منع "
            "التكنولوجيا لحماية القديم، بل إدماج الطرفين في منظومة واحدة عادلة."
        ),
    },
    "en": {
        "label": "Our vision",
        "title": "Morocco beyond 2030",
        "lead": (
            "The 2030 World Cup is a date, not a project. The project is what remains after the "
            "lights go out: a productive economy, technological capability, security, stable "
            "institutions, and reasons for young Moroccans to stay, return, invest and build."
        ),
        "pillars": [
            ("An economy that produces",
             "An industrial and service base creating value inside Morocco, not merely assembling what was made elsewhere."),
            ("Technological capability",
             "Engineering, research and precision manufacturing: owning the knowledge rather than importing it ready-made each cycle."),
            ("Dignity and security",
             "Security built at a reasonable cost, and dignity measured by whether a citizen has a real choice."),
            ("Stable institutions",
             "An administration, judiciary and education system whose services do not stop when a government changes."),
            ("Diaspora expertise",
             "Five million Moroccans abroad treated as a knowledge network rather than a source of transfers."),
            ("A reason to stay",
             "A clear path from training to first employment, housing within reach, and procedures that do not consume years."),
        ],
        "plan_title": "Plan A and Plan B",
        "plan_lead": (
            "Plan A is the national preparation for major commitments: infrastructure, investment, "
            "organisation, and economic and social transformation. Plan B is what the party proposes "
            "for the worst plausible scenarios."
        ),
        "plan_body": [
            "What if global trade, supply chains, semiconductor manufacturing and maritime shipping "
            "suffer a major disruption? What if a serious crisis in East Asia affects the world "
            "economy more broadly than we have grown used to expecting? Does the commitment survive "
            "in the form we are planning for? Do we hold an alternative scenario, a reserve, and a "
            "plan to protect projects and jobs?",
            "Studying worst-case scenarios is not pessimism. Even the owner of a small shop considers "
            "the possibility of a competitor opening on the same street. A state with more than "
            "thirty-seven million citizens, national security responsibilities, billions in "
            "investment and international commitments owes itself at least the same discipline.",
            "Developed states give risk management the same weight they give the finance law. Serious "
            "politics is not assuming everything will go well. It is hoping for the best outcome "
            "while preparing for the worst.",
        ],
        "example_title": "A worked example: transport",
        "example_body": (
            "Plan A prepares the transport sector for an international event, including language and "
            "hospitality training for taxi drivers. That is useful, but it does not by itself resolve "
            "the sector's structural problems. Plan B proposes an integrated reform: organised "
            "licences, protected professional drivers, licensed ride-hailing applications, transparent "
            "pricing, insurance, quality supervision, and a digital system that defines rights and "
            "responsibilities. The aim is neither to abolish taxis in favour of applications nor to "
            "block technology to preserve the old arrangement, but to bring both inside one fair system."
        ),
    },
}

BUS = {
    "ar": {
        "label": "حافلة المغرب",
        "title": "من الليل إلى النهار",
        "lead": (
            "تُعرض هذه الرؤية عبر صورة واحدة: حافلة تمثل المغرب في رحلة من الليل إلى "
            "النهار. الحافلة لا تبحث عن سائق أبدي. إنها تحتاج إلى مسؤوليات واضحة، "
            "وقيادة مناسبة لكل مرحلة، وطريق يحدده الدستور، ومؤسسات تراقب الرحلة."
        ),
        "stages": [
            {
                "key": "night",
                "role": "سائق الليل",
                "subtitle": "مهمة العبور الآمن",
                "body": (
                    "مرحلة انتقالية مؤسساتية هدفها كشف شبكات الفساد وتفكيك تضارب المصالح، "
                    "من دون كشف أسرار الدولة أو تعريض الأمن القومي للخطر. من يتولى هذا "
                    "الدور لا يحكم المغرب، بل يساعده على عبور منطقة مظلمة بأقل خطر ممكن."
                ),
                "requirements_label": "ما يشترطه هذا الدور",
                "requirements": [
                    "الخضوع للقانون المغربي وللسلطات القضائية المختصة.",
                    "رقابة مؤسساتية مستقلة.",
                    "حماية الشهود والمبلغين.",
                    "الفصل بين أسرار الأمن القومي وملفات الفساد.",
                    "نشر ما يمكن نشره للمواطنين دون الإضرار بالدولة.",
                ],
            },
            {
                "key": "dawn",
                "role": "مصمم الطريق",
                "subtitle": "تحديد الوجهة",
                "body": (
                    "دور المستشار ومصمم الأفكار والعقائد والمشاريع: يحدد المشكلات، ويطور "
                    "النماذج، ويقدم المقترحات، ثم يترك التنفيذ للمؤسسات وللأشخاص المؤهلين. "
                    "يتولى عبدالله بن زكار هذا الدور، ولا يطالب بمنصب حكومي ولا بعضوية "
                    "المكتب السياسي ولا بكرسي في القيادة التنفيذية."
                ),
                "requirements_label": "المبدأ",
                "requirements": [
                    "القوة ليست في امتلاك الكرسي، بل في القدرة على تحديد الطريق.",
                ],
            },
            {
                "key": "day",
                "role": "سائق النهار",
                "subtitle": "مهمة البناء",
                "body": (
                    "قيادة مرحلة الإصلاح الديمقراطي واستعادة الثقة وبناء دولة المعرفة "
                    "والمؤسسات. يرمز هذا الدور إلى المغرب الذي يعرف وجهته: تعليم قوي، "
                    "وإدارة كفؤة، وصحافة حرة ومسؤولة، واقتصاد منتج، واستراتيجية طويلة "
                    "الأمد تستفيد من تجارب التنمية الناجحة من دون تقليدها تقليداً أعمى."
                ),
                "requirements_label": "ما يشترطه هذا الدور",
                "requirements": [
                    "شرعية مهنية معترف بها خارج الحزب.",
                    "استقلالية عن شبكات المصالح القائمة.",
                    "قدرة مثبتة على بناء مؤسسات لا على إدارة أشخاص.",
                ],
            },
        ],
        "note_title": "ملاحظة عن الأشخاص",
        "note_body": (
            "يصف الحزب هذه الأدوار بما تتطلبه، لا بأسماء أصحابها. أي دعوة موجهة إلى شخص "
            "بعينه ستُعلن باسمه فقط بعد أن يُتَّصل به فعلياً ويوافق على الإعلان. ولا يجوز "
            "تقديم أي اسم يرد في نقاش عام بوصفه عضواً أو مؤيداً أو موافقاً."
        ),
        "closing": [
            "نحمي الملكية لأنها تحمي استمرارية المغرب.",
            "نرفض الثورة بلا خريطة، والإصلاح بلا نتائج، والقيادة بلا مسؤولية.",
            "حافلة المغرب يجب أن تخرج من الليل من دون أن تسقط في الهاوية، وأن تصل إلى "
            "النهار بقيادة مؤسسات أقوى من الأشخاص.",
        ],
    },
    "en": {
        "label": "The Morocco Bus",
        "title": "From night into daylight",
        "lead": (
            "This vision is presented through a single image: a bus representing Morocco "
            "travelling from night into daylight. The bus is not looking for an eternal driver. "
            "It needs defined responsibilities, leadership suited to each stage, a road set by "
            "the Constitution, and institutions capable of supervising the journey."
        ),
        "stages": [
            {
                "key": "night",
                "role": "The Night Driver",
                "subtitle": "Securing the crossing",
                "body": (
                    "A supervised institutional transition whose purpose is to expose corrupt "
                    "networks and dismantle conflicts of interest, without revealing legitimate "
                    "state secrets or endangering national security. Whoever holds this role does "
                    "not govern Morocco. They help it cross a dark stretch of road with the least "
                    "possible risk."
                ),
                "requirements_label": "What the role requires",
                "requirements": [
                    "Operating under Moroccan law and the competent judicial authorities.",
                    "Independent institutional oversight.",
                    "Protection for witnesses and whistleblowers.",
                    "A strict separation between national-security information and corruption evidence.",
                    "Public reporting wherever disclosure does not endanger the state.",
                ],
            },
            {
                "key": "dawn",
                "role": "The Route Designer",
                "subtitle": "Setting the destination",
                "body": (
                    "The role of consultant and designer of ideas, doctrines and projects: "
                    "identifying problems, developing models, proposing routes, and leaving "
                    "delivery to qualified people and institutions. Abdullah Ben Zakar holds this "
                    "role, and seeks no government office, no seat in the political bureau, and no "
                    "executive position in the party."
                ),
                "requirements_label": "The principle",
                "requirements": [
                    "Power is not possession of the driver's seat. It is the ability to identify the right road.",
                ],
            },
            {
                "key": "day",
                "role": "The Day Driver",
                "subtitle": "Building what comes next",
                "body": (
                    "Leading the stage of democratic reform, restored trust, and the construction of "
                    "a knowledge-based state. This role represents a Morocco that knows where it is "
                    "going: strong education, competent administration, a free and responsible press, "
                    "a productive economy, and long-term strategy informed by successful development "
                    "experiences without copying them blindly."
                ),
                "requirements_label": "What the role requires",
                "requirements": [
                    "Professional legitimacy recognised outside the party.",
                    "Independence from existing networks of interest.",
                    "A demonstrated record of building institutions rather than managing individuals.",
                ],
            },
        ],
        "note_title": "A note about names",
        "note_body": (
            "The party describes these roles by what they require, not by who might hold them. Any "
            "invitation to a specific individual will be published with their name only after they "
            "have actually been contacted and have agreed to the announcement. No name raised in "
            "public discussion should be presented as a member, a supporter, or as having accepted."
        ),
        "closing": [
            "We defend the monarchy because it protects Morocco's continuity.",
            "We reject revolution without a map, reform without results, and leadership without responsibility.",
            "Morocco's bus must emerge from the night without falling into the abyss, and reach the "
            "daylight led by institutions stronger than individuals.",
        ],
    },
}

MONARCHY = {
    "ar": {
        "label": "الملكية والاستمرارية",
        "title": "الملكية أبقى من الأشخاص",
        "body": [
            "نؤمن بأن الملكية ليست مرتبطة بعهد ملك واحد، بل هي مؤسسة وطنية دستورية تحمل "
            "وحدة المغرب واستمرارية دولته عبر الأجيال. الملك يخدم مؤسسة العرش خلال مرحلة "
            "من تاريخ الوطن، بينما تظل الملكية أقدم وأبقى من كل شخص يحمل أمانتها.",
            "اثنا عشر قرناً من الملكية علّمتنا أن الاستمرارية تُبنى بالمؤسسات لا بالأشخاص. "
            "جيل يسلّم لجيل، بينما تبقى الملكية حاملة لوحدة الدولة والأمانة بين الأجيال.",
            "جدودنا علّمونا أن نقول «الله يبارك فعمر سيدنا»، لا صيغة تركّز على بقاء الشخص "
            "وحده. والفرق ليس في الكلمات بل في الفلسفة: البركة في العمر، والبركة في العمل، "
            "والبركة في ما يُترك للجيل الذي يأتي بعد.",
            "نحن مع الاستمرارية التي تتطور، لا مع الجمود؛ ومع الإصلاح الذي يحمي الدولة، "
            "لا مع المغامرة التي تهدمها. وانتقال الأمانة شأن يحدده الدستور وصاحب الجلالة، "
            "في الوقت والطريقة اللذين يحددهما.",
        ],
        "questions_title": "سؤالنا إلى دعاة الثورة",
        "questions_lead": (
            "لا يجرّم الحزب المعارضة السلمية ولا يمنع النقد. لكنه يطلب من كل من يدعو إلى "
            "إسقاط النظام أن يجيب عن أسئلة واضحة:"
        ),
        "questions": [
            "ما خطتكم لليوم التالي؟",
            "من سيحافظ على الأمن ووحدة التراب الوطني؟",
            "من سيضمن استمرار الإدارات والمستشفيات والموانئ والطاقة؟",
            "من سيمنع الفراغ السياسي من التحول إلى حكم عسكري؟",
            "كيف ستحمون المغرب من التدخل الخارجي ومن استغلال أعدائه للفوضى؟",
        ],
        "warning_lead": (
            "إسقاط مؤسسة من دون بناء بديل دستوري قابل للحياة لا ينتج الديمقراطية تلقائياً. "
            "وقد ينتهي بانفراد الجيش بالسلطة أو بولادة نظام أشد قسوة مما سبقه. وهذه أمثلة "
            "موثقة تستحق التفكير:"
        ),
        "examples": [
            ("مصر", "انتقد باسم يوسف الرئيس المنتخب محمد مرسي ورحّب بالاحتجاجات التي سبقت "
                    "تدخل الجيش. وفي المناخ السياسي الذي تلا ذلك، وجد أن مساحة السخرية "
                    "تقلصت، وتوقف برنامجه."),
            ("سوريا", "انتقلت رئاسة الجمهورية من حافظ الأسد إلى ابنه بشار."),
            ("توغو", "عيّن الجيش فور وفاة غناسينغبي إياديما ابنه فور غناسينغبي رئيساً، "
                    "خلافاً لمسار الخلافة الدستورية."),
            ("تشاد", "تولى مجلس عسكري يقوده محمد إدريس ديبي السلطة بعد وفاة والده."),
            ("ليبيا", "قُدِّم سيف الإسلام القذافي بوصفه وريثاً محتملاً، لكن سقوط النظام "
                     "أدخل البلاد في سنوات من الانقسام والصراع."),
        ],
        "warning_close": (
            "لا نقول إن صحفياً واحداً أو ساخراً واحداً صنع انقلاباً. نقول إن هدم الشرعية "
            "من دون حماية قواعد التداول قد يساعد، ولو من دون قصد، على فتح الطريق أمام "
            "سلطة يصعب تغييرها. رسالتنا بسيطة: لا تدعُ شعباً إلى القفز من الحافلة قبل أن "
            "تشرح له من سيقودها، وإلى أين، وبأي دستور."
        ),
    },
    "en": {
        "label": "Monarchy and continuity",
        "title": "The monarchy is greater than any one monarch",
        "body": [
            "We believe the Moroccan monarchy is not confined to the reign of one King. It is a "
            "permanent constitutional institution carrying the unity, continuity and historical "
            "memory of the Moroccan state across generations. A King serves the Crown during one "
            "chapter of the nation's history; the institution is older and more enduring than any "
            "individual entrusted with it.",
            "Twelve centuries of monarchy have taught us that continuity is built through "
            "institutions rather than through individuals. One generation hands to the next, while "
            "the institution carries the unity of the state and the trust between generations.",
            "Our grandparents taught us to say “may God bless the life of our sovereign” rather "
            "than a formula concerned only with one person's survival. The difference is not "
            "linguistic but philosophical: blessing in life, blessing in work, and blessing in what "
            "is left to the generation that follows.",
            "We support continuity that evolves rather than paralysis, and reform that strengthens "
            "the state rather than adventure that dismantles it. The transfer of responsibility is "
            "determined by the Constitution and by His Majesty the King, at the time and in the "
            "manner they determine.",
        ],
        "questions_title": "Our question to those calling for revolution",
        "questions_lead": (
            "The party does not criminalise peaceful opposition or silence legitimate criticism. It "
            "does ask everyone calling for the destruction of the existing order to answer clear "
            "questions:"
        ),
        "questions": [
            "What is your plan for the following morning?",
            "Who will protect public safety and Morocco's territorial integrity?",
            "Who will keep hospitals, ports, energy systems and public administrations running?",
            "Who will prevent a political vacuum from becoming military rule?",
            "How will Morocco be protected from foreign intervention and hostile exploitation of the chaos?",
        ],
        "warning_lead": (
            "Destroying an institution without constructing a viable constitutional alternative does "
            "not automatically produce democracy. It can leave the military as the only organised "
            "force able to take control. These documented examples are worth studying:"
        ),
        "examples": [
            ("Egypt", "Bassem Youssef criticised elected President Mohamed Morsi and welcomed the "
                      "protests preceding the military's removal of Morsi. In the political "
                      "environment that followed, he found the space for satire far narrower, and "
                      "his programme ended."),
            ("Syria", "The presidency passed from Hafez al-Assad to his son Bashar."),
            ("Togo", "The military installed Faure Gnassingbé immediately following the death of his "
                     "father, contrary to the constitutional succession process."),
            ("Chad", "A military council led by Mahamat Idriss Déby assumed power following his "
                     "father's death."),
            ("Libya", "Saif al-Islam Gaddafi was treated as a possible heir, but the collapse of the "
                      "regime was followed by prolonged fragmentation and conflict."),
        ],
        "warning_close": (
            "We do not claim that one journalist or one satirist caused a military takeover. We "
            "argue that destroying legitimacy without defending the rules of succession can "
            "unintentionally clear the road for a government that is much harder to replace. Our "
            "message is simple: do not ask a nation to jump from the bus until you can explain who "
            "will drive it, where it is going, and under what Constitution."
        ),
    },
}

ACCOUNTABILITY = {
    "ar": {
        "label": "المساءلة والأدلة",
        "title": "الادعاء يفتح الملف، والدليل يحسمه",
        "summary": (
            "شرح لكيفية التعامل مع ادعاءات الفساد: كيف يبدأ التحقيق، وأين تنتهي حدود "
            "الادعاء، ولماذا يظل القضاء وحده صاحب الحكم. هذا الشرح لا يتعلق بشخص بعينه "
            "ولا يوجه أي ادعاء إلى أي أحد."
        ),
        "disclaimer": (
            "هذا القسم شرح قانوني عام يقترح إطاراً للتعامل مع ادعاءات الفساد إن وُجدت. "
            "لا يتضمن أي ادعاء ضد أي شخص أو مؤسسة، ولا يشير إلى أي ملف قائم، ولا يجب أن "
            "يُقرأ بوصفه اتهاماً موجهاً إلى أحد."
        ),
        "ladder_title": "ثلاث درجات لا يجوز الخلط بينها",
        "ladder": [
            ("رأي", "تقدير شخصي أو موقف سياسي. مشروع، لكنه ليس دليلاً."),
            ("ادعاء", "قول بوقوع فعل. يفتح الباب أمام التحقق، ولا يثبت شيئاً بذاته."),
            ("دليل", "معطى قابل للفحص: وثيقة، تحويل، شهادة يمكن اختبارها."),
            ("حكم قضائي", "ما يقرره قضاء مستقل بعد محاكمة عادلة. وحده يُنشئ الإدانة."),
        ],
        "body": [
            "يستعمل الحزب نموذج قوانين RICO الأمريكية بوصفه مثالاً تعليمياً لتوضيح فكرة "
            "واحدة: الادعاء ليس حكماً بالإدانة، لكنه قد يكون بداية مشروعة للتحقيق. في "
            "ذلك النموذج، يمكن لادعاءات متعددة، وشهادات، ووثائق، وتحويلات مالية، وعلاقات "
            "متكررة بين أشخاص ومؤسسات، أن تساعد المحققين على اكتشاف نمط منظم لا يظهر عند "
            "النظر إلى كل واقعة على حدة.",
            "الادعاء يفتح الباب. التحقيق يجمع الأدلة. القضاء وحده يصدر الحكم.",
            "نرفض فكرتين متطرفتين: أن يتحول كل ادعاء إلى إدانة فورية، وأن يُمنع المواطن "
            "من طرح أي ادعاء يتعلق بالمال العام خوفاً من أصحاب النفوذ.",
            "يكفل الفصل 25 من الدستور المغربي حرية الفكر والرأي والتعبير. ويقترح الحزب "
            "تعزيز هذه الحماية بقانون خاص بادعاءات المصلحة العامة، يحمي المواطن والصحفي "
            "والموظف والمبلغ حين يتحدث بحسن نية ويقدم ما يعرفه. ولا تعني هذه الحماية "
            "السماح باختلاق الأكاذيب عمداً، أو تزوير الوثائق، أو إصدار أحكام مسبقة على الناس.",
        ],
        "framework_title": "إطار مغربي مستوحى من منطق RICO",
        "framework_lead": (
            "يقترح الحزب إطاراً مغربياً للتحقيق في شبكات الفساد المنظم وتضارب المصالح، "
            "مستوحى من منطق RICO من دون نسخ القانون الأمريكي حرفياً، ومن دون الادعاء بأن "
            "للقانون الفيدرالي الأمريكي أي اختصاص في المغرب. لا ينظر هذا الإطار إلى كل "
            "واقعة بوصفها حادثة معزولة، بل يسأل:"
        ),
        "framework_questions": [
            "هل توجد شبكة مستمرة أم وقائع منفصلة؟",
            "هل يتكرر الأشخاص والوسطاء أنفسهم؟",
            "هل تُستعمل مؤسسات أو شركات أو مناصب لخدمة مصالح خاصة؟",
            "هل توجد أوامر أو تحويلات أو حماية متبادلة يمكن توثيقها؟",
            "هل تكشف شهادات مستقلة النمط نفسه؟",
        ],
        "protection_title": "الحماية مقابل الحقيقة، لا الحصانة مقابل الصمت",
        "protection_body": [
            "يمكن للشاهد المتعاون أن يحصل، وفق قانون يقره البرلمان وتحت رقابة القضاء، على "
            "حماية شخصية وإجرائية مقابل شهادة كاملة وصادقة ومدعومة بما يمكن التحقق منه.",
            "لكن الحماية ليست حصانة مطلقة. ولا يستطيع أي حزب أن يعفي شخصاً من المسؤولية "
            "الجنائية. القضاء وحده يحدد المسؤوليات، وأي اتفاق تعاون يجب أن يكون مكتوباً، "
            "محدوداً، قابلاً للمراجعة، وخاضعاً للمصلحة الوطنية.",
            "ويجب أن يفصل الإطار بين ثلاثة أنواع من المعلومات: معلومات مرتبطة بفساد محتمل "
            "يجب فحصها قضائياً؛ ومعرفة مؤسساتية يمكن أن تُستعمل لإصلاح الإدارة؛ وأسرار "
            "مشروعة تتعلق بالأمن القومي يجب حمايتها.",
            "لا نريد نشر أسرار الدولة. ولا نريد إعطاء خصوم المملكة خريطة مؤسساتها الأمنية. "
            "ولا نريد استعمال محاربة الفساد للانتقام السياسي.",
        ],
        "closing": "الادعاء بداية السؤال، والدليل أساس الحكم، والمغرب فوق الجميع.",
    },
    "en": {
        "label": "Accountability and evidence",
        "title": "An allegation opens the file; evidence decides it",
        "summary": (
            "An explainer on how corruption allegations should be handled: how an investigation "
            "legitimately begins, where the limits of an allegation lie, and why only a court can "
            "deliver a judgment. This explainer concerns no individual and makes no allegation "
            "against anyone."
        ),
        "disclaimer": (
            "This section is a general legal explainer proposing a framework for handling corruption "
            "allegations should they arise. It contains no allegation against any person or "
            "institution, refers to no existing case, and must not be read as an accusation directed "
            "at anyone."
        ),
        "ladder_title": "Four levels that must never be confused",
        "ladder": [
            ("Opinion", "A personal assessment or political position. Legitimate, but not evidence."),
            ("Allegation", "A claim that something occurred. It opens the door to verification and proves nothing by itself."),
            ("Evidence", "Something examinable: a document, a transfer, testimony that can be tested."),
            ("Judicial finding", "What an independent court determines after a fair trial. Only this establishes guilt."),
        ],
        "body": [
            "The party uses American RICO legislation as a teaching example to illustrate one "
            "principle: an allegation is not a conviction, but it can be a legitimate beginning of "
            "an investigation. In that model, multiple allegations, witness accounts, documents, "
            "financial transfers and recurring relationships between people and institutions can "
            "help investigators discover an organised pattern that stays invisible when each "
            "incident is examined separately.",
            "An allegation opens the door. An investigation gathers the evidence. Only a court "
            "delivers a judgment.",
            "We reject two extremes: treating every allegation as immediate proof of guilt, and "
            "preventing citizens from raising allegations about public money because influential "
            "people might be affected.",
            "Article 25 of the Moroccan Constitution guarantees freedom of thought, opinion and "
            "expression. The party proposes strengthening that protection with a statute covering "
            "public-interest allegations made in good faith by citizens, journalists, officials and "
            "whistleblowers. Such protection would not cover deliberately fabricated accusations, "
            "forged documents, or knowingly false claims.",
        ],
        "framework_title": "A Moroccan framework inspired by RICO's logic",
        "framework_lead": (
            "The party proposes a Moroccan framework for investigating organised corruption and "
            "networks of conflicting interest — inspired by RICO's pattern-based logic without "
            "copying American law literally, and without pretending that US federal law has any "
            "jurisdiction in Morocco. Such a framework would not treat each incident as isolated. It "
            "would ask:"
        ),
        "framework_questions": [
            "Is there a continuing network, or a set of separate incidents?",
            "Do the same people and intermediaries repeatedly appear?",
            "Are public institutions, companies or offices being used for private benefit?",
            "Is there documentable evidence of instructions, transfers, or mutual protection?",
            "Do independent witness accounts reveal the same pattern?",
        ],
        "protection_title": "Protection in exchange for truth — not immunity in exchange for silence",
        "protection_body": [
            "A cooperating witness could receive personal and procedural protection under legislation "
            "passed by Parliament and supervised by the judiciary, conditional on complete, truthful "
            "and verifiable cooperation.",
            "Protection is not unlimited immunity. No political party can erase criminal "
            "responsibility. Only competent judicial authorities determine responsibility, and any "
            "cooperation agreement must be written, limited, reviewable, and consistent with the "
            "national interest.",
            "Such a framework must separate three categories of information: material concerning "
            "possible corruption that should be judicially examined; institutional knowledge that can "
            "help reform the administration; and legitimate national-security secrets that must stay "
            "protected.",
            "We do not want state secrets released. We do not want Morocco's opponents handed a map "
            "of its security institutions. And we do not want anti-corruption work turned into "
            "political revenge.",
        ],
        "closing": "The allegation begins the question. Evidence supports the judgment. Morocco stands above everyone.",
    },
}

FOUNDER = {
    "ar": {
        "label": "المؤسس",
        "name": "عبدالله بن زكار",
        "title": "رسالة المؤسس",
        "standfirst": "مغربي من أكادير، عاش في نيويورك، ويقترح على المغرب ما تعلّمه هناك.",
        "message": [
            "معكم عبدالله بن زكار. مغربي من مواليد أكادير، عشت في نيويورك أربعة عشر عاماً، "
            "ودرست علوم الكمبيوتر في جامعة نيويورك.",
            "لم أدخل السياسة لأنني أبحث عن منصب. دخلتها لأنني تعبت من أن أرى مشكلات "
            "مغربية معروفة تبقى معلقة سنوات، بينما الحل التقني موجود ولا ينقصه سوى من "
            "يتحمل كلفة تصميمه بالتفصيل.",
            "الوطنية عندي لا تُثبت بالخطابة. تُثبت بالعمل، وبالاختراع، وبالتضحية، وبالخدمة "
            "العملية. ولهذا لا أطلب منصباً حكومياً، ولا عضوية المكتب السياسي، ولا كرسياً في "
            "القيادة التنفيذية. دوري أن أحدد المشكلات، وأطور النماذج، وأقدم المقترحات، ثم "
            "أترك التنفيذ لمن هو أكفأ مني فيه.",
            "أكبر مشاريعي هو ما سميته «عقيدة أوكرانيا»: أن نبني أمناً كافياً بتحالفات "
            "مختبرة وقدرة ذكية، بدل أن نستنزف في سباق تسلح ما نحتاجه للتعليم والصحة "
            "والبنية التحتية ومحاربة الفساد. والسؤال الذي أشتغل عليه: ماذا يحدث حين تأتي "
            "المبادرة من شعب إلى شعب، لا من حكومة إلى حكومة؟ من الشعب المغربي، الذي وقف "
            "مع الولايات المتحدة في مرحلة استقلالها، إلى الشعب الأمريكي.",
            "وفي ملف الهجرة، أعتقد أن الإصلاح يبدأ من إعادة النظر في طريقة تطبيق حق اللجوء "
            "دولياً، لا من الجدران. وهذا ما تقترحه مبادرة «المساواة في الهجرة».",
            "ما أطلبه من المغاربة بسيط: لا تصدقوني، بل قيسوني. اقرأوا العقائد، وانتقدوها، "
            "وحاسبونا على ما ننشره من نتائج.",
        ],
        "youtube_label": "قناة المؤسس على يوتيوب",
        "youtube_note": "رابط خارجي — يفتح في نافذة جديدة.",
    },
    "en": {
        "label": "Founder",
        "name": "Abdullah Ben Zakar",
        "title": "The founder's message",
        "standfirst": "A Moroccan from Agadir who lived in New York, proposing to Morocco what he learned there.",
        "message": [
            "I am Abdullah Ben Zakar. I was born in Agadir, lived fourteen years in New York, and "
            "studied computer science at New York University.",
            "I did not enter politics looking for a position. I entered because I grew tired of "
            "watching well-known Moroccan problems stay unresolved for years, while the technical "
            "answer existed and lacked only someone willing to absorb the cost of designing it "
            "properly.",
            "Patriotism, as I understand it, is not demonstrated through speeches. It is demonstrated "
            "through work, invention, sacrifice and practical service. That is why I seek no "
            "government office, no seat in the political bureau, and no executive position. My role "
            "is to identify problems, develop models, and propose routes — then leave delivery to "
            "people more capable of it than I am.",
            "My largest project is what I called the Ukraine Doctrine: building sufficient security "
            "through tested alliances and intelligent capability, rather than draining into an arms "
            "race what Morocco needs for education, health, infrastructure and the fight against "
            "corruption. The question I work on is what happens when the initiative comes from one "
            "people to another rather than one government to another — from the Moroccan people, who "
            "stood with the United States during its independence, to the American people.",
            "On migration, I believe reform begins with revisiting how the right to asylum is applied "
            "internationally, not with walls. That is what the Immigration Equality initiative "
            "proposes.",
            "What I ask of Moroccans is simple: do not believe me — measure me. Read the doctrines, "
            "argue with them, and hold us to the results we publish.",
        ],
        "youtube_label": "The founder's YouTube channel",
        "youtube_note": "External link — opens in a new window.",
    },
}

JOIN = {
    "ar": {
        "label": "انضم إلينا",
        "title": "الحركة تحتاج بُناة، لا جمهوراً",
        "lead": (
            "ندعو المغاربة داخل المغرب وخارجه إلى المساهمة بالأفكار والمعرفة التقنية "
            "والبحث والتنظيم والمشاركة السياسية المسؤولة. لا نطلب تصفيقاً. نطلب عملاً "
            "يمكن قياسه."
        ),
        "paths": [
            ("أفكار ومشكلات",
             "اقترح مشكلاً وطنياً محدداً ومرئياً، مع وصف واضح لمن يتضرر منه وكيف."),
            ("معرفة تقنية",
             "هندسة، برمجة، تصميم، بيانات، صحة، طاقة، نقل — النماذج تحتاج من يبنيها."),
            ("بحث وتوثيق",
             "قراءة القوانين والميزانيات والتقارير، وتحويلها إلى ملخصات يفهمها المواطن."),
            ("تنظيم محلي",
             "بناء نواة في مدينتك تختبر النماذج على نطاق صغير وتوثق النتائج."),
            ("مغاربة العالم",
             "خبرة قصيرة المدى من موقعك الحالي، من دون اشتراط العودة النهائية."),
            ("مشاركة سياسية",
             "المساهمة في النقاش العام بالحجة والمعطى، والدفاع عن قواعد التداول."),
        ],
        "how_title": "كيف تبدأ",
        "how_body": (
            "الحزب في طور التأسيس، ولم تُفتح بعد قنوات العضوية الرسمية. حتى ذلك الحين، "
            "أفضل مساهمة هي عمل يمكن عرضه: ورقة مشكل، أو تصميم نموذج، أو مراجعة نقدية "
            "لعقيدة من عقائدنا."
        ),
        "contact_title": "الاتصال",
        "contact_note": (
            "لم تُنشر بعد بيانات اتصال رسمية أو مقر أو تسجيل قانوني للحزب. ستُضاف هذه "
            "المعلومات هنا فور توفرها، ولن نعرض بيانات غير مؤكدة."
        ),
    },
    "en": {
        "label": "Join us",
        "title": "The movement needs builders, not an audience",
        "lead": (
            "We invite Moroccans at home and abroad to contribute ideas, technical knowledge, "
            "research, organisation and responsible political participation. We are not asking for "
            "applause. We are asking for work that can be measured."
        ),
        "paths": [
            ("Ideas and problems",
             "Propose a specific, visible national problem, with a clear description of who it harms and how."),
            ("Technical knowledge",
             "Engineering, software, design, data, health, energy, transport — prototypes need people to build them."),
            ("Research and documentation",
             "Read the laws, budgets and reports, and turn them into summaries a citizen can understand."),
            ("Local organisation",
             "Build a group in your city that tests prototypes at small scale and documents the results."),
            ("Moroccans abroad",
             "Short-term expertise from where you already are, with no requirement to return permanently."),
            ("Political participation",
             "Contribute to public debate with argument and evidence, and defend the rules of democratic succession."),
        ],
        "how_title": "How to start",
        "how_body": (
            "The party is still being founded, and formal membership channels are not yet open. Until "
            "they are, the most useful contribution is work that can be shown: a problem paper, a "
            "prototype design, or a serious critical review of one of our doctrines."
        ),
        "contact_title": "Contact",
        "contact_note": (
            "No official contact details, headquarters, or legal registration have been published "
            "yet. This information will be added here as soon as it exists. We will not display "
            "details we cannot confirm."
        ),
    },
}

DECLARATION = {
    "ar": {
        "lines": [
            "المغرب أولاً، قبل الحزب وقبل الإيديولوجيا.",
            "الفعل أولاً، قبل الخطاب وقبل الوعد.",
            "المستقبل أولاً، لجيل يبقى ويبني.",
        ],
        "cta": "انضم إلى الحركة",
    },
    "en": {
        "lines": [
            "Morocco first — before party, before ideology.",
            "Action first — before speeches, before promises.",
            "The future first — for a generation that stays and builds.",
        ],
        "cta": "Join the movement",
    },
}

FOOTER = {
    "ar": {
        "tagline": "حزب اليمين المغربي — مشروع سياسي في طور التأسيس.",
        "legal_title": "ملاحظات قانونية",
        "legal": [
            "الحزب في طور التأسيس ولم يُستكمل بعد أي تسجيل قانوني. لا تُعرض هنا أي بيانات "
            "تسجيل أو تمويل قبل توفرها رسمياً.",
            "كل دعوة واردة في هذا الموقع هي دعوة معلنة أو اقتراح، ولا تعني موافقة أو "
            "عضوية أو تأييد من أي شخص أو جهة.",
            "قسم المساءلة والأدلة شرح عام لا يتضمن أي ادعاء ضد أي شخص أو مؤسسة.",
        ],
        "rights": "© 2026 حزب اليمين المغربي",
    },
    "en": {
        "tagline": "The Moroccan Right Party — a political project in formation.",
        "legal_title": "Legal notes",
        "legal": [
            "The party is in formation and no legal registration has been completed. No registration "
            "or funding details are displayed here before they officially exist.",
            "Every invitation on this site is a public invitation or proposal. None implies agreement, "
            "membership, or endorsement by any person or organisation.",
            "The accountability and evidence section is a general explainer containing no allegation "
            "against any person or institution.",
        ],
        "rights": "© 2026 The Moroccan Right Party",
    },
}

META = {
    "ar": {
        "home": ("حزب اليمين المغربي — حزب الفعل",
                 "مشروع سياسي مغربي جديد: ملكي، منتج، عملي. عقائد مفصلة، نماذج تُختبر، "
                 "ونتائج تُنشر. المغرب أولاً، الفعل أولاً، المستقبل أولاً."),
        "about": ("من نحن — حزب اليمين المغربي",
                  "مشروع سياسي يبدأ من المشكل لا من الكرسي: المسؤولية الوطنية، الرأسمالية "
                  "المنتجة، استقرار المؤسسات، والنتائج القابلة للقياس."),
        "doctrines": ("عقائدنا — حزب اليمين المغربي",
                      "عشر عقائد مغربية أصلية: المغرب أولاً، المواطن المنتج، البرونكس، لالة "
                      "خديجة، مغاربة العالم، دولة الفعل وغيرها."),
        "vision": ("رؤيتنا: مغرب ما بعد 2030 — حزب اليمين المغربي",
                   "اقتصاد منتج، قدرة تكنولوجية، أمن، ومؤسسات مستقرة. خطة ألف وخطة باء."),
        "news": ("الأخبار — حزب اليمين المغربي",
                 "مستجدات الحزب ومبادراته، بما فيها مبادرة «المساواة في الهجرة» المقترحة."),
        "founder": ("المؤسس عبدالله بن زكار — حزب اليمين المغربي",
                    "رسالة المؤسس: مغربي من أكادير عاش في نيويورك، ويقترح على المغرب ما تعلّمه هناك."),
        "join": ("انضم إلينا — حزب اليمين المغربي",
                 "الحركة تحتاج بُناة لا جمهوراً: أفكار، معرفة تقنية، بحث، تنظيم، ومشاركة مسؤولة."),
        "accountability": ("المساءلة والأدلة — حزب اليمين المغربي",
                           "شرح عام: الادعاء يفتح الملف، والدليل يحسمه، والقضاء وحده يحكم."),
        "bus": ("حافلة المغرب: من الليل إلى النهار — حزب اليمين المغربي",
                "مسؤوليات واضحة، وقيادة لكل مرحلة، وطريق يحدده الدستور."),
        "monarchy": ("الملكية والاستمرارية — حزب اليمين المغربي",
                     "الملكية مؤسسة دستورية أبقى من الأشخاص، والإصلاح يقوّي الدولة ولا يهدمها."),
    },
    "en": {
        "home": ("The Moroccan Right Party — a party of action",
                 "A new Moroccan political project: monarchist, productive, practical. Detailed "
                 "doctrines, tested prototypes, published results. Morocco First. Action First."),
        "about": ("About — The Moroccan Right Party",
                  "A political project that starts from the problem, not the seat: national "
                  "responsibility, productive capitalism, stable institutions, measurable results."),
        "doctrines": ("Doctrines — The Moroccan Right Party",
                      "Ten original Moroccan doctrines: Morocco First, the Productive Citizen, the "
                      "Bronx Doctrine, Lalla Khadija, the Diaspora, the Action-State and more."),
        "vision": ("Vision: Morocco beyond 2030 — The Moroccan Right Party",
                   "A productive economy, technological capability, security and stable institutions. "
                   "Plan A and Plan B."),
        "news": ("News — The Moroccan Right Party",
                 "Party updates and initiatives, including the proposed Immigration Equality initiative."),
        "founder": ("Founder Abdullah Ben Zakar — The Moroccan Right Party",
                    "The founder's message: a Moroccan from Agadir who lived in New York, proposing "
                    "to Morocco what he learned there."),
        "join": ("Join us — The Moroccan Right Party",
                 "The movement needs builders, not an audience: ideas, technical knowledge, research, "
                 "organisation and responsible participation."),
        "accountability": ("Accountability and evidence — The Moroccan Right Party",
                           "A general explainer: an allegation opens the file, evidence decides it, "
                           "and only a court delivers judgment."),
        "bus": ("The Morocco Bus: from night into daylight — The Moroccan Right Party",
                "Defined responsibilities, leadership for each stage, and a road set by the Constitution."),
        "monarchy": ("Monarchy and continuity — The Moroccan Right Party",
                     "A constitutional institution greater than any individual; reform that "
                     "strengthens the state rather than dismantling it."),
    },
}
