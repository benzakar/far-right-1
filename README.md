# حزب اليمين المغربي — The Moroccan Right Party

الموقع الرسمي، بالمغربية. الدارجة هي الصوت الأساسي، والفصحى كتستعمل غير
فين كتكون الدقة ضرورية: القانون، الدستور، المؤسسات، المصطلح التقني.

The site is Moroccan Arabic only. This README is in English because it is
developer documentation, not site content.

## Build

No dependencies. Python 3.8+ only.

```bash
python3 build.py
```

Output lands in `dist/`, which any static host can serve.

To preview locally:

```bash
python3 -m http.server 4321 --directory dist
```

Then open <http://127.0.0.1:4321/>.

## Layout

```
build.py             generator + templates (one file)
content/site.py      homepage sections, pages, UI strings, metadata
content/doctrines.py the ten doctrines
static/css/          design system + font faces
static/js/           scroll choreography, navigation
static/fonts/        self-hosted woff2 subsets
static/img/          optimised images
assets/originals/    untouched source files
```

Content lives entirely in `content/`. Editing a doctrine or a section
means editing one Python dictionary — no HTML.

## Routes

Everything sits at the root. `lang="ar"` and `dir="rtl"` throughout.

```
/                        home
/about/                  identity, the four differences, Plan A / Plan B
/doctrines/              register of all ten
/doctrines/<slug>/       one page per doctrine
/vision/                 مغرب ما بعد 2030
/news/                   updates
/news/immigration-equality/
/founder/                رسالة المؤسس
/join/                   ways to contribute
/monarchy/               الملكية والاستمرارية
/bus/                    حافلة المغرب, night to daylight
/accountability/         المساءلة والأدلة (explainer)
```

## Design

Carved ivory relief. Sections are planes at different depths rather than
cards, lit from the top-inline-start. Restrained gold for rules and
emphasis, deep green for decisive actions, red rationed to legal-status
labels only.

Typography: **Reem Kufi** for titles — architectural, kufic, and the
reason the headings read as carved. **IBM Plex Sans Arabic** for body
copy and long paragraphs: even colour, holds up at small sizes, and its
plainness lets the Kufi headings carry the personality.

Fonts are self-hosted. Embedding Google's CDN has been ruled a GDPR
problem in the EU, and this site expects EU visitors.

The signature element is the seam where the two hero portraits meet. It
continues down the whole document as a carved centre axis carrying a
scroll-progress traveller.

## Motion

One engine, `static/js/motion.js`. It writes two custom properties
(`--rise` in pixels, `--fade`) and a per-section `--p`; CSS turns those
into `translate3d` and opacity. Nothing that triggers layout is animated,
and native scrolling is never intercepted — there is no wheel or touch
handler, and the only pinning is `position: sticky`.

On the hero the copy rises roughly 4.6× faster than the portraits, which
drift at slightly different rates and scale to a maximum of 1.038. The
copy fades out before it can reach the navigation.

`prefers-reduced-motion: reduce` removes the scroll stage, unpins the
hero, disables smooth scrolling and the axis traveller, collapses every
transform, and pins the Morocco Bus to its daylight state. All content
stays present and readable.

## القواعد التحريرية — editorial rules

These are enforced throughout `content/` and should be kept:

- الأسماء المسكوكة ما كتتبدلش — عقيدة البرونكس، عقيدة لالة خديجة، عقلية
  سيبولا، عقيدة أوكرانيا، عقيدة دولة الفعل، وباقي الأسماء.
- الدعوة كتتسمى دعوة، والاقتراح كيتسمى اقتراح.
- حتى شخص من برا ما كيتقدم بحال إلا وافق ولا انضم ولا أيّد. أدوار حافلة
  المغرب موصوفة بما كيتطلبو الدور، ماشي باسم شكون غادي يديرو.
- قسم المساءلة شرح عام، ما فيه حتى ادعاء ضد حتى واحد.
- ما كاينش إحصائيات ولا تأييدات ولا لقاءات ولا عضويات مخترعة.
- التسمية الرسمية هي «حزب اليمين المغربي».

## Deploying

### GitHub Pages

`.github/workflows/pages.yml` builds and publishes automatically. It
needs one setting, once:

**Settings → Pages → Build and deployment → Source → GitHub Actions**

Without that, Pages stays in its default Jekyll mode and publishes this
README instead of the site.

A project Pages site serves from `/<repo>/`, so the workflow passes
`BASE_PATH`. Never set `BASE_PATH` for a root deployment.

### Netlify / Cloudflare Pages / Render

`netlify.toml` is included and needs no changes. The same settings work
elsewhere: build `python3 build.py`, publish `dist`.

### Connecting fromparty.com

The owner must do these — they need account access and payment details:

1. Confirm `fromparty.com` is actually available or already owned. This
   has **not** been checked or reserved.
2. Register or transfer it at any registrar.
3. In the host's dashboard, add `fromparty.com` and `www.fromparty.com`.
4. Point DNS at the host — either the host's nameservers, or an `ALIAS`
   /`ANAME` on the apex plus a `CNAME` for `www`.
5. Let the host issue the TLS certificate, then set the canonical
   redirect (`www` → apex).

If the domain changes, update `SITE["domain"]` in `content/site.py`.
Canonical URLs, the sitemap and `robots.txt` all read from it.

## Still needs the owner's confirmation

- Whether `fromparty.com` is available.
- Legal registration status, headquarters, and contact details. The join
  page and footer currently say these do not exist yet rather than
  showing placeholders.
- Whether any named individual has actually agreed to an invitation. If
  so, that person can be named on `/bus/`.
- The supplied emblem carries the phrase "Far Right of Morocco". The
  site's own text uses the formal name throughout; the emblem is shown
  and explained on `/about/`.
