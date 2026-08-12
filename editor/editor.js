(async function(){
  "use strict";
  var config, token, current, mode="click", dirty=false, selected=null;
  var sections=document.getElementById("sections"), form=document.getElementById("form"), status=document.getElementById("status"), frame=document.getElementById("frame"), title=document.getElementById("view-title"), pageSel=document.getElementById("page");
  function say(message,error){status.textContent=message;status.style.color=error?"#9a271e":""}
  function mark(){dirty=true;say("عندك تغييرات مازال ما تحفظوش");}
  function esc(s){return String(s||"").replace(/[&<>\"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
  function pageKey(){return pageSel.value}
  function pageOps(){config.page_overrides=config.page_overrides||{};return config.page_overrides[pageKey()]||(config.page_overrides[pageKey()]={})}
  function op(id){return pageOps()[id]||(pageOps()[id]={})}
  function nav(){sections.innerHTML="";Object.keys(config.sections).forEach(function(id){var b=document.createElement("button");b.textContent=config.sections[id].name||id;b.dataset.id=id;b.className=id===current?"active":"";b.onclick=function(){showSection(id)};sections.appendChild(b)})}
  function setMode(next){mode=next;document.querySelectorAll('[data-view]').forEach(function(b){b.classList.toggle('active',b.dataset.view===next)});sections.hidden=next!=="sections";selected=null;if(next==="click")showClick();if(next==="sections"){current=Object.keys(config.sections)[0];nav();showSection(current)}if(next==="blocks")showBlocks();if(next==="theme")showTheme()}
  /* Tweets are a list. The older single `tweet` object is folded into it on
     first edit so existing configuration is never silently dropped. */
  function tweetsOf(s){
    if(!Array.isArray(s.tweets)){
      s.tweets=[];
      if(s.tweet&&s.tweet.text){var t=s.tweet;t.enabled=t.enabled!==false;s.tweets.push(t)}
      delete s.tweet;
    }
    return s.tweets;
  }
  function drawTweets(s){
    var list=document.getElementById("tweet-list");if(!list)return;
    var items=tweetsOf(s);list.innerHTML="";
    if(!items.length){list.innerHTML='<p class="hint">ما كايناش تغريدات فهاد المقطع.</p>'}
    items.forEach(function(t,i){
      var box=document.createElement("div");box.className="tweet-item";
      box.innerHTML='<div class="tweet-item__head"><strong>تغريدة '+(i+1)+'</strong>'
        +'<label class="switch"><input type="checkbox" data-t="enabled"'+(t.enabled!==false?" checked":"")+'> مفعّلة</label>'
        +'<button type="button" class="danger" data-remove="'+i+'">امسح</button></div>'
        +'<div class="grid">'
        +'<label>الاسم<input data-t="name" value="'+esc(t.name||"Ben Zakar")+'"></label>'
        +'<label>الحساب<input data-t="handle" dir="ltr" value="'+esc(t.handle||"@benzakarMorocco")+'"></label>'
        +'<label class="wide">نص التغريدة<textarea data-t="text" rows="4">'+esc(t.text||"")+'</textarea></label>'
        +'<label>التاريخ<input data-t="date" dir="ltr" value="'+esc(t.date||"")+'" placeholder="Aug 11, 2026"></label>'
        +'<label>صورة الحساب<input data-t="avatar" dir="ltr" value="'+esc(t.avatar||"")+'" placeholder="/img/..."></label>'
        +'</div>';
      box.querySelectorAll("[data-t]").forEach(function(el){
        el.oninput=function(){t[el.dataset.t]=el.type==="checkbox"?el.checked:el.value;mark()};
        el.onchange=el.oninput;
      });
      box.querySelector("[data-remove]").onclick=function(){
        if(!confirm("تمسح هاد التغريدة؟"))return;
        items.splice(i,1);mark();drawTweets(s);
      };
      list.appendChild(box);
    });
  }
  function showSection(id){current=id;nav();var s=config.sections[id], node=document.getElementById("section-template").content.cloneNode(true);title.textContent=s.name||id;form.innerHTML="";form.appendChild(node);form.querySelectorAll("[data-field]").forEach(function(el){el.value=s[el.dataset.field]||"";el.oninput=function(){s[el.dataset.field]=el.value;mark();if(el.dataset.field==="name"){title.textContent=el.value;nav()}}});drawTweets(s);document.getElementById("tweet-add").onclick=function(){tweetsOf(s).push({enabled:true,name:"Ben Zakar",handle:"@benzakarMorocco",text:"",date:"",avatar:"/img/ben-zakar-x-profile.jpg"});mark();drawTweets(s)}}
  function showTheme(){title.textContent="ألوان الموقع والزوايا";var t=config.theme;form.innerHTML='<div class="theme-grid">'+[["green","الأخضر"],["red","الأحمر"],["gold","الذهبي"],["panel","لون الصناديق"],["ink","لون الكتابة"]].map(function(x){return'<label>'+x[1]+'<input type="color" data-theme="'+x[0]+'" value="'+esc(t[x[0]])+'"></label>'}).join("")+'<label>استدارة الصناديق<input type="range" min="8" max="48" data-theme="radius" value="'+(t.radius||28)+'"><output>'+(t.radius||28)+'px</output></label></div>';form.querySelectorAll("[data-theme]").forEach(function(el){el.oninput=function(){t[el.dataset.theme]=el.type==="range"?Number(el.value):el.value;if(el.nextElementSibling)el.nextElementSibling.textContent=el.value+"px";mark()}})}
  function showBlocks(){title.textContent="النصوص والصور داخل المقاطع";form.innerHTML="";form.appendChild(document.getElementById("block-template").content.cloneNode(true));var select=document.getElementById("block-select");Object.keys(config._blocks).forEach(function(key){var o=document.createElement("option");o.value=key;o.textContent=config._blocks[key].name||key;select.appendChild(o)});function load(){var key=select.value,b=config._blocks[key];form.querySelector('[data-block=eyebrow]').value=b.eyebrow||"";form.querySelector('[data-block=title]').value=b.title||"";form.querySelector('[data-block=body]').value=Array.isArray(b.body)?b.body.join("\n\n"):b.body||"";document.getElementById("image-path").value=(config.images&&config.images[key])||""}select.onchange=load;form.querySelectorAll("[data-block]").forEach(function(el){el.oninput=function(){var b=config._blocks[select.value],key=el.dataset.block;b[key]=key==="body"?el.value.split(/\n\s*\n/).filter(Boolean):el.value;mark()}});document.getElementById("image-path").oninput=function(){config.images=config.images||{};config.images[select.value]=this.value;mark()};document.getElementById("image-file").onchange=function(){upload(this.files[0],select.value,function(path){config.images=config.images||{};config.images[select.value]=path;document.getElementById("image-path").value=path;mark()})};load()}
  function showClick(){title.textContent="اختار من المعاينة";form.innerHTML="";form.appendChild(document.getElementById("click-template").content.cloneNode(true));wireControls();if(selected)drawSelection()}
  function describe(el){var t=el.tagName.toLowerCase();if(/^h/.test(t))return"عنوان";if(t==="p")return"فقرة";if(t==="blockquote")return"اقتباس";if(t==="img")return"صورة";if(t==="a")return"زر أو رابط";if(t==="section")return"مقطع";return"صندوق أو بطاقة"}
  function wireFrame(){var doc=frame.contentDocument;if(!doc||!doc.getElementById("main"))return;var style=doc.createElement("style");style.textContent='[data-edit-id]{transition:outline-color .15s}[data-edit-id]:hover{outline:2px dashed #c9a45e!important;outline-offset:2px;cursor:pointer}.editor-selected{outline:4px solid #8c2f23!important;outline-offset:3px}';doc.head.appendChild(style);doc.addEventListener("click",function(e){var el=e.target.closest("[data-edit-id]");if(!el)return;e.preventDefault();e.stopPropagation();doc.querySelectorAll(".editor-selected").forEach(function(n){n.classList.remove("editor-selected")});el.classList.add("editor-selected");selected={el:el,id:el.dataset.editId};if(mode!=="click")setMode("click");else drawSelection();document.getElementById("form").scrollIntoView({behavior:"smooth",block:"start"})},true)}
  function mergeStyle(existing,prop,value){var out={};String(existing||"").split(";").forEach(function(d){var i=d.indexOf(":");if(i>0)out[d.slice(0,i).trim()]=d.slice(i+1).trim()});if(value)out[prop]=value;else delete out[prop];return Object.keys(out).map(function(k){return k+":"+out[k]}).join("; ")}
  function styleValue(style,prop){var found="";String(style||"").split(";").forEach(function(d){var i=d.indexOf(":");if(i>0&&d.slice(0,i).trim()===prop)found=d.slice(i+1).trim()});return found}
  function setStyle(prop,value){if(!selected)return;var o=op(selected.id);o.style=mergeStyle(o.style||selected.el.getAttribute("style"),prop,value);selected.el.style.setProperty(prop,value);mark();drawSelection()}
  function setAttr(name,value){if(!selected)return;op(selected.id)[name]=value;selected.el.setAttribute(name,value);mark()}
  function drawSelection(){if(!selected)return;var el=selected.el,tag=el.tagName.toLowerCase(),o=op(selected.id);document.getElementById("selection-empty").hidden=true;document.getElementById("selection-controls").hidden=false;document.getElementById("selection-name").textContent=describe(el)+" · "+selected.id;var textual=/^(h1|h2|h3|p|blockquote|a)$/.test(tag);document.getElementById("text-field").hidden=!textual;
    /* a paragraph can become a heading and back; nothing else re-tags */
    document.getElementById("shape-tools").hidden=!/^(p|h3)$/.test(tag);
    document.querySelectorAll("[data-tag]").forEach(function(b){b.classList.toggle("active",b.dataset.tag===tag)});
    document.getElementById("remove-element").hidden=!!o.removed;
    document.getElementById("restore-element").hidden=!o.removed;var ta=document.getElementById("selected-text");ta.value=o.text!==undefined?o.text:el.textContent.trim();document.getElementById("box-tools").hidden=!/^(section|article|div)$/.test(tag);document.getElementById("image-tools").hidden=tag!=="img";document.getElementById("link-tools").hidden=tag!=="a";document.getElementById("quote-tool").hidden=tag!=="p";document.getElementById("selected-quote").checked=(o.class||el.className).split(/\s+/).indexOf("section-quote")>=0;if(tag==="img")document.getElementById("selected-src").value=o.src||el.getAttribute("src")||"";if(tag==="a")document.getElementById("selected-href").value=o.href||el.getAttribute("href")||"";document.querySelectorAll("[data-style]").forEach(function(b){b.classList.toggle("active",styleValue(o.style||el.getAttribute("style"),b.dataset.style)===b.dataset.value)})}
  /* The preview mirrors a split so the result is visible before saving; the
     authoritative rewrite happens at build time. */
  function paintSplit(el,value){
    var chunks=String(value).split(/\n\s*\n/).map(function(c){return c.trim()}).filter(Boolean);
    while(el.nextSibling&&el.nextSibling.dataset&&/-\d+$/.test(el.nextSibling.dataset.editId||"")
          &&(el.nextSibling.dataset.editId||"").indexOf(el.dataset.editId+"-")===0){
      el.nextSibling.remove();
    }
    el.textContent=chunks[0]||"";
    var after=el;
    chunks.slice(1).forEach(function(chunk,i){
      var clone=el.cloneNode(false);
      clone.dataset.editId=el.dataset.editId+"-"+(i+1);
      clone.textContent=chunk;
      after.insertAdjacentElement("afterend",clone);
      after=clone;
    });
  }
  function wireControls(){document.getElementById("selected-text").oninput=function(){if(!selected)return;op(selected.id).text=this.value;paintSplit(selected.el,this.value);mark()};
    document.querySelectorAll("[data-tag]").forEach(function(b){b.onclick=function(){
      if(!selected)return;
      var want=b.dataset.tag, el=selected.el, cur=el.tagName.toLowerCase();
      if(cur===want)return;
      op(selected.id).tag=want;
      /* swap the node in the preview so the change is visible at once */
      var replacement=frame.contentDocument.createElement(want);
      replacement.innerHTML=el.innerHTML;
      Array.prototype.forEach.call(el.attributes,function(a){replacement.setAttribute(a.name,a.value)});
      el.replaceWith(replacement);
      replacement.classList.add("editor-selected");
      selected.el=replacement;
      mark();drawSelection();
    }});
    document.getElementById("remove-element").onclick=function(){
      if(!selected)return;
      if(!confirm("تمسح هاد العنصر من الصفحة؟"))return;
      op(selected.id).removed=true;
      selected.el.hidden=true;selected.el.style.display="none";
      mark();drawSelection();
    };
    document.getElementById("restore-element").onclick=function(){
      if(!selected)return;
      delete op(selected.id).removed;
      selected.el.hidden=false;selected.el.style.display="";
      mark();drawSelection();
    };document.querySelectorAll("[data-style]").forEach(function(b){b.onclick=function(){setStyle(b.dataset.style,b.dataset.value)}});document.querySelectorAll("[data-section-tone]").forEach(function(b){b.onclick=function(){if(!selected)return;var section=selected.el.closest("section[id]");if(!section)return say("هاد العنصر ما تابع حتى لمقطع قابل لتغيير الخلفية",true);var id=section.id;if(!config.sections[id])return say("هاد المقطع ما كاينش فإعدادات الرئيسية",true);config.sections[id].background=b.dataset.sectionTone;section.classList.toggle("bay--greenback",b.dataset.sectionTone==="green");section.classList.toggle("bay--redback",b.dataset.sectionTone==="red");mark()}});document.getElementById("selected-src").onchange=function(){setAttr("src",this.value.trim())};document.getElementById("selected-href").onchange=function(){setAttr("href",this.value.trim())};document.getElementById("selected-quote").onchange=function(){if(!selected)return;var names=(op(selected.id).class||selected.el.className).split(/\s+/).filter(Boolean),i=names.indexOf("section-quote");if(this.checked&&i<0)names.push("section-quote");if(!this.checked&&i>=0)names.splice(i,1);op(selected.id).class=names.join(" ");selected.el.className=names.join(" ");mark()};document.getElementById("selected-file").onchange=function(){upload(this.files[0],pageKey()+"-"+selected.id,function(path){document.getElementById("selected-src").value=path;setAttr("src",path)})}}
  async function upload(file,slot,done){if(!file)return;try{say("كنرفع الصورة…");var r=await fetch("/api/upload",{method:"POST",headers:{"X-Editor-Token":token,"X-Slot":slot,"X-Filename":file.name,"Content-Type":file.type||"application/octet-stream"},body:file}),data=await r.json();if(!r.ok)throw new Error(data.error);done(data.path);say("الصورة ترفعات. دير حفظ باش تتسجل") }catch(e){say(e.message,true)}}
  async function post(path,body){var r=await fetch(path,{method:"POST",headers:{"X-Editor-Token":token,"Content-Type":"application/json"},body:body}),data=await r.json();if(!r.ok)throw new Error(data.error||"فشل الطلب");return data}
  function loadPage(){selected=null;frame.src=config._pages[pageKey()].url+"?v="+Date.now();if(mode==="click")showClick()}
  document.querySelectorAll("[data-view]").forEach(function(b){b.onclick=function(){setMode(b.dataset.view)}});
  document.getElementById("save").onclick=async function(){try{say("كنحفظ وكنبني المعاينة…");var r=await post("/api/save",JSON.stringify(config));dirty=false;say(r.message);loadPage()}catch(e){say(e.message,true)}};
  document.getElementById("preview").onclick=function(){frame.scrollIntoView({behavior:"smooth"});frame.src=config._pages[pageKey()].url+"?v="+Date.now()};
  document.getElementById("publish").onclick=async function(){if(!confirm("واش متأكد بغيتي تحفظ، تدير commit، وتنشر التغييرات فـ main؟"))return;try{if(dirty)await post("/api/save",JSON.stringify(config));say("كننشر فـ GitHub…");var r=await post("/api/publish","{}");dirty=false;say(r.message)}catch(e){say(e.message,true)}};
  frame.addEventListener("load",wireFrame);
  try{var r=await fetch("/api/config",{cache:"no-store"});config=await r.json();token=config._token;delete config._token;Object.keys(config._pages).forEach(function(key){var o=document.createElement("option");o.value=key;o.textContent=config._pages[key].name;pageSel.appendChild(o)});pageSel.onchange=loadPage;say(config._git?"كاينة تغييرات محلية قبل المحرر؛ النشر غادي يشملها":"المحرر واجد");nav();setMode("click");loadPage()}catch(e){say("ما قدرناش نحملو الإعدادات: "+e.message,true)}
}());
