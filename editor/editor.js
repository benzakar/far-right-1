/* Local visual editor for fromparty.com.
 *
 * Organised in five layers, top to bottom:
 *   state    — what is loaded and what is selected
 *   config   — reading and writing content/editor.json in memory
 *   preview  — the iframe bridge and live DOM mirroring
 *   panel    — the controls for the selected element
 *   forms    — section, block and theme views, plus save/publish
 *
 * Every edit does two things: record it in `config`, and mirror it into the
 * preview immediately. The mirror is what makes the editor feel real; the
 * record is what survives a save. If a control only did the first, the
 * change would appear to do nothing until a rebuild.
 */
(async function () {
  "use strict";

  /* ---------------------------------------------------------------- state */

  var config = null;
  var token = null;
  var mode = "click";
  var current = null;
  var dirty = false;
  var selected = null;      // { el, id }

  var el = {
    sections: document.getElementById("sections"),
    form: document.getElementById("form"),
    status: document.getElementById("status"),
    frame: document.getElementById("frame"),
    title: document.getElementById("view-title"),
    page: document.getElementById("page")
  };

  var ADDED = /^(.*)-add(\d+)$/;
  var TEXT_TAGS = /^(h1|h2|h3|p|blockquote|a)$/;

  function say(message, isError) {
    el.status.textContent = message;
    el.status.style.color = isError ? "#9a271e" : "";
  }

  function mark() {
    dirty = true;
    say("عندك تغييرات مازال ما تحفظوش");
  }

  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  /* --------------------------------------------------------------- config */

  function pageKey() {
    return el.page.value;
  }

  function pageOps() {
    if (!config.page_overrides) config.page_overrides = {};
    var key = pageKey();
    if (!config.page_overrides[key]) config.page_overrides[key] = {};
    return config.page_overrides[key];
  }

  /* Read without creating. Reading used to insert an empty record for every
     element merely clicked on, which slowly filled the config with noise. */
  function peek(id) {
    return pageOps()[id] || null;
  }

  function op(id) {
    var ops = pageOps();
    if (!ops[id]) ops[id] = {};
    return ops[id];
  }

  /* Blocks added under an element live in that element's `after` list rather
     than as records of their own, so `p-5-add2` reads as "the second block
     added under p-5". Positional ids therefore never shift when one is
     inserted, and edits already made below stay attached to the right node. */
  function addedRef(id) {
    var m = ADDED.exec(id || "");
    if (!m) return null;
    var record = peek(m[1]);
    if (!record || !Array.isArray(record.after)) return null;
    var index = Number(m[2]) - 1;
    var item = record.after[index];
    return item ? { list: record.after, index: index, item: item } : null;
  }

  /* One place decides where an edit lands, so every control behaves the same
     whether the selection is a generated element or one added underneath. */
  function target() {
    if (!selected) return null;
    var ref = addedRef(selected.id);
    return ref ? ref.item : op(selected.id);
  }

  function targetRead() {
    if (!selected) return {};
    var ref = addedRef(selected.id);
    return ref ? ref.item : (peek(selected.id) || {});
  }

  function mergeStyle(existing, prop, value) {
    var out = {};
    String(existing || "").split(";").forEach(function (decl) {
      var i = decl.indexOf(":");
      if (i > 0) out[decl.slice(0, i).trim()] = decl.slice(i + 1).trim();
    });
    if (value) out[prop] = value; else delete out[prop];
    return Object.keys(out).map(function (k) { return k + ": " + out[k]; }).join("; ");
  }

  function styleValue(style, prop) {
    var found = "";
    String(style || "").split(";").forEach(function (decl) {
      var i = decl.indexOf(":");
      if (i > 0 && decl.slice(0, i).trim() === prop) found = decl.slice(i + 1).trim();
    });
    return found;
  }

  /* -------------------------------------------------------------- preview */

  var PREVIEW_CSS =
    '[data-edit-id]{transition:outline-color .15s}' +
    '[data-edit-id]:hover{outline:2px dashed #c9a45e!important;outline-offset:2px;cursor:pointer}' +
    '.editor-selected{outline:4px solid #8c2f23!important;outline-offset:3px}' +
    '.editor-new{animation:editorPop .9s ease}' +
    '@keyframes editorPop{from{background:rgba(201,164,94,.45)}to{background:transparent}}';

  function previewDoc() {
    return el.frame.contentDocument;
  }

  function select(node) {
    var doc = previewDoc();
    if (doc) {
      doc.querySelectorAll(".editor-selected").forEach(function (n) {
        n.classList.remove("editor-selected");
      });
    }
    node.classList.add("editor-selected");
    selected = { el: node, id: node.dataset.editId };
    if (mode !== "click") setMode("click"); else drawSelection();
  }

  function wireFrame() {
    var doc = previewDoc();
    if (!doc || !doc.getElementById("main")) return;
    var style = doc.createElement("style");
    style.textContent = PREVIEW_CSS;
    doc.head.appendChild(style);
    doc.addEventListener("click", function (event) {
      var node = event.target.closest("[data-edit-id]");
      if (!node) return;
      event.preventDefault();
      event.stopPropagation();
      select(node);
      el.form.scrollIntoView({ behavior: "smooth", block: "start" });
    }, true);
  }

  /* ---------------------------------------------------------------- panel */

  function describe(node) {
    var tag = node.tagName.toLowerCase();
    if (/^h/.test(tag)) return "عنوان";
    if (tag === "p") return "فقرة";
    if (tag === "blockquote") return "اقتباس";
    if (tag === "img") return "صورة";
    if (tag === "a") return "زر أو رابط";
    if (tag === "section") return "مقطع";
    return "صندوق أو بطاقة";
  }

  function show(id, visible) {
    var node = document.getElementById(id);
    if (node) node.hidden = !visible;
  }

  function drawEmpty() {
    show("selection-empty", true);
    show("selection-controls", false);
  }

  function drawSelection() {
    if (!selected) return drawEmpty();
    var node = selected.el;
    var tag = node.tagName.toLowerCase();
    var record = targetRead();

    show("selection-empty", false);
    show("selection-controls", true);
    document.getElementById("selection-name").textContent =
      describe(node) + " · " + selected.id;

    var textual = TEXT_TAGS.test(tag);
    show("text-field", textual);
    show("shape-tools", /^(p|h3)$/.test(tag));
    show("insert-tools", textual);
    show("box-tools", /^(section|article|div)$/.test(tag));
    show("image-tools", tag === "img");
    show("link-tools", tag === "a");
    show("quote-tool", tag === "p");
    show("remove-element", !record.removed);
    show("restore-element", !!record.removed);

    document.getElementById("selected-text").value =
      record.text !== undefined ? record.text : node.textContent.trim();

    document.querySelectorAll("[data-tag]").forEach(function (button) {
      button.classList.toggle("active", button.dataset.tag === tag);
    });

    var className = record.class !== undefined ? record.class : node.className;
    document.getElementById("selected-quote").checked =
      String(className || "").split(/\s+/).indexOf("section-quote") >= 0;

    if (tag === "img") {
      document.getElementById("selected-src").value =
        record.src || node.getAttribute("src") || "";
    }
    if (tag === "a") {
      document.getElementById("selected-href").value =
        record.href || node.getAttribute("href") || "";
    }

    var style = record.style || node.getAttribute("style");
    document.querySelectorAll("[data-style]").forEach(function (button) {
      button.classList.toggle("active",
        styleValue(style, button.dataset.style) === button.dataset.value);
    });
  }

  function setStyle(prop, value) {
    if (!selected) return;
    var record = target();
    record.style = mergeStyle(record.style || selected.el.getAttribute("style"), prop, value);
    selected.el.style.setProperty(prop, value);
    mark();
    drawSelection();
  }

  function setAttr(name, value) {
    if (!selected) return;
    target()[name] = value;
    selected.el.setAttribute(name, value);
    mark();
  }

  /* Insert a block under the selection and mirror it into the preview at
     once, so the new paragraph is visible and clickable straight away
     instead of only appearing after a rebuild. */
  function addBelow(tag) {
    if (!selected) {
      return say("كليكي أولاً على فقرة ولا عنوان فالمعاينة، ومن بعد زيد تحتو", true);
    }
    var anchorId = selected.id;
    var ref = addedRef(anchorId);
    if (ref) anchorId = ADDED.exec(anchorId)[1];

    var record = op(anchorId);
    if (!Array.isArray(record.after)) record.after = [];
    var text = tag === "h3" ? "عنوان جديد" : "فقرة جديدة";
    record.after.push({ tag: tag, text: text });

    var doc = previewDoc();
    var anchor = doc && doc.querySelector('[data-edit-id="' + anchorId + '"]');
    if (!anchor) {
      mark();
      return say("زدنا العنصر. دير حفظ باش يبان فالمعاينة");
    }

    /* land after the anchor's existing additions, matching build order */
    var last = anchor;
    record.after.forEach(function (_, i) {
      var existing = doc.querySelector('[data-edit-id="' + anchorId + '-add' + (i + 1) + '"]');
      if (existing) last = existing;
    });

    var node = doc.createElement(tag);
    node.dataset.editId = anchorId + "-add" + record.after.length;
    node.textContent = text;
    node.classList.add("editor-new");
    last.insertAdjacentElement("afterend", node);

    mark();
    select(node);
    var field = document.getElementById("selected-text");
    if (field) { field.focus(); field.select(); }
    say("زدنا " + (tag === "h3" ? "عنوان" : "فقرة") + ". بدّل النص دابا، ومن بعد دير حفظ");
  }

  function removeSelected() {
    if (!selected) return;
    if (!confirm("تمسح هاد العنصر من الصفحة؟")) return;
    var ref = addedRef(selected.id);
    if (ref) {
      /* an added block leaves the list entirely rather than lingering as a
         flag, and the ids after it are renumbered to stay contiguous */
      ref.list.splice(ref.index, 1);
      var anchorId = ADDED.exec(selected.id)[1];
      var doc = previewDoc();
      selected.el.remove();
      if (doc) {
        ref.list.forEach(function (_, i) {
          var stale = doc.querySelector(
            '[data-edit-id="' + anchorId + '-add' + (i + 2) + '"]');
          if (stale) stale.dataset.editId = anchorId + "-add" + (i + 1);
        });
      }
      selected = null;
      drawEmpty();
      mark();
      return say("تمسح");
    }
    op(selected.id).removed = true;
    selected.el.style.display = "none";
    mark();
    drawSelection();
  }

  function restoreSelected() {
    if (!selected) return;
    delete op(selected.id).removed;
    selected.el.style.display = "";
    mark();
    drawSelection();
  }

  function retag(want) {
    if (!selected) return;
    var node = selected.el;
    if (node.tagName.toLowerCase() === want) return;
    target().tag = want;
    var doc = previewDoc();
    var replacement = doc.createElement(want);
    replacement.innerHTML = node.innerHTML;
    Array.prototype.forEach.call(node.attributes, function (attr) {
      replacement.setAttribute(attr.name, attr.value);
    });
    node.replaceWith(replacement);
    selected.el = replacement;
    select(replacement);
    mark();
  }

  function wireControls() {
    document.getElementById("selected-text").oninput = function () {
      if (!selected) return;
      target().text = this.value;
      selected.el.textContent = this.value;
      mark();
    };

    document.querySelectorAll("[data-add]").forEach(function (button) {
      button.onclick = function () { addBelow(button.dataset.add); };
    });

    document.querySelectorAll("[data-tag]").forEach(function (button) {
      button.onclick = function () { retag(button.dataset.tag); };
    });

    document.getElementById("remove-element").onclick = removeSelected;
    document.getElementById("restore-element").onclick = restoreSelected;

    document.querySelectorAll("[data-style]").forEach(function (button) {
      button.onclick = function () { setStyle(button.dataset.style, button.dataset.value); };
    });

    document.querySelectorAll("[data-section-tone]").forEach(function (button) {
      button.onclick = function () {
        if (!selected) return;
        var section = selected.el.closest("section[id]");
        if (!section) return say("هاد العنصر ما تابع حتى لمقطع قابل لتغيير الخلفية", true);
        if (!config.sections[section.id]) {
          return say("هاد المقطع ما كاينش فإعدادات الرئيسية", true);
        }
        var tone = button.dataset.sectionTone;
        config.sections[section.id].background = tone;
        section.classList.toggle("bay--greenback", tone === "green");
        section.classList.toggle("bay--redback", tone === "red");
        mark();
      };
    });

    document.getElementById("selected-src").onchange = function () {
      setAttr("src", this.value.trim());
    };
    document.getElementById("selected-href").onchange = function () {
      setAttr("href", this.value.trim());
    };
    document.getElementById("selected-quote").onchange = function () {
      if (!selected) return;
      var record = target();
      var names = String(record.class !== undefined ? record.class : selected.el.className)
        .split(/\s+/).filter(Boolean);
      var i = names.indexOf("section-quote");
      if (this.checked && i < 0) names.push("section-quote");
      if (!this.checked && i >= 0) names.splice(i, 1);
      record.class = names.join(" ");
      selected.el.className = record.class;
      mark();
    };
    document.getElementById("selected-file").onchange = function () {
      if (!selected) return;
      upload(this.files[0], pageKey() + "-" + selected.id, function (path) {
        document.getElementById("selected-src").value = path;
        setAttr("src", path);
      });
    };
  }

  /* ---------------------------------------------------------------- forms */

  function nav() {
    el.sections.innerHTML = "";
    Object.keys(config.sections).forEach(function (id) {
      var button = document.createElement("button");
      button.textContent = config.sections[id].name || id;
      button.className = id === current ? "active" : "";
      button.onclick = function () { showSection(id); };
      el.sections.appendChild(button);
    });
  }

  /* Tweets are a list. The older single `tweet` object is folded in on first
     edit so existing configuration is never silently dropped. */
  function tweetsOf(section) {
    if (!Array.isArray(section.tweets)) {
      section.tweets = [];
      if (section.tweet && section.tweet.text) {
        section.tweet.enabled = section.tweet.enabled !== false;
        section.tweets.push(section.tweet);
      }
      delete section.tweet;
    }
    return section.tweets;
  }

  function drawTweets(section) {
    var list = document.getElementById("tweet-list");
    if (!list) return;
    var items = tweetsOf(section);
    list.innerHTML = items.length ? "" : '<p class="hint">ما كايناش تغريدات فهاد المقطع.</p>';

    items.forEach(function (tweet, index) {
      var box = document.createElement("div");
      box.className = "tweet-item";
      box.innerHTML =
        '<div class="tweet-item__head"><strong>تغريدة ' + (index + 1) + '</strong>' +
        '<label class="switch"><input type="checkbox" data-t="enabled"' +
        (tweet.enabled !== false ? " checked" : "") + '> مفعّلة</label>' +
        '<button type="button" class="danger" data-remove>امسح</button></div>' +
        '<div class="grid">' +
        '<label>الاسم<input data-t="name" value="' + esc(tweet.name || "Ben Zakar") + '"></label>' +
        '<label>الحساب<input data-t="handle" dir="ltr" value="' + esc(tweet.handle || "@benzakarMorocco") + '"></label>' +
        '<label class="wide">نص التغريدة<textarea data-t="text" rows="4">' + esc(tweet.text || "") + '</textarea></label>' +
        '<label>التاريخ<input data-t="date" dir="ltr" value="' + esc(tweet.date || "") + '" placeholder="Aug 11, 2026"></label>' +
        '<label>صورة الحساب<input data-t="avatar" dir="ltr" value="' + esc(tweet.avatar || "") + '" placeholder="/img/..."></label>' +
        '</div>';

      box.querySelectorAll("[data-t]").forEach(function (field) {
        field.oninput = function () {
          tweet[field.dataset.t] = field.type === "checkbox" ? field.checked : field.value;
          mark();
        };
        field.onchange = field.oninput;
      });
      box.querySelector("[data-remove]").onclick = function () {
        if (!confirm("تمسح هاد التغريدة؟")) return;
        items.splice(index, 1);
        mark();
        drawTweets(section);
      };
      list.appendChild(box);
    });
  }

  function showSection(id) {
    current = id;
    nav();
    var section = config.sections[id];
    el.title.textContent = section.name || id;
    el.form.innerHTML = "";
    el.form.appendChild(document.getElementById("section-template").content.cloneNode(true));

    el.form.querySelectorAll("[data-field]").forEach(function (field) {
      field.value = section[field.dataset.field] || "";
      field.oninput = function () {
        section[field.dataset.field] = field.value;
        mark();
        if (field.dataset.field === "name") { el.title.textContent = field.value; nav(); }
      };
    });

    drawTweets(section);
    document.getElementById("tweet-add").onclick = function () {
      tweetsOf(section).push({
        enabled: true, name: "Ben Zakar", handle: "@benzakarMorocco",
        text: "", date: "", avatar: "/img/ben-zakar-x-profile.jpg"
      });
      mark();
      drawTweets(section);
    };
  }

  function showTheme() {
    el.title.textContent = "ألوان الموقع والزوايا";
    var theme = config.theme;
    var swatches = [["green", "الأخضر"], ["red", "الأحمر"], ["gold", "الذهبي"],
                    ["panel", "لون الصناديق"], ["ink", "لون الكتابة"]];
    el.form.innerHTML = '<div class="theme-grid">' + swatches.map(function (pair) {
      return '<label>' + pair[1] + '<input type="color" data-theme="' + pair[0] +
             '" value="' + esc(theme[pair[0]]) + '"></label>';
    }).join("") + '<label>استدارة الصناديق<input type="range" min="8" max="48" data-theme="radius" value="' +
      (theme.radius || 28) + '"><output>' + (theme.radius || 28) + 'px</output></label></div>';

    el.form.querySelectorAll("[data-theme]").forEach(function (field) {
      field.oninput = function () {
        theme[field.dataset.theme] = field.type === "range" ? Number(field.value) : field.value;
        if (field.nextElementSibling) field.nextElementSibling.textContent = field.value + "px";
        mark();
      };
    });
  }

  function showBlocks() {
    el.title.textContent = "النصوص والصور داخل المقاطع";
    el.form.innerHTML = "";
    el.form.appendChild(document.getElementById("block-template").content.cloneNode(true));

    var select = document.getElementById("block-select");
    Object.keys(config._blocks).forEach(function (key) {
      var option = document.createElement("option");
      option.value = key;
      option.textContent = config._blocks[key].name || key;
      select.appendChild(option);
    });

    function load() {
      var block = config._blocks[select.value];
      el.form.querySelector('[data-block=eyebrow]').value = block.eyebrow || "";
      el.form.querySelector('[data-block=title]').value = block.title || "";
      el.form.querySelector('[data-block=body]').value =
        Array.isArray(block.body) ? block.body.join("\n\n") : (block.body || "");
      document.getElementById("image-path").value =
        (config.images && config.images[select.value]) || "";
    }

    select.onchange = load;
    el.form.querySelectorAll("[data-block]").forEach(function (field) {
      field.oninput = function () {
        var block = config._blocks[select.value];
        var key = field.dataset.block;
        block[key] = key === "body" ? field.value.split(/\n\s*\n/).filter(Boolean) : field.value;
        mark();
      };
    });
    document.getElementById("image-path").oninput = function () {
      if (!config.images) config.images = {};
      config.images[select.value] = this.value;
      mark();
    };
    document.getElementById("image-file").onchange = function () {
      upload(this.files[0], select.value, function (path) {
        if (!config.images) config.images = {};
        config.images[select.value] = path;
        document.getElementById("image-path").value = path;
        mark();
      });
    };
    load();
  }

  function newsSlides() {
    if (!Array.isArray(config.news_slides)) config.news_slides = [];
    return config.news_slides;
  }

  function drawNews() {
    var list = document.getElementById("news-list");
    if (!list) return;
    var items = newsSlides();
    list.innerHTML = items.length ? "" : '<p class="hint">ما كايناش صور. زيد وحدة.</p>';

    items.forEach(function (slide, index) {
      var box = document.createElement("div");
      box.className = "tweet-item";
      box.innerHTML =
        '<div class="tweet-item__head"><strong>خبر ' + (index + 1) + '</strong>' +
        '<button type="button" data-up ' + (index ? "" : "disabled") + '>▲</button>' +
        '<button type="button" data-down ' + (index === items.length - 1 ? "disabled" : "") + '>▼</button>' +
        '<button type="button" class="danger" data-remove>امسح</button></div>' +
        '<div class="grid">' +
        '<label class="wide">الصورة<input data-n="image" dir="ltr" value="' + esc(slide.image || "") + '" placeholder="/img/..."></label>' +
        '<label class="wide">حمّل صورة<input type="file" data-n-file accept="image/png,image/jpeg,image/webp,image/gif"></label>' +
        '<label class="wide">وصف الصورة<input data-n="alt" value="' + esc(slide.alt || "") + '"></label>' +
        '<label class="wide">رابط اختياري<input data-n="link" dir="ltr" value="' + esc(slide.link || "") + '"></label>' +
        '</div>' +
        (slide.image ? '<img class="news-thumb" src="' + esc(slide.image) + '" alt="">' : "");

      box.querySelectorAll("[data-n]").forEach(function (field) {
        field.oninput = function () { slide[field.dataset.n] = field.value; mark(); };
      });
      box.querySelector("[data-n-file]").onchange = function () {
        upload(this.files[0], "news-" + (index + 1), function (path) {
          slide.image = path; mark(); drawNews();
        });
      };
      box.querySelector("[data-remove]").onclick = function () {
        if (!confirm("تمسح هاد الصورة؟")) return;
        items.splice(index, 1); mark(); drawNews();
      };
      box.querySelector("[data-up]").onclick = function () {
        if (!index) return;
        items.splice(index - 1, 0, items.splice(index, 1)[0]); mark(); drawNews();
      };
      box.querySelector("[data-down]").onclick = function () {
        if (index === items.length - 1) return;
        items.splice(index + 1, 0, items.splice(index, 1)[0]); mark(); drawNews();
      };
      list.appendChild(box);
    });
  }

  function showNews() {
    el.title.textContent = "صور الأخبار";
    el.form.innerHTML = "";
    el.form.appendChild(document.getElementById("news-template").content.cloneNode(true));
    drawNews();
    document.getElementById("news-add").onclick = function () {
      newsSlides().push({ image: "", alt: "", link: "" });
      mark();
      drawNews();
    };
  }

  function showClick() {
    el.title.textContent = "اختار من المعاينة";
    el.form.innerHTML = "";
    el.form.appendChild(document.getElementById("click-template").content.cloneNode(true));
    wireControls();
    if (selected) drawSelection(); else drawEmpty();
  }

  function setMode(next) {
    mode = next;
    document.querySelectorAll("[data-view]").forEach(function (button) {
      button.classList.toggle("active", button.dataset.view === next);
    });
    el.sections.hidden = next !== "sections";
    if (next !== "click") selected = null;
    if (next === "click") showClick();
    if (next === "sections") { current = Object.keys(config.sections)[0]; nav(); showSection(current); }
    if (next === "blocks") showBlocks();
    if (next === "news") showNews();
    if (next === "theme") showTheme();
  }

  /* -------------------------------------------------------------- actions */

  async function upload(file, slot, done) {
    if (!file) return;
    try {
      say("كنرفع الصورة…");
      var response = await fetch("/api/upload", {
        method: "POST",
        headers: {
          "X-Editor-Token": token, "X-Slot": slot,
          "X-Filename": file.name, "Content-Type": file.type || "application/octet-stream"
        },
        body: file
      });
      var data = await response.json();
      if (!response.ok) throw new Error(data.error);
      done(data.path);
      say("الصورة ترفعات. دير حفظ باش تتسجل");
    } catch (error) {
      say(error.message, true);
    }
  }

  async function post(path, body) {
    var response = await fetch(path, {
      method: "POST",
      headers: { "X-Editor-Token": token, "Content-Type": "application/json" },
      body: body
    });
    var data = await response.json();
    if (!response.ok) throw new Error(data.error || "فشل الطلب");
    return data;
  }

  function loadPage() {
    selected = null;
    el.frame.src = config._pages[pageKey()].url + "?v=" + Date.now();
    if (mode === "click") showClick();
  }

  document.querySelectorAll("[data-view]").forEach(function (button) {
    button.onclick = function () { setMode(button.dataset.view); };
  });

  document.getElementById("save").onclick = async function () {
    try {
      say("كنحفظ وكنبني المعاينة…");
      var result = await post("/api/save", JSON.stringify(config));
      dirty = false;
      say(result.message);
      loadPage();
    } catch (error) {
      say(error.message, true);
    }
  };

  document.getElementById("preview").onclick = function () {
    el.frame.scrollIntoView({ behavior: "smooth" });
    el.frame.src = config._pages[pageKey()].url + "?v=" + Date.now();
  };

  document.getElementById("publish").onclick = async function () {
    if (!confirm("واش متأكد بغيتي تحفظ، تدير commit، وتنشر التغييرات فـ main؟")) return;
    try {
      if (dirty) await post("/api/save", JSON.stringify(config));
      say("كننشر فـ GitHub…");
      var result = await post("/api/publish", "{}");
      dirty = false;
      say(result.message);
    } catch (error) {
      say(error.message, true);
    }
  };

  window.addEventListener("beforeunload", function (event) {
    if (!dirty) return;
    event.preventDefault();
    event.returnValue = "";
  });

  el.frame.addEventListener("load", wireFrame);

  /* ----------------------------------------------------------------- boot */

  try {
    var response = await fetch("/api/config", { cache: "no-store" });
    config = await response.json();
    token = config._token;
    delete config._token;

    Object.keys(config._pages).forEach(function (key) {
      var option = document.createElement("option");
      option.value = key;
      option.textContent = config._pages[key].name;
      el.page.appendChild(option);
    });
    el.page.onchange = loadPage;

    say(config._git
      ? "كاينة تغييرات محلية قبل المحرر؛ النشر غادي يشملها"
      : "المحرر واجد");
    nav();
    setMode("click");
    loadPage();
  } catch (error) {
    say("ما قدرناش نحملو الإعدادات: " + error.message, true);
  }
}());
