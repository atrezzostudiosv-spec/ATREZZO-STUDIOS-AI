"""Private source adaptation: pinned 7617 / 28236 Work stages.
No original chunks are shipped. Apply owned edit manifest only to the user's ZIP.
"""
import json, hashlib
from pathlib import Path
from html import escape
from selected_work import cover,LAB

def adapt(s):
 manifest=json.loads(Path(__file__).with_name('work-patches.json').read_text())
 digest=lambda text:hashlib.sha256(text.encode()).hexdigest()
 if digest(s)!=manifest['source_sha256']:raise ValueError('Work source mismatch')
 for a,b,value in reversed(manifest['operations']):s=s[:a]+value+s[b:]
 if digest(s)!=manifest['result_sha256']:raise ValueError('Work patch integrity failure')
 # Only replace the two text nodes, not original Work positioning or timings.
 for old,new in [
  ('(0,t.jsx)("h3",{className:"text-light-font transition-transform duration-700 max-w-100 lg:max-w-116",children:globalThis.__ATZ_WORK_COPY.end})','(0,t.jsx)(globalThis.__ATZ_WorkReveal,{as:"h3",text:globalThis.__ATZ_WORK_COPY.end,className:"atz-work-end-title text-light-font",kind:"end"})'),
  ('(0,t.jsx)("h2",{children:globalThis.__ATZ_WORK_COPY.bridge})','(0,t.jsx)(globalThis.__ATZ_WorkReveal,{as:"h2",text:globalThis.__ATZ_WORK_COPY.bridge,className:"atz-work-bridge-title",kind:"bridge"})')]:
  if s.count(old)!=1:raise ValueError('Work title adaptation anchor mismatch')
  s=s.replace(old,new,1)
 return s

def data(lang,assets):
 es=lang=='es';t=lambda a,b:b if es else a
 # Actual owned media if fetched; editorial fallback is explicitly labeled.
 flag='coming-soon-visual.webp' if 'coming-soon-visual.webp' in assets else 'work-01.svg'
 lab='work-02.svg'
 return ([dict(title='Design in Motion',subTitle=t('Studio project · Flagship in development','Proyecto propio · Website insignia en desarrollo'),image='/assets/'+flag,alt=t('ATREZZO flagship project visual','Visual del proyecto insignia ATREZZO'),href='#top'),dict(title='Motion Lab',subTitle=t('Studio experiment · Floating Portfolio','Experimento propio · Floating Portfolio'),image='/assets/'+lab,alt=t('Editorial illustration of the published Motion Lab','Ilustración editorial del Motion Lab publicado'),href=LAB)],dict(heading=t('Selected<br/>work.','Proyectos<br/>selectos.'),explore=t('Explore project','Explorar proyecto'),cta=t('Explore our services','Explorar servicios'),end=t('Digital experiences built with intention.','Experiencias digitales creadas con intención.'),bridge=t('Find your digital solution.','Encuentra tu solución digital.')))

def section(lang,assets):
 projects,copy=data(lang,assets);es=lang=='es';t=lambda a,b:b if es else a
 cards=''.join(f'<article><a href="{escape(p["href"])}"><img src="{escape(p["image"])}" alt="{escape(p["alt"])}" width="1280" height="800"><h3>{escape(p["title"])}</h3></a><p>{escape(p["subTitle"])}</p><a class="atz-work-link" href="{escape(p["href"])}">{copy["explore"]} ↗</a></article>' for p in projects)
 config=json.dumps({'projects':projects,'copy':copy},ensure_ascii=False).replace('<','\\u003c')
 return f'<section id="keyfacts-section" class="atz-work-shell" tabindex="-1"><div id="work" tabindex="-1"></div><script type="application/json" id="atz-work-config">{config}</script><div id="atz-work-fallback" class="atz-work-fallback"><span class="eyebrow">02 / SELECTED WORK</span><h2>{t("Selected work. Design in action.","Proyectos. Diseño en acción.")}</h2><div class="atz-work-static-grid">{cards}</div><a class="atz-work-link" href="#websites">{copy["cta"]} ↗</a></div><div id="atz-work-mount"></div></section>'
