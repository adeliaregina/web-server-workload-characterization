# Results index and manuscript correspondence

The provided `hasil_SASK/` and `hasil_NASA/` folders contain outputs from the original pipeline. Filenames `table2`–`table6` refer to **pipeline output tables**, not necessarily the final manuscript table numbers. The manuscript combines and rearranges these outputs.

| Files | Interpretation |
| --- | --- |
| `table2_reconciliation.csv` | Input lines, failed parsing, per-window application/static requests, coverage and absent durations |
| `table3_routes.csv` | Route-level request counts, error shares and traffic composition |
| `table4_execution.csv` | Software version, input size, and parse/aggregation timing |
| `table5_test_parameters.csv` | Window selection, initial/median/peak request rates and route mix at peak |
| `table6_intervals.csv` | Moving-block bootstrap intervals for median rates, median ratio and 5xx difference |
| `per_minute_a.csv`, `per_minute_b.csv` | 600-bin per-minute application request series |
| `scenario_a.json`, `scenario_b.json` | Exported per-minute arrival series and route shares for replay |
| `replay_*_summary.json` | Replay counts, P50/P95 and HTTP error shares |
| `replay_*_requests.csv` | Individual replay measurements (test-bed only) |
| `log_replay_*.txt` | Console output captured during replay |
| `results.md` | Markdown presentation of the pipeline tables |

## Values appearing in the manuscript

| Measure | Saskatchewan | NASA |
| --- | ---: | ---: |
| Full trace input lines | 2,408,625 | 1,891,715 |
| Failed parse lines | 90 | 10 |
| Regular/break application requests | 3,700 | 14,656 |
| Busy/term application requests | 6,903 | 36,841 |
| Median rate ratio, busy / regular | 1.833 | 2.250 |
| 95% block-bootstrap interval | 1.667–2.200 | 2.040–2.565 |
| Replay P95, regular (typical runs) | approx. 35.7 ms | approx. 25.2 ms |
| Replay P95, busy | approx. 55.0 ms | approx. 39.5 ms |

**Anomalous run:** `hasil_SASK/replay_a_s1_summary.json` reports P95 235.74 ms and 0.086% 5xx, whereas `replay_a_s1_ulang_summary.json` reports P95 35.39 ms and 0% 5xx. Both are preserved and must be disclosed when summarizing the experiment.

**No original-log latency:** P95 from replay cannot be interpreted as the original web servers' response time.
