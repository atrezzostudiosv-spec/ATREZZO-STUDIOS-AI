"""Own V06 monogram media only. Source e48da05c1cb4a7e65be8ff11652fd2a05058a1bb, service_motion.py write_media: removed two unrelated study images. No captured runtime or third-party resources. Provisional A, not master logo."""
import json, sys, hashlib
from math import sin, cos, pi
from pathlib import Path
BRAND = json.loads("{\"source\":\"ATREZZO-STUDIOS-AI@33bf6d0451ae9532c88d6977ec6d2856bd6cdcf5/public/lab/floating-portfolio/index.html\",\"status\":\"Provisional geometry for private study; not the master logo\",\"paths\":[[[241,163],[331,163],[209,423],[119,423]],[[331,163],[385,278],[323,342],[286,258]],[[385,278],[453,423],[361,423],[323,342]]],\"center\":[286,293],\"scale\":0.0082,\"palette\":{\"ink\":\"#090812\",\"paper\":\"#F5F5FA\",\"electric\":\"#153B9D\",\"violet\":\"#7436F5\",\"luminous\":\"#B967EF\"}}\n")

def write_frames(out,brand,put):
    # Authored abstract study of the approved provisional A, no third-party media.
    paths=brand['paths']
    for i in range(371):
        p=i/370;theta=(-.38+p*.76);w=.62+.38*cos(theta);x=960+150*sin(p*pi*2);y=540+30*sin(p*pi);size=2.7+1.4*sin(p*pi)
        # Approved geometry and pose formulas; refined solid silver/violet faces.
        # Transparent frame: the live WebGL field is rendered behind it.
        dx,dy=11.0*sin(theta),11.0
        faces=[];walls=[]
        for n,path in enumerate(paths):
            d='M'+' L'.join(f'{a} {b}' for a,b in path)+' Z'
            for j,(a,b) in enumerate(path):
                c,d2=path[(j+1)%len(path)]
                walls.append(f'<path d="M{a} {b} L{c} {d2} L{c+dx:.3f} {d2+dy:.3f} L{a+dx:.3f} {b+dy:.3f} Z" fill="url(#edge{j%2})"/>')
            faces.append(f'<path d="{d}" fill="url(#face{n})" stroke="#d5cff7" stroke-width=".28" stroke-linejoin="round"/>')
        svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 1920 1080"><defs>
          <linearGradient id="face0" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#b9c4f0"/><stop offset=".13" stop-color="#747ba8"/><stop offset=".32" stop-color="#34375c"/><stop offset=".54" stop-color="#69658f"/><stop offset=".69" stop-color="#a9a2da"/><stop offset=".85" stop-color="#574579"/><stop offset="1" stop-color="#221b42"/></linearGradient>
          <linearGradient id="face1" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#aaa5e2"/><stop offset=".16" stop-color="#62528f"/><stop offset=".45" stop-color="#2b214e"/><stop offset=".68" stop-color="#7962ba"/><stop offset=".9" stop-color="#453069"/><stop offset="1" stop-color="#1c1737"/></linearGradient>
          <linearGradient id="face2" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#a1b6e8"/><stop offset=".2" stop-color="#58679d"/><stop offset=".47" stop-color="#2d2856"/><stop offset=".76" stop-color="#7762b1"/><stop offset="1" stop-color="#33254f"/></linearGradient>
          <linearGradient id="edge0"><stop stop-color="#25223f"/><stop offset="1" stop-color="#625092"/></linearGradient><linearGradient id="edge1"><stop stop-color="#17142e"/><stop offset="1" stop-color="#403b70"/></linearGradient></defs><g transform="translate({x:.3f} {y:.3f}) scale({size*w:.4f} {size:.4f}) skewY({theta*14:.3f}) translate(-285 -290)">{''.join(walls)}{''.join(faces)}</g></svg>'''
        put(out/f'assets/service-frames/frame_{i+1:04d}.svg',svg)


if __name__ == "__main__":
    root = Path(sys.argv[1])
    def put(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8"))
    write_frames(root, BRAND, put)
    frames = sorted((root / "assets/service-frames").glob("frame_*.svg"))
    hashes = [hashlib.sha256(f.read_bytes()).hexdigest() for f in frames]
    assert len(frames) == len(set(hashes)) == 371
    print("371 distinct own monogram frames; bytes:", sum(f.stat().st_size for f in frames))
