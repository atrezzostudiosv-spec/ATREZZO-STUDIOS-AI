import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {createServer} from "node:http";
import {readFile,writeFile,mkdir} from "node:fs/promises";
import {resolve,extname} from "node:path";
import {chromium} from "playwright";
const root=resolve("public"),lab="lab/floating-portfolio",origin="http://127.0.0.1:8780",url=origin+"/"+lab+"/";
const headers=await readFile(root+"/_headers","utf8");
const strict=headers.match(/Content-Security-Policy: ([^\n]+)/)[1], relaxed=headers.match(/\/lab\/floating-portfolio\/\*\n  Content-Security-Policy: ([^\n]+)/)[1];
assert.match(strict,/script-src 'none'/);assert.match(relaxed,/script-src 'self' https:\/\/cdn\.jsdelivr\.net/);
const hash=buf=>createHash("sha256").update(buf).digest("hex");
const original=await readFile("vendor/ATZ-SEC-012/engine.original.js","utf8");
const engine=await readFile(root+"/"+lab+"/engine.original.js","utf8");
assert.equal(engine,original);
assert.equal(hash(engine.split("/* BEGIN EXACT ORIGINAL FLOATING CORE */\n")[1].split("\n/* END EXACT ORIGINAL FLOATING CORE */")[0]),"01dff3c3ccbc869cc444ab4d6d72f1209b2cead0cdefb4789ed9f1b0b91659fd");
const manifest=JSON.parse(await readFile("vendor/ATZ-SEC-012/manifest.json","utf8"));
for(const file of manifest.files)await readFile("vendor/ATZ-SEC-012/"+file);
const images=JSON.parse(await readFile(root+"/"+lab+"/images.json","utf8"));assert.equal(images.length,21);assert.equal(new Set(images).size,21);
const mime={".html":"text/html; charset=utf-8",".js":"text/javascript; charset=utf-8",".css":"text/css; charset=utf-8",".json":"application/json",".svg":"image/svg+xml",".webp":"image/webp",".ico":"image/x-icon"};
const server=createServer(async(req,res)=>{try{const path=new URL(req.url,origin).pathname;const rel=path.endsWith("/")?path+"index.html":path;const file=resolve(root,"."+rel);if(!file.startsWith(root+"/")){res.writeHead(403).end();return}const buf=await readFile(file);res.writeHead(200,{"Content-Type":mime[extname(file)]||"application/octet-stream","Content-Security-Policy":path.startsWith("/lab/")?relaxed:strict,"X-Robots-Tag":"noindex, nofollow","X-Content-Type-Options":"nosniff"}).end(buf)}catch{res.writeHead(404).end()}});
await new Promise(r=>server.listen(8780,"127.0.0.1",r));
const output="qa-floating-portfolio";await mkdir(output,{recursive:true});let browser;const results=[];
const setup=async page=>{await page.route("https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/**",route=>route.fulfill({path:resolve("node_modules/gsap/dist",new URL(route.request().url()).pathname.split("/").at(-1)),contentType:"application/javascript"}))};
const measure=()=>[...document.querySelectorAll(".ft")].map(e=>({transform:e.style.transform,opacity:Number(e.style.opacity)}));
try{
 browser=await chromium.launch({headless:true});
 for(const width of [1440,1024,768,375]){
 const page=await browser.newPage({viewport:{width,height:width===375?812:900},hasTouch:width===375,isMobile:width===375});
 await setup(page);const errors=[];page.on("pageerror",e=>errors.push(e.message));page.on("console",m=>{if(m.type()==="error")errors.push(m.text())});
 await page.goto(url);await page.waitForFunction(()=>Boolean(document.documentElement.dataset.lab));assert.equal(await page.locator("html").getAttribute("data-lab"),"ready",await page.locator("#lab-error").textContent());
 assert.equal(await page.locator(".ft").count(),21);assert.equal(await page.locator("#t1,#t2,#t3").count(),3);assert.equal(await page.locator("svg image").count(),3);
 assert(await page.evaluate(()=>[...document.querySelectorAll(".ft img")].every(i=>i.complete&&i.naturalWidth>0)));
 await page.waitForTimeout(2400);const before=await page.evaluate(measure);await page.waitForTimeout(400);const after=await page.evaluate(measure);assert(after.some((e,i)=>e.transform!==before[i].transform));assert(Math.max(...after.map(e=>e.opacity))>.5);
 if(width>768){await page.mouse.move(width*.15,150);await page.waitForTimeout(350);const t=await page.locator("#logo-circle").evaluate(e=>e.style.transform);await page.mouse.move(width*.85,650);await page.waitForTimeout(350);assert.notEqual(await page.locator("#logo-circle").evaluate(e=>e.style.transform),t)}
 await page.screenshot({path:output+"/"+width+"-initial.png"});
 await page.evaluate(()=>scrollTo(0,innerHeight*.55));await page.waitForTimeout(1300);const mid=await page.evaluate(()=>window.__TRIONN_FLOATING__.progress);assert(mid>.35&&mid<.75);
 await page.evaluate(()=>scrollTo(0,innerHeight));await page.waitForTimeout(1800);assert(await page.evaluate(()=>window.__TRIONN_FLOATING__.progress)>.98);assert(Math.max(...(await page.evaluate(measure)).map(e=>e.opacity))<.03);
 await page.screenshot({path:output+"/"+width+"-converged.png"});
 await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(1800);assert(await page.evaluate(()=>window.__TRIONN_FLOATING__.progress)<.02);assert(Math.max(...(await page.evaluate(measure)).map(e=>e.opacity))>.1);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));assert.deepEqual(errors,[]);
 await page.locator("#motion-toggle").click();assert.equal(await page.locator("html").getAttribute("data-lab"),"static");await page.screenshot({path:output+"/"+width+"-paused.png"});results.push({width,mid,reverse:true,pause:true,images:21});await page.close();
 }
 const reduced=await browser.newPage({viewport:{width:375,height:812},reducedMotion:"reduce"});await setup(reduced);await reduced.goto(url);await reduced.waitForFunction(()=>document.documentElement.dataset.lab==="static");assert.equal(await reduced.locator(".ft").count(),21);assert.equal(await reduced.locator("#motion-toggle").isVisible(),false);await reduced.screenshot({path:output+"/reduced.png"});await reduced.close();
 const nojs=await browser.newPage({viewport:{width:375,height:812},javaScriptEnabled:false});await nojs.goto(url);assert(await nojs.locator("h1").isVisible());assert(await nojs.locator("#logo-circle").isVisible());await nojs.close();
 const homepage=await browser.newPage();await homepage.goto(origin+"/");assert.equal(await homepage.locator(".copy h1").innerText(),"COMING SOON");assert.equal(await homepage.locator("#page-header-pin").count(),0);await homepage.close();
 await writeFile(output+"/report.json",JSON.stringify({passed:true,results,reducedMotion:true,nojs:true,enginePreserved:true,rootUnchanged:true},null,2));console.log(JSON.stringify({passed:true,results}));
}finally{await browser?.close();server.close();}
