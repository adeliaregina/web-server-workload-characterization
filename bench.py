#!/usr/bin/env python3
"""Measure parse + aggregation cost on 25%, 50% and 100% prefixes of a log (clean process per size).
Usage: python3 bench.py LOGFILE        (extra arguments, e.g. --tz/--a/--b, are accepted and ignored)
Windows are not needed: only parsing and a per-minute/per-status aggregation are timed."""
import subprocess, sys, tempfile, time, os, csv, json
try:
    import resource
except ImportError:
    resource = None   # Windows: memory column is left as n/a

HERE = os.path.dirname(os.path.abspath(__file__))
CHILD = r'''
import sys, time, json
sys.path.insert(0, sys.argv[2])
import log_pipeline as lp
t0 = time.perf_counter()
df, total, failed = lp.parse(sys.argv[1])
t1 = time.perf_counter()
m = df["ts"].dt.floor("min")
g = df.groupby([m, df["status"] // 100]).size()
t2 = time.perf_counter()
print(json.dumps(dict(total=total, failed=failed, parsed=len(df), parse_s=t1 - t0, agg_s=t2 - t1)))
'''

log = sys.argv[1]
n = sum(1 for _ in open(log, "rb"))
rows = []
for frac in (0.25, 0.5, 1.0):
    k = int(n * frac)
    with tempfile.NamedTemporaryFile("wb", delete=False, suffix=".log") as t:
        with open(log, "rb") as f:
            for i, line in enumerate(f):
                if i >= k: break
                t.write(line)
    t0 = time.perf_counter()
    out = subprocess.run([sys.executable, "-c", CHILD, t.name, HERE], check=True, capture_output=True, text=True).stdout
    wall = time.perf_counter() - t0
    r = json.loads(out.strip().splitlines()[-1])
    rss = round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024, 1) if resource else "n/a"
    rows.append((int(frac * 100), k, round(os.path.getsize(t.name) / 1e6, 2), round(r["parse_s"], 2), round(r["agg_s"], 2), round(wall, 2), rss))
    os.unlink(t.name)
hdr = ["percent", "rows", "size_mb", "parse_s", "aggregate_s", "total_process_s", "peak_rss_mb"]
print(",".join(hdr))
for r in rows: print(",".join(map(str, r)))
with open("bench_table.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
print("note: peak RSS (Linux/macOS only) is the running maximum over child processes; on Windows it is n/a.")
