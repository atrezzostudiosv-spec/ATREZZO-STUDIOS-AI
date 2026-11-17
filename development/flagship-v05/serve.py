#!/usr/bin/env python3
"""Private loopback-only preview. No external deployment or form submission."""
import argparse, functools, threading, webbrowser
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from build import build, find_zip
HERE=Path(__file__).resolve().parent
class Preview(SimpleHTTPRequestHandler):
 def end_headers(self):
  self.send_header('Cache-Control','no-store')
  self.send_header('X-Robots-Tag','noindex, nofollow, noarchive')
  self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; media-src 'self' blob: data:; connect-src 'self' blob:; worker-src 'self' blob:; frame-src 'none'; form-action 'none'; object-src 'none'; base-uri 'self'")
  super().end_headers()
 def list_directory(self,path):self.send_error(403,'Private preview: directory listing disabled');return None
 def do_POST(self):self.send_error(405,'Private preview: submissions disabled')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--archive');p.add_argument('--port',type=int,default=8770);p.add_argument('--no-open',action='store_true');p.add_argument('--offline',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--out',default=str(HERE/'private-preview'));a=p.parse_args()
 out=Path(a.out).resolve();build(find_zip(a.archive),out,a.offline)
 if a.check:raise SystemExit(0)
 handler=functools.partial(Preview,directory=str(out))
 for port in range(a.port,a.port+10):
  try:server=ThreadingHTTPServer(('127.0.0.1',port),handler);break
  except OSError:continue
 else:raise SystemExit('No free local preview port')
 url=f'http://127.0.0.1:{port}/en/'
 print('\nATREZZO STUDIOS — private Home V05\n'+url+'\nKeep this window open while reviewing. Ctrl+C stops the server.',flush=True)
 if not a.no_open:threading.Timer(.7,lambda:webbrowser.open(url)).start()
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.server_close()
