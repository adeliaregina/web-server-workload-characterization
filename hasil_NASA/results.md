## Table 2

| Measure                      | Regular   | Spike   |
|:-----------------------------|:----------|:--------|
| Input rows (whole file)      | 1891715   | 1891715 |
| Failed to parse (whole file) | 10        | 10      |
| Parsed rows in window        | 42700     | 87826   |
| Application requests         | 14656     | 36841   |
| Static assets                | 28044     | 50985   |
| Complete/planned minutes     | 600/600   | 600/600 |
| Valid duration/application   | 0/14656   | 0/36841 |

## Table 3

| period   | route       |   requests |   peak_per_min | peak_time                 |   s5xx |   s429 |   s4xx |   pct_5xx |   pct_4xx |   share_of_traffic | p95_ms           |
|:---------|:------------|-----------:|---------------:|:--------------------------|-------:|-------:|-------:|----------:|----------:|-------------------:|:-----------------|
| Regular  | /shuttle    |       6889 |             30 | 1995-07-20 11:39:00-04:00 |      0 |      0 |     31 |     0     |     0.45  |              47    | n/a (not in CLF) |
| Regular  | /history    |       3122 |             22 | 1995-07-20 13:27:00-04:00 |      0 |      0 |     77 |     0     |     2.466 |              21.3  | n/a (not in CLF) |
| Regular  | /ksc.html   |       1202 |              8 | 1995-07-20 15:15:00-04:00 |      0 |      0 |      0 |     0     |     0     |               8.2  | n/a (not in CLF) |
| Regular  | /           |        815 |             12 | 1995-07-20 17:54:00-04:00 |      0 |      0 |      0 |     0     |     0     |               5.56 | n/a (not in CLF) |
| Regular  | /cgi-bin    |        571 |              6 | 1995-07-20 08:45:00-04:00 |      0 |      0 |      0 |     0     |     0     |               3.9  | n/a (not in CLF) |
| Regular  | /htbin      |        493 |              6 | 1995-07-20 16:43:00-04:00 |      0 |      0 |      3 |     0     |     0.609 |               3.36 | n/a (not in CLF) |
| Regular  | /facilities |        346 |              7 | 1995-07-20 09:56:00-04:00 |      0 |      0 |      2 |     0     |     0.578 |               2.36 | n/a (not in CLF) |
| Regular  | /software   |        204 |              4 | 1995-07-20 08:04:00-04:00 |      0 |      0 |      0 |     0     |     0     |               1.39 | n/a (not in CLF) |
| Spike    | /shuttle    |      18437 |             88 | 1995-07-13 09:49:00-04:00 |      0 |      0 |     70 |     0     |     0.38  |              50.04 | n/a (not in CLF) |
| Spike    | /htbin      |       8528 |            115 | 1995-07-13 09:40:00-04:00 |      0 |      0 |      4 |     0     |     0.047 |              23.15 | n/a (not in CLF) |
| Spike    | /history    |       3011 |             22 | 1995-07-13 13:57:00-04:00 |      0 |      0 |     49 |     0     |     1.627 |               8.17 | n/a (not in CLF) |
| Spike    | /cgi-bin    |       2688 |             18 | 1995-07-13 09:47:00-04:00 |      0 |      0 |      0 |     0     |     0     |               7.3  | n/a (not in CLF) |
| Spike    | /ksc.html   |       1600 |             10 | 1995-07-13 09:14:00-04:00 |      2 |      0 |      0 |     0.125 |     0     |               4.34 | n/a (not in CLF) |
| Spike    | /           |       1084 |              9 | 1995-07-13 17:04:00-04:00 |      0 |      0 |      0 |     0     |     0     |               2.94 | n/a (not in CLF) |
| Spike    | /facilities |        441 |              6 | 1995-07-13 16:24:00-04:00 |      0 |      0 |      0 |     0     |     0     |               1.2  | n/a (not in CLF) |
| Spike    | /software   |        174 |              4 | 1995-07-13 17:39:00-04:00 |      0 |      0 |      2 |     0     |     1.149 |               0.47 | n/a (not in CLF) |

## Table 4

| Component          | Actual result   |
|:-------------------|:----------------|
| Pandas             | 3.1.1           |
| Input rows         | 1891715         |
| Parse time (s)     | 17.15           |
| Aggregate time (s) | 0.45            |
| File size (MB)     | 205.24          |

## Table 5

| Parameter                    | Regular                                                                                                                             | Spike                                                                                                                               |
|:-----------------------------|:------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|
| Window                       | 1995-07-20 08:00:00-04:00 to 1995-07-20 18:00:00-04:00                                                                              | 1995-07-13 08:00:00-04:00 to 1995-07-13 18:00:00-04:00                                                                              |
| Initial rate (req/min)       | 20                                                                                                                                  | 26                                                                                                                                  |
| Median rate (req/min)        | 24.0                                                                                                                                | 54.0                                                                                                                                |
| Peak rate (req/min)          | 49                                                                                                                                  | 193                                                                                                                                 |
| Peak time                    | 1995-07-20 11:39:00-04:00                                                                                                           | 1995-07-13 09:49:00-04:00                                                                                                           |
| Minutes at >=90% of peak     | 7                                                                                                                                   | 3                                                                                                                                   |
| Route mix at peak minute (%) | {'/shuttle': 61.2, '/history': 12.2, '/facts': 8.2, '/': 4.1, '/facilities': 4.1, '/cgi-bin': 2.0, '/histor-y': 2.0, '/htbin': 2.0} | {'/shuttle': 45.6, '/htbin': 39.4, '/cgi-bin': 7.3, '/': 3.1, '/history': 1.6, '/ksc.html': 1.6, '/facilities': 1.0, '/facts': 0.5} |

## Table 6

| Measure                                          |   Estimate | 95% interval (block bootstrap, 10-min blocks)   |
|:-------------------------------------------------|-----------:|:------------------------------------------------|
| Median rate, Regular (req/min)                   |     24     | 22.00 to 25.00                                  |
| Median rate, Spike (req/min)                     |     54     | 50.00 to 60.00                                  |
| Ratio of medians (Spike/Regular)                 |      2.25  | 2.040 to 2.565                                  |
| Difference in 5xx proportion (percentage points) |      0.005 | 0.000 to 0.018                                  |

