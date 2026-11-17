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

def bridge_copy(lang):
    es=lang=='es';t=lambda en,sp:sp if es else en
    # V1.2: exact public phrases relocated to the approved narrative bridge.
    return dict(label='DESIGN IN MOTION',lines=t(['IDENTITY','DESIGN','INTERACTION'],['IDENTIDAD','DISEÑO','INTERACCIÓN']),opening=t('A better website begins with better decisions.','Una web mejor empieza con mejores decisiones.'),closing=t('Every business deserves its own approach.','Cada negocio necesita su propio enfoque.'),cards=[
      [t('Business first.','El negocio primero.'),t('The structure follows the offer, audience and action the visitor needs to take.','La estructura responde a la oferta, al público y a la acción que necesita realizar el visitante.')],
      [t('A distinct visual direction.','Una dirección visual propia.'),t('Design is adapted to the identity and content of the project, not applied as an identical template.','Adaptamos el diseño a la identidad y al contenido del proyecto, no aplicamos una misma plantilla a todos.')],
      [t('Purposeful interaction.','Interacción con sentido.'),t('Motion supports the narrative and does not replace important information or clear navigation.','El movimiento apoya la narrativa y no sustituye información importante ni una navegación clara.')],
      [t('A clear path to the next action.','Un camino claro hacia la siguiente acción.'),t('Your website should explain what you do, reflect the quality of your work and help the right people take the next step.','Tu web debe explicar lo que haces, reflejar la calidad de tu trabajo y ayudar a las personas adecuadas a dar el siguiente paso.')],
      [t('A design reviewed across devices.','Un diseño revisado en distintos dispositivos.'),t('We consider responsive behavior, legibility, accessibility and functionality before launch.','Consideramos el comportamiento responsive, legibilidad, accesibilidad y funcionamiento antes del lanzamiento.')],
      [t('A scope defined for your project.','Un alcance definido para tu proyecto.'),t('The proposal defines pages, deliverables, integrations, review rounds, launch and price before work begins.','La propuesta define páginas, entregables, integraciones, rondas de revisión, lanzamiento y precio antes de comenzar.')]])

def section(lang,ctas):
    c=copy(lang);c["bridge"]=bridge_copy(lang);e=escape;es=lang=='es';cfg=json.dumps(c,ensure_ascii=False).replace('<','\\u003c')
    items=[]
    for i,s in enumerate(c['services']):
        key=('express','custom')[i];price=f'<p class="atz-service-price" data-express-price>{e(c["price"]["USD"])}</p>' if i==0 else ''
        items.append(f'<article class="atz-service-copy" id="{key}" tabindex="-1"><span class="eyebrow">0{i+1} / {e(c["selectors"][i])}</span><h3>{e(s["title"])}</h3>{price}<p class="atz-service-lead">{e(s["lead"])}</p><p>{e(s["body"])}</p>{ctas((s["cta"],"#contact"))}<figure class="atz-offer-study"><img src="/assets/{key}-study.svg" width="640" height="360" alt="{e(s["caption"])}" loading="lazy"><figcaption class="atz-study-caption">{e(s["caption"])}</figcaption></figure></article>')
    return f'''<section id="websites" class="atz-services" tabindex="-1" aria-labelledby="atz-services-heading"><script type="application/json" id="atz-services-config">{cfg}</script><div id="atz-service-mount" hidden></div><div id="atz-offers" class="atz-offers"><header class="atz-services-head"><div><span class="eyebrow">{e(c['eyebrow'])}</span><h2 id="atz-services-heading">{e(c['heading'])}</h2></div><div class="atz-services-intro"><p>{e(c['intro'])}</p><nav aria-label="{'Elige un servicio web' if es else 'Choose a website service'}"><a href="#express">01 / {e(c['selectors'][0])} ↗</a><a href="#custom">02 / {e(c['selectors'][1])} ↗</a></nav></div></header><div class="atz-offer-grid">{''.join(items)}</div><div class="atz-services-exit"><span class="eyebrow">{e(c['exit'])}</span><a class="atz-work-link" href="#method">{e(c['process'])} ↗</a></div></div></section>'''

