# The Moroccan Right Party — حزب اليمين المغربي

A bilingual (Arabic-first) website for an emerging Moroccan political
movement. Arabic is the primary experience; the English side is an
authored international adaptation, not a translation.

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
build.py            generator + templates (one file)
content/site.py     homepage sections, pages, UI strings, metadata
content/doctrines.py the ten doctrines, Arabic and English
static/css/         design system + per-language font faces
static/js/          scroll choreography, navigation
static/fonts/       self-hosted woff2 subsets
static/img/         optimised images
assets/originals/   untouched source files
```

Arabic and English share every template. Only the content differs;
direction and typography follow from the `<html>` element.

## Routes

`/` redirects to `/ar/`. Every route exists in both languages, and the
language switch on any page opens the same page in the other language.

```
/ar/  /en/                    home
      about/                  identity, the four differences, Plan A / Plan B
      doctrines/              index of all ten
      doctrines/<slug>/       one page per doctrine
      vision/                 Morocco beyond 2030
      news/                   updates
      news/immigration-equality/
      founder/                the founder's message
      join/                   ways to contribute
      monarchy/               monarchy, continuity, the question to revolutionaries
      bus/                    the Morocco Bus, night to daylight
      accountability/         how allegations should be handled (explainer)
```

## Design

Carved ivory relief. Sections are planes at different depths rather than
cards, lit from the top-inline-start. Restrained gold for rules and
emphasis, deep green for decisive actions, red rationed to legal-status
labels only.

Typography: Reem Kufi with Noto Naskh Arabic for Arabic; Fraunces with
Archivo for English. Fonts are self-hosted — embedding Google's CDN has
been ruled a GDPR problem in the EU, and this site expects EU visitors.

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

## Editorial rules

These are enforced throughout the content files and should be kept:

- Coined doctrine names are fixed vocabulary — The Bronx Doctrine, The
  Lalla Khadija Doctrine, The Cipolla Mentality, The Ukraine Doctrine,
  The Action-State Doctrine and the rest.
- Invitations are labelled invitations, proposals are labelled proposals.
- No third party is presented as having accepted, endorsed, or joined.
  The Morocco Bus describes its roles by what each role requires rather
  than by naming who might hold it.
- The accountability section is an explainer. It proposes how allegations
  should be handled and makes no allegation against anyone.
- No invented statistics, endorsements, meetings, or memberships.
- The formal identity is "The Moroccan Right Party / حزب اليمين المغربي".

## Deploying and connecting fromparty.com

`netlify.toml` is included and needs no changes. Cloudflare Pages and
Render work with the same settings: build `python3 build.py`, publish
`dist`.

To connect the domain (the owner must do these — they need account
access and payment details):

1. Confirm `fromparty.com` is actually available or already owned. This
   has **not** been checked or reserved.
2. Register or transfer it at any registrar.
3. In the host's dashboard, add `fromparty.com` and `www.fromparty.com`
   as custom domains.
4. Point DNS at the host — either the host's nameservers, or an `ALIAS`
   /`ANAME` record on the apex plus a `CNAME` for `www`.
5. Let the host issue the TLS certificate, then set the canonical
   redirect (`www` → apex, matching the `SITE["domain"]` value in
   `content/site.py`).

If the domain changes, update `SITE["domain"]` — canonical URLs,
`hreflang`, the sitemap and `robots.txt` all read from it.

## Still needs the owner's confirmation

- Whether `fromparty.com` is available.
- Legal registration status, headquarters, and contact details. The join
  page and footer currently say these do not exist yet rather than
  showing placeholders.
- Whether any named individual has actually agreed to an invitation. If
  so, that person can be named on the Morocco Bus page.
- The supplied emblem carries the phrase "Far Right of Morocco". The
  site's own text uses the formal name throughout; the emblem is shown
  and explained on the About page.
