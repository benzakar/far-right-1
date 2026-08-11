#!/bin/sh
python3 build.py || exit 1
python3 - <<'PY'
p='dist/js/motion.js'; s=open(p,encoding='utf-8').read()
s=s.replace('if (reduced.matches) return;','if (reduced.matches && !location.search.includes("motion=1")) return;',1)
s=s.replace('    requestAnimationFrame(frame);','    frame();',1)
open(p,'w',encoding='utf-8').write(s)
p='dist/css/site.css'; s=open(p,encoding='utf-8').read()
s=s.replace('@media (prefers-reduced-motion: reduce) {','@media (prefers-reduced-motion: reduce) and (min-width:99999px) {')
open(p,'w',encoding='utf-8').write(s)
PY
echo "dev patches applied (dist only)"
