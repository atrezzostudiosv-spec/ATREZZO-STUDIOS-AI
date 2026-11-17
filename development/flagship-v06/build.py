#!/usr/bin/env python3
"""Build an isolated private ATREZZO preview from the user's authorized archive.
No captured code is distributed with this source package; output stays local.
"""
import argparse, hashlib, json, re, shutil, zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from html import escape
from urllib.request import urlopen, Request
from work_sequence import section as selected_work, adapt as adapt_work, cover as work_cover
from service_motion import section as services_section, write_media, frame_module
from particle_bridge import module as particle_module, BLOB as PARTICLE_BLOB

HERE=Path(__file__).resolve().parent
PIN='a21d4347e0b09a849681dedc8b2373b390bfa002'
LIB='9ee01f9e4de7208e0f1ec16882239b9124e68f78'
CORP='33bf6d0451ae9532c88d6977ec6d2856bd6cdcf5'
OWNER='atrezzostudiosv-spec'
SRC='trionn-dev-autonomous/workspace/_next/static/chunks/'
ORIGINAL={'0sue_k2sp00no.js':'43378a2e58a1365289ea95b3ac6b7caf257434c6','1233qowaitufq.js': '922eabe133b37c0d573396f5c23d41b746096c84', '13xgo04nefn8q.js': 'db3e364ee49a7795382ecc09331a2fa2160d86de', '15ky3h9upk1qm.js': '5f7964b3cbb00190550e373bc90b918656bfa90b', '02m2onmcd.l.g.js': '4509b2999fc0aa3dac40a1c3aa2fa79b3a30052e', '0z-5e_9x.n-.p.js': '37a3c2ae5d584f3f0e889dc9762ee8bbe21093d2', '08uh6.imupez1.js': '8e8f58275e03c70d95cc762bf41a75bf4bc3c304', '0_-x7hddx_1l6.js': 'a3800ce2fe02cd0b19a7b84f69be6bf74f92a065', '0eq63v9bib54k.js': '825c5bbf6511d160bd2be0198dc382c20799cc24', 'turbopack-0nz662b_cli3l.js': '4aff2a0e86593335f0569e207455912464d6c69f'}
FILES={
'components/navegacion/ATZ-NAV-001.html':'fc45a9cd087dfe7bb5d94330e0a2761a016d9532','components/navegacion/ATZ-NAV-001.css':'fa65dc547d07b54880d4d3c1e70e0ca69f2fadb4','components/navegacion/ATZ-NAV-001.js':'ecb5118341c09fa59a8cc0b2d4e199c990fad6c1','components/navegacion/runtime.js':'8cced31370b55c7681c9d6eb30fcd67e10d5cab8',
'components/microinteractions/ATZ-MIC-003.html':'a8a1f3bcfdac8f7aae498a4d88aaa33a7ae38ea6','components/microinteractions/ATZ-MIC-003.js':'4642cd1c12b3bf43a81bb67569e86255b0fe73c2','components/microinteractions/runtime.js':'6e825c6835333a7ae47a449ec98af6545ef37dd9','components/microinteractions/atrezzo-microinteractions.css':'dabdb8dbb9d73530aa0e117f68171e04f95e5f8a',
'components/motion/ATZ-MOT-002.html':'014628c4d7789e8cc5a6eb4caecd960fa1f97d34','components/motion/ATZ-MOT-002.js':'15a4322a568c20139af4b0bcbcf5b51e4d63c659','components/motion/ATZ-MOT-003.html':'e9c8415f210bce59f872f13f6f75044d835fa070','components/motion/ATZ-MOT-003.js':'042747e293eda691521df5493e29006c8958fd67','components/motion/ATZ-MOT-006.html':'f16c269972ea9095dbcb8438c0846eb45c65ab4c','components/motion/ATZ-MOT-006.js':'e97104b360f325cbfdab486baee44ad6c103014a','components/motion/runtime.js':'d4fc5105b346c52cf947f53be8a822c98abefaa4','components/motion/atrezzo-motion-v1.css':'7fb9ccf2eade5aa061425ca3c10169b3136d5a90'}
ASSETS={'public/assets/wordmark.svg':'13470f929e099fda97ebc1676ce8aef8f11872ee','public/assets/brand-social.webp':'4977bc49bc12d873cbaa8f9c4179e46622cdfeb8','public/assets/coming-soon-visual.webp':'c41fa9dbc272c71a112d01e3bffaa407a7e1d1b2','public/lab/floating-portfolio/images/atrezzo-ref-13.webp':'d5506fdbf0ea8c0685443ddde4a5a0ea2b23146b','public/lab/floating-portfolio/images/atrezzo-ref-14.webp':'8e83a26394579386062c6be517f508c383ecc911'}
CHUNKS=['0zaia6i55l01..js','0y3~cortx~or~.js','00nvzi6qb_-1r.js','0_-x7hddx_1l6.js','0cayk5enk9uhw.js','02m2onmcd.l.g.js','0z-5e_9x.n-.p.js','08uh6.imupez1.js','0eq63v9bib54k.js','0d~m1vbg607mf.js','0d3shmwh5_nmn.js','13z7xnmanm326.js','13xgo04nefn8q.js','0_.rc2afwy26s.js','0eox~aw2ff066.js','0sue_k2sp00no.js','04srvx.z7_jun.js','15ky3h9upk1qm.js','03~yq9q893hmn.js','1233qowaitufq.js','turbopack-0nz662b_cli3l.js']

