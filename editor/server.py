#!/usr/bin/env python3
"""Local-only visual editor for fromparty.com."""

import json
import mimetypes
import os
import re
import secrets
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDITOR = os.path.join(ROOT, "editor")
CONFIG = os.path.join(ROOT, "content", "editor.json")
ARTICLES = os.path.join(ROOT, "content", "articles.json")
UPLOADS = os.path.join(ROOT, "static", "img", "editor")
TOKEN = secrets.token_urlsafe(24)

sys.path.insert(0, ROOT)
from content.site import VISION, NEWS_FEATURED, MONARCHY, WHO, FOUNDER, BUS, ACCOUNTABILITY, JOIN  # noqa: E402
from content.doctrines import DOCTRINES  # noqa: E402


def run(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True)


def editable_blocks():
    blocks = {
        "section-vision": {"name": "خطة ألف وخطة باء", "eyebrow": VISION["label"], "title": VISION["plan_title"], "body": [VISION["plan_lead"]]},
        "project-taxis": {"name": "خطة باء ديال الطاكسيات", "eyebrow": "المثال الثالث", "title": VISION["example_title"], "body": [VISION["example_body"]]},
        "news-immigration-equality": {"name": "المساواة فالهجرة", "eyebrow": "آخر المستجدات · 10 غشت 2026", "title": NEWS_FEATURED["title"], "body": [NEWS_FEATURED["standfirst"], NEWS_FEATURED["status_note"]]},
        "section-monarchy": {"name": "الملكية والاستمرارية", "eyebrow": MONARCHY["label"], "title": MONARCHY["title"], "body": [MONARCHY["body"][1]]},
        "about-identity": {"name": "هوية الحزب", "eyebrow": WHO["label"], "title": WHO["title"], "body": [WHO["lead"]]},
        "about-founder": {"name": "المؤسس", "eyebrow": FOUNDER["label"], "title": FOUNDER["name"], "body": [FOUNDER["standfirst"], FOUNDER["message"][5]]},
        "section-bus": {"name": "حافلة المغرب", "eyebrow": BUS["label"], "title": BUS["title"], "body": [BUS["lead"]]},
        "section-accountability": {"name": "المساءلة والنتائج", "eyebrow": ACCOUNTABILITY["label"], "title": ACCOUNTABILITY["title"], "body": [ACCOUNTABILITY["summary"]]},
        "section-join": {"name": "الحركة والبنّايين", "eyebrow": JOIN["label"], "title": JOIN["title"], "body": [JOIN["lead"]]},
    }
    for doctrine in DOCTRINES:
        blocks["doctrine-" + doctrine["slug"]] = {
            "name": doctrine["name"], "eyebrow": "عقيدة {:02d}".format(doctrine["order"]),
            "title": doctrine["name"], "body": [doctrine["summary"], doctrine["slogan"]],
        }
    return blocks


PAGES = {
    "home": ("الرئيسية", "/preview/"),
    "about": ("من حنا", "/preview/about/"),
    "doctrines": ("عقائدنا", "/preview/doctrines/"),
    "vision": ("رؤيتنا", "/preview/vision/"),
    "news": ("الأخبار", "/preview/news/"),
    "news-article": ("مقال المساواة فالهجرة", "/preview/news/immigration-equality/"),
    "join": ("انضم لينا", "/preview/join/"),
    "monarchy": ("الملكية والاستمرارية", "/preview/monarchy/"),
    "bus": ("حافلة المغرب", "/preview/bus/"),
    "accountability": ("المساءلة", "/preview/accountability/"),
}
for doctrine in DOCTRINES:
    PAGES["doctrine-" + doctrine["slug"]] = (
        doctrine["name"], "/preview/doctrines/{}/".format(doctrine["slug"]))


