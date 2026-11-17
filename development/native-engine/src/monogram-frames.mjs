// Independent browser adapter for ATREZZO-owned monogram frames.
import {createFramePlayer} from "./frame-player.mjs";
export function mountMonogramFrames(image,{baseURL,frameURLs,onFrame=()=>{},onError=()=>{}}={}){
 if(!image||(!baseURL&&!frameURLs))throw TypeError("image and frame source required");
 if(frameURLs&&(!Array.isArray(frameURLs)||frameURLs.length!==371))throw TypeError("371 frame URLs required");
 const urls=frameURLs??Array.from({length:371},(_,i)=>new URL("frame_"+String(i+1).padStart(4,"0")+".svg",baseURL).href);
 const fallback=urls[0];let reduced=false,dead=false,player=null,progress=0;
 const load=(url,{signal})=>new Promise((resolve,reject)=>{
  const asset=new Image();let done=false;
  const finish=(error)=>{if(done)return;done=true;signal.removeEventListener("abort",abort);asset.onload=null;asset.onerror=null;error?reject(error):resolve(asset)};
  const abort=()=>{asset.removeAttribute("src");finish(new DOMException("Aborted","AbortError"))};
  if(signal.aborted){abort();return}
  signal.addEventListener("abort",abort,{once:true});
  asset.onerror=()=>finish(Error("Could not load monogram frame"));
  asset.onload=()=>{if(asset.decode)asset.decode().then(()=>finish(),finish);else finish()};
  asset.src=url;
 });
 const start=()=>{if(!player&&!reduced&&!dead){player=createFramePlayer({frames:urls,load,present:(asset,index)=>{image.src=asset.src;onFrame(index)},release:asset=>asset.removeAttribute("src"),onError,maxConcurrent:4,cacheSize:24,prefetch:4});player.setProgress(progress)}};
 image.src=fallback;start();
 return {
  setProgress(value){if(dead)return;if(!Number.isFinite(value))throw TypeError("Invalid progress");progress=Math.max(0,Math.min(1,value));player?.setProgress(progress)},
  setReducedMotion(value){if(dead||reduced===Boolean(value))return;reduced=Boolean(value);if(reduced){player?.destroy();player=null;image.src=fallback}else start()},
  get state(){return player?.state??{disposed:dead,displayed:0}},
  destroy(){if(dead)return;dead=true;player?.destroy();player=null;image.src=fallback}
 };
}
