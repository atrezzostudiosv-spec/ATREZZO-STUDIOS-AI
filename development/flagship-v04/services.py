"""ATREZZO-owned service composition and illustrative media. The original private G
frame engine is resolved by exact source anchors at build; no captured code ships."""
from html import escape
from math import sin, pi, cos
from pathlib import Path
import hashlib

# Screen graphics are studio service illustrations, not client projects or screenshots.
def art(kind, p=1.0, brand=None):
    custom=kind=='custom'; p=max(0,min(1,p)); q=p*p*(3-2*p)
    paths=brand['paths']; mark=''.join('<path d="M'+' L'.join(f'{x} {y}' for x,y in path)+' Z" fill="url(#metal)" stroke="#d9c6ff" stroke-width="1"/>' for path in paths)
    # Same concept throughout: a digital interface composed around the actual ATREZZO symbol.
    grid=''.join(f'<path d="M{x} 0V720"/>' for x in range(0,1281,80))+''.join(f'<path d="M0 {y}H1280"/>' for y in range(0,721,80))
    defs='''<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#090812"/><stop offset=".58" stop-color="#100c35"/><stop offset="1" stop-color="#153b9d"/></linearGradient><linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f5f5fa"/><stop offset=".30" stop-color="#c9b2ff"/><stop offset=".65" stop-color="#7436f5"/><stop offset="1" stop-color="#153b9d"/></linearGradient><radialGradient id="glow"><stop stop-color="#7436f5" stop-opacity=".55"/><stop offset="1" stop-color="#7436f5" stop-opacity="0"/></radialGradient><linearGradient id="screen" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#18132b"/><stop offset="1" stop-color="#090812"/></linearGradient><linearGradient id="paper"><stop stop-color="#f5f5fa"/><stop offset="1" stop-color="#ded9f4"/></linearGradient></defs>'''
    base=f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 1280 720">{defs}<rect width="1280" height="720" fill="url(#bg)"/><ellipse cx="{810+80*q:.1f}" cy="{360-30*q:.1f}" rx="510" ry="400" fill="url(#glow)"/><g stroke="#b967ef" stroke-width="1" opacity=".085">{grid}</g><g fill="none" stroke="#b967ef" opacity=".4"><path d="M34 36H1246M34 684H1246"/><path d="M46 55V85M31 70H61M1234 635V665M1219 650H1249"/></g>'
    if not custom:
      # An expressive but practical responsive website concept, desktop + phone.
      desktop='''<g transform="translate(125 105)"><rect x="0" y="0" width="870" height="510" rx="13" fill="#080711" stroke="#a89cd2" stroke-width="2"/><rect x="15" y="15" width="840" height="480" rx="4" fill="url(#paper)"/><rect x="15" y="15" width="840" height="55" fill="#ece9f4"/><g fill="#19152d" font-family="Arial,sans-serif"><text x="43" y="50" font-size="18" font-weight="700" letter-spacing="4">ATREZZO</text><text x="626" y="48" font-size="12">WORK      STUDIO      CONTACT</text><text x="57" y="191" font-size="63" letter-spacing="-4">A clearer</text><text x="57" y="253" font-size="63" letter-spacing="-4">way online.</text><text x="60" y="301" font-size="16" fill="#4c4864">Purpose. Clarity. A strong digital presence.</text></g><rect x="60" y="330" width="153" height="41" rx="20" fill="#100c35"/><text x="78" y="355" font-size="13" font-family="Arial" fill="#f5f5fa">Explore the work ↗</text><rect x="482" y="104" width="344" height="340" fill="#100c35"/><g transform="translate(426 26) scale(.79)">'''+mark+'''</g><path d="M57 417H423M57 445H280" stroke="#100c35" stroke-opacity=".22" stroke-width="2"/></g>'''
      phone='''<g transform="translate(906 237)"><rect width="214" height="390" rx="24" fill="#0a0812" stroke="#c7b5ff" stroke-width="2"/><rect x="9" y="9" width="196" height="372" rx="17" fill="#f5f5fa"/><rect x="76" y="18" width="62" height="6" rx="3" fill="#100c35"/><text x="25" y="59" fill="#100c35" font-size="13" font-family="Arial" letter-spacing="2">ATREZZO</text><text x="24" y="108" fill="#100c35" font-size="26" font-family="Arial" letter-spacing="-1">A clearer</text><text x="24" y="137" fill="#100c35" font-size="26" font-family="Arial" letter-spacing="-1">way online.</text><rect x="24" y="162" width="166" height="137" fill="#100c35"/><g transform="translate(-1 125) scale(.36)">'''+mark+'''</g><rect x="24" y="324" width="119" height="29" rx="14" fill="#100c35"/><text x="36" y="343" fill="#f5f5fa" font-size="10" font-family="Arial">Explore ↗</text></g>'''
      return base+desktop+phone+'<text x="46" y="661" fill="#d2c3f8" font-family="Arial" font-size="14" letter-spacing="3">01 / EXPRESS — STUDIO DESIGN STUDY</text></svg>'
    # Original 371-frame media: actual vector states of one authored interface,
    # from precise grid / initial geometry to dimensional, branded composition.
    # Do not pretend these are filmed footage or a customer project.
    dx=110*q;dy=-36*q;angle=-9+9*q
    orbit=''.join(f'<ellipse cx="{840+20*sin(p*pi):.2f}" cy="338" rx="{r+34*q:.2f}" ry="{r*.53+10*q:.2f}" transform="rotate({-24+20*q:.2f} 840 338)" fill="none" stroke="#b967ef" opacity="{.08+.06*i:.2f}" stroke-width="1.5"/>' for i,r in enumerate([210,260,310]))
    layers=''.join(f'<g transform="translate({40*i*(1-q)+dx*.3:.2f} {18*i*(1-q)+dy*.3:.2f})"><rect x="{146+12*i}" y="{140+9*i}" width="944" height="456" fill="#100c35" fill-opacity=".38" stroke="#b967ef" stroke-opacity="{.12+.06*i:.2f}" stroke-width="1.2"/></g>' for i in range(3,0,-1))
    screen=f'''<g transform="translate({dx*.35:.2f} {dy*.35:.2f}) rotate({angle:.2f} 640 360)">{layers}<rect x="144" y="136" width="992" height="470" rx="10" fill="#070610" stroke="#a59ad3" stroke-width="2"/><rect x="158" y="150" width="964" height="442" rx="3" fill="url(#screen)"/><path d="M158 201H1122" stroke="#b967ef" stroke-opacity=".35"/><g font-family="Arial,sans-serif" fill="#f5f5fa"><text x="183" y="181" font-size="16" letter-spacing="4" font-weight="700">ATREZZO</text><text x="1050" y="181" font-size="11" text-anchor="end" letter-spacing="2">DESIGN IN MOTION</text><text x="194" y="321" font-size="74" letter-spacing="-5">Made to</text><text x="194" y="397" font-size="74" letter-spacing="-5">move.</text><text x="198" y="444" fill="#bfb3de" font-size="17">A digital experience built around the brand.</text></g><path d="M198 482H410" stroke="#b967ef" stroke-width="2"/><circle cx="843" cy="381" r="{156+25*q:.2f}" fill="#7436f5" fill-opacity=".08" stroke="#b967ef" stroke-opacity=".35"/><g transform="translate({532+dx*.4:.2f} {65+dy*.5:.2f}) scale({.83+.20*q:.4f})">{mark}</g></g>'''
    return base+orbit+screen+f'<g fill="#cfc0f8" font-family="Arial" font-size="14" letter-spacing="3"><text x="46" y="661">02 / CUSTOM — STUDIO DESIGN STUDY</text><text x="1234" y="661" text-anchor="end">FORM / {round(p*370)+1:03d}</text></g></svg>'

def write_media(out,brand,put):
    put(out/'assets/express-study.svg',art('express',brand=brand))
    put(out/'assets/custom-study.svg',art('custom',1,brand))
    for i in range(371):put(out/f'assets/service-frames/frame_{i+1:04d}.svg',art('custom',i/370,brand))

def section(lang,ctas):
    es=lang=='es';t=lambda a,b:b if es else a
    def title(id,tag,copy,cls):
      return f'<div id="{id}" class="atz-service-reveal"><{tag} class="{cls}" data-service-fallback>{escape(copy)}</{tag}><div data-service-title="{escape(copy,quote=True)}" data-service-tag="{tag}" data-service-class="{cls}"></div></div>'
    return f'''<section id="websites" class="atz-services" tabindex="-1" aria-labelledby="atz-services-heading"><div class="atz-services-head"><div><span class="eyebrow">03 / {t('YOUR DIGITAL SOLUTION','TU SOLUCIÓN DIGITAL')}</span>{title('atz-services-heading','h2',t('Two ways forward.','Dos caminos para avanzar.'),'atz-services-title')}</div><div class="atz-services-intro"><p>{t('Different needs. One standard of design. Choose the digital experience that fits your business.','Distintas necesidades. Un mismo estándar de diseño. Elige la experiencia digital que encaja con tu negocio.')}</p><nav aria-label="{t('Choose a website service','Elige un servicio web')}"><a href="#express">01 / Express ↗</a><a href="#custom">02 / Custom ↗</a></nav></div></div>
    <article id="express" class="atz-service-row atz-service-express" tabindex="-1"><div class="atz-service-copy"><span class="eyebrow">01 / EXPRESS</span>{title('atz-express-title','h3',t('Express Websites','Web Express'),'atz-service-title')}<p class="atz-service-lead">{t('A focused digital presence for businesses ready to get online.','Una presencia digital enfocada para negocios que quieren estar en internet.')}</p><p>{t('A clear, responsive website that presents your business, its services and the next step for your customers.','Una web clara y adaptable que presenta tu negocio, tus servicios y el siguiente paso para tus clientes.')}</p>{ctas((t('Explore Express','Explorar Express'),'#contact'))}</div><figure class="atz-service-art"><img src="/assets/express-study.svg" width="640" height="360" alt="{t('Illustrative studio design: responsive desktop and mobile website','Diseño ilustrativo del estudio: web adaptable de escritorio y móvil')}" loading="lazy"><figcaption>{t('DESIGN STUDY / RESPONSIVE EXPERIENCE','ESTUDIO DE DISEÑO / EXPERIENCIA RESPONSIVE')}</figcaption></figure></article>
    <article id="custom" class="atz-service-row atz-service-custom" tabindex="-1"><figure class="atz-service-art atz-service-motion"><img id="atz-service-frame" src="/assets/custom-study.svg" width="640" height="360" alt="{t('Illustrative studio design: dimensional branded website','Diseño ilustrativo del estudio: web de marca con profundidad')}" loading="lazy"><figcaption>{t('DESIGN STUDY / MOTION & IDENTITY','ESTUDIO DE DISEÑO / MOVIMIENTO E IDENTIDAD')}</figcaption></figure><div class="atz-service-copy"><span class="eyebrow">02 / CUSTOM</span>{title('atz-custom-title','h3',t('Custom Websites','Web a medida'),'atz-service-title')}<p class="atz-service-lead">{t('A tailored digital experience built around your brand, content and goals.','Una experiencia digital a medida de tu marca, contenido y objetivos.')}</p><p>{t('Creative direction, a distinctive visual system and purposeful interaction, designed as one experience.','Dirección creativa, un sistema visual propio e interacción con propósito, diseñados como una sola experiencia.')}</p>{ctas((t('Explore Websites','Explorar diseño web'),'#contact'))}</div></article>
    <div class="atz-services-exit"><span class="eyebrow">{t('FROM DIRECTION TO EXECUTION','DE LA DIRECCIÓN A LA EJECUCIÓN')}</span><a class="atz-work-link" href="#method">{t('Discover our process','Descubre nuestro proceso')} ↗</a></div></section>'''

def frame_module(source):
    # Exact G source anchors, verified by build's pinned git blob SHA.
    # Only frame preload / display callbacks and original smoothing are reused;
    # source layout, six transient cards, videos/audio and 800% pin are excluded.
    start=source.index('L=(0,E.useCallback)(e=>{let t=u.current;')
    end=source.index(',D=(0,E.useCallback)',start)
    L=source[start:end].replace('n&&n.complete&&','n&&n.complete&&n.naturalWidth>0&&',1)
    start=source.index('B=(0,E.useCallback)(()=>{let e=C.current;if(e.preloading')
    end=source.index(';return(0,w.useGSAP)',start)
    B=source[start:end].replace('/images/stone/frame_','/assets/service-frames/frame_').replace('.webp`','.svg`')
    # Cancellation guard is host lifecycle adaptation, not a change to batch size or interpolation.
    B=B.replace('r=l=>{let n=', 'r=l=>{if(e.disposed)return;let n=',1).replace('a++,e.loaded++','if(e.disposed)return;a++,e.loaded++',1)
    tick='let c=370*t.scrollT;t.videoIdx+=(c-t.videoIdx)*.12;'
    if source.count(tick)!=1:raise ValueError('Original interpolation not found')
    return '''(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push([document.currentScript,999002,e=>{"use strict";
const {ScrollTrigger}=e.i(83495),{getCanvasManager}=e.i(71871);
function mount(section){const img=section.querySelector('#atz-service-frame'),stage=section.querySelector('.atz-service-motion');if(!img||!stage||matchMedia('(prefers-reduced-motion: reduce)').matches)return ()=>{};
const C={current:{imgs:Array(371),loaded:0,preloading:false,videoIdx:0,scrollT:0,disposed:false}},u={current:img},E={useCallback:fn=>fn};
const '''+L+','+B+''';
const manager=getCanvasManager(),id=manager.register(()=>{let t=C.current;if(!t.loaded)return;'''+tick+'''L(t.videoIdx)},false,'atz-service-frame');
const trigger=ScrollTrigger.create({trigger:stage,start:'top bottom',end:'bottom top',onUpdate:s=>{C.current.scrollT=s.progress},onRefresh:s=>{C.current.scrollT=s.progress}});
const preload=new IntersectionObserver(([entry])=>{if(entry.isIntersecting){B();preload.disconnect()}},{rootMargin:'1000px 0px'});preload.observe(stage);
const active=new IntersectionObserver(([entry])=>manager.setActive(id,entry.isIntersecting&&!matchMedia('(prefers-reduced-motion: reduce)').matches),{threshold:0,rootMargin:'120px 0px'});active.observe(stage);
const media=matchMedia('(prefers-reduced-motion: reduce)'),reduce=()=>{if(media.matches){manager.setActive(id,false);img.src='/assets/custom-study.svg'}else if(!C.current.disposed){manager.setActive(id,stage.getBoundingClientRect().bottom>0&&stage.getBoundingClientRect().top<innerHeight)}};media.addEventListener('change',reduce);
return ()=>{C.current.disposed=true;preload.disconnect();active.disconnect();trigger.kill();manager.unregister(id);media.removeEventListener('change',reduce);C.current.imgs=[];img.src='/assets/custom-study.svg'};
} e.s(['mount',0,mount]);}]);'''
