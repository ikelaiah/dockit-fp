"""Shared DocKit-FP browser assets."""

SITE_CSS = r'''
:root{
  color-scheme:light dark;
  --dk-accent:#2563eb;
  --dk-accent-secondary:#0ea5e9;
  --bg:#fff;
  --surface:#f8fafc;
  --text:#172033;
  --muted:#526076;
  --border:#d9e0ea;
  --code:#111827;
  --code-text:#e5e7eb;
  --dk-font-ui:"Segoe UI Variable Text","Aptos",Inter,system-ui,-apple-system,"Segoe UI",sans-serif;
  --dk-font-display:"Segoe UI Variable Display","Aptos Display",var(--dk-font-ui);
  --dk-font-mono:"Cascadia Code",ui-monospace,SFMono-Regular,Consolas,monospace;
}
html[data-theme="light"]{color-scheme:light}
html[data-theme="dark"]{color-scheme:dark;--bg:#111827;--surface:#1f2937;--text:#f3f4f6;--muted:#b8c2d3;--border:#3b4659;--code:#030712}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--dk-font-ui);font-size:17px;line-height:1.72;font-synthesis:none;text-rendering:optimizeLegibility}
.site-header{border-bottom:1px solid var(--border);background:var(--bg);position:sticky;top:0;z-index:2}
.topbar{display:flex;gap:1rem;align-items:center;max-width:1440px;margin:auto;padding:.7rem 1rem}
.brand{font-family:var(--dk-font-display);font-size:.95rem;font-weight:750;letter-spacing:-.025em;color:var(--text);text-decoration:none;white-space:nowrap}
.brand span{color:var(--dk-accent)}
.topbar input{min-width:8rem;max-width:25rem;flex:1;padding:.5rem .6rem;border:1px solid var(--border);border-radius:.35rem;background:var(--surface);color:var(--text);font:inherit;font-size:.82rem}
select,button{min-height:2.5rem;border:1px solid var(--border);border-radius:.35rem;padding:.35rem .5rem;background:var(--surface);color:var(--text);font:inherit;font-size:.82rem}
button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid var(--dk-accent-secondary);outline-offset:2px}
.shell{max-width:1440px;margin:auto;display:grid;grid-template-columns:15rem minmax(0,46rem) 13rem;gap:2.5rem;padding:1.75rem 1rem}
.sidebar{font-size:.86rem;line-height:1.45}
.sidebar a{display:block;padding:.28rem .35rem;color:var(--muted);text-decoration:none}
.sidebar a:hover{color:var(--text);text-decoration:underline;text-decoration-color:var(--dk-accent-secondary);text-underline-offset:.2em}
.sidebar a.active{color:var(--dk-accent);font-weight:700;border-left:3px solid var(--dk-accent)}
.sidebar h2{margin:1.1rem 0 .5rem;font-family:var(--dk-font-display);font-size:.72rem;font-weight:750;letter-spacing:.09em;text-transform:uppercase}
.sidebar h2:first-child{margin-top:.25rem}
.prose{min-width:0;max-width:46rem}
.prose h1,.prose h2,.prose h3{font-family:var(--dk-font-display);font-weight:720;letter-spacing:-.032em;text-wrap:balance}
.prose h1{font-size:clamp(2.3rem,4vw,3rem);line-height:1.08;margin:0 0 1rem}
.prose h2{font-size:1.7rem;line-height:1.2;margin:2.75rem 0 .8rem}
.prose h3{font-size:1.25rem;line-height:1.3;margin:2.15rem 0 .6rem}
.prose p,.prose li{max-width:43rem}
.prose p{margin:.8rem 0}
.prose ul,.prose ol{padding-left:1.45rem}
.prose a{color:var(--dk-accent);font-weight:600;text-decoration-thickness:.08em;text-underline-offset:.16em}
.prose a:hover{text-decoration-thickness:.13em}
.prose pre{overflow:auto;background:var(--code);color:var(--code-text);padding:1rem 1.15rem;border-radius:.45rem;font-size:.9rem;line-height:1.6}
.prose code{font-family:var(--dk-font-mono);font-size:.88em}
.prose :not(pre)>code{background:var(--surface);padding:.12rem .28rem;border-radius:.2rem}
.table-scroll{overflow:auto}
.prose table{border-collapse:collapse;min-width:32rem;width:100%;font-size:.92rem}
.prose th,.prose td{border:1px solid var(--border);padding:.6rem;text-align:left}
.prose th{font-family:var(--dk-font-display);font-weight:700;background:var(--surface)}
.admonition{border-left:4px solid var(--dk-accent);padding:.75rem 1rem;background:var(--surface)}
.admonition p:first-child{margin-top:0}.admonition p:last-child{margin-bottom:0}
.banner{max-width:100%;height:auto;max-height:14rem}
.search-results{position:absolute;top:3.8rem;left:max(1rem,calc((100% - 70rem)/2));width:min(34rem,calc(100% - 2rem));background:var(--bg);border:1px solid var(--border);box-shadow:0 .7rem 2rem #0003;padding:.5rem}
.search-results a{display:block;color:var(--text);padding:.45rem;text-decoration:none}.search-results small{display:block;color:var(--muted)}
.mobile-nav{display:none}.toc{font-size:.82rem;line-height:1.45;color:var(--muted)}
@media(max-width:1024px){.shell{grid-template-columns:13rem minmax(0,46rem);gap:2rem}.toc{display:none}}
@media(max-width:768px){body{font-size:16px}.topbar{flex-wrap:wrap}.topbar input{order:3;flex-basis:100%;max-width:none}.shell{display:block;padding-top:1rem}.sidebar{display:none}.mobile-nav{display:block;padding:0 1rem 1rem}.mobile-nav summary{cursor:pointer}.toc{display:none}.prose h1{font-size:2.05rem}}
@media(max-width:420px){.topbar{gap:.5rem}.brand{font-size:.9rem}.topbar select,button{font-size:.78rem}}
'''

