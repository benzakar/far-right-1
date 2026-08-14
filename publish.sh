#!/bin/sh
# Rebuild the copy of the site that GitHub Pages serves.
#
# Where Pages serves from decides every absolute path in the build, and
# there are two cases:
#
#   CNAME present  the site is served from the DOMAIN ROOT, so BASE_PATH
#                  must stay empty. Setting one would point every link
#                  and asset at a sub-directory that does not exist.
#
#   CNAME absent   the custom domain is off and Pages falls back to
#                  https://USER.github.io/REPO/. Now the opposite is
#                  true: without a BASE_PATH every "/css/...", "/img/..."
#                  and "/js/..." resolves against the user root, one
#                  level above the site, and 404s. The page still loads
#                  and still says the right words, but with no stylesheet
#                  and no script — which reads as a plain, uncoloured
#                  document rather than as an error.
#
# So the base path is derived, never guessed: drop the CNAME and the
# build follows, restore it and the build follows back.
#
# .nojekyll stops Pages from treating the repo as a Jekyll site and
# publishing README.md instead of the site.
#
# Run this after any content or style change, then commit and push.
set -e
cd "$(dirname "$0")"

DOMAIN="$(cat CNAME 2>/dev/null | tr -d '[:space:]')"

if [ -n "$DOMAIN" ]; then
  ORIGIN="https://$DOMAIN"
  BASE=""
else
  # Read the account and repository off the origin remote rather than
  # hard-coding them, so a fork or a rename does not silently publish a
  # build pointing at someone else's Pages URL.
  REMOTE="$(git config --get remote.origin.url 2>/dev/null || true)"
  [ -n "$REMOTE" ] || { echo "no CNAME and no origin remote — cannot work out where this is served"; exit 1; }
  SLUG="$(printf '%s' "$REMOTE" | sed -e 's#^git@github.com:##' -e 's#^https://github.com/##' -e 's#\.git$##')"
  USER="${SLUG%%/*}"
  REPO="${SLUG##*/}"
  [ -n "$USER" ] && [ -n "$REPO" ] || { echo "could not parse owner/repo out of '$REMOTE'"; exit 1; }
  ORIGIN="https://$USER.github.io/$REPO"
  BASE="/$REPO"
fi

SITE_ORIGIN="$ORIGIN" BASE_PATH="$BASE" python3 build.py
cp -R dist/. .
touch .nojekyll

if [ -n "$BASE" ]; then
  echo "root copy refreshed for $ORIGIN/ (no custom domain — built with BASE_PATH=$BASE)"
else
  echo "root copy refreshed for $ORIGIN — commit and push to publish"
fi
