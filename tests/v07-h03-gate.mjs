import {chromium,webkit} from "playwright";
import assert from "node:assert/strict";
import {createServer} from "node:http";
import {readFile,stat,mkdir} from "node:fs/promises";
import {resolve,extname,sep} from "node:path";
const root=resolve(process.argv[2]),prefix=process.argv[3].replace(/\/$/,"")+"/";
const mime={".html":"text/html; charset=utf-8",".js":"text/javascript; charset=utf-8",".css":"text/css; charset=utf-8",".svg":"image/svg+xml",".webp":"image/webp",".txt":"text/plain"};
const server=createServer(async(req,res)=>{try{const path=new URL(req.url,"http://localhost").pathname;if(!path.startsWith(prefix)){res.writeHead(404).end();return}let p=resolve(root,decodeURIComponent(path.slice(prefix.length)));if(p!==root&&!p.startsWith(root+sep)){res.writeHead(403).end();return}if((await stat(p)).isDirectory())p=resolve(p,"index.html");res.writeHead(200,{"content-type":mime[extname(p)]||"application/octet-stream","cache-control":"no-cache"});res.end(await readFile(p))}catch{res.writeHead(404).end()}});
await new Promise(r=>server.listen(0,"127.0.0.1",r));const base=process.env.ATREZZO_ONLINE_BASE||"http://127.0.0.1:"+server.address().port+prefix;
const results=[];await mkdir("qa-v07",{recursive:true});
try{
for(const [name,engine] of [["chromium",chromium],["webkit",webkit]]){
 const browser=await engine.launch(name==="chromium"?{args:["--use-angle=swiftshader","--enable-unsafe-swiftshader","--disable-dev-shm-usage"]}:{});
 try{
 for(const lang of ["en","es"])for(const width of [375,768,1024,1440]){
 const page=await browser.newPage({viewport:{width,height:900},reducedMotion:"no-preference"});
 const errors=[],failed=[],external=[],consoleErrors=[];
 page.on("pageerror",e=>errors.push(String(e)));
 page.on("console",m=>{if(m.type()==="error")consoleErrors.push(m.text().slice(0,300))});
 page.on("response",r=>{if(r.status()>=400)failed.push(r.status()+" "+r.url())});
 page.on("request",r=>{if(!r.url().startsWith(base)&&!r.url().startsWith("data:")&&!r.url().startsWith("blob:"))external.push(r.url())});
 try{
 await page.goto(base+lang+"/",{waitUntil:"load"});
 await page.waitForFunction(()=>document.querySelector("#preview-state")?.textContent.includes("ORIGINAL MOTION")&&document.querySelector("#atrezzo-symbol-canvas-wrap canvas"),{},{timeout:25000});
 await page.waitForFunction(()=>document.querySelector("#work-section")&&document.querySelector("#atz-service-mount canvas"),{},{timeout:25000});
 await page.waitForTimeout(1800);
 const initial=await page.evaluate(()=>({hero:!!document.querySelector("#atrezzo-symbol-canvas-wrap canvas"),work:!!document.querySelector("#work-section"),service:!!document.querySelector("#atz-service-mount canvas"),state:document.querySelector("#preview-state")?.textContent,overflow:document.documentElement.scrollWidth>innerWidth+2,heading:document.querySelector("h1")?.textContent,copy:document.body.innerText.slice(0,3000)}));
 assert(initial.hero&&initial.work&&initial.service);
 assert(!initial.overflow,"Horizontal overflow at entry");
 assert(!new RegExp(['tri','onn'].join(''),'i').test(initial.copy),"Original studio name in visible page");
 assert.equal(await page.locator("html").getAttribute("lang"),lang);
 const menu=page.locator("[data-azn1-menu-trigger]");await menu.click();await page.waitForFunction(()=>document.querySelector("[data-azn1-menu-trigger]").getAttribute("aria-expanded")==="true");
 await page.keyboard.press("Escape");await page.waitForFunction(()=>document.querySelector("[data-azn1-menu-trigger]").getAttribute("aria-expanded")==="false");
 await page.waitForTimeout(900);
 const service=await page.locator(".atz-service-kinetic").evaluate(el=>({top:el.getBoundingClientRect().top+scrollY,height:el.offsetHeight}));
 await page.evaluate(y=>window.scrollTo(0,y),service.top+900*3);
 await page.waitForTimeout(1800);
 const frame=await page.evaluate(()=>{const c=document.querySelector("#atz-service-mount #c");return {w:c?.width,h:c?.height,scroll:scrollY,text:document.querySelector("#atz-service-mount")?.innerText.slice(0,1500)}});
 assert(frame.w>0&&frame.h>0,"Real original frame canvas missing");
 await page.evaluate(y=>window.scrollTo(0,y),Math.max(0,service.top+900));
 await page.waitForTimeout(1300);
 assert(!new RegExp(['tri','onn'].join(''),'i').test(frame.text||""),"Original studio copy in services");

// H03 handoff: actual WebGL source is still the single original bridge canvas.
// The second canvas must be a live 2D projection, not another WebGL instance.
const gotoScene=async(id)=>{await page.evaluate(id=>{const el=document.getElementById(id);window.scrollTo(0,el.getBoundingClientRect().top+scrollY+8)},id);await page.waitForFunction(id=>{const r=document.getElementById(id).getBoundingClientRect();return Math.abs(r.top)<90},id,{timeout:15000});};
const sample=async()=>page.evaluate(()=>{const c=document.getElementById("atz-v07-field"),src=document.querySelector("#atz-service-mount .atz-galaxy"),temp=document.createElement("canvas");temp.width=temp.height=32;const x=temp.getContext("2d");x.drawImage(c,0,0,32,32);const pixels=x.getImageData(0,0,32,32).data;let energy=0;for(let i=0;i<pixels.length;i+=4)energy+=pixels[i]+pixels[i+1]+pixels[i+2]+pixels[i+3];return {frame:Number(c.dataset.frame||0),rendered:c.dataset.rendered,source:src?.dataset.rendered,energy,blend:Number(getComputedStyle(document.getElementById("atz-offers")).getPropertyValue("--atz-blend")),layers:[...document.querySelectorAll("#express [data-depth],#custom [data-depth]")].map(el=>getComputedStyle(el).transform),overflow:document.documentElement.scrollWidth>innerWidth+2,viewport:document.querySelector(".atz-v07-viewport").getBoundingClientRect().top,sourceCount:document.querySelectorAll("#atz-service-mount .atz-galaxy").length,mirrorIs2D:!!c.getContext("2d")};});
await gotoScene("express");
await page.waitForFunction(()=>document.getElementById("atz-v07-field")?.dataset.rendered==="true",{},{timeout:20000});
await page.waitForTimeout(2300);
const express=await sample();await page.waitForTimeout(650);const express2=await sample();
assert(express.source==="true"&&express.rendered==="true"&&express.energy>0,"No live original particle projection: "+JSON.stringify(express));
assert(express2.frame>express.frame&&express2.layers[0]!==express.layers[0],"No active original frames or foreground motion");
assert(express.sourceCount===1&&express.mirrorIs2D&&express.layers.length===6,"Unexpected renderer or layer count");
assert(express.blend<.3&&!express.overflow,"Express color/layout incorrect: "+JSON.stringify(express));
assert(await page.locator("#express [data-atz-id='ATZ-MOT-008'] .ty-unit").count()>0,"Exact typography missing");
assert(await page.locator("#express .mi-cta").isVisible());
await page.screenshot({path:`qa-v07/${name}-${lang}-${width}-express.png`});
await gotoScene("custom");await page.waitForTimeout(2400);const custom=await sample();
assert(custom.blend>.85&&custom.frame>express2.frame&&custom.energy>0&&!custom.overflow,"Custom handoff failed: "+JSON.stringify(custom));
assert(custom.layers[4]!==express.layers[4],"Custom planes did not update");
assert(await page.locator("#custom [data-atz-id='ATZ-MOT-008'] .ty-unit").count()>0);
assert(await page.locator("#custom .mi-cta").isVisible());
await page.screenshot({path:`qa-v07/${name}-${lang}-${width}-custom.png`});
await gotoScene("express");await page.waitForTimeout(900);const reverse=await sample();
assert(reverse.blend<.3&&reverse.frame>custom.frame&&reverse.energy>0,"Reverse handoff failed: "+JSON.stringify(reverse));
const stack=await page.evaluate(()=>{const a=document.getElementById("express").getBoundingClientRect(),b=document.getElementById("custom").getBoundingClientRect();return b.top>=a.bottom-2});
assert(stack,"Offers are not sequential independent scenes");
console.log("H03 PASS",JSON.stringify({name,lang,width,expressEnergy:express.energy,customEnergy:custom.energy,blend:[express.blend,custom.blend,reverse.blend],layers:express.layers.length}));

 assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);assert.deepEqual(external,[]);
 assert.deepEqual(consoleErrors,[]);
 results.push({name,lang,width,hero:initial.hero,work:initial.work,service:initial.service,frame});
 console.log("PASS",JSON.stringify({name,lang,width,hero:initial.hero,work:initial.work,service:initial.service,frame:[frame.w,frame.h]}));
 }catch(e){console.error("FAIL",name,lang,width,JSON.stringify({errors,failed,external,consoleErrors,status:await page.locator("#preview-state").textContent().catch(()=>null),dom:await page.evaluate(()=>({canvas:[...document.querySelectorAll("canvas")].map(c=>[c.id,c.width,c.height]),work:!!document.querySelector("#work-section"),text:document.body.innerText.slice(0,1000)})).catch(()=>null)}));throw e}
 finally{await page.close()}
 }
 const reduced=await browser.newPage({viewport:{width:375,height:900},reducedMotion:"reduce"});
 try{await reduced.goto(base+"en/");await reduced.waitForFunction(()=>document.querySelector("#preview-state")?.textContent.includes("Reduced motion"));assert(await reduced.locator("h1").isVisible());assert(await reduced.locator("#atz-work-fallback").isVisible());assert(await reduced.locator("#atz-offers").isVisible());assert(await reduced.locator("#express h3").isVisible());assert(await reduced.locator("#custom .mi-cta").isVisible());assert.equal(await reduced.locator("#atz-v07-field").isVisible(),false)}finally{await reduced.close()}
 const nojs=await browser.newPage({viewport:{width:375,height:900},javaScriptEnabled:false});
 try{await nojs.goto(base+"en/");assert(await nojs.locator("h1").isVisible());assert(await nojs.locator(".atz-nav-fallback").isVisible());assert(await nojs.locator("#atz-offers").isVisible());assert(await nojs.locator("#express h3").isVisible());assert(await nojs.locator("#custom .mi-cta").isVisible())}finally{await nojs.close()}
 }finally{await browser.close()}
}
console.log("V07 H03 integration gate passed",results.length);
}finally{await new Promise(r=>server.close(r))}
