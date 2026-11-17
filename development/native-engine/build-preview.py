#!/usr/bin/env python3
"""Build an autonomous V06 migration candidate from owned static markup/media only.
Never executes the private archive builder or the captured-engine patch functions.
H01-H03 animation equivalence is not yet approved. H04-H07 are existing placeholders.
"""
import sys, json, re, shutil, subprocess, hashlib
from pathlib import Path
from html import escape

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE=ROOT/"development/flagship-v06"
sys.path.insert(0,str(BASE))
from build import page, svg_symbol, make_art, FILES, ASSETS, CORP, LIB
from service_motion import write_media, bridge_copy
from work_sequence import cover, data

out=Path(sys.argv[1]).resolve()
library=Path(sys.argv[2]).resolve()
assert not out.exists(), "Use a new output directory"
out.mkdir(parents=True)
brand=json.loads((BASE/"brand.json").read_text())
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(b.encode("utf-8") if isinstance(b,str) else b)
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=library,text=True).strip()==LIB
available=set()
for path,sha in FILES.items():
    b=(library/path).read_bytes()
    assert blob(b)==sha, path
    put(out/path,b);available.add(path)
assets=set()
for path,sha in ASSETS.items():
    b=subprocess.check_output(["git","show",CORP+":"+path],cwd=ROOT)
    assert blob(b)==sha,path
    put(out/"assets"/Path(path).name,b);assets.add(Path(path).name)
put(out/"assets/mark.svg",svg_symbol(brand))
write_media(out,brand,put)
for i in (1,2):
    put(out/f"assets/work-{i:02}.svg",cover(i,brand,[(out/"assets"/n).read_bytes() for n in ("atrezzo-ref-13.webp","atrezzo-ref-14.webp")] if i==2 else ()))
for i in range(1,4):
    put(out/f"assets/study-{i}.svg",make_art(i));put(out/f"assets/process-{i}.svg",make_art(i,True))
for path in ("brand.css","selected-work.css","services.css"):
    put(out/path,(BASE/path).read_bytes())
put(out/"native-preview.css",(HERE/"preview.css").read_bytes())
for lang in ("en","es"):
    es=lang=="es"
    t=lambda en,sp:sp if es else en
    text=page(lang,assets,available,{"coming-soon-visual.webp":1,"atrezzo-ref-13.webp":2,"atrezzo-ref-14.webp":3,"brand-social.webp":2})
    # Retain existing authored HTML/content; remove all references to captured engines.
    text=re.sub(r'<link[^>]+href="/_next/[^"]+"[^>]*>','',text)
    text=re.sub(r'<script defer src="[^"]+"></script>','',text)
    text=text.replace('<script type="module" src="/library.js"></script>','<script type="module" src="../native-preview.js"></script>')
    text=text.replace('</head>','<link rel="stylesheet" href="../native-preview.css"></head>')
    text=text.replace('ATREZZO STUDIOS — Private Home V06','ATREZZO STUDIOS — V06 Native Migration Preview')
    text=text.replace('PRIVATE STUDY V06 · INITIALIZING','V06 NATIVE MIGRATION · VISUAL REVIEW PENDING')
    text=text.replace('Vista privada · La ruta de contacto se conectará en el website aprobado.','Preview de migración · La ruta de contacto se conectará en el website aprobado.').replace('Private preview · The contact route will be connected in the approved website.','Migration preview · The contact route will be connected in the approved website.')
    text=text.replace('<span class="eyebrow">↓ '+t('SCROLL TO EXPLORE','EXPLORA')+'</span><span></span>','<span class="eyebrow">↓ '+t('SCROLL TO EXPLORE','EXPLORA')+'</span><span class="eyebrow desktop-only native-hold">'+t('HOLD TO TRANSFORM','MANTÉN PARA TRANSFORMAR')+'</span>')
    text=text.replace('</h2></div></section></div><section class="fallback-vision">','</h2><p>'+t('Creative direction, technology and design working as one.','Dirección creativa, tecnología y diseño trabajando como uno.')+'</p></div></section></div><section class="fallback-vision">',1)
    text=text.replace('<div id="hero-section" class="hero-section">','<div id="hero-section" class="hero-section"><canvas id="native-hero-canvas" aria-hidden="true" hidden></canvas>')
    projects,work=data(lang,assets)
    text=text.replace('<div id="atz-work-mount"></div>','<div id="atz-work-mount"><div class="atz-work-bridge native-work-bridge"><span class="eyebrow">03 / ATREZZO</span><p>'+escape(work["end"])+'</p><h2>'+escape(work["bridge"])+'</h2><a class="atz-work-link" href="#websites">'+escape(work["cta"])+' ↗</a></div></div>')
    c=bridge_copy(lang)
    cards=''.join(f'<article class="native-panel"><span class="eyebrow">{i+1:02} / 06</span><h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for i,(a,b) in enumerate(c["cards"]))
    bridge='<div id="atz-service-mount" class="native-bridge"><div class="native-bridge-stage"><canvas id="native-particles" aria-hidden="true" hidden></canvas><div class="native-bridge-art"><img id="native-monogram" src="../assets/service-frames/frame_0001.svg" width="960" height="540" alt=""></div><div class="native-bridge-copy"><span class="eyebrow">'+escape(c["label"])+'</span><h2>'+escape(' / '.join(c["lines"]))+'</h2><p>'+escape(c["opening"])+'</p></div><div class="native-panels">'+cards+'</div><p class="native-bridge-closing">'+escape(c["closing"])+'</p></div></div>'
    text=text.replace('<div id="atz-service-mount" hidden></div>',bridge)
    # All links and media are relative to this isolated Pages subdirectory.
    text=text.replace('href="/brand.css"','href="../brand.css"').replace('href="/selected-work.css"','href="../selected-work.css"').replace('href="/services.css"','href="../services.css"')
    text=text.replace('"/assets/','"../assets/').replace('"/components/','"../components/').replace('href="/en/"','href="../en/"').replace('href="/es/"','href="../es/"')
    assert "/_next/" not in text and "service-frame-engine.js" not in text and "service-particles.js" not in text
    put(out/lang/"index.html",text)
put(out/"index.html",'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url=./en/"><title>ATREZZO V06 Native Migration Preview</title><a href="./en/">Open preview</a></html>')
frames=sorted((out/"assets/service-frames").glob("frame_*.svg"))
assert len(frames)==len({hashlib.sha256(f.read_bytes()).hexdigest() for f in frames})==371
print("Native preview generated: owned markup, 371 frames, EN/ES; no captured runtime.")
