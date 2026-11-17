"""Private extraction adapter for TRIONN Name Story (84066).
The two point-cloud constructors, shaders, camera interpolation and rotation
are resolved at build time from the user's pinned archive, not distributed.
No planets, nebula planes, brand-story text, audio or third-party images.
"""
import hashlib
BLOB='85d52e56041ccf852c742b281f2496c22c7d045f'
def blob(s):
    b=s.encode();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def module(source):
    if blob(source)!=BLOB:raise ValueError('Name Story source mismatch')
    # Original 4,000 stars and 8,000 ring particles, exact shader source.
    a=source.index('let w=new Float32Array(12e3)');b=source.index('let k=[];',a)
    points=source[a:b]
    # Only color data changes; original positions, point sizes, GLSL, counts stay intact.
    points=points.replace('M[3*e]=n?1:.8+.2*Math.random(),M[3*e+1]=n?.9:.85+.15*Math.random(),M[3*e+2]=n?.6:1','M[3*e]=n?.72:.48+.2*Math.random(),M[3*e+1]=n?.57:.49+.15*Math.random(),M[3*e+2]=n?.94:1')
    points=points.replace('N[3*e]=i?.9*n:.4*n,N[3*e+1]=i?.7*n:.5*n,N[3*e+2]=i?.4*n:.9*n','N[3*e]=i?.65*n:.25*n,N[3*e+1]=i?.38*n:.36*n,N[3*e+2]=i?.95*n:.9*n')
    # Exact camera keyframes, pointer interpolation, easing and rotation.
    a=source.index('let E=[{pos:');b=source.index(',j=0,A=0',a);cameras=source[a:b]+';'
    a=source.index('let i=Math.max(1,document.documentElement.scrollHeight');b=source.index(',y.forEach',a)
    motion=source[a:b].replace('let i=Math.max(1,document.documentElement.scrollHeight-window.innerHeight),r=Math.min(A/i,1)','let i=1,r=Math.min(A/i,1)')+';'
    # Integrate on the existing shared CanvasManager, local normalized H03 progress.
    # Clock advances while visible, including when scroll stops; original rotation and twinkle.
    return '''(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push([document.currentScript,999003,e=>{
const React=e.i(71645),s=e.i(32009),{getCanvasManager}=e.i(71871);
function Galaxy({scrollProgressRef}){const ref=React.useRef(null);React.useEffect(()=>{
 const canvas=ref.current;if(!canvas)return;let t,o,n,manager,handle,observer,resize,move,disposed=false;
 try{t=new s.WebGLRenderer({canvas,antialias:!0,alpha:!0,powerPreference:"high-performance"});t.setClearColor(0x090812,0);t.toneMapping=s.ACESFilmicToneMapping;t.toneMappingExposure=1.2;
 o=new s.Scene;n=new s.PerspectiveCamera(55,innerWidth/innerHeight,.1,600);n.position.set(0,45,75);n.lookAt(0,0,0);
 const size=()=>{let w=canvas.parentElement.clientWidth,h=canvas.parentElement.clientHeight;if(!w||!h)return;t.setPixelRatio(Math.min(devicePixelRatio||1,w<768?1:1.5));t.setSize(w,h,false);n.aspect=w/h;n.updateProjectionMatrix()};size();resize=new ResizeObserver(size);resize.observe(canvas.parentElement);
 '''+points+cameras+'''
 let j=0,A=0,z=.5,_=.5;move=e=>{z=e.clientX/window.innerWidth,_=1-e.clientY/window.innerHeight};window.addEventListener("mousemove",move,{passive:true});
 let F=new s.Vector3(0,45,75),L=new s.Vector3,q=e=>e*e*(3-2*e),V=Date.now();
 manager=getCanvasManager();handle=manager.register(()=>{if(disposed)return;let a=(Date.now()-V)/1e3;let mobile=innerWidth<768,before=200+(mobile?60:150),duration=mobile?600:800,total=before+duration+200;
 j=Math.max(0,Math.min(1,((scrollProgressRef.current||0)*total-before)/duration));A+=(j-A)*.055;
 '''+motion+'''
 o.children.filter(e=>e.isPoints).forEach(e=>{let t=e.material;t?.uniforms?.uTime&&(t.uniforms.uTime.value=a)});t.render(o,n);canvas.dataset.rendered="true";
 },false);observer=new IntersectionObserver(([entry])=>manager.setActive(handle,entry.isIntersecting),{rootMargin:"0px",threshold:0});observer.observe(canvas);
 }catch(error){console.warn("H03 particle field unavailable",error);canvas.hidden=true;}
 return()=>{disposed=true;observer?.disconnect();resize?.disconnect();if(move)window.removeEventListener("mousemove",move);if(manager&&handle!=null)manager.unregister(handle);o?.traverse(e=>{e.geometry?.dispose();e.material?.dispose()});t?.dispose();};
 },[scrollProgressRef]);return React.createElement("canvas",{ref,className:"atz-galaxy", "aria-hidden":true});}
e.s(["default",0,Galaxy]);}]);'''
