/* Articles editor. Local only — it talks to editor/server.py on 127.0.0.1.
 *
 * State lives in one `data` object mirroring content/articles.json. Every
 * edit mutates that object and re-renders; Save writes the whole file and
 * rebuilds, Publish commits and pushes. Nothing is written until you press
 * Save, so an accidental edit costs a reload, not a commit.
 */
(function () {
  "use strict";

  var data = { articles: [] };
  var token = "";
  var current = -1;

  var $ = function (id) { return document.getElementById(id); };
  var listEl = $("list"), blocksEl = $("blocks");
  var editorEl = $("editor"), emptyEl = $("empty");

  function say(message, bad) {
    var el = $("status");
    el.textContent = message;
    el.style.color = bad ? "#c0392b" : "";
  }

  function article() { return data.articles[current]; }

  /* ---------- rendering ---------- */

  function renderList() {
    listEl.innerHTML = "";
    data.articles.forEach(function (a, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.innerHTML = "";
      b.appendChild(document.createTextNode(a.title || "(بلا عنوان)"));
      var s = document.createElement("small");
      s.textContent = (a.date || "بلا تاريخ") + " · " + (a.slug || "");
      b.appendChild(s);
      if (i === current) b.setAttribute("aria-current", "true");
      b.onclick = function () { select(i); };
      listEl.appendChild(b);
    });
  }

  var KINDS = {
    p: "فقرة", h3: "عنوان فرعي", quote: "اقتباس",
    note: "ملاحظة", image: "صورة", embed: "فيديو / سوشل ميديا"
  };

  function renderBlocks() {
    blocksEl.innerHTML = "";
    var blocks = article().blocks || [];
    blocks.forEach(function (block, i) {
      var wrap = document.createElement("div");
      wrap.className = "block";

      var head = document.createElement("div");
      head.className = "block__head";
      var kind = document.createElement("span");
      kind.className = "block__kind";
      kind.textContent = KINDS[block.type] || block.type;
      head.appendChild(kind);

      [["↑", -1], ["↓", 1]].forEach(function (pair) {
        var b = document.createElement("button");
        b.type = "button"; b.textContent = pair[0];
        b.title = pair[1] < 0 ? "طلّع" : "هبّط";
        b.onclick = function () { move(i, pair[1]); };
        head.appendChild(b);
      });
      var del = document.createElement("button");
      del.type = "button"; del.textContent = "×"; del.title = "حيّد";
      del.onclick = function () { blocks.splice(i, 1); renderBlocks(); };
      head.appendChild(del);
      wrap.appendChild(head);

      if (block.type === "image") {
        wrap.appendChild(field("input", "المسار", block, "src", "/img/…"));
        wrap.appendChild(field("input", "وصف الصورة", block, "alt", ""));
        wrap.appendChild(field("input", "تعليق", block, "caption", ""));
        var up = document.createElement("button");
        up.type = "button"; up.textContent = "رفع صورة";
        up.onclick = function () { pickFile(function (path) { block.src = path; renderBlocks(); }); };
        wrap.appendChild(up);
      } else if (block.type === "embed") {
        wrap.appendChild(field("input", "الرابط", block, "url",
          "https://www.youtube.com/watch?v=…"));
        wrap.appendChild(field("input", "تعليق", block, "caption", ""));
        var hint = document.createElement("p");
        hint.className = "hint";
        hint.textContent = "كيخدم مع يوتيوب، X، إنستغرام وتيك توك. " +
          "المحتوى ما كيتحملش حتى يضغط القارئ، باش ما يتسجلش عندهم.";
        wrap.appendChild(hint);
      } else if (block.type === "note") {
        wrap.appendChild(field("input", "الوسم", block, "tag", "اقتراح"));
        wrap.appendChild(field("textarea", "النص", block, "text", ""));
      } else {
        wrap.appendChild(field("textarea", "النص", block, "text", ""));
      }

      blocksEl.appendChild(wrap);
    });
  }

  function field(tag, label, obj, key, placeholder) {
    var l = document.createElement("label");
    l.textContent = label;
    var input = document.createElement(tag);
    if (tag === "textarea") input.rows = 3; else input.type = "text";
    if (key === "src" || key === "url") input.dir = "ltr";
    input.value = obj[key] || "";
    input.placeholder = placeholder || "";
    input.oninput = function () { obj[key] = input.value; };
    l.appendChild(input);
    return l;
  }

  function move(i, delta) {
    var blocks = article().blocks;
    var j = i + delta;
    if (j < 0 || j >= blocks.length) return;
    var tmp = blocks[i]; blocks[i] = blocks[j]; blocks[j] = tmp;
    renderBlocks();
  }

  /* ---------- selection ---------- */

  function select(i) {
    current = i;
    var a = article();
    if (!a) { editorEl.hidden = true; emptyEl.hidden = false; renderList(); return; }
    editorEl.hidden = false; emptyEl.hidden = true;
    $("view-title").textContent = a.title || "مقال جديد";
    $("f-title").value = a.title || "";
    $("f-slug").value = a.slug || "";
    $("f-date").value = a.date || "";
    $("f-summary").value = a.summary || "";
    $("f-image").value = a.image || "";
    $("f-keywords").value = (a.keywords || []).join(", ");
    if (!a.blocks) a.blocks = [];
    renderBlocks();
    renderList();
  }

  function bindHeader() {
    var map = {
      "f-title": "title", "f-slug": "slug", "f-date": "date",
      "f-summary": "summary", "f-image": "image"
    };
    Object.keys(map).forEach(function (id) {
      $(id).oninput = function () {
        article()[map[id]] = $(id).value;
        if (map[id] === "title") $("view-title").textContent = $(id).value;
        renderList();
      };
    });
    $("f-keywords").oninput = function () {
      article().keywords = $("f-keywords").value
        .split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    };
  }

  /* ---------- uploads ---------- */

  function pickFile(done) {
    var input = $("f-file");
    input.value = "";
    input.onchange = function () {
      var file = input.files[0];
      if (!file) return;
      say("كنرفع الصورة…");
      fetch("/api/upload", {
        method: "POST",
        headers: {
          "X-Editor-Token": token,
          "X-Slot": "article-" + (article().slug || "new"),
          "X-Filename": file.name,
          "Content-Type": file.type || "application/octet-stream"
        },
        body: file
      }).then(function (r) { return r.json(); }).then(function (res) {
        if (!res.path) throw new Error(res.error || "ما تسناش الرفع");
        done(res.path);
        say("الصورة ترفعات. دير حفظ باش تتسجل");
      }).catch(function (e) { say(e.message, true); });
    };
    input.click();
  }

  /* ---------- server ---------- */

  function post(path, payload) {
    return fetch(path, {
      method: "POST",
      headers: { "X-Editor-Token": token, "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().then(function (d) {
        if (!r.ok) throw new Error(d.error || "فشل الطلب");
        return d;
      });
    });
  }

  $("save").onclick = function () {
    say("كنسجل…");
    post("/api/articles/save", data)
      .then(function (d) { say(d.message || "تسجل"); })
      .catch(function (e) { say(e.message, true); });
  };

  $("publish").onclick = function () {
    if (!confirm("نشر المقالات فـ GitHub؟ هادشي غادي يبان على الموقع الحقيقي.")) return;
    say("كننشر…");
    post("/api/publish", { message: "Update articles" })
      .then(function (d) { say(d.message || "تنشر"); })
      .catch(function (e) { say(e.message, true); });
  };

  $("preview").onclick = function () {
    var a = article();
    if (!a || !a.slug) return say("خاص الرابط (slug) قبل المعاينة", true);
    window.open("/preview/articles/" + a.slug + "/", "_blank", "noopener");
  };

  $("new").onclick = function () {
    var today = new Date().toISOString().slice(0, 10);
    data.articles.unshift({
      slug: "", title: "", date: today, summary: "",
      keywords: [], image: "", blocks: [{ type: "p", text: "" }]
    });
    select(0);
    $("f-title").focus();
    say("مقال جديد. عمّر العنوان والرابط، ومن بعد دير حفظ");
  };

  $("delete").onclick = function () {
    var a = article();
    if (!confirm("تحيّد «" + (a.title || "هاد المقال") + "»؟")) return;
    data.articles.splice(current, 1);
    select(Math.min(current, data.articles.length - 1));
    say("تحيّد. دير حفظ باش يتأكد");
  };

  document.querySelectorAll("[data-add]").forEach(function (b) {
    b.onclick = function () {
      var kind = b.getAttribute("data-add");
      var block = { type: kind };
      if (kind === "image") { block.src = ""; block.alt = ""; }
      else if (kind === "embed") { block.url = ""; }
      else if (kind === "note") { block.tag = "ملاحظة"; block.text = ""; }
      else block.text = "";
      article().blocks.push(block);
      renderBlocks();
    };
  });

  /* ---------- boot ---------- */

  fetch("/api/articles", { cache: "no-store" })
    .then(function (r) { return r.json(); })
    .then(function (d) {
      token = d._token;
      delete d._token; delete d._git;
      data = d;
      if (!Array.isArray(data.articles)) data.articles = [];
      bindHeader();
      renderList();
      if (data.articles.length) select(0);
      else { editorEl.hidden = true; emptyEl.hidden = false; }
      say(data.articles.length + " مقال محمّل");
    })
    .catch(function (e) { say("ما قدرناش نحملو المقالات: " + e.message, true); });
})();
