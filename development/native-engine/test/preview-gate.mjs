import assert from "node:assert/strict";
import {chromium,webkit} from "playwright";
import {createServer} from "node:http";
import {readFile,stat} from "node:fs/promises";
import {resolve,extname,sep} from "node:path";
const root=resolve(process.argv[2]),prefix="/ATREZZO-STUDIOS-AI/public/preview/v06-native/";
const mime={".html":"text/html; charset=utf-8",".js":"text/javascript; charset=utf-8",".css":"text/css; charset=utf-8",".svg":"image/svg+xml",".webp":"image/webp",".txt":"text/plain; charset=utf-8"};
const server=createServer(async(req,res)=>{try{
 const path=new URL(req.url,"http://localhost").pathname;
 if(!path.startsWith(prefix)){res.writeHead(404).end();return}
 let p=resolve(root,decodeURIComponent(path.slice(prefix.length)));
 if(p!==root&&!p.startsWith(root+sep)){res.writeHead(403).end();return}
 if((await stat(p)).isDirectory())p=resolve(p,"index.html");
 res.writeHead(200,{"content-type":mime[extname(p)]||"application/octet-stream","cache-control":"no-cache"});res.end(await readFile(p));
}catch{res.writeHead(404).end()}});
await new Promise(r=>server.listen(0,"127.0.0.1",r));const base="http://127.0.0.1:"+server.address().port+prefix;
const results=[];
try{
 for(const [name,engine] of [["chromium",chromium],["webkit",webkit]]){
  const browser=await engine.launch(name==="chromium"?{args:["--use-angle=swiftshader","--enable-unsafe-swiftshader"]}:{});
  try{
   for(const lang of ["en","es"])for(const width of [375,768,1024,1440]){
    const page=await browser.newPage({viewport:{width,height:900},reducedMotion:"no-preference"});
    const errors=[],failed=[],external=[];
    page.on("pageerror",e=>errors.push(String(e)));
    page.on("response",r=>{if(r.status()>=400)failed.push(r.status()+" "+r.url())});
    page.on("requestfailed",r=>{if(!r.failure()?.errorText?.includes("ABORTED"))failed.push(r.url()+" "+r.failure()?.errorText)});
    page.on("request",r=>{if(!r.url().startsWith(base)&&!r.url().startsWith("data:")&&!r.url().startsWith("blob:"))external.push(r.url())});
    try{
     await page.goto(base+lang+"/");await page.waitForFunction(()=>window.ATREZZO_NATIVE?.ready);
     assert.equal(await page.locator("html").getAttribute("lang"),lang);
     assert.equal(await page.locator('meta[name="robots"]').getAttribute("content"),"noindex,nofollow");
     assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true,"Initial horizontal overflow");
     assert.equal(await page.locator("h1").count(),1);
     assert.equal(await page.locator(".native-panel").count(),6);
     assert.equal(await page.locator("#work").count(),1);
     assert.equal(await page.locator("#contact").count(),1);
     assert.equal(await page.locator(".language").getAttribute("href"),lang==="en"?"../es/":"../en/");
     const initial=await page.evaluate(()=>ATREZZO_NATIVE);
     if(name==="chromium")assert(initial.hero&&initial.particles,"Chromium software WebGL must mount both scenes");
     const menu=page.locator("[data-azn1-menu-trigger]");
     await menu.click();await page.waitForFunction(()=>document.querySelector("[data-azn1-menu-trigger]").getAttribute("aria-expanded")==="true");
     await page.keyboard.press("Escape");await page.waitForFunction(()=>document.querySelector("[data-azn1-menu-trigger]").getAttribute("aria-expanded")==="false");
     await page.waitForTimeout(850);
     const bounds=await page.locator(".native-bridge").evaluate(el=>({top:el.getBoundingClientRect().top+scrollY,height:el.offsetHeight,pinned:el.classList.contains("native-pinned")}));
     const forward=bounds.pinned?bounds.top+900*5.6:bounds.top+bounds.height*.55;
     await page.evaluate(y=>window.scrollTo(0,y),forward);
     await page.waitForFunction(()=>ATREZZO_NATIVE.frame>120);
     const high=await page.evaluate(()=>ATREZZO_NATIVE.frame);
     const reverse=bounds.pinned?bounds.top+900*1.2:bounds.top-500;
     await page.evaluate(y=>window.scrollTo(0,y),reverse);
     await page.waitForFunction(n=>ATREZZO_NATIVE.frame<n-30,high);
     await page.waitForFunction(()=>{const img=document.querySelector("#native-monogram");return img.complete&&img.naturalWidth>0&&img.currentSrc.endsWith("/frame_"+String(ATREZZO_NATIVE.frame+1).padStart(4,"0")+".svg")});
     const low=await page.evaluate(()=>ATREZZO_NATIVE.frame);
     await page.emulateMedia({reducedMotion:"reduce"});
     await page.waitForFunction(()=>!document.querySelector(".native-bridge").classList.contains("native-pinned")&&document.querySelector("#native-monogram").src.endsWith("frame_0001.svg"));
     assert.equal(await page.locator(".native-panel[aria-hidden=true]").count(),0);
     assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true,"Reduced-motion overflow");
     const state=await page.evaluate(()=>ATREZZO_NATIVE);
     assert.deepEqual(state.errors,[]);assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);assert.deepEqual(external,[]);
     results.push({name,lang,width,hero:state.hero,particles:state.particles,forward:high,reverse:low,reduced:true});
     console.log("PASS",JSON.stringify(results.at(-1)));
    }catch(e){console.error("PREVIEW FAILURE",name,lang,width,JSON.stringify({errors,failed,external,state:await page.evaluate(()=>window.ATREZZO_NATIVE).catch(()=>null)}));throw e}
    finally{await page.close()}
   }
   const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:375,height:900}});
   try{await nojs.goto(base+"en/");assert(await nojs.locator("h1").isVisible());assert(await nojs.locator(".atz-nav-fallback").isVisible());assert.equal(await nojs.locator(".native-panel").count(),6);assert(await nojs.locator("#native-monogram").evaluate(async img=>{await img.decode();return img.naturalWidth>0}))}finally{await nojs.close()}
  }finally{await browser.close()}
 }
 console.log("Preview gate passed",JSON.stringify(results));
}finally{await new Promise(r=>server.close(r))}
