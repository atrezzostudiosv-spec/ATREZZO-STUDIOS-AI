import test from "node:test";
import {createMotionRuntime} from "../src/motion-runtime.mjs";
import {createFramePlayer} from "../src/frame-player.mjs";
function assert(x,m){if(!x)throw Error(m)}
async function verify(runtime,playerFactory){
  const events=()=>{const e=new Map();return{addEventListener:(k,f)=>e.set(k,f),removeEventListener:k=>e.delete(k),emit:k=>e.get(k)?.(),count:()=>e.size}};
  const doc={...events(),hidden:false},media={...events(),matches:false};const ticks=new Set();let draws=0,updates=0,removed=0,disposed=0,observer,listener,errors=0;
  class IO{constructor(cb){this.cb=cb;observer=this}observe(){}unobserve(){}disconnect(){}set(target,isIntersecting){this.cb([{target,isIntersecting}])}}
  class Lenis{constructor(o){assert(o.autoRaf===false&&o.syncTouch===false,"single clock/native touch")}on(_,f){listener=f;return()=>{listener=null}}raf(t){assert(Number.isFinite(t),"time")}destroy(){removed++}}
  const r=runtime({gsap:{ticker:{add:f=>ticks.add(f),remove:f=>ticks.delete(f)},registerPlugin(){}},ScrollTrigger:{update:()=>updates++,refresh(){}},Lenis,document:doc,mediaQuery:media,Observer:IO,onError:()=>errors++});
  const e={};const stop=r.register(e,{render:()=>draws++,dispose:()=>disposed++});const tick=t=>{for(const f of ticks)f(t)};
  r.start();r.start();assert(ticks.size===1,"single ticker");tick(0);assert(draws===0,"offscreen");observer.set(e,true);tick(1);assert(draws===1,"visible");listener();assert(updates===1,"scroll sync");doc.hidden=true;doc.emit("visibilitychange");tick(2);assert(draws===1,"hidden");doc.hidden=false;doc.emit("visibilitychange");media.matches=true;media.emit("change");tick(3);assert(draws===1&&removed===1,"reduced");media.matches=false;media.emit("change");tick(4);assert(draws===2,"resume");let bad={};r.register(bad,{render(){throw Error("expected")}});observer.set(bad,true);tick(5);tick(6);assert(errors===1,"isolate error");stop();stop();r.destroy();r.destroy();assert(ticks.size===0&&disposed===1&&removed===2&&doc.count()===0&&media.count()===0,"cleanup");
  const tasks=[],shown=[],released=[];
  const factory=()=>{let signal={aborted:false};return{signal,abort(){signal.aborted=true}}};
  const p=playerFactory({frames:Array.from({length:371},(_,i)=>String(i)),load:(url,{index,signal})=>new Promise(resolve=>tasks.push({index,signal,resolve})),present:(_,index)=>shown.push(index),release:x=>released.push(x),createController:factory,maxConcurrent:2,cacheSize:2,prefetch:0});
  const flush=async()=>{for(let i=0;i<14;i++)await Promise.resolve()};
  p.setProgress(0);await flush();p.setProgress(1);await flush();assert(tasks[0].index===0&&tasks[1].index===370,"endpoints");tasks[1].resolve("last");await flush();tasks[0].resolve("first");await flush();assert(shown.join(",")==="370","stale guard");p.setProgress(0);assert(shown.join(",")==="370,0","reverse");p.setProgress(.5);await flush();tasks[2].resolve("middle");await flush();assert(shown.at(-1)===185&&p.state.cached<=2,"midpoint/cache");p.setProgress(.25);await flush();p.destroy();assert(tasks[3].signal.aborted,"abort");tasks[3].resolve("late");await flush();assert(released.includes("late")&&p.state.cached===0&&shown.at(-1)===185,"late disposal");
  const requests=[];const q=playerFactory({frames:["0","1","2","3","4"],load:async(_,o)=>{requests.push(o.index);return o.index},present(){},createController:factory,cacheSize:2,prefetch:20});q.setProgress(.5);await flush();assert(requests.length===1&&q.state.pending===0,"bounded prefetch no reload loop");q.destroy();
}
test("native lifecycle and frame playback",()=>verify(createMotionRuntime,createFramePlayer));
