#!/bin/sh
# Rebuild the copy of the site that GitHub Pages serves.
#
# Pages is set to "Deploy from a branch", which serves files straight out
# of the repository. So the built site lives at the repo root alongside
# the source, and .nojekyll stops Pages from treating the repo as a
# Jekyll site and publishing README.md instead.
#
# Run this after any content or style change, then commit and push.
#
# If Pages is ever switched to the "GitHub Actions" source, this script
# and the committed output stop being needed — .github/workflows/pages.yml
# builds and deploys on its own.
set -e
cd "$(dirname "$0")"
BASE_PATH=/far-right-1 SITE_ORIGIN=https://benzakar.github.io python3 build.py
cp -R dist/. .
touch .nojekyll
echo "root copy refreshed — commit and push to publish"