def write_media(out,brand,put):
    # Authored abstract study of the approved provisional A, no third-party media.
    # The frame content changes; the source engine's playback math does not.
    for key in ('express','custom'):put(out/f'assets/{key}-study.svg',art(key,brand=brand))
    paths=brand['paths']
    for i in range(371):
        p=i/370;theta=(-.38+p*.76);w=.62+.38*cos(theta);x=960+150*sin(p*pi*2);y=540+30*sin(p*pi);size=2.7+1.4*sin(p*pi)
        # Approved geometry and pose formulas; refined solid silver/violet faces.
        # Transparent frame: the live WebGL field is rendered behind it.
        dx,dy=11.0*sin(theta),11.0
        faces=[];walls=[]
        for n,path in enumerate(paths):
            d='M'+' L'.join(f'{a} {b}' for a,b in path)+' Z'
            for j,(a,b) in enumerate(path):
                c,d2=path[(j+1)%len(path)]
                walls.append(f'<path d="M{a} {b} L{c} {d2} L{c+dx:.3f} {d2+dy:.3f} L{a+dx:.3f} {b+dy:.3f} Z" fill="url(#edge{j%2})"/>')
            faces.append(f'<path d="{d}" fill="url(#face{n})" stroke="#d5cff7" stroke-width=".28" stroke-linejoin="round"/>')
        svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 1920 1080"><defs>
          <linearGradient id="face0" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#b9c4f0"/><stop offset=".13" stop-color="#747ba8"/><stop offset=".32" stop-color="#34375c"/><stop offset=".54" stop-color="#69658f"/><stop offset=".69" stop-color="#a9a2da"/><stop offset=".85" stop-color="#574579"/><stop offset="1" stop-color="#221b42"/></linearGradient>
          <linearGradient id="face1" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#aaa5e2"/><stop offset=".16" stop-color="#62528f"/><stop offset=".45" stop-color="#2b214e"/><stop offset=".68" stop-color="#7962ba"/><stop offset=".9" stop-color="#453069"/><stop offset="1" stop-color="#1c1737"/></linearGradient>
          <linearGradient id="face2" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#a1b6e8"/><stop offset=".2" stop-color="#58679d"/><stop offset=".47" stop-color="#2d2856"/><stop offset=".76" stop-color="#7762b1"/><stop offset="1" stop-color="#33254f"/></linearGradient>
          <linearGradient id="edge0"><stop stop-color="#25223f"/><stop offset="1" stop-color="#625092"/></linearGradient><linearGradient id="edge1"><stop stop-color="#17142e"/><stop offset="1" stop-color="#403b70"/></linearGradient></defs><g transform="translate({x:.3f} {y:.3f}) scale({size*w:.4f} {size:.4f}) skewY({theta*14:.3f}) translate(-285 -290)">{''.join(walls)}{''.join(faces)}</g></svg>'''
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
    s=s[:a]+'''V=[0,1,2].map((n)=>({id:"card-L"+n,svgIndex:n,title:globalThis.__ATZ_SERVICE_COPY.bridge.cards[n*2][0],description:globalThis.__ATZ_SERVICE_COPY.bridge.cards[n*2][1]})),O=[0,1,2].map((n)=>({id:"card-R"+n,svgIndex:n+3,title:globalThis.__ATZ_SERVICE_COPY.bridge.cards[n*2+1][0],description:globalThis.__ATZ_SERVICE_COPY.bridge.cards[n*2+1][1]})),W=globalThis.__ATZ_SERVICE_COPY.bridge.lines'''+s[b:]
    once('src:`/images/stone/frame_${String(t+1).padStart(4,"0")}.webp`','src:`/assets/service-frames/frame_${String(t+1).padStart(4,"0")}.svg`') if 'src:`/images/stone' in s else once('r.src=`/images/stone/frame_${String(t+1).padStart(4,"0")}.webp`','r.src=`/assets/service-frames/frame_${String(t+1).padStart(4,"0")}.svg`')
    once('n&&n.complete&&t.src','n&&n.complete&&n.naturalWidth>0&&t.src')
    once('text:"OUR SERVICES"','text:globalThis.__ATZ_SERVICE_COPY.bridge.label')
    once('text:"✦ Design with intent. Built to work."','text:globalThis.__ATZ_SERVICE_COPY.bridge.opening')
    once('html:"✦ Different disciplines. One standard of craft."','text:globalThis.__ATZ_SERVICE_COPY.bridge.closing')
    once('text:"view services",href:"/services"','text:"",href:"#atz-offers"')
    # Native anchor rather than original Next route. No third-party video/audio.
    once('var r=e.i(11846);','var r={WordShiftButton:()=>null};')
    a=s.index('(0,t.jsx)("video",{ref:f');b=s.index('(0,t.jsxs)("div",{className:"absolute inset-0 pointer-events-none overflow-hidden z-2',a)
    s=s[:a]+s[b:]
    once('bg-white",style:{opacity:+!!s}','bg-[#090812]",style:{opacity:+!!s}')
    once('overflow-hidden bg-[#000] ${s?','overflow-hidden bg-[#090812] ${s?')
    once('backgroundColor:"#fff",transform:"scaleY(0)"','backgroundColor:"#090812",transform:"scaleY(0)"')
    once('stroke:"#d8d8d8"','stroke:"#b967ef"')
    once('k.current.style.mixBlendMode="difference"','k.current.style.mixBlendMode="normal"')
    once('isolation:isolate;mix-blend-mode:difference;','isolation:isolate;mix-blend-mode:normal;')
    # Keep the source's per-character crossfade, but prevent the nested reveal
    # from leaving letters hidden when the separate pinned phase is scrubbed.
    once('let t=g.current.querySelectorAll(".chars"),r=b.current.querySelectorAll(".chars");','let t=g.current.querySelectorAll(".chars"),r=b.current.querySelectorAll(".chars");[g.current,b.current].forEach(el=>{el.querySelectorAll(".title,.words,.lines,.chars").forEach(n=>{n.style.visibility="visible";if(!n.classList.contains("chars")){n.style.opacity="1";n.style.filter="none"}})});')

    once('var t=e.i(43476);','var t=e.i(43476),Galaxy=e.i(999003).default;')
    once('(0,t.jsx)("img",{ref:u,id:"c"','(0,t.jsx)(Galaxy,{scrollProgressRef:e}),(0,t.jsx)("img",{ref:u,id:"c"')
    # The private bridge has no testimonials; do not tween a nonexistent node.
    once('t?r.to(n,{yPercent:0,ease:"none"},"stripes_start-=0.16"):r.to(n,{yPercent:0,ease:"none"},"stripes_start-=0.4")','n&&(t?r.to(n,{yPercent:0,ease:"none"},"stripes_start-=0.16"):r.to(n,{yPercent:0,ease:"none"},"stripes_start-=0.4"))')
    # G's original pair choreography F/I, particle P/q/z, frame D/B/L, smoothing,
    # original thresholds and DOM are retained. The final stripe phase belongs
    # to the next section and is not driven by this standalone service phase.
    return '(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push([document.currentScript,'+s+'e.s(["default",0,G])}]);'
