// Browser gate for the independent foundation only, not a Home V06 preview.
import assert from "node:assert/strict";
import {build} from "esbuild";
import {chromium,webkit} from "playwright";
import {createServer} from "node:http";
import {mkdir,writeFile,readFile,rm} from "node:fs/promises";
import {resolve} from "node:path";
const out=resolve(".browser-gate");
await mkdir(out,{recursive:true});
const entry=`
import {createBrowserRuntime,gsap,ScrollTrigger,THREE} from "./src/official.mjs";
import {createFramePlayer} from "./src/frame-player.mjs";
const root=document.querySelector("#scene");
const state=window.gate={frames:[],draws:0,progress:0,webgl:false,static:false,errors:[]};
const runtime=createBrowserRuntime({onError:e=>state.errors.push(String(e))});
const player=createFramePlayer({frames:Array.from({length:371},(_,i)=>i),load:async n=>n,present:(_,i)=>{state.frames.push(i);document.querySelector("#frame").textContent=i}});
let renderer,scene,camera,mesh,geometry,material;
try {
 renderer=new THREE.WebGLRenderer({canvas:document.querySelector("canvas"),antialias:false});
 renderer.setSize(64,64,false);scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(45,1,.1,10);camera.position.z=3;
 geometry=new THREE.BoxGeometry(1,1,1);material=new THREE.MeshBasicMaterial({color:0x7555ff});mesh=new THREE.Mesh(geometry,material);scene.add(mesh);
 renderer.render(scene,camera);state.webgl=renderer.getContext().getError()===0;
} catch(e){state.webglError=String(e)}
runtime.register(root,{render:({delta})=>{state.draws++;if(renderer&&mesh){mesh.rotation.y+=delta;renderer.render(scene,camera)}},static:flag=>{state.static=flag;if(flag)document.querySelector("#frame").textContent="Static fallback"},dispose:()=>{geometry?.dispose();material?.dispose();renderer?.dispose()}});
runtime.start();
const mm=gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)",()=>{const trigger=ScrollTrigger.create({trigger:root,start:"top top",end:"+=1000",pin:true,onUpdate:self=>{state.progress=self.progress;player.setProgress(self.progress)}});player.setProgress(0);return()=>trigger.kill()});
window.disposeGate=()=>{mm.revert();player.destroy();runtime.destroy();state.disposed=true};
state.ready=true;
`;
await build({stdin:{contents:entry,resolveDir:process.cwd(),sourcefile:"gate-entry.js"},bundle:true,format:"esm",outfile:resolve(out,"gate.js")});
await writeFile(resolve(out,"index.html"),'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>ATREZZO foundation test only</title><style>body{margin:0;font-family:sans-serif}#scene{height:100vh;display:grid;place-content:center;background:#121019;color:white}canvas{width:64px;height:64px}footer{height:150vh}#frame{min-height:1em}</style><main><section id="scene"><h1>Foundation test</h1><canvas></canvas><p id="frame">Static fallback</p></section><footer>End of test</footer></main><script type="module" src="./gate.js"></script></html>');
const server=createServer(async(req,res)=>{try{const js=req.url==="/gate.js";if(!js&&req.url!=="/"){res.writeHead(404).end();return}res.setHeader("Content-Type",js?"text/javascript":"text/html");res.end(await readFile(resolve(out,js?"gate.js":"index.html")))}catch{res.writeHead(500).end()}});
await new Promise(r=>server.listen(0,"127.0.0.1",r));
const url="http://127.0.0.1:"+server.address().port;
const report=[];
try{
 for(const [name,engine] of [["chromium",chromium],["webkit",webkit]]){
  const browser=await engine.launch(name==="chromium"?{args:["--use-angle=swiftshader","--enable-unsafe-swiftshader"]}:{});
  try{
   for(const width of [375,768,1024,1440]){
    const page=await browser.newPage({viewport:{width,height:900}});
    try{
     const errors=[];page.on("pageerror",e=>errors.push(String(e)));
     await page.goto(url);await page.waitForFunction(()=>window.gate?.ready&&window.gate.draws>0);
     assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
     await page.evaluate(()=>window.scrollTo(0,700));
     await page.waitForFunction(()=>gate.progress>.6&&gate.frames.at(-1)>220);
     const forward=await page.evaluate(()=>gate.frames.at(-1));
     await page.evaluate(()=>window.scrollTo(0,150));
     await page.waitForFunction(()=>gate.progress<.25&&gate.frames.at(-1)<90);
     const reverse=await page.evaluate(()=>gate.frames.at(-1));
     assert(reverse<forward);
     const webgl=await page.evaluate(()=>gate.webgl);
     if(name==="chromium")assert(webgl,"Chromium software WebGL must initialize");
     await page.emulateMedia({reducedMotion:"reduce"});
     await page.waitForFunction(()=>gate.static);
     const draws=await page.evaluate(()=>gate.draws);
     await page.waitForTimeout(250);
     assert.equal(await page.evaluate(()=>gate.draws),draws);
     await page.evaluate(()=>disposeGate());
     assert.equal(await page.evaluate(()=>gate.disposed),true);
     assert.deepEqual(errors,[]);
     assert.deepEqual(await page.evaluate(()=>gate.errors),[]);
     report.push({name,width,forward,reverse,webgl,reducedMotion:true,dispose:true});
    }finally{await page.close()}
   }
   const nojs=await browser.newPage({javaScriptEnabled:false});
   try{await nojs.goto(url);assert.equal(await nojs.locator("#frame").textContent(),"Static fallback")}finally{await nojs.close()}
  }finally{await browser.close()}
 }
 console.log(JSON.stringify(report,null,2));
}finally{await new Promise(r=>server.close(r));await rm(out,{recursive:true,force:true})}
