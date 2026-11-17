// Independent V06 migration candidate. No captured engine, CSS or shader.
import {createBrowserRuntime,gsap,ScrollTrigger,THREE} from "./src/official.mjs";
import {mountMonogramFrames} from "./src/monogram-frames.mjs";
import brand from "../flagship-v06/brand.json";
const q=(s,r=document)=>r.querySelector(s);
const clamp=(n,a=0,b=1)=>Math.min(b,Math.max(a,n));
export function initPreview(mounts){
 const status=q("#preview-state"),media=matchMedia("(prefers-reduced-motion: reduce)");
 const state=window.ATREZZO_NATIVE={ready:false,hero:false,particles:false,frame:0,bridgeProgress:0,workProgress:0,panel:0,errors:[]};
 const error=e=>{state.errors.push(String(e));console.error(e)};
 const controllers=[];
 for(const [id,mount] of mounts)for(const root of document.querySelectorAll('[data-atz-id="'+id+'"]'))try{controllers.push(mount(root))}catch(e){error(e)}
 const runtime=createBrowserRuntime({onError:error});
 runtime.start();
 const mm=gsap.matchMedia();
 const clean=[];
 const renderers=[];
 const rendererFor=(canvas)=>{const renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true,powerPreference:"low-power"});renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.5));renderer.outputEncoding=THREE.sRGBEncoding;renderer.setClearColor(0,0);renderers.push(renderer);return renderer};
 const resize=(renderer,camera,element)=>{const r=element.getBoundingClientRect(),w=Math.max(1,r.width),h=Math.max(1,r.height);renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();return w/h};
 const hero=q(".main-banner"),heroSection=q("#hero-section"),heroCanvas=q("#native-hero-canvas");
 if(hero&&heroSection&&heroCanvas){
  try{
   const renderer=rendererFor(heroCanvas),scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(38,1,.1,100);
   camera.position.set(0,0,10);
   scene.add(new THREE.HemisphereLight(0xe6dcff,0x241643,2.2));
   for(const [color,intensity,x,y,z] of [[0xe7e5ff,3,4,5,6],[0x7436f5,2,-5,1,3],[0x416aff,2,0,-4,-2]]){
    const light=new THREE.DirectionalLight(color,intensity);light.position.set(x,y,z);scene.add(light);
   }
   const group=new THREE.Group();scene.add(group);
   const pieces=brand.paths.map((path,i)=>{
    const shape=new THREE.Shape();
    path.forEach(([x,y],j)=>shape[j?"lineTo":"moveTo"]((x-brand.center[0])*brand.scale,(brand.center[1]-y)*brand.scale));
    shape.closePath();
    const geometry=new THREE.ExtrudeGeometry(shape,{depth:.19,bevelEnabled:true,bevelSize:.015,bevelThickness:.018,bevelSegments:2,steps:1,curveSegments:1});
    const center=new THREE.Vector3();geometry.computeBoundingBox();geometry.boundingBox.getCenter(center);geometry.translate(-center.x,-center.y,-center.z);
    const material=new THREE.MeshStandardMaterial({color:[0xc9c6e2,0x9990d1,0x8f9ed8][i],metalness:.48,roughness:.29});
    const mesh=new THREE.Mesh(geometry,material);mesh.position.copy(center);group.add(mesh);
    return {mesh,center,geometry,material};
   });
   let pointer={x:0,y:0},held=false,aspect=1,progress=0;
   const fit=()=>{aspect=resize(renderer,camera,heroCanvas);group.scale.setScalar(aspect<.85?1.0:1.28);group.position.set(aspect<.85?0:Math.min(1.7,aspect*.9),aspect<.85?-.75:-.08,0)};
   const onMove=e=>{const r=hero.getBoundingClientRect();pointer.x=clamp((e.clientX-r.left)/r.width)*2-1;pointer.y=clamp((e.clientY-r.top)/r.height)*2-1};
   const down=e=>{if(!e.target.closest("a,button,input"))held=true};
   const up=()=>{held=false};
   hero.addEventListener("pointermove",onMove,{passive:true});hero.addEventListener("pointerdown",down,{passive:true});window.addEventListener("pointerup",up,{passive:true});window.addEventListener("pointercancel",up,{passive:true});
   const leave=()=>{pointer={x:0,y:0};held=false};hero.addEventListener("pointerleave",leave);
   const ro=new ResizeObserver(fit);ro.observe(hero);heroCanvas.hidden=false;fit();
   const trigger=ScrollTrigger.create({trigger:hero,start:"top top",end:"bottom top",onUpdate:self=>progress=self.progress});
   renderer.render(scene,camera);heroSection.classList.add("native-hero-ready");state.hero=true;
   const stop=runtime.register(hero,{
    render:({delta,time})=>{
     const smooth=1-Math.exp(-delta*7),spread=held?.6:progress*.22;
     group.rotation.y+=(pointer.x*.34+Math.sin(time*.32)*.13+progress*.6-group.rotation.y)*smooth;
     group.rotation.x+=(-pointer.y*.18-group.rotation.x)*smooth;
     pieces.forEach(({mesh,center},i)=>{
      const x=center.x+(i===0?-1:i===2?1:.12)*spread,y=center.y+(i===1?1:-.3)*spread;
      mesh.position.x+=(x-mesh.position.x)*smooth;mesh.position.y+=(y-mesh.position.y)*smooth;mesh.rotation.z+=((held?(i-1)*.17:0)-mesh.rotation.z)*smooth;
     });renderer.render(scene,camera);
    },
    static:flag=>{heroCanvas.hidden=flag;heroSection.classList.toggle("native-hero-ready",!flag);if(!flag){fit();renderer.render(scene,camera)}},
    dispose:()=>{trigger.kill();ro.disconnect();hero.removeEventListener("pointermove",onMove);hero.removeEventListener("pointerdown",down);hero.removeEventListener("pointerleave",leave);window.removeEventListener("pointerup",up);window.removeEventListener("pointercancel",up);pieces.forEach(p=>{p.geometry.dispose();p.material.dispose()});renderer.dispose()}
   });clean.push(stop);
  }catch(e){heroCanvas.hidden=true;state.heroFallback=String(e)}
 }
 const work=q("#atz-work-fallback"),track=q(".atz-work-static-grid",work);
 if(work&&track)mm.add("(min-width: 768px) and (min-height: 650px) and (prefers-reduced-motion: no-preference)",()=>{
  work.classList.add("native-horizontal");
  const distance=()=>Math.max(0,track.scrollWidth-work.clientWidth+2*parseFloat(getComputedStyle(work).paddingLeft));
  const update=self=>{state.workProgress=self.progress;gsap.set(track,{x:-distance()*self.progress})};
  const trigger=ScrollTrigger.create({trigger:work,start:"top top",end:()=>"+="+Math.max(innerHeight,distance()*1.8),pin:true,anticipatePin:1,invalidateOnRefresh:true,onUpdate:update,onRefresh:update});
  const focus=e=>{const card=e.target.closest("article");if(!card)return;const r=card.getBoundingClientRect();if(r.right>innerWidth||r.left<0){const fraction=clamp(card.offsetLeft/Math.max(1,distance()));window.scrollTo(0,trigger.start+(trigger.end-trigger.start)*fraction)}};
  track.addEventListener("focusin",focus);
  return()=>{track.removeEventListener("focusin",focus);trigger.kill();gsap.set(track,{clearProps:"transform"});work.classList.remove("native-horizontal")};
 });
 const bridge=q(".native-bridge"),stage=q(".native-bridge-stage"),img=q("#native-monogram"),canvas=q("#native-particles");
 if(bridge&&stage&&img){
  const player=mountMonogramFrames(img,{baseURL:new URL("../assets/service-frames/",location.href),onFrame:i=>{state.frame=i},onError:error});
  player.setReducedMotion(media.matches);
  clean.push(()=>player.destroy());
  const panels=[...stage.querySelectorAll(".native-panel")];
  const show=i=>{state.panel=i;panels.forEach((panel,k)=>{panel.classList.toggle("is-current",k===i);if(bridge.classList.contains("native-pinned"))panel.setAttribute("aria-hidden",String(k!==i));else panel.removeAttribute("aria-hidden")})};
  mm.add("(min-width: 768px) and (min-height: 650px) and (prefers-reduced-motion: no-preference)",()=>{
   bridge.classList.add("native-pinned");player.setReducedMotion(false);
   const update=self=>{state.bridgeProgress=self.progress;player.setProgress(self.progress);show(Math.min(5,Math.floor(self.progress*6)))};
   const trigger=ScrollTrigger.create({trigger:stage,start:"top top",end:()=>"+="+innerHeight*8,pin:true,anticipatePin:1,invalidateOnRefresh:true,onUpdate:update,onRefresh:update});show(0);
   return()=>{trigger.kill();bridge.classList.remove("native-pinned");panels.forEach(p=>{p.removeAttribute("aria-hidden");p.classList.remove("is-current")})};
  });
  mm.add("(max-width: 767px) and (prefers-reduced-motion: no-preference), (max-height: 649px) and (prefers-reduced-motion: no-preference)",()=>{
   player.setReducedMotion(false);const update=self=>{state.bridgeProgress=self.progress;player.setProgress(self.progress)};
   const trigger=ScrollTrigger.create({trigger:bridge,start:"top bottom",end:"bottom top",onUpdate:update,onRefresh:update});return()=>trigger.kill();
  });
  mm.add("(prefers-reduced-motion: reduce)",()=>{player.setReducedMotion(true);return()=>player.setReducedMotion(false)});
  if(canvas)try{
   const renderer=rendererFor(canvas),scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(47,1,.1,100);camera.position.z=13;
   let seed=0x6d2b79f5;const random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
   const makeField=(count,radius,size)=>{
    const coords=new Float32Array(count*3),colors=new Float32Array(count*3);
    const a=new THREE.Color(0x8f72dd),b=new THREE.Color(0xc1cfff);
    for(let i=0;i<count;i++){const angle=random()*Math.PI*2,r=Math.sqrt(random())*radius,z=(random()-.5)*7;coords[i*3]=Math.cos(angle)*r;coords[i*3+1]=Math.sin(angle)*r*.6;coords[i*3+2]=z;const c=a.clone().lerp(b,random());colors.set([c.r,c.g,c.b],i*3)}
    const geometry=new THREE.BufferGeometry();geometry.setAttribute("position",new THREE.BufferAttribute(coords,3));geometry.setAttribute("color",new THREE.BufferAttribute(colors,3));
    const material=new THREE.PointsMaterial({size,sizeAttenuation:true,vertexColors:true,transparent:true,opacity:.7,depthWrite:false,blending:THREE.AdditiveBlending});const points=new THREE.Points(geometry,material);scene.add(points);return {points,geometry,material};
   };
   const fields=[makeField(4000,8,.025),makeField(8000,14,.014)];let pointer={x:0,y:0};
   const move=e=>{const r=stage.getBoundingClientRect();pointer.x=clamp((e.clientX-r.left)/r.width)*2-1;pointer.y=clamp((e.clientY-r.top)/r.height)*2-1};
   stage.addEventListener("pointermove",move,{passive:true});const fit=()=>resize(renderer,camera,canvas);
   const ro=new ResizeObserver(fit);ro.observe(stage);canvas.hidden=false;fit();renderer.render(scene,camera);state.particles=true;
   const stop=runtime.register(stage,{render:({delta,time})=>{const k=1-Math.exp(-delta*3);fields.forEach(({points},i)=>{points.rotation.z=time*(i?-.009:.014)+state.bridgeProgress*(i?.22:.38);points.rotation.y+=(pointer.x*.08-points.rotation.y)*k;points.rotation.x+=(-pointer.y*.05-points.rotation.x)*k});renderer.render(scene,camera)},static:flag=>{canvas.hidden=flag;if(!flag){fit();renderer.render(scene,camera)}},dispose:()=>{ro.disconnect();stage.removeEventListener("pointermove",move);fields.forEach(f=>{f.geometry.dispose();f.material.dispose()});renderer.dispose()}});
   clean.push(stop);
  }catch(e){canvas.hidden=true;state.particleFallback=String(e)}
 }
 // Same preview-only market convention as V06; not a real IP-country service.
 const zone=Intl.DateTimeFormat().resolvedOptions().timeZone||"",price=q("[data-express-price]");
 if(price&&zone.startsWith("Europe/"))price.textContent=document.documentElement.lang==="es"?"Desde 350 €":"From €350";
 state.ready=true;status.textContent="V06 NATIVE MIGRATION · VISUAL REVIEW PENDING";
 requestAnimationFrame(()=>ScrollTrigger.refresh());
 window.addEventListener("pagehide",()=>{mm.revert();clean.reverse().forEach(f=>f());runtime.destroy();controllers.reverse().forEach(c=>c?.destroy?.())},{once:true});
}
