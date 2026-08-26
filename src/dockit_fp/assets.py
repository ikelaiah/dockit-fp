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
  --raised:#fff;
  --focus-ring:#087ea4;
  --interactive:color-mix(in srgb,var(--dk-accent) 78%,#000);
  --dk-content-width:46rem;
  --dk-reading-width:43rem;
  --dk-shell-width:90rem;
  --dk-radius:.35rem;
  --dk-font-ui:"Segoe UI Variable Text","Aptos",Inter,system-ui,-apple-system,"Segoe UI",sans-serif;
  --dk-font-display:"Segoe UI Variable Display","Aptos Display",var(--dk-font-ui);
  --dk-font-body:var(--dk-font-ui);
  --dk-font-mono:"Cascadia Code",ui-monospace,SFMono-Regular,Consolas,monospace;
}
html[data-content-width="compact"]{--dk-content-width:40rem;--dk-reading-width:38rem;--dk-shell-width:84rem}
html[data-content-width="wide"]{--dk-content-width:54rem;--dk-reading-width:46rem;--dk-shell-width:98rem}
html[data-theme="light"]{color-scheme:light}
html[data-theme="dark"]{color-scheme:dark;--bg:#111827;--surface:#1f2937;--text:#f3f4f6;--muted:#b8c2d3;--border:#3b4659;--code:#030712;--raised:#172033;--focus-ring:#67e8f9;--interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}
html[data-visual-theme="paper"]{--bg:#fdfbf7;--surface:#f4eee3;--text:#312d26;--muted:#6c6254;--border:#d7cab7;--code:#2b2925;--raised:#fffefb;--focus-ring:#9a3412;--dk-font-display:Georgia,"Times New Roman",serif;--dk-font-body:Georgia,"Times New Roman",serif}
html[data-visual-theme="paper"][data-theme="dark"]{color-scheme:dark;--bg:#1c1a17;--surface:#29251f;--text:#f7f0e5;--muted:#c9bcaa;--border:#554b3d;--code:#11100e;--raised:#24211c;--focus-ring:#fdba74;--interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}
html[data-visual-theme="midnight"]{color-scheme:dark;--bg:#0d1220;--surface:#182033;--text:#eef3ff;--muted:#b4c0d8;--border:#35415a;--code:#050912;--raised:#121a2b;--focus-ring:#67e8f9;--interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}
html[data-visual-theme="midnight"][data-theme="light"]{color-scheme:light;--bg:#f5f8ff;--surface:#e8eefb;--text:#17223a;--muted:#52617c;--border:#c7d2e8;--code:#101827;--raised:#fff;--focus-ring:#075985;--interactive:color-mix(in srgb,var(--dk-accent) 78%,#000)}
@media(prefers-color-scheme:dark){html[data-visual-theme="classic"]:not([data-theme]){color-scheme:dark;--bg:#111827;--surface:#1f2937;--text:#f3f4f6;--muted:#b8c2d3;--border:#3b4659;--code:#030712}}
@media(prefers-color-scheme:dark){html[data-visual-theme="classic"]:not([data-theme]){--raised:#172033;--focus-ring:#67e8f9;--interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}}
@media(prefers-color-scheme:dark){html[data-visual-theme="paper"]:not([data-theme]){color-scheme:dark;--bg:#1c1a17;--surface:#29251f;--text:#f7f0e5;--muted:#c9bcaa;--border:#554b3d;--code:#11100e;--raised:#24211c;--focus-ring:#fdba74;--interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}}
*{box-sizing:border-box}
.visually-hidden{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--dk-font-body);font-size:17px;line-height:1.72;font-synthesis:none;text-rendering:optimizeLegibility}
.reading-progress{position:fixed;inset:0 0 auto;z-index:3;height:3px;background:var(--border);pointer-events:none}.reading-progress span{display:block;width:100%;height:100%;background:var(--dk-accent);transform:scaleX(0);transform-origin:left}
.site-header{border-bottom:1px solid var(--border);background:var(--bg);position:sticky;top:0;z-index:2}
.topbar{display:flex;gap:1rem;align-items:center;max-width:var(--dk-shell-width);margin:auto;padding:.7rem 1rem;font-family:var(--dk-font-ui)}
.brand{display:inline-flex;align-items:center;gap:.35rem;font-family:var(--dk-font-display);font-size:.95rem;font-weight:750;letter-spacing:-.025em;color:var(--text);text-decoration:none;white-space:nowrap}
.brand>span{color:var(--text)}.brand em{color:var(--interactive);font-style:normal}
.brand-mark{width:1.05rem;height:1.05rem;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:1.4;color:var(--interactive)}
.search-control{position:relative;display:flex;align-items:center;min-width:8rem;max-width:25rem;flex:1}
.topbar .search-control input{width:100%;min-width:0;max-width:none;padding:.5rem 2rem .5rem .6rem;border:1px solid var(--border);border-radius:var(--dk-radius);background:var(--surface);color:var(--text);font:inherit;font-size:.82rem}
.search-control kbd{position:absolute;right:.45rem;border:1px solid var(--border);border-radius:.2rem;padding:0 .22rem;color:var(--muted);font-family:var(--dk-font-mono);font-size:.7rem;line-height:1.3}
select,button{min-height:2.5rem;border:1px solid var(--border);border-radius:var(--dk-radius);padding:.35rem .5rem;background:var(--surface);color:var(--text);font:inherit;font-size:.82rem}
button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--focus-ring);outline-offset:3px}
.shell{max-width:var(--dk-shell-width);margin:auto;display:grid;grid-template-columns:15rem minmax(0,var(--dk-content-width)) 13rem;gap:2.5rem;padding:2rem 1rem 2.5rem}
.sidebar{font-size:.86rem;line-height:1.45}
.sidebar a{display:block;padding:.28rem .35rem;color:var(--muted);text-decoration:none}
.sidebar a:hover{color:var(--text);text-decoration:underline;text-decoration-color:var(--dk-accent-secondary);text-underline-offset:.2em}
.sidebar a.active{color:var(--interactive);font-weight:700;border-left:3px solid var(--dk-accent)}
.sidebar h2{margin:1.1rem 0 .5rem;font-family:var(--dk-font-display);font-size:.72rem;font-weight:750;letter-spacing:.09em;text-transform:uppercase}
.sidebar h2:first-child{margin-top:.25rem}
.prose{min-width:0;max-width:var(--dk-content-width)}
.prose h1,.prose h2,.prose h3{font-family:var(--dk-font-display);font-weight:720;letter-spacing:-.032em;text-wrap:balance}
.prose h1{font-size:clamp(2.3rem,4vw,3rem);line-height:1.08;margin:0 0 1rem}
.prose h2{font-size:1.7rem;line-height:1.2;margin:2.75rem 0 .8rem}
.prose h3{font-size:1.25rem;line-height:1.3;margin:2.15rem 0 .6rem}
.prose p,.prose li,.prose dl{max-width:var(--dk-reading-width)}
.prose p{margin:.8rem 0}
.prose ul,.prose ol{padding-left:1.45rem}
.prose blockquote{max-width:var(--dk-reading-width);margin:1.25rem 0;padding:.1rem 1rem;border-left:3px solid var(--border);color:var(--muted)}
.prose hr{margin:2.5rem 0;border:0;border-top:1px solid var(--border)}
html[data-visual-theme="paper"] .prose h1,html[data-visual-theme="paper"] .prose h2,html[data-visual-theme="paper"] .prose h3{letter-spacing:-.018em}
html[data-visual-theme="midnight"] .prose h1{color:color-mix(in srgb,var(--text) 88%,var(--dk-accent-secondary))}
.task-list{display:inline-block;width:1.25em;color:var(--interactive);font-weight:700}
.capability-strip{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.5rem;margin:1.25rem 0 1.5rem;padding:0;list-style:none}
.capability-strip li{max-width:none;padding:.7rem .8rem;border:1px solid var(--border);border-radius:var(--dk-radius);background:var(--raised);line-height:1.4}
.capability-strip strong{display:block;font-family:var(--dk-font-display);font-size:.78rem;font-weight:750;letter-spacing:.01em;color:var(--text)}
.capability-strip span{display:block;margin-top:.15rem;color:var(--muted);font-size:.75rem}
.release-context{display:flex;gap:.5rem;align-items:baseline;margin:1rem 0;padding:.55rem .75rem;border-left:3px solid var(--dk-accent);background:var(--surface);font-size:.82rem}.release-context strong{font-family:var(--dk-font-display)}.release-context span{color:var(--muted);font-family:var(--dk-font-mono)}
.prose a{color:var(--interactive);font-weight:600;text-decoration-thickness:.08em;text-underline-offset:.16em}
.prose a:hover{text-decoration-thickness:.13em}
.prose pre{position:relative;overflow:auto;background:var(--code);color:var(--code-text);padding:1.05rem 1.2rem;border:1px solid color-mix(in srgb,var(--border) 55%,transparent);border-radius:var(--dk-radius);font-size:.9rem;line-height:1.65;tab-size:2}
.prose code{font-family:var(--dk-font-mono);font-size:.88em}
.prose :not(pre)>code{background:var(--surface);border:1px solid var(--border);padding:.08rem .28rem;border-radius:.2rem}
.copy-code{position:absolute;top:.55rem;right:.55rem;min-height:0;padding:.2rem .45rem;border-color:#ffffff3d;background:#ffffff12;color:inherit;font-family:var(--dk-font-mono);font-size:.7rem;line-height:1.3;opacity:0;transition:opacity .15s ease}.prose pre:hover .copy-code,.copy-code:focus-visible{opacity:1}
.table-scroll{overflow:auto;margin:1.4rem 0;border:1px solid var(--border);border-radius:var(--dk-radius)}
.prose table{border-collapse:collapse;min-width:32rem;width:100%;font-size:.92rem;line-height:1.5}
.prose th,.prose td{border:0;border-bottom:1px solid var(--border);padding:.65rem .75rem;text-align:left;vertical-align:top}
.prose tr:last-child td{border-bottom:0}.prose tbody tr:nth-child(even){background:color-mix(in srgb,var(--surface) 62%,transparent)}
.prose th{font-family:var(--dk-font-display);font-weight:700;background:var(--surface)}
.admonition{--admonition-accent:var(--dk-accent);max-width:var(--dk-reading-width);margin:1.35rem 0;border:1px solid var(--border);border-left:4px solid var(--admonition-accent);border-radius:0 var(--dk-radius) var(--dk-radius) 0;padding:.8rem 1rem;background:var(--surface)}
.admonition.note{--admonition-accent:#0284c7}.admonition.important{--admonition-accent:#7c3aed}.admonition.tip{--admonition-accent:#0f766e}.admonition.warning{--admonition-accent:#b45309}
.admonition p:first-child{margin-top:0}.admonition p:last-child{margin-bottom:0}
.banner{max-width:100%;height:auto;max-height:14rem}
.search-results{position:absolute;top:3.8rem;left:max(1rem,calc((100% - var(--dk-shell-width))/2 + 16rem));width:min(34rem,calc(100% - 2rem));background:var(--raised);border:1px solid var(--border);border-radius:var(--dk-radius);box-shadow:0 .7rem 2rem #0003;padding:.35rem}
.search-results a{display:block;color:var(--text);padding:.5rem .6rem;text-decoration:none}.search-results a:hover{background:var(--surface)}.search-results small{display:block;color:var(--muted);font-size:.76rem}.search-results mark{background:var(--surface);color:inherit;border-radius:.1rem}.search-results mark{background:color-mix(in srgb,var(--dk-accent) 18%,transparent)}.search-empty{margin:.25rem;padding:.55rem .6rem;color:var(--muted);font-size:.82rem}
.mobile-nav{display:none}.toc{position:sticky;top:5rem;align-self:start;font-size:.8rem;line-height:1.4;color:var(--muted)}
.toc-title{margin:0 0 .5rem;font-family:var(--dk-font-display);font-size:.7rem;font-weight:750;letter-spacing:.08em;text-transform:uppercase;color:var(--text)}
.toc a{display:block;padding:.24rem 0;color:var(--muted);text-decoration:none}.toc a:hover,.toc a.is-active{color:var(--interactive)}.toc a.is-active{font-weight:700}.toc .toc-level-3{padding-left:.75rem;font-size:.94em}.toc-empty-copy{margin:0;font-size:.9em}
.page-navigation{display:flex;gap:.75rem;margin:3.25rem 0 1rem;padding-top:1rem;border-top:1px solid var(--border)}.page-navigation a{display:flex;flex-direction:column;max-width:48%;color:var(--text);font-family:var(--dk-font-display);text-decoration:none}.page-navigation a small{font-family:var(--dk-font-mono);font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}.page-navigation a span{font-size:1rem}.page-navigation a:hover span{color:var(--interactive);text-decoration:underline;text-decoration-thickness:.08em;text-underline-offset:.16em}.page-navigation .page-next{margin-left:auto;text-align:right;align-items:flex-end}
.site-footer{display:flex;gap:1rem;flex-wrap:wrap;max-width:var(--dk-shell-width);margin:0 auto;padding:1rem;border-top:1px solid var(--border);color:var(--muted);font-family:var(--dk-font-ui);font-size:.82rem}.site-footer a{color:var(--interactive);font-weight:650;text-decoration-thickness:.08em;text-underline-offset:.16em}
@media(max-width:1024px){.shell{grid-template-columns:13rem minmax(0,var(--dk-content-width));gap:2rem}.toc{display:none}}
@media(max-width:768px){body{font-size:16px}.topbar{flex-wrap:wrap}.search-control{order:3;flex-basis:100%;max-width:none}.shell{display:block;padding-top:1rem}.sidebar{display:none}.mobile-nav{display:block;padding:0 1rem 1rem}.mobile-nav summary{cursor:pointer}.toc{display:none}.prose h1{font-size:2.05rem}.copy-code{opacity:1}}
@media(max-width:600px){.topbar{gap:.5rem}.brand{flex:0 0 100%}.topbar select{flex:0 1 calc(50% - .25rem);width:calc(50% - .25rem);min-width:0}.capability-strip{grid-template-columns:1fr}}
@media(max-width:420px){.topbar{gap:.5rem}.brand{font-size:.9rem}.topbar select,button{font-size:.78rem}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;transition-duration:.01ms!important;animation-duration:.01ms!important;animation-iteration-count:1!important}}
@media(forced-colors:active){button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline-color:Highlight}.reading-progress span{background:Highlight}}
'''

SITE_JS = r'''
(()=>{
  const root=document.documentElement,key='dockit-fp-theme',select=document.querySelector('#theme-select');
  function setTheme(value){if(value==='system')delete root.dataset.theme;else root.dataset.theme=value;try{localStorage.setItem(key,value)}catch(_){}}
  try{const value=localStorage.getItem(key);if(['light','dark','system'].includes(value)){select.value=value;setTheme(value)}}catch(_){}
  select?.addEventListener('change',()=>setTheme(select.value));
  const visual=document.querySelector('#visual-theme'),visualKey='dockit-fp-visual-theme';
  function setVisualTheme(value){root.dataset.visualTheme=value;try{localStorage.setItem(visualKey,value)}catch(_){}}
  try{const value=localStorage.getItem(visualKey);if(['classic','paper','midnight'].includes(value)){visual.value=value;setVisualTheme(value)}else if(visual){visual.value=root.dataset.visualTheme||'classic'}}catch(_){ }
  visual?.addEventListener('change',()=>setVisualTheme(visual.value));
  const version=document.querySelector('#version-select');
  version?.addEventListener('change',()=>{location.href=version.value});

  const input=document.querySelector('#search'),results=document.querySelector('#search-results');
  let entries=[];
  function closeSearch(){if(!results)return;results.hidden=true;input?.setAttribute('aria-expanded','false')}
  function appendHighlight(element,text,query){
    const haystack=text.toLowerCase();let offset=0,index=haystack.indexOf(query,offset);
    while(index!==-1){element.append(text.slice(offset,index));const mark=document.createElement('mark');mark.textContent=text.slice(index,index+query.length);element.append(mark);offset=index+query.length;index=haystack.indexOf(query,offset)}
    element.append(text.slice(offset));
  }
  function excerpt(text,query){const index=text.toLowerCase().indexOf(query);if(index<0)return text.slice(0,90);const start=Math.max(0,index-36),end=Math.min(text.length,index+query.length+54);return `${start?'…':''}${text.slice(start,end)}${end<text.length?'…':''}`}
  function rank(entry,terms){
    const title=entry.title.toLowerCase(),section=entry.section.toLowerCase(),text=entry.text.toLowerCase();
    if(!terms.every(term=>(title+' '+section+' '+text).includes(term)))return Number.POSITIVE_INFINITY;
    return terms.reduce((score,term)=>score+(title===term?0:title.startsWith(term)?1:title.includes(term)?2:section.startsWith(term)?3:section.includes(term)?4:text.indexOf(term)/Math.max(text.length,1)+5),0);
  }
  function showSearch(){
    const query=input.value.trim().toLowerCase();
    if(!query){closeSearch();return}
    const terms=query.split(/\s+/),matches=entries.map(entry=>({entry,score:rank(entry,terms)})).filter(match=>Number.isFinite(match.score)).sort((left,right)=>left.score-right.score||left.entry.title.localeCompare(right.entry.title)).slice(0,8);
    if(!matches.length){const empty=document.createElement('p');empty.className='search-empty';empty.textContent=`No pages match “${input.value.trim()}”.`;results.replaceChildren(empty)}
    else results.replaceChildren(...matches.map(({entry})=>{
      const link=document.createElement('a');link.href=entry.url;
      const title=document.createElement('strong');appendHighlight(title,entry.title,terms[0]);
      const summary=document.createElement('small');summary.textContent=`${entry.section} — `;appendHighlight(summary,excerpt(entry.text,terms[0]),terms[0]);
      link.append(title,summary);return link;
    }));
    results.hidden=false;input.setAttribute('aria-expanded','true');
  }
  if(input&&results){
    fetch(input.dataset.searchIndex||'search-index.json').then(response=>response.ok?response.json():[]).then(value=>entries=value).catch(()=>{});
    input.addEventListener('input',showSearch);
    input.addEventListener('keydown',event=>{
      const links=[...results.querySelectorAll('a')];const current=links.indexOf(document.activeElement);
      if(event.key==='ArrowDown'&&links.length){event.preventDefault();links[Math.min(current+1,links.length-1)].focus()}
      if(event.key==='ArrowUp'&&links.length){event.preventDefault();if(current>0)links[current-1].focus();else input.focus()}
      if(event.key==='End'&&links.length){event.preventDefault();links[links.length-1].focus()}
      if(event.key==='Enter'&&links.length){event.preventDefault();links[0].click()}
    });
    results.addEventListener('keydown',event=>{const links=[...results.querySelectorAll('a')],current=links.indexOf(document.activeElement);if(event.key==='ArrowDown'&&current>=0&&current+1<links.length){event.preventDefault();links[current+1].focus()}if(event.key==='ArrowUp'&&current>=0){event.preventDefault();if(current)links[current-1].focus();else input.focus()}if(event.key==='Home'&&links.length){event.preventDefault();links[0].focus()}if(event.key==='End'&&links.length){event.preventDefault();links[links.length-1].focus()}if(event.key==='Escape'){closeSearch();input.focus()}});
    document.addEventListener('pointerdown',event=>{if(!results.contains(event.target)&&event.target!==input)closeSearch()});
  }
  document.addEventListener('keydown',event=>{
    if(event.key==='/'&&document.activeElement!==input){event.preventDefault();input?.focus()}
    if(event.key==='Escape')closeSearch();
  });

  document.querySelectorAll('.prose pre').forEach(block=>{
    const code=block.querySelector('code');
    if(!code)return;
    const button=document.createElement('button');button.type='button';button.className='copy-code';
    const setCopyLabel=label=>{button.textContent=label;button.setAttribute('aria-label',label)};
    setCopyLabel('Copy code');
    button.addEventListener('click',async()=>{
      if(!navigator.clipboard?.writeText){setCopyLabel('Copy unavailable');return}
      try{await navigator.clipboard.writeText(code.textContent||'');setCopyLabel('Copied');window.setTimeout(()=>{setCopyLabel('Copy code')},1600)}catch(_){setCopyLabel('Copy unavailable')}
    });
    block.append(button);
  });

  const progress=document.querySelector('.reading-progress span');
  function updateProgress(){if(!progress)return;const range=document.documentElement.scrollHeight-window.innerHeight;const amount=range>0?Math.min(1,Math.max(0,window.scrollY/range)):0;progress.style.transform=`scaleX(${amount})`}
  if(progress){window.addEventListener('scroll',updateProgress,{passive:true});window.addEventListener('resize',updateProgress);updateProgress()}

  const tocLinks=[...document.querySelectorAll('.toc a[href^="#"]')];
  if(tocLinks.length&&'IntersectionObserver'in globalThis){
    const linksById=new Map(tocLinks.map(link=>[link.getAttribute('href').slice(1),link]));
    const activate=id=>tocLinks.forEach(link=>{const current=link===linksById.get(id);link.classList.toggle('is-active',current);if(current)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current')});
    const observer=new IntersectionObserver(entries=>{const visible=entries.find(entry=>entry.isIntersecting);if(visible)activate(visible.target.id)},{rootMargin:'0px 0px -70% 0px'});
    linksById.forEach((_link,id)=>{const heading=document.getElementById(id);if(heading)observer.observe(heading)});
  }
})();
'''

MATH_JS = r'''
(()=>{function render(node,displayMode){if(!globalThis.katex){node.textContent=node.dataset.tex||'';return}try{globalThis.katex.render(node.dataset.tex||'',node,{displayMode,throwOnError:false,strict:'ignore'})}catch(_){node.textContent=node.dataset.tex||''}}document.querySelectorAll('.math-inline').forEach(node=>render(node,false));document.querySelectorAll('.math-display').forEach(node=>render(node,true))})();
'''