def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def put(p,b):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b if isinstance(b,bytes) else b.encode())
def once(s,a,b):
 if s.count(a)!=1:raise ValueError(f'Expected exactly one source match: {a[:80]} ({s.count(a)})')
 return s.replace(a,b,1)
def fetch(repo,rev,path,sha,offline=False):
 cached=HERE/'approved-cache'/repo/Path(path)
 seed=HERE/'library-seed'/Path(path)
 if cached.exists():data=cached.read_bytes()
 elif repo=='atrezzo-repositorio' and seed.is_file():data=seed.read_bytes()
 elif offline:return None
 else:
  url=f'https://raw.githubusercontent.com/{OWNER}/{repo}/{rev}/{path}'
  with urlopen(Request(url,headers={'User-Agent':'ATREZZO-private-preview'}),timeout=10) as r:data=r.read()
 if blob(data)!=sha:raise ValueError(f'Asset integrity failure: {path}')
 if not cached.exists():put(cached,data)
 return data

def find_zip(explicit=None):
 if explicit:return Path(explicit).expanduser().resolve()
 for folder in (HERE,HERE.parent,Path.home()/'Downloads',Path.home()/'Desktop'):
  for p in sorted(folder.glob('trionn-dev-autonomous*.zip')):
   if p.is_file():return p
 raise FileNotFoundError('No encuentro trionn-dev-autonomous.zip. Conserva el ZIP original en Descargas o junto al paquete.')

def svg_symbol(brand):
 paths=['M'+' L'.join(f'{x} {y}' for x,y in path)+' Z' for path in brand['paths']]
 return '<svg viewBox="100 145 370 295" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f5f5fa"/><stop offset=".45" stop-color="#b967ef"/><stop offset="1" stop-color="#153b9d"/></linearGradient></defs>'+''.join('<path fill="url(#g)" d="'+d+'"/>' for d in paths)+'</svg>'

