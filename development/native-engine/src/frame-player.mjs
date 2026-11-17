// Independent generic frame playback; no captured application code.
export function createFramePlayer({frames,load,present,release=()=>{},onError=()=>{},createController=()=>new AbortController(),maxConcurrent=4,cacheSize=24,prefetch=3}){
  if(!Array.isArray(frames)||!frames.length||typeof load!=="function"||typeof present!=="function")throw TypeError("Invalid frames");
  if(!Number.isInteger(maxConcurrent)||maxConcurrent<1||!Number.isInteger(cacheSize)||cacheSize<2||!Number.isInteger(prefetch)||prefetch<0)throw RangeError("Invalid limits");
  let desired=0,displayed=-1,dead=false;const cache=new Map(),pending=new Map(),failed=new Set();
  function priorities(){const p=[desired];for(let i=1;i<=prefetch;i++){if(desired+i<frames.length)p.push(desired+i);if(desired-i>=0)p.push(desired-i)}return p.slice(0,cacheSize-1)}
  function show(index){if(dead||index!==desired||index===displayed||!cache.has(index))return;const asset=cache.get(index);present(asset,index);displayed=index;cache.delete(index);cache.set(index,asset)}
  function trim(){const keep=new Set([...priorities(),displayed]);for(const [index,asset] of cache)if(cache.size>cacheSize&&!keep.has(index)){cache.delete(index);release(asset)}}
  function pump(){
    if(dead)return;
    for(const index of priorities()){
      if(pending.size>=maxConcurrent)break;if(cache.has(index)||pending.has(index)||failed.has(index))continue;
      const controller=createController();pending.set(index,controller);
      Promise.resolve().then(()=>load(frames[index],{signal:controller.signal,index})).then(asset=>{
        if(dead||controller.signal.aborted){release(asset);return}
        cache.set(index,asset);show(index);
      }).catch(error=>{if(!dead&&!controller.signal.aborted){failed.add(index);onError(error,index)}}).finally(()=>{pending.delete(index);if(!dead){trim();pump()}});
    }
  }
  return {setProgress(value){if(dead)return;if(!Number.isFinite(value))throw TypeError("Invalid progress");desired=Math.round(Math.max(0,Math.min(1,value))*(frames.length-1));show(desired);trim();pump()},retry(){if(!dead){failed.delete(desired);pump()}},get state(){return {desired,displayed,cached:cache.size,pending:pending.size,disposed:dead}},destroy(){if(dead)return;dead=true;for(const c of pending.values())c.abort();pending.clear();for(const asset of cache.values())release(asset);cache.clear();failed.clear()}};
}
