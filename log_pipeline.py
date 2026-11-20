#!/usr/bin/env python3
"""Batch workload-characterization pipeline for web server access logs.

Reads a Common Log Format (CLF) file, validates and reconciles it, and writes the
tables used in the manuscript (Tables 2, 3 and 5) as CSV plus a Markdown summary.

Example (NASA-HTTP July 1995 log, local time = UTC-4; Saskatchewan-HTTP lines carry -0600, use Etc/GMT+6):
  python3 log_pipeline.py NASA_access_log_Jul95 --tz Etc/GMT+4 \
      --a "1995-07-05 08:00" "1995-07-05 12:00" --a-label Regular \
      --b "1995-07-12 08:00" "1995-07-12 12:00" --b-label Busy --out results

Only the columns available in CLF are used: time, method, route, status, bytes.
Request duration is NOT part of CLF, so P95 duration is reported as n/a.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

CLF = re.compile(r'^(\S+) \S+ \S+ \[(\d{1,2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\] "(\S+) (\S+)(?: [^"]*)?" (\d{3}) (\S+)\s*$')
STATIC = re.compile(r"\.(gif|jpe?g|png|ico|css|js|xbm|bmp|svg|woff2?)$", re.I)


def route_group(path: str, depth: int) -> str:
    path = path.split("?", 1)[0]
    parts = [p for p in path.split("/") if p]
    if not parts:
        return "/"
    return "/" + "/".join(parts[:depth])


def parse(path: Path):
    total = failed = 0
    ts, method, url, status = [], [], [], []
    with open(path, "r", encoding="latin-1", errors="replace") as fh:
        for line in fh:
            total += 1
            m = CLF.match(line)
            if not m:
                failed += 1
                continue
            ts.append(m.group(2))
            method.append(m.group(3))
            url.append(m.group(4))
            status.append(int(m.group(5)))
    df = pd.DataFrame({"ts": ts, "method": method, "url": url, "status": status})
    df["ts"] = pd.to_datetime(df["ts"], format="%d/%b/%Y:%H:%M:%S %z", utc=True, errors="coerce")
    bad_dates = int(df["ts"].isna().sum())   # e.g. impossible dates: counted as failed, never a crash
    if bad_dates:
        df = df[df["ts"].notna()].reset_index(drop=True)
        failed += bad_dates
    return df, total, failed


def window(df, start, end, tz):
    s = pd.Timestamp(start, tz=tz)
    e = pd.Timestamp(end, tz=tz)
    return df[(df["ts"] >= s) & (df["ts"] < e)], s, e


def analyse(df, total_rows, failed_rows, label, start, end, tz, depth, top):
    w, s, e = window(df, start, end, tz)
    w = w.copy()
    w["static"] = w["url"].map(lambda u: bool(STATIC.search(u.split("?", 1)[0])))
    app = w[~w["static"]].copy()
    app["route"] = app["url"].map(lambda u: route_group(u, depth))
    app["minute"] = app["ts"].dt.floor("min")

    planned = int((e - s).total_seconds() // 60)
    cov_start, cov_end = df["ts"].min(), df["ts"].max()
    ov_s, ov_e = max(s, cov_start.floor("min")), min(e, cov_end.floor("min") + pd.Timedelta(minutes=1))
    complete = max(0, int((ov_e - ov_s).total_seconds() // 60))

    idx = pd.date_range(s, e, freq="min", inclusive="left")
    per_min = app.groupby("minute").size().reindex(idx, fill_value=0)

    # reconciliation: route groups must add up to application requests
    by_route = app.groupby("route").size().sort_values(ascending=False)
    assert int(by_route.sum()) == len(app), "route groups do not sum to application requests"
    assert len(app) + int(w["static"].sum()) == len(w), "app + static != window rows"

    peak = int(per_min.max()) if len(per_min) else 0
    peak_times = per_min[per_min == peak].index
    info = dict(
        label=label, start=str(s), end=str(e), rows=len(w), app=len(app),
        static=int(w["static"].sum()), planned=planned, complete=complete,
        median_rate=float(per_min.median()) if len(per_min) else 0.0,
        peak=peak, peak_time=str(peak_times[0].tz_convert(tz)) if len(peak_times) else "n/a",
        n_peak_minutes=len(peak_times),
        sustained=int((per_min >= 0.9 * peak).sum()) if peak else 0,
    )

    rows = []
    for r in by_route.index[:top]:
        g = app[app["route"] == r]
        gm = g.groupby("minute").size().reindex(idx, fill_value=0)
        n = len(g)
        rows.append(dict(
            period=label, route=r, requests=n,
            peak_per_min=int(gm.max()), peak_time=str(gm.idxmax().tz_convert(tz)),
            s5xx=int(g["status"].between(500, 599).sum()),
            s429=int((g["status"] == 429).sum()),
            s4xx=int(g["status"].between(400, 499).sum()),
            pct_5xx=round(100 * g["status"].between(500, 599).mean(), 3),
            pct_4xx=round(100 * g["status"].between(400, 499).mean(), 3),
            share_of_traffic=round(100 * n / len(app), 2) if len(app) else 0.0,
            p95_ms="n/a (not in CLF)",
        ))
    # route mix inside the peak minute
    pk = app[app["minute"] == peak_times[0]] if len(peak_times) else app.iloc[0:0]
    mix = (pk.groupby("route").size().sort_values(ascending=False).head(top) / max(len(pk), 1) * 100).round(1)
    info["mix_at_peak"] = mix.to_dict()
    err_min = app[app["status"].between(500, 599)].groupby("minute").size().reindex(idx, fill_value=0)
    info["rate_series"] = per_min.values.astype(float)
    info["err_series"] = err_min.values.astype(float)
    info["route_share"] = (by_route / max(len(app), 1)).to_dict()
    info["route_method"] = app.groupby("route")["method"].agg(lambda x: x.mode().iat[0]).to_dict() if len(app) else {}
    info["first_minute_rate"] = int(per_min.iloc[0]) if len(per_min) else 0
    return info, pd.DataFrame(rows), per_min


def block_bootstrap(ia, ib, block=10, n_boot=2000, seed=20261119):
    """Moving-block bootstrap over minutes. Returns 95% percentile intervals."""
    rng = np.random.default_rng(seed)
    ra, ea, rb, eb = ia["rate_series"], ia["err_series"], ib["rate_series"], ib["err_series"]

    def draw(n):
        blk = max(1, min(block, n))
        nb = int(np.ceil(n / blk))
        starts = rng.integers(0, max(n - blk + 1, 1), size=nb)
        return (starts[:, None] + np.arange(blk)).ravel()[:n]

    out = {"med_a": [], "med_b": [], "ratio": [], "d5xx": []}
    for _ in range(n_boot):
        xa, xb = draw(len(ra)), draw(len(rb))
        ma, mb = np.median(ra[xa]), np.median(rb[xb])
        out["med_a"].append(ma); out["med_b"].append(mb)
        out["ratio"].append(mb / ma if ma > 0 else np.nan)
        pa = 100 * ea[xa].sum() / max(ra[xa].sum(), 1)
        pb = 100 * eb[xb].sum() / max(rb[xb].sum(), 1)
        out["d5xx"].append(pb - pa)
    return {k: (float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))) for k, v in out.items()}


def write_scenario(info, path, dataset, top=15):
    shares = sorted(info["route_share"].items(), key=lambda kv: -kv[1])
    keep = shares[:top]
    other = 1.0 - sum(s for _, s in keep)
    routes = [{"route": r, "method": info["route_method"].get(r, "GET"), "share": round(s, 6)} for r, s in keep]
    if other > 1e-9:
        routes.append({"route": "/__other__", "method": "GET", "share": round(other, 6)})
    scen = {
        "dataset": dataset, "label": info["label"], "window": [info["start"], info["end"]],
        "bin_seconds": 60, "rate_per_min": [int(x) for x in info["rate_series"]],
        "routes": routes,
        "note": "Derived from server access logs; replay on a test bed describes the test bed only.",
    }
    with open(path, "w") as f:
        json.dump(scen, f, indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logfile", type=Path)
    ap.add_argument("--tz", default="UTC", help="IANA zone of the service, e.g. Asia/Makassar or Etc/GMT+4")
    ap.add_argument("--a", nargs=2, required=True, metavar=("START", "END"))
    ap.add_argument("--b", nargs=2, required=True, metavar=("START", "END"))
    ap.add_argument("--a-label", default="Regular")
    ap.add_argument("--b-label", default="Busy")
    ap.add_argument("--depth", type=int, default=1, help="path segments kept as the route group")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--out", type=Path, default=Path("results"))
    ap.add_argument("--dataset-name", default="dataset")
    ap.add_argument("--block", type=int, default=10, help="bootstrap block length in minutes")
    ap.add_argument("--n-boot", type=int, default=2000)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)

    t0 = time.perf_counter()
    df, total, failed = parse(a.logfile)
    assert len(df) + failed == total, "input rows != parsed + failed"
    t_parse = time.perf_counter() - t0

    wa = pd.Timestamp(a.a[1]) - pd.Timestamp(a.a[0])
    wb = pd.Timestamp(a.b[1]) - pd.Timestamp(a.b[0])
    if wa != wb:
        print("WARNING: the two windows differ in length; comparison is not matched", file=sys.stderr)
    for lab, st in ((a.a_label, a.a[0]), (a.b_label, a.b[0])):
        print(f"{lab}: weekday {pd.Timestamp(st).day_name()}")

    t1 = time.perf_counter()
    ia, ta, ma = analyse(df, total, failed, a.a_label, *a.a, a.tz, a.depth, a.top)
    ib, tb, mb = analyse(df, total, failed, a.b_label, *a.b, a.tz, a.depth, a.top)
    t_an = time.perf_counter() - t1

    # Table 2
    t2 = pd.DataFrame([
        ("Input rows (whole file)", total, total),
        ("Failed to parse (whole file)", failed, failed),
        ("Parsed rows in window", ia["rows"], ib["rows"]),
        ("Application requests", ia["app"], ib["app"]),
        ("Static assets", ia["static"], ib["static"]),
        ("Complete/planned minutes", f'{ia["complete"]}/{ia["planned"]}', f'{ib["complete"]}/{ib["planned"]}'),
        ("Valid duration/application", "0/%d" % ia["app"], "0/%d" % ib["app"]),
    ], columns=["Measure", a.a_label, a.b_label])
    t3 = pd.concat([ta, tb]).reset_index(drop=True)
    t5 = pd.DataFrame([
        ("Window", f'{ia["start"]} to {ia["end"]}', f'{ib["start"]} to {ib["end"]}'),
        ("Initial rate (req/min)", ia["first_minute_rate"], ib["first_minute_rate"]),
        ("Median rate (req/min)", ia["median_rate"], ib["median_rate"]),
        ("Peak rate (req/min)", ia["peak"], ib["peak"]),
        ("Peak time", ia["peak_time"], ib["peak_time"]),
        ("Minutes at >=90% of peak", ia["sustained"], ib["sustained"]),
        ("Route mix at peak minute (%)", ia["mix_at_peak"], ib["mix_at_peak"]),
    ], columns=["Parameter", a.a_label, a.b_label])
    t4 = pd.DataFrame([
        ("Pandas", pd.__version__), ("Input rows", total),
        ("Parse time (s)", round(t_parse, 2)), ("Aggregate time (s)", round(t_an, 2)),
        ("File size (MB)", round(a.logfile.stat().st_size / 1e6, 2)),
    ], columns=["Component", "Actual result"])

    ci = block_bootstrap(ia, ib, block=a.block, n_boot=a.n_boot)
    t6 = pd.DataFrame([
        ("Median rate, " + a.a_label + " (req/min)", round(float(np.median(ia["rate_series"])), 2), f'{ci["med_a"][0]:.2f} to {ci["med_a"][1]:.2f}'),
        ("Median rate, " + a.b_label + " (req/min)", round(float(np.median(ib["rate_series"])), 2), f'{ci["med_b"][0]:.2f} to {ci["med_b"][1]:.2f}'),
        ("Ratio of medians (" + a.b_label + "/" + a.a_label + ")", round(float(np.median(ib["rate_series"]) / np.median(ia["rate_series"])), 3) if np.median(ia["rate_series"]) > 0 else "n/a", f'{ci["ratio"][0]:.3f} to {ci["ratio"][1]:.3f}'),
        ("Difference in 5xx proportion (percentage points)", round(100 * ib["err_series"].sum() / max(ib["rate_series"].sum(), 1) - 100 * ia["err_series"].sum() / max(ia["rate_series"].sum(), 1), 3), f'{ci["d5xx"][0]:.3f} to {ci["d5xx"][1]:.3f}'),
    ], columns=["Measure", "Estimate", f"95% interval (block bootstrap, {a.block}-min blocks)"])
    t6.to_csv(a.out / "table6_intervals.csv", index=False)
    write_scenario(ia, a.out / "scenario_a.json", a.dataset_name)
    write_scenario(ib, a.out / "scenario_b.json", a.dataset_name)
    t2.to_csv(a.out / "table2_reconciliation.csv", index=False)
    t3.to_csv(a.out / "table3_routes.csv", index=False)
    t4.to_csv(a.out / "table4_execution.csv", index=False)
    t5.to_csv(a.out / "table5_test_parameters.csv", index=False)
    pd.DataFrame({a.a_label: ma.values}).to_csv(a.out / "per_minute_a.csv", index=False)
    pd.DataFrame({a.b_label: mb.values}).to_csv(a.out / "per_minute_b.csv", index=False)
    with open(a.out / "results.md", "w") as f:
        for name, t in (("Table 2", t2), ("Table 3", t3), ("Table 4", t4), ("Table 5", t5), ("Table 6", t6)):
            f.write(f"## {name}\n\n{t.to_markdown(index=False) if hasattr(t,'to_markdown') else t.to_string(index=False)}\n\n")
    print(open(a.out / "results.md").read())


if __name__ == "__main__":
    main()