def adapt_engine(s,brand):
 start=s.index('(t=p(e=>');end=s.index('.forEach((e,t)=>(function(e,t)',start)
 cx,cy=brand['center'];scale=brand['scale']
 def xy(x,y):return f'{(x-cx)*scale:.6f},{(cy-y)*scale:.6f}'
 shapes=[];anchors=[]
 for path in brand['paths']:
  shapes.append('p(e=>{e.moveTo('+xy(*path[0])+');'+''.join('e.lineTo('+xy(*p)+');' for p in path[1:])+'e.closePath()})')
  anchors.append(xy(sum(p[0] for p in path)/len(path),sum(p[1] for p in path)/len(path)))
 s=s[:start]+'(['+','.join(shapes)+'])'+s[end:]
 s=once(s,'let eh=new a.Vector3(-.59,.1,.21),ep=new a.Vector3(.28,-.85,.21),em=new a.Vector3(.54,.48,.21)',f'let eh=new a.Vector3({anchors[0]},.21),ep=new a.Vector3({anchors[1]},.21),em=new a.Vector3({anchors[2]},.21)')
 # Brand tokens only. Motion, camera, renderer, materials' physical properties,
 # geometry subdivision, interaction, scroll and cleanup remain original.
 for a,b in {'789516':str(0x090812),'2764864':str(0x302454),'8952234':str(0xB967EF),'6715306':str(0x153B9D),'0xff3300':'0x7436f5','0xff2200':'0x153b9d','0xff5500':'0xb967ef','3816770':str(0x716b91),'1712176':str(0x211640),'3554893':str(0xB967EF),'8969727':str(0xB967EF),'4500223':str(0x7436F5),'0xaaddff':'0xc3b8ff','0x99ddff':'0xb967ef','0xbbddff':'0xe7d6ff','0xaaccff':'0xd6c3ff'}.items():
  s=re.sub(r'(?<![\w.])'+re.escape(a)+r'(?![\w.])',b,s)
 # Original audio is not authorized for this pilot. Disable unconditional loads.
 s=once(s,'g.preloadSparkBuffer(),g.initHoverAudio();',';')
 return s

def adapt_vision(s):
 for a,en,es in [('Focused vision. <br/>Measured execution.','Design in motion. <br/>Creative editorial studio.','Diseño en movimiento. <br/>Estudio creativo editorial.'),('Inspire','Design','Diseño'),('innovate','in','en'),('Impact','motion','movimiento'),('✦ From idea to outcome.','Selected work follows.','A continuación, proyectos.')]:
  s=once(s,json.dumps(a,ensure_ascii=False),f'(document.documentElement.lang==="es"?{json.dumps(es,ensure_ascii=False)}:{json.dumps(en,ensure_ascii=False)})')
 s=once(s,'backgroundColor:"#D2D2D2"','backgroundColor:"#090812"')
 return s

