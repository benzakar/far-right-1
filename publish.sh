#!/bin/sh
# Rebuild the copy of the site that GitHub Pages serves.
#
# Pages is set to "Deploy from a branch" and the repository carries a
# CNAME for fromparty.com, so the site is served from the domain ROOT.
# That means no BASE_PATH — adding one would point every link and asset
# at a sub-directory that does not exist on the domain.
#
# .nojekyll stops Pages from treating the repo as a Jekyll site and
# publishing README.md instead of the site.
#
# Run this after any content or style change, then commit and push.
set -e
cd "$(dirname "$0")"
DOMAIN="$(cat CNAME 2>/dev/null | tr -d '[:space:]')"
[ -n "$DOMAIN" ] || { echo "no CNAME found — refusing to guess the origin"; exit 1; }
SITE_ORIGIN="https://$DOMAIN" python3 build.py
cp -R dist/. .
touch .nojekyll
echo "root copy refreshed for https://$DOMAIN — commit and push to publish"
