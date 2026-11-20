"""Correctness test on a tiny synthetic log with hand-computed expectations.
This verifies the code only; it produces NO research results."""
import subprocess, sys, pandas as pd, tempfile, pathlib
d = pathlib.Path(tempfile.mkdtemp()); log = d/"t.log"
def line(day, hh, mm, ss, url, st): return f'h - - [{day}/Jul/1995:{hh:02d}:{mm:02d}:{ss:02d} -0400] "GET {url} HTTP/1.0" {st} 100\n'
L=[]
# window A (day 05, 08:00-08:10): 1 req/min on /a, +1 static (ignored in app), 1 bad line
for m in range(10): L.append(line(5,8,m,1,"/a/x.html",200))
L.append(line(5,8,3,2,"/img/l.gif",200)); L.append("garbage line\n")
# window B (day 12, 08:00-08:10): minute 4 has 20 req (15 on /a with 3x500, 5 on /b with 1x429), others 1 on /a
for m in range(10):
    if m!=4: L.append(line(12,8,m,1,"/a/y.html",200))
for i in range(15): L.append(line(12,8,4,i,"/a/z.html",500 if i<3 else 200))
for i in range(5): L.append(line(12,8,4,20+i,"/b/q.html",429 if i==0 else 200))
log.write_text("".join(L))
out=d/"o"
r=subprocess.run([sys.executable,"log_pipeline.py",str(log),"--tz","Etc/GMT+4","--a","1995-07-05 08:00","1995-07-05 08:10",
 "--b","1995-07-12 08:00","1995-07-12 08:10","--out",str(out)],capture_output=True,text=True)
assert r.returncode==0, r.stderr
t2=pd.read_csv(out/"table2_reconciliation.csv",dtype=str).set_index("Measure")
assert t2.loc["Failed to parse (whole file)","Regular"]=="1"
assert t2.loc["Application requests","Regular"]=="10" and t2.loc["Static assets","Regular"]=="1"
assert t2.loc["Application requests","Busy"]==str(9+20)
assert t2.loc["Complete/planned minutes","Busy"]=="10/10"
t3=pd.read_csv(out/"table3_routes.csv"); b=t3[(t3.period=="Busy")&(t3.route=="/a")].iloc[0]
assert b.requests==9+15 and b.s5xx==3 and b.peak_per_min==15, b
bb=t3[(t3.period=="Busy")&(t3.route=="/b")].iloc[0]; assert bb.s429==1 and bb.requests==5
t5=pd.read_csv(out/"table5_test_parameters.csv",dtype=str).set_index("Parameter")
assert t5.loc["Peak rate (req/min)","Busy"]=="20" and t5.loc["Peak rate (req/min)","Regular"]=="1"
assert "08:04" in t5.loc["Peak time","Busy"]
print("ALL TESTS PASSED")