def page(lang,assets,library,art):
 es=lang=='es';t=lambda a,b:b if es else a
 def cta(label,href):return f'<a class="mi-cta" href="{href}">{escape(label)} <span class="mi-arrow" aria-hidden="true"><span>↗</span><span>↗</span></span></a>'
 def ctas(*pairs):return '<div class="atz-mi" data-atz-id="ATZ-MIC-003"><div class="mi-actions">'+''.join(cta(*p) for p in pairs)+'</div></div>'
 def media(name,alt,cls=''):
  if name in assets:return f'<img class="{cls}" src="/assets/{name}" alt="{escape(alt)}" loading="lazy">'
  return f'<img class="{cls}" src="/assets/study-{art.get(name,1)}.svg" alt="{escape(alt)}" loading="lazy">'
 brand='<img src="/assets/wordmark.svg" alt="ATREZZO STUDIOS" width="991" height="155">' if 'wordmark.svg' in assets else 'ATREZZO STUDIOS'
 menu_pairs=[(t('Websites','Diseño web'),'#websites'),(t('Express','Web Express'),'#express'),(t('Work','Portfolio'),'#work'),(t('Studio','Estudio'),'#studio'),(t('Start a Project','Inicia tu proyecto'),'#contact')]
 nav_links=''.join(f'<li><a data-azn1-menu-link href="{url}"><strong>{label}</strong><small>{i:02}</small></a></li>' for i,(label,url) in enumerate(menu_pairs,1))
 nav_photos=''.join(f'<div data-azn1-menu-photo class="atz-nav-photo{" is-active" if i==0 else ""}" style="background-image:linear-gradient(140deg,#100c35,#7436f5)"></div>' for i in range(len(menu_pairs)))
 menu=f'''<div class="atz-nav atz-nav-menuhost" data-atz-id="ATZ-NAV-001" id="private-nav"><header class="atz-nav-bar site-header"><a class="atz-nav-logo brandmark" href="/{lang}/" aria-label="ATREZZO STUDIOS">{brand}</a><nav class="atz-nav-fallback" aria-label="Navigation">{''.join(f'<a href="{u}">{l}</a>' for l,u in menu_pairs)}</nav><div class="header-right"><a class="language" href="/{'en' if es else 'es'}/" lang="{'en' if es else 'es'}">{'EN' if es else 'ES'}</a><a class="contact-link" href="#contact">{t('Start a Project','Inicia tu proyecto')}</a><button class="atz-nav-trigger" type="button" data-azn1-menu-trigger aria-controls="atz-nav-dialog-001" aria-expanded="false" aria-label="{t('Open menu','Abrir menú')}"><span class="atz-nav-glyph" aria-hidden="true"><i></i><i></i></span><span>MENU</span></button></div></header><div class="atz-nav-dialog" id="atz-nav-dialog-001" role="dialog" aria-modal="true" aria-label="Navigation" tabindex="-1" data-azn1-menu hidden><div class="atz-nav-dialog-left"><div class="atz-nav-dialog-head"><strong>ATREZZO</strong><button type="button" data-azn1-menu-close aria-label="{t('Close menu','Cerrar menú')}">{t('CLOSE','CERRAR')} <span aria-hidden="true">×</span></button></div><div class="atz-nav-dialog-links-wrap"><span>DESIGN IN MOTION</span><ul class="atz-nav-dialog-links">{nav_links}</ul></div><div class="atz-nav-dialog-foot">CREATIVE EDITORIAL STUDIO</div></div><div class="atz-nav-dialog-visual" aria-hidden="true">{nav_photos}<span class="atz-nav-photo-caption">LUMINOUS DIGITAL EDITORIAL</span></div></div></div>'''
 fallback=f'''<div id="hero-section" class="hero-section"><img class="fallback-symbol" src="/assets/mark.svg" alt=""><div id="sticky-wrap"><section class="main-banner"><div class="hero-top"><span class="eyebrow">DESIGN IN MOTION</span><h1 class="hero-title">{t('Your business. Better online.','Tu negocio. Mejor en internet.')}</h1>{ctas((t('Start a Project','Inicia tu proyecto'),'#contact'),(t('View Work','Ver proyectos'),'#work'))}</div><div class="hero-bottom"><span class="eyebrow">↓ {t('SCROLL TO EXPLORE','EXPLORA')}</span><span></span><div class="hero-caption"><span class="eyebrow">CREATIVE EDITORIAL STUDIO</span><p>{t('Web design and digital experiences for businesses.','Diseño web y experiencias digitales para negocios.')}</p></div></div></section><section class="home-about"><div id="s2-text"><span class="eyebrow">01 / ATREZZO</span><h2 class="manifesto-title">{t('We design experiences. Not just websites.','Diseñamos experiencias. No solo sitios web.')}</h2></div></section></div><section class="fallback-vision">DESIGN<br>IN MOTION.</section></div>'''
 work=selected_work(lang,assets)
 offer=services_section(lang,ctas)
 stages=[(t('Understand','Comprender'),t('Clarify the business, audience and purpose before designing.','Definir negocio, audiencia y objetivo antes de diseñar.')),(t('Design','Diseñar'),t('Translate strategy into a coherent visual system and experience.','Traducir la estrategia en un sistema visual y una experiencia coherentes.')),(t('Build','Construir'),t('Bring the design into a responsive, usable digital experience.','Convertir el diseño en una experiencia digital adaptable y usable.'))]
 def stageimg(i):return f'<img src="/assets/process-{i}.svg" alt="{t("Illustrative process study","Estudio ilustrativo del proceso")} {i}" loading="lazy">'
 journey=f'''<section id="method" class="scene ink atz-motion-v1" data-atz-id="ATZ-MOT-006"><div class="scene-head journey-intro"><span class="eyebrow">04 / {t('THE TRANSFORMATION','LA TRANSFORMACIÓN')}</span><h2>{t('From idea to experience.','De la idea a la experiencia.')}</h2></div><div data-am-journey><div class="am-journey__sticky">{''.join(f'<div data-am-journey-frame aria-hidden="{"false" if i==1 else "true"}" class="{"am-active" if i==1 else ""}">{stageimg(i)}</div>' for i in range(1,4))}<span data-am-journey-counter aria-label="Current chapter">01</span></div><div class="am-journey__content">{''.join(f'<article data-am-journey-step class="process-copy"><div class="am-step-image">{stageimg(i)}</div><span class="am-small">0{i} / {t("CHAPTER","CAPÍTULO")}</span><h3>{title}</h3><p>{desc}</p></article>' for i,(title,desc) in enumerate(stages,1))}</div></div></section>'''
 creative=f'''<section id="creative" class="scene ink atz-motion-v1" data-atz-id="ATZ-MOT-003"><div class="am-parallax-stage"><div><span class="eyebrow">05 / {t('BUILT TO GROW','DISEÑADA PARA CRECER')}</span><h2>{t('Ready for what’s next.','Preparada para lo que viene.')}</h2><p>{t('Your website should be able to evolve with your business.','Tu web debe poder evolucionar con tu negocio.')}</p><p>{t('We plan the structure, content and technology with your next steps in mind. When you need new pages, updated content or additional functionality, we can define the right scope for that project.','Planificamos la estructura, el contenido y la tecnología pensando en tus próximos pasos. Cuando necesites nuevas páginas, actualizar contenido o añadir funcionalidades, definiremos el alcance adecuado para ese proyecto.')}</p><a class="studio-cta" href="#websites">{t('Explore website design','Descubre el diseño web')} ↗</a></div><div data-am-parallax>{media('brand-social.webp',t('ATREZZO studio brand concept','Concepto de marca ATREZZO'))}</div></div></section>'''
 standard=f'''<section id="studio" class="scene paper atz-motion-v1" data-atz-id="ATZ-MOT-002"><div class="am-reveal-stage"><span class="eyebrow">06 / THE ATREZZO STANDARD</span><h2 data-am-text="scrub">{t('Design with purpose. Motion with meaning.','Diseño con propósito. Movimiento con sentido.')}</h2><p>{t('Creative Editorial Studio.','Estudio creativo editorial.')}</p></div></section>'''
 closing=f'''<section id="contact" class="scene ink closing"><span class="eyebrow">07 / {t('START A PROJECT','INICIA TU PROYECTO')}</span><h2>{t('Let’s build your next experience.','Construyamos tu próxima experiencia.')}</h2><p class="private-note">{t('Private preview · The contact route will be connected in the approved website.','Vista privada · La ruta de contacto se conectará en el website aprobado.')}</p><a class="studio-cta" href="#top">{t('Back to top','Volver arriba')} ↑</a></section>'''
 css=''.join(f'<link rel="stylesheet" href="/{p}">' for p in FILES if p.endswith('.css') and p in library)
 scripts=''.join(f'<script defer src="/_next/static/chunks/{p}"></script>' for p in CHUNKS if not p.startswith('turbopack'))+'<script defer src="/service-particles.js"></script><script defer src="/service-frame-engine.js"></script><script defer src="/host.js"></script><script defer src="/_next/static/chunks/turbopack-0nz662b_cli3l.js"></script>'
 return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#090812"><title>ATREZZO STUDIOS — Private Home V06</title><link rel="stylesheet" href="/_next/static/chunks/0-x39_77jza10.css"><link rel="stylesheet" href="/_next/static/chunks/0wf1gwg29cqjw.css">{css}<link rel="stylesheet" href="/brand.css"><link rel="stylesheet" href="/selected-work.css"><link rel="stylesheet" href="/services.css"></head><body id="top"><a class="skip-link" href="#work">{t('Skip motion','Saltar movimiento')}</a>{menu}<main id="site-main"><div id="experience">{fallback}</div>{work}{offer}{journey}{creative}{standard}{closing}</main><footer class="footer"><a class="brandmark" href="/{lang}/">{brand}</a><span>ATREZZO STUDIOS · DESIGN IN MOTION</span><a href="/{'en' if es else 'es'}/">{'EN' if es else 'ES'}</a></footer><div class="preview-label"><span id="preview-state">PRIVATE STUDY V06 · INITIALIZING</span></div>{scripts}<script type="module" src="/library.js"></script></body></html>'''


