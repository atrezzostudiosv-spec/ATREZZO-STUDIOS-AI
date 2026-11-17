import {build} from "esbuild";
import {resolve} from "node:path";
import {readFile,writeFile,readdir} from "node:fs/promises";
const output=resolve(process.argv[2]);
const ids=[["navegacion","ATZ-NAV-001"],["microinteractions","ATZ-MIC-003"],["motion","ATZ-MOT-002"],["motion","ATZ-MOT-003"],["motion","ATZ-MOT-006"]];
const imports=ids.map(([cat,id],i)=>"import {mount as m"+i+"} from "+JSON.stringify(resolve(output,"components",cat,id+".js"))+";");
const entry=imports.join("\n")+"\nimport {initPreview} from './preview-entry.mjs';\ninitPreview(["+ids.map(([,id],i)=>"["+JSON.stringify(id)+",m"+i+"]").join(",")+"]);";
await build({stdin:{contents:entry,resolveDir:process.cwd(),sourcefile:"native-preview-entry.mjs"},bundle:true,format:"esm",minify:true,legalComments:"eof",target:["es2020"],outfile:resolve(output,"native-preview.js")});
let licenses="ATREZZO V06 native migration candidate. No captured proprietary runtime.\n";
for(const pkg of ["three","lenis","gsap"]){
 const dir=resolve("node_modules",pkg),files=await readdir(dir);const meta=JSON.parse(await readFile(resolve(dir,"package.json"),"utf8"));
 licenses+="\n"+pkg+" "+meta.version+" | "+(meta.license||"See official package license")+"\n";
 for(const f of files.filter(x=>/^licen[cs]e(\.|$)/i.test(x)))licenses+=await readFile(resolve(dir,f),"utf8")+"\n";
}
licenses+="\nGSAP Standard License: https://gsap.com/standard-license/\nThree: https://github.com/mrdoob/three.js/blob/dev/LICENSE\nLenis: https://github.com/darkroomengineering/lenis/blob/main/LICENSE\n";
await writeFile(resolve(output,"THIRD-PARTY-NOTICES.txt"),licenses);
console.log("Independent preview bundle generated");
