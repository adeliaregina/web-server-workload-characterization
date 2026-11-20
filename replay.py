#!/usr/bin/env python3
"""Open-loop replay of a scenario.json (from log_pipeline.py) against a target URL.
Standard library only. Arrivals are Poisson within each bin. The per-minute rate series is
rescaled so the highest bin equals --peak-rps, and each original minute lasts --bin-seconds.
Only replay against a system you own or are explicitly authorised to test.
"""
import argparse, csv, http.client, json, random, threading, time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import numpy as np

local = threading.local()

def conn(host, port, timeout):
    c = getattr(local, "c", None)
    if c is None:
        c = http.client.HTTPConnection(host, port, timeout=timeout); local.c = c
    return c

def one(host, port, method, path, timeout, t0, out, lock):
    t = time.perf_counter(); status = 0
    try:
        c = conn(host, port, timeout)
        c.request(method, path); r = c.getresponse(); r.read(); status = r.status
    except Exception:
        local.c = None
    dur = (time.perf_counter() - t) * 1000
    with lock: out.append((t - t0, path, status, dur))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario"); ap.add_argument("--base-url", default="http://127.0.0.1:8080")
    ap.add_argument("--peak-rps", type=float, default=200.0)
    ap.add_argument("--bin-seconds", type=float, default=10.0)
    ap.add_argument("--max-threads", type=int, default=256)
    ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--ref", default=None, help="scenario whose peak sets the scale (use scenario_b.json for BOTH runs so regular and busy are comparable)")
    ap.add_argument("--out", default="replay_out")
    a = ap.parse_args()
    sc = json.load(open(a.scenario)); rate = np.array(sc["rate_per_min"], dtype=float)
    ref_rate = np.array(json.load(open(a.ref))["rate_per_min"], dtype=float) if a.ref else rate
    peak = ref_rate.max() if ref_rate.max() > 0 else 1.0
    rps = rate / peak * a.peak_rps
    routes = sc["routes"]; w = np.array([r["share"] for r in routes]); w = w / w.sum()
    rng = random.Random(a.seed); nrng = np.random.default_rng(a.seed)
    u = urlparse(a.base_url); host, port = u.hostname, u.port or 80
    out, lock = [], threading.Lock()
    pool = ThreadPoolExecutor(max_workers=a.max_threads)
    t0 = time.perf_counter(); sent = 0
    for i, r in enumerate(rps):
        bin_end = t0 + (i + 1) * a.bin_seconds
        n = int(nrng.poisson(r * a.bin_seconds))
        offs = np.sort(nrng.uniform(0, a.bin_seconds, n))
        picks = nrng.choice(len(routes), size=n, p=w)
        for o, k in zip(offs, picks):
            target = t0 + i * a.bin_seconds + o
            d = target - time.perf_counter()
            if d > 0: time.sleep(d)
            rt = routes[k]
            pool.submit(one, host, port, rt["method"], rt["route"] if rt["route"] != "/__other__" else "/other", a.timeout, t0, out, lock)
            sent += 1
        d = bin_end - time.perf_counter()
        if d > 0: time.sleep(d)
    pool.shutdown(wait=True)
    dur = np.array([x[3] for x in out]); st = np.array([x[2] for x in out])
    ok = dur[(st >= 200) & (st < 400)]
    summ = {
        "requests": len(out), "duration_s": round(len(rps) * a.bin_seconds, 1),
        "achieved_rps": round(len(out) / (len(rps) * a.bin_seconds), 2), "requested_peak_rps": a.peak_rps,
        "p50_ms_all": round(float(np.percentile(dur, 50)), 2), "p95_ms_all": round(float(np.percentile(dur, 95)), 2),
        "p95_ms_success": round(float(np.percentile(ok, 95)), 2) if len(ok) else None,
        "pct_5xx": round(100 * float(((st >= 500) & (st < 600)).mean()), 3),
        "pct_status0_timeout_or_error": round(100 * float((st == 0).mean()), 3),
    }
    with open(a.out + "_requests.csv", "w", newline="") as f:
        cw = csv.writer(f); cw.writerow(["t_s", "path", "status", "ms"]); cw.writerows(out)
    json.dump(summ, open(a.out + "_summary.json", "w"), indent=1)
    print(json.dumps(summ, indent=1))

if __name__ == "__main__":
    main()