def make_art(n,process=False):
 # Own illustrative SVGs, not client projects. Three stages of one concept.
 color=['#153b9d','#7436f5','#b967ef'][n-1];label=('WIREFRAME','VISUAL SYSTEM','DIGITAL EXPERIENCE')[n-1] if process else f'ATREZZO / STUDY 0{n}'
 surface='#10102a';shapes=''.join(f'<rect x="{120+24*i}" y="{125+18*i}" width="{520-48*i}" height="{275-36*i}" rx="{8+3*i}" fill="none" stroke="{color}" stroke-width="2" opacity="{.35+.1*i}"/>' for i in range(5))
 if process:
  if n==1:shapes='<rect x="90" y="90" width="620" height="370" rx="14" fill="#17182e" stroke="#777b9e"/>'+''.join(f'<rect x="{130+170*(i%3)}" y="{150+100*(i//3)}" width="150" height="80" fill="none" stroke="#989ab8"/>' for i in range(6))
  elif n==2:shapes='<rect x="85" y="95" width="630" height="365" rx="14" fill="#19133b"/>'+''.join(f'<circle cx="{220+i*180}" cy="265" r="72" fill="{c}"/>' for i,c in enumerate(['#153b9d','#7436f5','#b967ef']))
  else:shapes='<rect x="85" y="95" width="630" height="365" rx="14" fill="#14122e" stroke="#b967ef" stroke-width="3"/><text x="130" y="220" fill="#f5f5fa" font-size="60" font-family="Arial">Design in</text><text x="130" y="285" fill="#b967ef" font-size="60" font-family="Arial">motion.</text><path d="M510 140L650 380L370 380Z" fill="none" stroke="#7436f5" stroke-width="14"/>'
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 540"><rect width="800" height="540" fill="{surface}"/>{shapes}<text x="32" y="508" fill="#eee" font-family="monospace" font-size="15" letter-spacing="3">{label}</text></svg>'