class Handler(SimpleHTTPRequestHandler):
    server_version = "FromPartyEditor/1.0"

    def log_message(self, fmt, *args):
        sys.stdout.write("[editor] " + (fmt % args) + "\n")

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def authorized(self):
        return self.headers.get("X-Editor-Token", "") == TOKEN

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self.path = "/editor/index.html"
            return super().do_GET()
        if path == "/api/config":
            with open(CONFIG, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            defaults = editable_blocks()
            overrides = data.get("content_overrides", {})
            for key, block in defaults.items():
                if isinstance(overrides.get(key), dict):
                    block.update(overrides[key])
            data["_blocks"] = defaults
            data["_pages"] = {key: {"name": value[0], "url": value[1]} for key, value in PAGES.items()}
            data["_token"] = TOKEN
            data["_git"] = run("git", "status", "--short").stdout
            return self.send_json(200, data)
        if path == "/articles-edit" or path == "/articles-edit/":
            self.path = "/editor/articles.html"
            return super().do_GET()
        if path == "/api/articles":
            try:
                with open(ARTICLES, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
            except (OSError, ValueError):
                data = {"articles": []}
            data["_token"] = TOKEN
            data["_git"] = run("git", "status", "--short").stdout
            return self.send_json(200, data)
        if path.startswith("/preview"):
            rel = unquote(path[len("/preview"):]).lstrip("/") or "index.html"
            self.path = "/" + rel
            return super().do_GET()
        return super().do_GET()

    def do_POST(self):
        if not self.authorized():
            return self.send_json(403, {"ok": False, "error": "Invalid editor token"})
        path = urlparse(self.path).path
        size = int(self.headers.get("Content-Length", "0"))
        if size > 25 * 1024 * 1024:
            return self.send_json(413, {"ok": False, "error": "File is larger than 25 MB"})
        body = self.rfile.read(size)

        if path == "/api/articles/save":
            try:
                data = json.loads(body.decode("utf-8"))
                data.pop("_token", None)
                data.pop("_git", None)
                items = data.get("articles")
                if not isinstance(items, list):
                    raise ValueError("articles must be a list")
                seen = set()
                for item in items:
                    if not isinstance(item, dict):
                        raise ValueError("every article must be an object")
                    slug = str(item.get("slug", "")).strip()
                    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
                        raise ValueError(
                            "slug must be lowercase latin letters, digits and dashes: " + repr(slug))
                    if slug in seen:
                        raise ValueError("duplicate slug: " + slug)
                    seen.add(slug)
                    if not str(item.get("title", "")).strip():
                        raise ValueError("article '%s' has no title" % slug)
                with open(ARTICLES, "w", encoding="utf-8") as fh:
                    json.dump(data, fh, ensure_ascii=False, indent=2)
                    fh.write("\n")
                result = run("./publish.sh")
                if result.returncode:
                    return self.send_json(500, {"ok": False, "error": result.stderr or result.stdout})
                return self.send_json(200, {"ok": True, "message": "تسجلات المقالات وتبنات المعاينة"})
            except (ValueError, json.JSONDecodeError) as exc:
                return self.send_json(400, {"ok": False, "error": str(exc)})

        if path == "/api/save":
            try:
                data = json.loads(body.decode("utf-8"))
                data.pop("_token", None)
                data.pop("_git", None)
                blocks = data.pop("_blocks", {})
                data.pop("_pages", None)
                if isinstance(blocks, dict):
                    data["content_overrides"] = {
                        key: {field: value for field, value in block.items() if field in ("eyebrow", "title", "body")}
                        for key, block in blocks.items()
                    }
                if not isinstance(data.get("sections"), dict):
                    raise ValueError("sections is required")
                with open(CONFIG, "w", encoding="utf-8") as fh:
                    json.dump(data, fh, ensure_ascii=False, indent=2)
                    fh.write("\n")
                result = run("./publish.sh")
                if result.returncode:
                    return self.send_json(500, {"ok": False, "error": result.stderr or result.stdout})
                return self.send_json(200, {"ok": True, "message": "Saved and preview rebuilt"})
            except (ValueError, json.JSONDecodeError) as exc:
                return self.send_json(400, {"ok": False, "error": str(exc)})

        if path == "/api/upload":
            original = self.headers.get("X-Filename", "image")
            slot = re.sub(r"[^a-z0-9-]+", "-", self.headers.get("X-Slot", "image").lower()).strip("-")
            ext = os.path.splitext(original)[1].lower()
            if ext not in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
                return self.send_json(400, {"ok": False, "error": "Use PNG, JPG, WebP or GIF"})
            os.makedirs(UPLOADS, exist_ok=True)
            name = "{}{}".format(slot or "image", ext)
            with open(os.path.join(UPLOADS, name), "wb") as fh:
                fh.write(body)
            return self.send_json(200, {"ok": True, "path": "/img/editor/" + name})

        if path == "/api/publish":
            build = run("./publish.sh")
            if build.returncode:
                return self.send_json(500, {"ok": False, "error": build.stderr or build.stdout})
            allowed = ("content/editor.json", "static/img/editor/", "img/editor/", "editor/",
                       "index.html", "about/", "accountability/", "bus/", "doctrines/", "join/",
                       "monarchy/", "news/", "vision/", "css/", "fonts/", "img/", "sitemap.xml",
                       ".nojekyll", "README.md", "build.py", "static/css/", "edit-site.command")
            changed = [line[3:] for line in run("git", "status", "--porcelain").stdout.splitlines()]
            unexpected = [name for name in changed if not any(name == p or name.startswith(p) for p in allowed)]
            if unexpected:
                return self.send_json(409, {"ok": False, "error": "Unrelated local changes block publishing: " + ", ".join(unexpected)})
            run("git", "add", "-A")
            commit = run("git", "commit", "-m", "Update website from local editor")
            if commit.returncode and "nothing to commit" not in (commit.stdout + commit.stderr).lower():
                return self.send_json(500, {"ok": False, "error": commit.stderr or commit.stdout})
            push = run("git", "push", "origin", "main")
            if push.returncode:
                return self.send_json(500, {"ok": False, "error": push.stderr or push.stdout})
            return self.send_json(200, {"ok": True, "message": "Published to main", "details": push.stderr or push.stdout})

        return self.send_json(404, {"ok": False, "error": "Unknown action"})

    def translate_path(self, path):
        clean = unquote(urlparse(path).path).lstrip("/")
        target = os.path.abspath(os.path.join(ROOT, clean))
        if not target.startswith(ROOT + os.sep):
            return ROOT
        return target


if __name__ == "__main__":
    port = int(os.environ.get("EDITOR_PORT", "8765"))
    os.chdir(ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("FromParty editor: http://127.0.0.1:{}/".format(port))
    print("Local access only. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEditor stopped.")
