// Independent ATREZZO orchestration; no captured application code.
export function createMotionRuntime({gsap,ScrollTrigger,Lenis,document,mediaQuery,Observer,onError=error=>console.error(error)}){
  const scenes=new Map();let started=false,dead=false,lenis=null,offScroll=null,last=null;
  const active=s=>started&&!dead&&!document.hidden&&!mediaQuery.matches&&s.visible&&!s.failed;
  function notify(s){const next=active(s);if(s.active!==next){s.active=next;(next?s.resume:s.pause)?.()}}
  const observer=Observer?new Observer(entries=>{for(const e of entries){const s=scenes.get(e.target);if(s){s.visible=e.isIntersecting;notify(s)}}}):null;
  function disconnect(){offScroll?.();offScroll=null;lenis?.destroy();lenis=null}
  function connect(){
    disconnect();
    if(started&&!mediaQuery.matches&&Lenis){
      lenis=new Lenis({autoRaf:false,smoothWheel:true,syncTouch:false});
      const handler=()=>ScrollTrigger.update();
      const off=lenis.on("scroll",handler);
      offScroll=typeof off==="function"?off:()=>lenis?.off("scroll",handler);
    }
  }
  function tick(time){if(!started||dead||document.hidden){last=null;return}
    const delta=last===null?0:Math.min(.1,Math.max(0,time-last));last=time;
    lenis?.raf(time*1000);
    for(const s of scenes.values())if(active(s)){try{s.render({time,delta})}catch(error){s.failed=true;notify(s);onError(error,s.element)}}
  }
  function visibility(){last=null;for(const s of scenes.values())notify(s)}
  function motion(){last=null;connect();for(const s of scenes.values()){s.static?.(mediaQuery.matches);notify(s)}ScrollTrigger.refresh()}
  return {
    start(){if(dead)throw Error("Disposed");if(started)return;started=true;gsap.registerPlugin(ScrollTrigger);document.addEventListener("visibilitychange",visibility);mediaQuery.addEventListener("change",motion);connect();gsap.ticker.add(tick);for(const s of scenes.values()){s.static?.(mediaQuery.matches);notify(s)}},
    register(element,callbacks){if(dead||!element||typeof callbacks.render!=="function"||scenes.has(element))throw Error("Invalid or duplicate scene");const s={...callbacks,element,visible:!observer,active:false,failed:false};scenes.set(element,s);observer?.observe(element);if(started){s.static?.(mediaQuery.matches);notify(s)}return()=>{if(!scenes.has(element))return;if(s.active)s.pause?.();observer?.unobserve(element);scenes.delete(element);s.dispose?.()}},
    destroy(){if(dead)return;dead=true;started=false;gsap.ticker.remove(tick);document.removeEventListener("visibilitychange",visibility);mediaQuery.removeEventListener("change",motion);disconnect();observer?.disconnect();for(const s of scenes.values()){if(s.active)s.pause?.();s.dispose?.()}scenes.clear();last=null}
  }
}
