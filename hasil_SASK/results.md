## Table 2

| Measure                      | Break   | Term    |
|:-----------------------------|:--------|:--------|
| Input rows (whole file)      | 2408625 | 2408625 |
| Failed to parse (whole file) | 90      | 90      |
| Parsed rows in window        | 5364    | 12289   |
| Application requests         | 3700    | 6903    |
| Static assets                | 1664    | 5386    |
| Complete/planned minutes     | 600/600 | 600/600 |
| Valid duration/application   | 0/3700  | 0/6903  |

## Table 3

| period   | route      |   requests |   peak_per_min | peak_time                 |   s5xx |   s429 |   s4xx |   pct_5xx |   pct_4xx |   share_of_traffic | p95_ms           |
|:---------|:-----------|-----------:|---------------:|:--------------------------|-------:|-------:|-------:|----------:|----------:|-------------------:|:-----------------|
| Break    | /          |        692 |              5 | 1995-07-18 11:12:00-06:00 |      0 |      0 |      0 |         0 |     0     |              18.7  | n/a (not in CLF) |
| Break    | /~scottp   |        581 |              5 | 1995-07-18 12:19:00-06:00 |      0 |      0 |      0 |         0 |     0     |              15.7  | n/a (not in CLF) |
| Break    | /cgi-bin   |        540 |             10 | 1995-07-18 10:20:00-06:00 |      0 |      0 |      3 |         0 |     0.556 |              14.59 | n/a (not in CLF) |
| Break    | /~lowey    |        314 |              7 | 1995-07-18 12:20:00-06:00 |      0 |      0 |      0 |         0 |     0     |               8.49 | n/a (not in CLF) |
| Break    | /~macphed  |        288 |             10 | 1995-07-18 12:40:00-06:00 |      0 |      0 |      0 |         0 |     0     |               7.78 | n/a (not in CLF) |
| Break    | /dcs       |        193 |             15 | 1995-07-18 12:21:00-06:00 |      0 |      0 |      1 |         0 |     0.518 |               5.22 | n/a (not in CLF) |
| Break    | /search    |        102 |              4 | 1995-07-18 11:26:00-06:00 |      0 |      0 |      0 |         0 |     0     |               2.76 | n/a (not in CLF) |
| Break    | /education |         91 |              7 | 1995-07-18 15:04:00-06:00 |      0 |      0 |      0 |         0 |     0     |               2.46 | n/a (not in CLF) |
| Term     | /          |       1229 |             10 | 1995-10-24 10:17:00-06:00 |      0 |      0 |      0 |         0 |     0     |              17.8  | n/a (not in CLF) |
| Term     | /dcs       |       1018 |             10 | 1995-10-24 13:48:00-06:00 |      0 |      0 |     15 |         0 |     1.473 |              14.75 | n/a (not in CLF) |
| Term     | /~macphed  |        524 |              8 | 1995-10-24 08:27:00-06:00 |      0 |      0 |      0 |         0 |     0     |               7.59 | n/a (not in CLF) |
| Term     | /~scottp   |        430 |              4 | 1995-10-24 08:48:00-06:00 |      0 |      0 |      0 |         0 |     0     |               6.23 | n/a (not in CLF) |
| Term     | /~lowey    |        402 |              9 | 1995-10-24 11:56:00-06:00 |      0 |      0 |      0 |         0 |     0     |               5.82 | n/a (not in CLF) |
| Term     | /cgi-bin   |        359 |              5 | 1995-10-24 10:45:00-06:00 |      0 |      0 |     12 |         0 |     3.343 |               5.2  | n/a (not in CLF) |
| Term     | /~reevesm  |        293 |              9 | 1995-10-24 13:13:00-06:00 |      0 |      0 |      0 |         0 |     0     |               4.24 | n/a (not in CLF) |
| Term     | /search    |        281 |              5 | 1995-10-24 10:30:00-06:00 |      0 |      0 |      0 |         0 |     0     |               4.07 | n/a (not in CLF) |

## Table 4

| Component          | Actual result   |
|:-------------------|:----------------|
| Pandas             | 3.1.1           |
| Input rows         | 2408625         |
| Parse time (s)     | 30.28           |
| Aggregate time (s) | 0.32            |
| File size (MB)     | 233.44          |

## Table 5

| Parameter                    | Break                                                                                  | Term                                                                                                                                                     |
|:-----------------------------|:---------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| Window                       | 1995-07-18 08:00:00-06:00 to 1995-07-18 18:00:00-06:00                                 | 1995-10-24 08:00:00-06:00 to 1995-10-24 18:00:00-06:00                                                                                                   |
| Initial rate (req/min)       | 5                                                                                      | 4                                                                                                                                                        |
| Median rate (req/min)        | 6.0                                                                                    | 11.0                                                                                                                                                     |
| Peak rate (req/min)          | 21                                                                                     | 31                                                                                                                                                       |
| Peak time                    | 1995-07-18 12:19:00-06:00                                                              | 1995-10-24 10:27:00-06:00                                                                                                                                |
| Minutes at >=90% of peak     | 2                                                                                      | 5                                                                                                                                                        |
| Route mix at peak minute (%) | {'/~macphed': 28.6, '/~scottp': 23.8, '/dcs': 19.0, '/cgi-bin': 14.3, '/~lowey': 14.3} | {'/dcs': 29.0, '/': 16.1, '/~reevesm': 16.1, '/search': 6.5, '/~ladd': 6.5, '/departments.html': 3.2, '/alternate_views.html': 3.2, '/agriculture': 3.2} |

## Table 6

| Measure                                          |   Estimate | 95% interval (block bootstrap, 10-min blocks)   |
|:-------------------------------------------------|-----------:|:------------------------------------------------|
| Median rate, Break (req/min)                     |      6     | 5.00 to 6.00                                    |
| Median rate, Term (req/min)                      |     11     | 10.00 to 12.00                                  |
| Ratio of medians (Term/Break)                    |      1.833 | 1.667 to 2.200                                  |
| Difference in 5xx proportion (percentage points) |      0     | 0.000 to 0.000                                  |

