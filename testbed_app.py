#!/usr/bin/env python3
"""Small test-bed web service for replaying log-derived load. Standard library only.

Every path is served. A route's service time class is fixed by a hash of the route:
  70% light (mean 8 ms), 20% medium (mean 30 ms), 10% heavy (mean 90 ms), lognormal spread.
At most --workers requests are served at once; a request that cannot get a worker within
--queue-timeout seconds receives HTTP 503. Overload therefore produces 5xx by a defined,
documented mechanism. Results describe THIS test bed only, never the original system.
"""
import argparse, hashlib, math, random, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MEAN_MS = {"light": 8.0, "medium": 30.0, "heavy": 90.0}

def klass(route: str) -> str:
    h = int(hashlib.sha1(route.encode()).hexdigest(), 16) % 10
    return "light" if h < 7 else ("medium" if h < 9 else "heavy")

def make_handler(sem, queue_timeout, scale):
    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        def do_GET(self):
            route = "/" + self.path.split("?", 1)[0].lstrip("/").split("/", 1)[0]
            if not sem.acquire(timeout=queue_timeout):
                body = b"busy"; self.send_response(503)
            else:
                try:
                    mean = MEAN_MS[klass(route)] * scale
                    sigma = 0.4
                    mu = math.log(mean) - sigma * sigma / 2
                    time.sleep(random.lognormvariate(mu, sigma) / 1000.0)
                finally:
                    sem.release()
                body = b"ok"; self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
        do_POST = do_GET
        def log_message(self, *a): pass
    return H

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--queue-timeout", type=float, default=0.5)
    ap.add_argument("--scale", type=float, default=1.0, help="multiply all service times")
    a = ap.parse_args()
    sem = threading.BoundedSemaphore(a.workers)
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(sem, a.queue_timeout, a.scale))
    srv.daemon_threads = True
    print(f"test bed on http://127.0.0.1:{a.port} workers={a.workers} scale={a.scale}", flush=True)
    srv.serve_forever()

if __name__ == "__main__":
    main()
