"""TEST-ONLY generator of a synthetic CLF log with a quiet day and a busy day. Not research data."""
import random, sys
random.seed(7)
out = open(sys.argv[1], "w")
routes = ["/a/x", "/a/y", "/b/q", "/c/z", "/d/w", "/e/m"]; w = [40, 25, 15, 10, 6, 4]
def day(d, base, peak_min):
    for m in range(0, 120):
        rate = base + (peak_min if 40 <= m < 60 else 0)
        for _ in range(rate):
            s = random.randint(0, 59); r = random.choices(routes, w)[0]
            st = 200 if random.random() > (0.01 if rate == base else 0.04) else 503
            out.write(f'h - - [{d}/Jul/1995:08:{m % 60:02d}:{s:02d} -0400] "GET {r}/p.html HTTP/1.0" {st} 123\n'.replace("08:", f"{8 + m // 60:02d}:", 1))
day(5, 20, 0); day(12, 20, 120)
