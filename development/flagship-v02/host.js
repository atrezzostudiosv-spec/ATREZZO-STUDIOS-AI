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
     h('div',{className:'hero-caption'},h('span',{id:'s1-box',className:'eyebrow'},'CREATIVE EDITORIAL STUDIO'),h('p',{id:'s1-sub'},t('Web design, digital experiences and creative content.','Diseño web, experiencias digitales y contenido creativo.'))))),
   h('section',{className:'home-about'},h('div',{id:'s2-text'},h('span',{className:'eyebrow'},'01 / ATREZZO'),h(Reveal,{as:'h2',text:t('We design experiences. Not just websites.','Diseñamos experiencias. No solo sitios web.'),animationType:'words',stagger:.05,className:'manifesto-title',once:true}),h('p',null,t('Creative direction, technology and design working as one.','Dirección creativa, tecnología y diseño trabajando como uno.'))))),
  h(Vision),h(Ready));}
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
  root.render(h(TransitionProvider,null,h(SiteSoundProvider,null,h(ScrollProvider,null,h(HeroHost)))));
  const state=document.getElementById('preview-state');
  const observer=new MutationObserver(()=>{if(mount.querySelector('#trionn-symbol-canvas-wrap canvas')){state.textContent='WebGL · PRIVATE STUDY V01';observer.disconnect();requestAnimationFrame(()=>ScrollTrigger.refresh());}});
  observer.observe(mount,{childList:true,subtree:true});
  setTimeout(()=>{if(!mount.querySelector('#trionn-symbol-canvas-wrap canvas')){observer.disconnect();fail(new Error('WebGL canvas did not initialize'));}},12000);
 }catch(err){fail(err);}
 e.s([]);
}]);