def build(archive,out,offline=False):
 brand=json.loads((HERE/'brand.json').read_text())
 if out.exists() and any(out.iterdir()) and not (out/'build-report.json').is_file():raise ValueError('Choose an empty dedicated preview directory; no existing website will be overwritten')
 out.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(archive) as z:
  if z.comment.decode().strip()!=PIN:raise ValueError('ZIP does not match the authorized commit '+PIN)
  if z.testzip():raise ValueError('Archive integrity failure')
  for p,sha in ORIGINAL.items():
   if blob(z.read(SRC+p))!=sha:raise ValueError('Source mismatch '+p)
  galaxy=z.read(SRC+'01rd0k2u.3.j_.js').decode()
  put(out/'service-particles.js',particle_module(galaxy))
  for p in CHUNKS:
   s=z.read(SRC+p).decode()
   if p=='1233qowaitufq.js':s=adapt_engine(s,brand)
   elif p=='13xgo04nefn8q.js':s=adapt_vision(s)
   elif p=='0sue_k2sp00no.js':
    put(out/'service-frame-engine.js',frame_module(s));s=adapt_work(s)
   elif p.startswith('turbopack-'):s=once(s,'runtimeModuleIds:[94553]','runtimeModuleIds:[999001]')
   put(out/'_next/static/chunks'/p,s)
  for p in ('0-x39_77jza10.css','0wf1gwg29cqjw.css'):
   s=z.read(SRC+p).decode();s=re.sub(r'@font-face\s*\{[^{}]*\}','',s);s=re.sub(r'url\(/images/[^)]+\)','none',s);put(out/'_next/static/chunks'/p,s)
 for f in ('host.js','brand.css','selected-work.css','services.css'):shutil.copyfile(HERE/f,out/f)
 available=set();assets=set();failures=[]
 tasks=[('atrezzo-repositorio',LIB,path,sha,False) for path,sha in FILES.items()]+[('ATREZZO-STUDIOS-AI',CORP,path,sha,True) for path,sha in ASSETS.items()]
 def download(job):
  repo,rev,path,sha,is_asset=job
  try:return job,fetch(repo,rev,path,sha,offline),None
  except Exception as ex:return job,None,str(ex)
 with ThreadPoolExecutor(max_workers=8) as pool:
  for job,data,error in pool.map(download,tasks):
   repo,rev,path,sha,is_asset=job
   if error:failures.append(f'{path}: {error}')
   if data is not None:
    if is_asset:put(out/'assets'/Path(path).name,data);assets.add(Path(path).name)
    else:put(out/path,data);available.add(path)
 # Native accessible content remains usable if a public library asset is unreachable.
 put(out/'assets/mark.svg',svg_symbol(brand))
 write_media(out,brand,put)
 for i in (1,2):put(out/f'assets/work-{i:02}.svg',work_cover(i,brand,[(out/'assets'/n).read_bytes() for n in ('atrezzo-ref-13.webp','atrezzo-ref-14.webp') if n in assets] if i==2 else ()))
 for i in range(1,4):put(out/f'assets/study-{i}.svg',make_art(i));put(out/f'assets/process-{i}.svg',make_art(i,True))
 art={'coming-soon-visual.webp':1,'atrezzo-ref-13.webp':2,'atrezzo-ref-14.webp':3,'brand-social.webp':2}
 for lang in ('en','es'):put(out/lang/'index.html',page(lang,assets,available,art))
 put(out/'index.html','<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url=/en/"><a href="/en/">ATREZZO Home</a>')
 # Mount only the exact registered library modules; observe host because React
 # replaces the first scene after startup. Components are not reimplemented.
 ids=[('navegacion','ATZ-NAV-001'),('microinteractions','ATZ-MIC-003'),('motion','ATZ-MOT-002'),('motion','ATZ-MOT-003'),('motion','ATZ-MOT-006')]
 mounts=[]
 for category,id in ids:
  path=f'components/{category}/{id}.js'
  if path in available and f'components/{category}/runtime.js' in available:mounts.append(f'import {{mount as mount_{id.replace("-","_")}}} from "/{path}";')
 put(out/'library.js','\n'.join(mounts)+ '\nconst mounts=['+','.join('['+json.dumps(id)+',mount_'+id.replace('-','_')+']' for category,id in ids if f'components/{category}/{id}.js' in available and f'components/{category}/runtime.js' in available)+'];\nconst done=new Map();function init(){for(const [root,controller] of done){if(!root.isConnected){controller?.destroy?.();done.delete(root)}}for(const [id,mount] of mounts){for(const root of document.querySelectorAll(`[data-atz-id="${id}"]`)){if(done.has(root))continue;try{done.set(root,mount(root))}catch(e){console.error(id,e)}}}}\ninit();const obs=new MutationObserver(init);obs.observe(document.getElementById("experience"),{childList:true,subtree:true});\n')
 report={'source_commit':PIN,'library_commit':LIB,'corporate_commit':CORP,'private':True,'browser_QA':'not performed','work_engine':'7617 / 28236 work + handoff only','original_engine':'54377','vision':'72959','patched':['three brand profiles and anchor coordinates','brand color tokens','disable original audio preload','localized Vision text and dark stripe token','original G bridge phase with six editorial beats, transparent 371 own A frames, original Name Story 84066 point clouds; same pin','private runtime entry; no Next hydration'],'available_library_files':len(available),'available_brand_assets':len(assets),'missing_or_failed_assets':failures,'offline':offline}
 put(out/'build-report.json',json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report,indent=2,ensure_ascii=False))
 return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--archive');p.add_argument('--out',default=str(HERE/'private-preview'));p.add_argument('--offline',action='store_true');a=p.parse_args();archive=find_zip(a.archive);out=Path(a.out).resolve();build(archive,out,a.offline)
