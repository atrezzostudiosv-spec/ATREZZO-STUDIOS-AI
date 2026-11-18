/* ATREZZO-owned integration host. The private original module IDs are resolved
   from the user's pinned archive by build.py; no captured engine in this file. */
(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push([document.currentScript,999001,e=>{
 'use strict';
 const React=e.i(71645), h=React.createElement, {createRoot}=e.r(88014);
 const {TransitionProvider,useTransition}=e.i(53477);
 const {SiteSoundProvider}=e.i(42936);
 const ScrollProvider=e.i(4173).default;
 const Hero=e.i(54377).default, Reveal=e.i(91092).default, Vision=e.i(72959).default;
 const {ScrollTrigger}=e.i(83495);
 const {createPortal}=e.r(18800);
 const {useTransitionReady}=e.i(62749);
 const es=document.documentElement.lang==='es';
 const t=(en,sp)=>es?sp:en;
 const ids=['s1-headline','s1-cta','s1-scroll','s1-stats','s1-box','s1-sub'];
 const arrow=()=>h('span',{className:'mi-arrow','aria-hidden':true},h('span',null,'↗'),h('span',null,'↗'));
 const cta=(label,href)=>h('a',{className:'mi-cta',href},label,arrow());
 function Ready(){const {markLoaderComplete}=useTransition();React.useEffect(()=>{markLoaderComplete();},[markLoaderComplete]);return null;}
 function HeroHost(){return h('div',{id:'hero-section',className:'hero-section'},
  h(Hero,{vibrateElementIds:ids}),
  h('div',{id:'sticky-wrap'},
   h('section',{className:'main-banner'},
    h('div',{className:'hero-top'},
     h('p',{className:'eyebrow'},'DESIGN IN MOTION'),
     h('div',{id:'s1-headline'},h(Reveal,{as:'h1',text:t('Your business. Better online.','Tu negocio. Mejor en internet.'),animationType:'chars',stagger:.08,delay:1.2,className:'hero-title',once:true})),
     h('div',{id:'s1-cta',className:'atz-mi hero-actions','data-atz-id':'ATZ-MIC-003'},h('div',{className:'mi-actions'},cta(t('Start a Project','Inicia tu proyecto'),'#contact'),cta(t('View Work','Ver proyectos'),'#work')))),
    h('div',{className:'hero-bottom'},
     h('span',{id:'s1-scroll',className:'eyebrow'},t('↓ SCROLL TO EXPLORE','↓ EXPLORA')),
     h('span',{id:'s1-stats',className:'eyebrow desktop-only'},t('HOLD TO TRANSFORM','MANTÉN PARA TRANSFORMAR')),
     h('div',{className:'hero-caption'},h('span',{id:'s1-box',className:'eyebrow'},'CREATIVE EDITORIAL STUDIO'),h('p',{id:'s1-sub'},t('Web design and digital experiences for businesses.','Diseño web y experiencias digitales para negocios.'))))),
   h('section',{className:'home-about'},h('div',{id:'s2-text'},h('span',{className:'eyebrow'},'01 / ATREZZO'),h(Reveal,{as:'h2',text:t('We design experiences. Not just websites.','Diseñamos experiencias. No solo sitios web.'),animationType:'words',stagger:.05,className:'manifesto-title',once:true}),h('p',null,t('Creative direction, technology and design working as one.','Dirección creativa, tecnología y diseño trabajando como uno.'))))),
  h(Vision),h(Ready));}
 // Same original BlurTextReveal as Selected Work, with visibility-aware
 // manual trigger for horizontal / covered panels. No original Work tween changes.
 function WorkReveal({as,text,className,kind}){
  const ready=useTransitionReady(), ref=React.useRef(null), holder=React.useRef(null);
  React.useEffect(()=>{if(!ready)return;let fired=false,frame=0,observer=null;
   const check=()=>{if(fired||!holder.current)return;const r=holder.current.getBoundingClientRect();
    const visible=r.right>innerWidth*.15&&r.left<innerWidth*.85&&r.bottom>innerHeight*.1&&r.top<innerHeight*.85;
    const overlay=document.querySelector('#work-section > div:first-child');
    const exposed=kind!=='bridge'||innerWidth<768||!overlay||overlay.getBoundingClientRect().right<innerWidth*.67;
    if(visible&&exposed&&ref.current){fired=true;ref.current.play();observer?.disconnect();ScrollTrigger.removeEventListener('update',schedule);window.removeEventListener('scroll',schedule);}
   };const schedule=()=>{if(!fired){cancelAnimationFrame(frame);frame=requestAnimationFrame(check)}};
   observer=new IntersectionObserver(schedule,{threshold:[0,.25,.5]});observer.observe(holder.current);
   ScrollTrigger.addEventListener('update',schedule);window.addEventListener('scroll',schedule,{passive:true});schedule();
   return()=>{cancelAnimationFrame(frame);observer?.disconnect();ScrollTrigger.removeEventListener('update',schedule);window.removeEventListener('scroll',schedule)};
  },[ready,kind]);
  return h('div',{ref:holder,className:'atz-work-reveal-wrap'},h(Reveal,{ref,as,text,className,animationType:'chars',stagger:.045,manual:true,once:true}));
 }
 globalThis.__ATZ_WorkReveal=WorkReveal;
 const serviceMount=document.getElementById('atz-service-mount');
 const serviceCopy=JSON.parse(document.getElementById('atz-services-config').textContent);
 globalThis.__ATZ_SERVICE_COPY=serviceCopy;
 const ServiceMotion=e.i(999002).default;
 function ServiceMotionHost(){const ready=useTransitionReady(), progress=React.useRef(0),container=React.useRef(null);
  const sync=()=>{const mobile=innerWidth<768, before=200+(mobile?60:150), duration=mobile?600:800,total=before+duration+200;return {mobile,before,duration,total}};
  React.useLayoutEffect(()=>{if(!ready)return;serviceMount.hidden=false;const initial=sync();progress.current=initial.before/initial.total;
   const trigger=ScrollTrigger.create({trigger:container.current,start:'top top',end:()=>'+='+sync().duration+'%',pin:true,pinSpacing:true,anticipatePin:1,invalidateOnRefresh:true,onUpdate:self=>{const s=sync();progress.current=(s.before+self.progress*s.duration)/s.total},onRefresh:self=>{const s=sync();progress.current=(s.before+self.progress*s.duration)/s.total}});
   requestAnimationFrame(()=>ScrollTrigger.refresh());return()=>{trigger.kill();serviceMount.hidden=true};
  },[ready]);
  return h('div',{ref:container,className:'atz-service-kinetic'},h(ServiceMotion,{scrollProgressRef:progress,embedded:true}));
 }
 function ServicesHost(){return createPortal(h(WorkBoundaryService,null,h(ServiceMotionHost)),serviceMount)}
 class WorkBoundaryService extends React.Component{constructor(p){super(p);this.state={failed:false}}static getDerivedStateFromError(){return {failed:true}}componentDidCatch(err){console.error('Services:',err);serviceMount.hidden=true;requestAnimationFrame(()=>ScrollTrigger.refresh())}render(){return this.state.failed?null:this.props.children}}
 // Private loopback cannot know a visitor country from IP. Resolve by IANA time zone
 // as a preview-only approximation; future edge supplies country/market independently of language.
 const zone=Intl.DateTimeFormat().resolvedOptions().timeZone||'';
 const eur=zone.startsWith('Europe/')||['Atlantic/Canary','Atlantic/Madeira','Atlantic/Azores','Atlantic/Faroe','Atlantic/Reykjavik'].includes(zone);
 document.querySelectorAll('[data-express-price]').forEach(n=>n.textContent=serviceCopy.price[eur?'EUR':'USD']);
 const workMount=document.getElementById('atz-work-mount'), workFallback=document.getElementById('atz-work-fallback');
 const config=JSON.parse(document.getElementById('atz-work-config').textContent);
 globalThis.__ATZ_WORK_PROJECTS=config.projects;globalThis.__ATZ_WORK_COPY=config.copy;
 class WorkBoundary extends React.Component {constructor(p){super(p);this.state={failed:false}}static getDerivedStateFromError(){return {failed:true}}componentDidCatch(err){console.error('Selected Work:',err);workFallback.hidden=false;workMount.hidden=true;requestAnimationFrame(()=>ScrollTrigger.refresh())}render(){return this.state.failed?null:this.props.children}}
 function WorkHost(){const Work=e.i(28236).default;React.useEffect(()=>{workFallback.hidden=true;return()=>{workFallback.hidden=false}},[]);return h(Work)}
 const mount=document.getElementById('experience');
 const fallback=mount.innerHTML;
 function fail(err){console.error('ATREZZO preview:',err);document.documentElement.classList.remove('motion-active');document.documentElement.style.overflow='';document.body.style.overflow='';document.getElementById('preview-state').textContent=t('WebGL preview unavailable · accessible content retained','Vista WebGL no disponible · contenido accesible conservado');try{root?.unmount()}catch{};mount.innerHTML=fallback;document.getElementById('keyfacts-section').style.marginTop='';}
 let root;
 try{
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduced){document.getElementById('preview-state').textContent=t('Reduced motion','Movimiento reducido');return;}
  if(!window.WebGL2RenderingContext){document.getElementById('preview-state').textContent='WebGL 2 unavailable';return;}
  document.documentElement.classList.add('motion-active');
  root=createRoot(mount,{onUncaughtError:fail});
  root.render(h(TransitionProvider,null,h(SiteSoundProvider,null,h(ScrollProvider,null,h(React.Fragment,null,h(HeroHost),createPortal(h(WorkBoundary,null,h(WorkHost)),workMount),h(ServicesHost))))));
  const state=document.getElementById('preview-state');
  const observer=new MutationObserver(()=>{if(mount.querySelector('#atrezzo-symbol-canvas-wrap canvas')){state.textContent='WebGL · V07 ORIGINAL MOTION';observer.disconnect();requestAnimationFrame(()=>ScrollTrigger.refresh());}});
  observer.observe(mount,{childList:true,subtree:true});
  setTimeout(()=>{if(!mount.querySelector('#atrezzo-symbol-canvas-wrap canvas')){observer.disconnect();fail(new Error('WebGL canvas did not initialize'));}},12000);
 }catch(err){fail(err);}
 e.s([]);
}]);