SITE_JS = r'''
(()=>{const root=document.documentElement,key='dockit-fp-theme',select=document.querySelector('#theme-select');function set(v){if(v==='system')delete root.dataset.theme;else root.dataset.theme=v;try{localStorage.setItem(key,v)}catch(_){}}try{const v=localStorage.getItem(key);if(['light','dark','system'].includes(v)){select.value=v;set(v)}}catch(_){}select?.addEventListener('change',()=>set(select.value));const version=document.querySelector('#version-select');version?.addEventListener('change',()=>{location.href=version.value});const input=document.querySelector('#search'),results=document.querySelector('#search-results');let entries=[];fetch(input?.dataset.searchIndex||'search-index.json').then(r=>r.ok?r.json():[]).then(v=>entries=v).catch(()=>{});function show(){const query=input.value.trim().toLowerCase();if(!query){results.hidden=true;return}const matches=entries.filter(e=>(e.title+' '+e.text).toLowerCase().includes(query)).slice(0,8);results.replaceChildren(...matches.map(e=>{const a=document.createElement('a');a.href=e.url;const b=document.createElement('strong');b.textContent=e.title;const s=document.createElement('small');s.textContent=e.section;a.append(b,s);return a}));results.hidden=false}input?.addEventListener('input',show);document.addEventListener('keydown',e=>{if(e.key==='/'&&document.activeElement!==input){e.preventDefault();input?.focus()}})})();
'''

MATH_JS = r'''
(()=>{function render(node,displayMode){if(!globalThis.katex){node.textContent=node.dataset.tex||'';return}try{globalThis.katex.render(node.dataset.tex||'',node,{displayMode,throwOnError:false,strict:'ignore'})}catch(_){node.textContent=node.dataset.tex||''}}document.querySelectorAll('.math-inline').forEach(node=>render(node,false));document.querySelectorAll('.math-display').forEach(node=>render(node,true))})();
'''
