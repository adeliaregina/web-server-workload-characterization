#!/usr/bin/env python3
"""Count requests per day and per day-hour in a CLF log (standard library only).
Usage: py daily_counts.py LOGFILE [NAME]
Writes NAME_daily.csv and NAME_hourly.csv and prints a day table with weekday names."""
import re, sys, csv, datetime as dt
from collections import Counter
ts = re.compile(r'\[(\d{1,2})/(\w{3})/(\d{4}):(\d{2}):\d{2}:\d{2} ')
M = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
path = sys.argv[1]; name = sys.argv[2] if len(sys.argv) > 2 else "log"
day, hour, bad = Counter(), Counter(), 0
with open(path, "r", encoding="latin-1", errors="replace") as f:
    for line in f:
        m = ts.search(line)
        if not m: bad += 1; continue
        d = dt.date(int(m.group(3)), M[m.group(2)], int(m.group(1)))
        day[d] += 1; hour[(d, int(m.group(4)))] += 1
days = sorted(day)
if days:
    d, last = days[0], days[-1]
    allday = []
    while d <= last: allday.append(d); d += dt.timedelta(days=1)
else: allday = []
with open(f"{name}_daily.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["date", "weekday", "requests"])
    for d in allday: w.writerow([d.isoformat(), d.strftime("%a"), day.get(d, 0)])
with open(f"{name}_hourly.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["date", "hour", "requests"])
    for (d, h), n in sorted(hour.items()): w.writerow([d.isoformat(), h, n])
print(f"unparsed lines: {bad}; days with data: {len(days)}; total: {sum(day.values())}")
print("date        wd   requests")
for d in allday: print(d.isoformat(), d.strftime("%a"), day.get(d, 0))
