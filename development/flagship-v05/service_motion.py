"""Resolve original private service choreography from the exact pinned archive.
Only resource, text, brand and lifecycle substitutions. Never ship captured chunks.
"""
from html import escape
import json
from math import sin,cos,pi
from pathlib import Path
from services import art

def copy(lang):
    es=lang=='es';t=lambda en,sp:sp if es else en
    return dict(eyebrow=t('03 / YOUR DIGITAL SOLUTION','03 / TU SOLUCIÓN DIGITAL'),heading=t('Two ways forward.','Dos caminos para avanzar.'),intro=t('Whether you need your first website or a more ambitious digital presence, choose the approach that fits your business.','Tanto si necesitas tu primera web como una presencia digital más ambiciosa, elige la solución que encaje con tu negocio.'),selectors=['Express',t('Custom','A medida')],services=[dict(title=t('Express Websites','Web Express'),lead=t('A professional website with a focused scope. First version in as little as 24 hours.','Una web profesional con un alcance definido. Primera versión en tan solo 24 horas.'),body=t('For businesses that need to get online or replace a simple, outdated website. Present your services clearly, make information easy to find and give customers a direct way to contact you.','Para negocios que necesitan salir a internet o renovar una web sencilla que se ha quedado anticuada. Presenta tus servicios con claridad, facilita el acceso a la información y ofrece una vía directa de contacto.'),caption=t('DESIGN STUDY / RESPONSIVE EXPERIENCE','ESTUDIO DE DISEÑO / EXPERIENCIA RESPONSIVE'),cta=t('Explore Express','Descubre Web Express')),dict(title=t('Custom Websites','Web a medida'),lead=t('A digital experience built around your business.','Una experiencia digital a la medida de tu negocio.'),body=t('For brands that need a distinctive visual identity online, a more complete website or specific functionality. We shape the structure, design and interaction around your goals.','Para marcas que necesitan una identidad digital diferenciada, una web más completa o funciones específicas. Definimos la estructura, el diseño y la interacción a partir de tus objetivos.'),caption=t('DESIGN STUDY / MOTION & IDENTITY','ESTUDIO DE DISEÑO / MOVIMIENTO E IDENTIDAD'),cta=t('Explore Websites','Descubre el diseño web a medida'))],exit=t('FROM DIRECTION TO EXECUTION','DE LA DIRECCIÓN A LA EJECUCIÓN'),process=t('Discover our process','Descubre nuestro proceso'),price={'USD':t('From $399','Desde 399 USD'),'EUR':t('From €350','Desde 350 €')})

def section(lang,ctas):
    c=copy(lang);e=escape;es=lang=='es';cfg=json.dumps(c,ensure_ascii=False).replace('<','\\u003c')
    items=[]
    for i,s in enumerate(c['services']):
        key=('express','custom')[i];price=f'<p class="atz-service-price" data-express-price>{e(c["price"]["USD"])}</p>' if i==0 else ''
        items.append(f'<article class="atz-service-copy" id="{key}" tabindex="-1"><span class="eyebrow">0{i+1} / {e(c["selectors"][i])}</span><h3>{e(s["title"])}</h3>{price}<p class="atz-service-lead">{e(s["lead"])}</p><p>{e(s["body"])}</p>{ctas((s["cta"],"#contact"))}<figure class="atz-offer-study"><img src="/assets/{key}-study.svg" width="640" height="360" alt="{e(s["caption"])}" loading="lazy"><figcaption class="atz-study-caption">{e(s["caption"])}</figcaption></figure></article>')
    return f'''<section id="websites" class="atz-services" tabindex="-1" aria-labelledby="atz-services-heading"><script type="application/json" id="atz-services-config">{cfg}</script><header class="atz-services-head"><div><span class="eyebrow">{e(c['eyebrow'])}</span><h2 id="atz-services-heading">{e(c['heading'])}</h2></div><div class="atz-services-intro"><p>{e(c['intro'])}</p><nav aria-label="{'Elige un servicio web' if es else 'Choose a website service'}"><a href="#express">01 / {e(c['selectors'][0])} ↗</a><a href="#custom">02 / {e(c['selectors'][1])} ↗</a></nav><label class="atz-market">{'Mercado' if es else 'Market'} <select id="atz-market"><option value="USD">USD</option><option value="EUR">EUR</option></select></label></div></header><div id="atz-service-mount" hidden></div><div class="atz-offer-grid">{''.join(items)}</div><div class="atz-services-exit"><span class="eyebrow">{e(c['exit'])}</span><a class="atz-work-link" href="#method">{e(c['process'])} ↗</a></div></section>'''

