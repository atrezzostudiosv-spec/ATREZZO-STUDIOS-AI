import {chromium,webkit} from "playwright";
import assert from "node:assert/strict";
import {createServer} from "node:http";
import {readFile,stat} from "node:fs/promises";
import {resolve,extname,sep} from "node:path";
const root=resolve(process.argv[2]),prefix=process.argv[3].replace(/\/$/,"")+"/";
const mime={".html":"text/html; charset=utf-8",".js":"text/javascript; charset=utf-8",".css":"text/css; charset=utf-8",".svg":"image/svg+xml",".webp":"image/webp",".txt":"text/plain"};
const server=createServer(async(req,res)=>{try{const path=new URL(req.url,"http://localhost").pathname;if(!path.startsWith(prefix)){res.writeHead(404).end();return}let p=resolve(root,decodeURIComponent(path.slice(prefix.length)));if(p!==root&&!p.startsWith(root+sep)){res.writeHead(403).end();return}if((await stat(p)).isDirectory())p=resolve(p,"index.html");res.writeHead(200,{"content-type":mime[extname(p)]||"application/octet-stream","cache-control":"no-cache"});res.end(await readFile(p))}catch{res.writeHead(404).end()}});
await new Promise(r=>server.listen(0,"127.0.0.1",r));const base=process.env.ATREZZO_ONLINE_BASE||"http://127.0.0.1:"+server.address().port+prefix;
const results=[];
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
 assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);assert.deepEqual(external,[]);
 assert.deepEqual(consoleErrors,[]);
 results.push({name,lang,width,hero:initial.hero,work:initial.work,service:initial.service,frame});
 console.log("PASS",JSON.stringify({name,lang,width,hero:initial.hero,work:initial.work,service:initial.service,frame:[frame.w,frame.h]}));
 }catch(e){console.error("FAIL",name,lang,width,JSON.stringify({errors,failed,external,consoleErrors,status:await page.locator("#preview-state").textContent().catch(()=>null),dom:await page.evaluate(()=>({canvas:[...document.querySelectorAll("canvas")].map(c=>[c.id,c.width,c.height]),work:!!document.querySelector("#work-section"),text:document.body.innerText.slice(0,1000)})).catch(()=>null)}));throw e}
 finally{await page.close()}
 }
 const reduced=await browser.newPage({viewport:{width:375,height:900},reducedMotion:"reduce"});
 try{await reduced.goto(base+"en/");await reduced.waitForFunction(()=>document.querySelector("#preview-state")?.textContent.includes("Reduced motion"));assert(await reduced.locator("h1").isVisible());assert(await reduced.locator("#atz-work-fallback").isVisible());assert(await reduced.locator("#atz-offers").isVisible())}finally{await reduced.close()}
 const nojs=await browser.newPage({viewport:{width:375,height:900},javaScriptEnabled:false});
 try{await nojs.goto(base+"en/");assert(await nojs.locator("h1").isVisible());assert(await nojs.locator(".atz-nav-fallback").isVisible());assert(await nojs.locator("#atz-offers").isVisible())}finally{await nojs.close()}
 }finally{await browser.close()}
}
console.log("Original V06 integration gate passed",results.length);
}finally{await new Promise(r=>server.close(r))}
