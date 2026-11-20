"""End-to-end smoke test on a SYNTHETIC log: pipeline -> test bed -> replay -> combine.
Checks that every stage runs and produces consistent files. It produces no research results."""
import json, os, subprocess, sys, tempfile, time, pathlib
here = pathlib.Path(__file__).resolve().parent; d = pathlib.Path(tempfile.mkdtemp())
py = [sys.executable, "-I"]
subprocess.run(py + [str(here / "make_synthetic.py"), str(d / "s.log")], check=True)
subprocess.run(py + [str(here / "log_pipeline.py"), str(d / "s.log"), "--tz", "Etc/GMT+4",
    "--a", "1995-07-05 08:00", "1995-07-05 10:00", "--b", "1995-07-12 08:00", "1995-07-12 10:00",
    "--out", str(d / "r"), "--dataset-name", "SYN", "--n-boot", "200"], check=True, stdout=subprocess.DEVNULL)
for f in ("table2_reconciliation.csv", "table3_routes.csv", "table4_execution.csv", "table5_test_parameters.csv", "table6_intervals.csv", "scenario_a.json", "scenario_b.json"):
    assert (d / "r" / f).exists(), f
sc = json.load(open(d / "r" / "scenario_b.json")); assert len(sc["rate_per_min"]) == 120 and abs(sum(r["share"] for r in sc["routes"]) - 1) < 1e-3
srv = subprocess.Popen(py + [str(here / "testbed_app.py"), "--port", "8097", "--workers", "4"], stdout=subprocess.DEVNULL)
time.sleep(1.5)
try:
    for x in "ab":
        subprocess.run(py + [str(here / "replay.py"), str(d / "r" / f"scenario_{x}.json"), "--base-url", "http://127.0.0.1:8097",
            "--peak-rps", "150", "--bin-seconds", "0.1", "--ref", str(d / "r" / "scenario_b.json"), "--out", str(d / f"rp_{x}")], check=True, stdout=subprocess.DEVNULL)
        s = json.load(open(d / f"rp_{x}_summary.json")); assert s["requests"] > 0 and s["p95_ms_all"] > 0
finally:
    srv.terminate()
out = subprocess.run(py + [str(here / "combine.py"), f"SYN={d / 'r'}"], capture_output=True, text=True, check=True).stdout
assert "SYN" in out
print("SMOKE TEST PASSED")