def write_media(out,brand,put):
    # Authored abstract study of the approved provisional A, no third-party media.
    # The frame content changes; the source engine's playback math does not.
    for key in ('express','custom'):put(out/f'assets/{key}-study.svg',art(key,brand=brand))
    paths=brand['paths']
    for i in range(371):
        p=i/370;theta=(-.38+p*.76);w=.62+.38*cos(theta);x=960+150*sin(p*pi*2);y=540+30*sin(p*pi);size=2.7+1.4*sin(p*pi)
        mark=''.join(f'<path d="M'+ ' L'.join(f'{a} {b}' for a,b in path)+' Z" fill="url(#metal)" stroke="#c8b9ff" stroke-width=".8"/>' for path in paths)
        # Depth is baked into the authored frames, not an alternate scroll animation.
        depth=''.join(f'<g transform="translate({d*1.5} {d*2.2})" opacity="{.12+d*.045}">'+mark+'</g>' for d in range(12,0,-1))
        svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 1920 1080"><defs><radialGradient id="bg" cx="50%" cy="53%" r="65%"><stop stop-color="#24174d"/><stop offset=".54" stop-color="#100c35"/><stop offset="1" stop-color="#090812"/></radialGradient><linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#d9c9ff"/><stop offset=".18" stop-color="#7768b5"/><stop offset=".48" stop-color="#24174d"/><stop offset=".67" stop-color="#7436f5"/><stop offset="1" stop-color="#153b9d"/></linearGradient></defs><rect width="1920" height="1080" fill="url(#bg)"/><g transform="translate({x:.3f} {y:.3f}) scale({size*w:.4f} {size:.4f}) skewY({theta*14:.3f}) translate(-285 -290)">{depth}{mark}</g></svg>'''
        put(out/f'assets/service-frames/frame_{i+1:04d}.svg',svg)

def frame_module(source):
    start=source.index('28236,e=>{');end=source.index('var U=e.i(7617)',start)
    s=source[start:end]
    def once(a,b):
        nonlocal s
        if s.count(a)!=1:raise ValueError('G anchor mismatch: '+a[:110]+' '+str(s.count(a)))
        s=s.replace(a,b,1)
    once('28236,e=>{','999002,e=>{');once('e.i(48062);','')
    # Exact source uses six travelling positions, not six new commercial services.
    a=s.index('V=[{id:"card-L0"');b=s.index(';function H(',a)
    s=s[:a]+'''V=[0,1,2].map((n)=>({id:"card-L"+n,svgIndex:n,title:globalThis.__ATZ_SERVICE_COPY.services[0].title,description:globalThis.__ATZ_SERVICE_COPY.services[0][["lead","body","caption"][n]]})),O=[0,1,2].map((n)=>({id:"card-R"+n,svgIndex:n+3,title:globalThis.__ATZ_SERVICE_COPY.services[1].title,description:globalThis.__ATZ_SERVICE_COPY.services[1][["lead","body","caption"][n]]})),W=globalThis.__ATZ_SERVICE_COPY.selectors'''+s[b:]
    once('src:`/images/stone/frame_${String(t+1).padStart(4,"0")}.webp`','src:`/assets/service-frames/frame_${String(t+1).padStart(4,"0")}.svg`') if 'src:`/images/stone' in s else once('r.src=`/images/stone/frame_${String(t+1).padStart(4,"0")}.webp`','r.src=`/assets/service-frames/frame_${String(t+1).padStart(4,"0")}.svg`')
    once('n&&n.complete&&t.src','n&&n.complete&&n.naturalWidth>0&&t.src')
    once('text:"OUR SERVICES"','text:globalThis.__ATZ_SERVICE_COPY.eyebrow')
    once('text:"✦ Design with intent. Built to work."','text:globalThis.__ATZ_SERVICE_COPY.services[0].title')
    once('html:"✦ Different disciplines. One standard of craft."','text:globalThis.__ATZ_SERVICE_COPY.services[1].title')
    once('text:"view services",href:"/services"','text:globalThis.__ATZ_SERVICE_COPY.services[0].cta,href:"#express"')
    # Native anchor rather than original Next route. No third-party video/audio.
    once('var r=e.i(11846);','var r={WordShiftButton:({text,href,customClass})=>(0,t.jsx)("a",{href,className:customClass+" atz-work-link",children:text+" ↗"})};')
    a=s.index('(0,t.jsx)("video",{ref:f');b=s.index('(0,t.jsxs)("div",{className:"absolute inset-0 pointer-events-none overflow-hidden z-2',a)
    s=s[:a]+s[b:]
    once('bg-white",style:{opacity:+!!s}','bg-[#090812]",style:{opacity:+!!s}')
    once('overflow-hidden bg-[#000] ${s?','overflow-hidden bg-[#090812] ${s?')
    once('backgroundColor:"#fff",transform:"scaleY(0)"','backgroundColor:"#090812",transform:"scaleY(0)"')
    once('stroke:"#d8d8d8"','stroke:"#b967ef"')
    # G's original pair choreography F/I, particle P/q/z, frame D/B/L, smoothing,
    # original thresholds and DOM are retained. The final stripe phase belongs
    # to the next section and is not driven by this standalone service phase.
    return '(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push([document.currentScript,'+s+'e.s(["default",0,G])}]);'
