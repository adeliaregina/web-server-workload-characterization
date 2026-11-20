# Reproducible workload characterization from web server access logs

**Companion research code and output files** for the manuscript *Reproducible Workload Characterization of Web Server Logs for Nonfunctional Requirements: Validation on Two Public Traces with Test-Bed Replay* (Adelia Regina Putri, Sean Fadel, and Sukriadi).

This repository packages the **original Python programs and output files provided by the authors** with documentation and dependency metadata. It does not contain the raw access logs. It is **not evidence of workload or performance of Universitas Lamappapoleonro's SIAKAD**.

## What is included

| Item | Purpose |
| --- | --- |
| `log_pipeline.py` | CLF parsing, reconciliation, workload metrics, moving-block bootstrap, and scenario export |
| `daily_counts.py` | Daily/hourly counts used to inspect and select windows |
| `testbed_app.py` | Local synthetic HTTP service (8 workers in the reported experiments) |
| `replay.py` | Open-loop Poisson load replay to the local test bed |
| `bench.py` | Parse/aggregation runtime measurements |
| `combine.py` | Merge summary measures across traces |
| `test_pipeline.py`, `smoke_test.py`, `make_synthetic.py` | Correctness and end-to-end tests using synthetic data |
| `run_replay_SASK.bat`, `run_replay_NASA.bat` | Windows replay command scripts used by the authors |
| `hasil_SASK/`, `hasil_NASA/` | Published scenarios, analysis tables, replay summaries, per-request replay results, and run logs |
| `SASK_daily.csv`, `SASK_hourly.csv`, `NASA_daily.csv`, `NASA_hourly.csv` | Archived daily/hourly traffic counts |
| `RESULTS_INDEX.md` | Map of result files and manuscript interpretation |
| `DATA_SOURCES.md` | Data provenance, omitted files, and privacy guidance |
| `PANDUAN_UPLOAD_GITHUB.md` | Step-by-step GitHub upload guide in Indonesian |

**No source-code license has been selected by the authors.** Please decide on a license before encouraging reuse or redistribution. See `LICENSE_NOTICE.md`.

## Quick start (without raw log files)

Requires Python 3.12+ for the manuscript environment. The scripts are also compatible with the versions available in the verification environment, but exact performance figures are hardware-dependent.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python test_pipeline.py
python smoke_test.py
```

The two tests use **synthetic data**, not the historical NASA or Saskatchewan datasets. They verify that the processing and replay workflow runs.

## Reproduce analysis from the public traces

Download the original traces from the Internet Traffic Archive and respect the source's conditions. Place the decompressed files at the repository root using the following filenames:

- `usask_access_log` (Saskatchewan)
- `NASA_access_log_Jul95` (NASA)

If you download compressed files ending in `.gz`, the included `extract_gz.py` can extract matching `.gz` files in the repository root. **Check the source, size and integrity before running.**

Run the Saskatchewan pipeline (Windows Command Prompt commands shown as single lines):

```bash
python log_pipeline.py usask_access_log --tz Etc/GMT+6 --dataset-name SASK --a "1995-07-18 08:00" "1995-07-18 18:00" --a-label Break --b "1995-10-24 08:00" "1995-10-24 18:00" --b-label Term --out hasil_SASK --top 15
```

Run the NASA pipeline:

```bash
python log_pipeline.py NASA_access_log_Jul95 --tz Etc/GMT+4 --dataset-name NASA --a "1995-07-20 08:00" "1995-07-20 18:00" --a-label Regular --b "1995-07-13 08:00" "1995-07-13 18:00" --b-label Spike --out hasil_NASA --top 15
```

These commands **overwrite analysis output files** in the named folders. Back up the provided results before rerunning. The code's default bootstrap configuration is 10-minute blocks, 2,000 resamples, with fixed seed `20261119`.

For replay, start a local server in one terminal:

```bash
python testbed_app.py --workers 8
```

In a second terminal, for example:

```bash
python replay.py hasil_NASA/scenario_a.json --ref hasil_NASA/scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 1 --out hasil_NASA/replay_a_s1
python replay.py hasil_NASA/scenario_b.json --ref hasil_NASA/scenario_b.json --peak-rps 300 --bin-seconds 1 --seed 1 --out hasil_NASA/replay_b_s1
```

For the full six-run experiments on Windows, see `run_replay_SASK.bat` and `run_replay_NASA.bat`. Note that `run_replay_NASA.bat` starts with the repeat of Saskatchewan break seed 1 before the NASA runs. These scripts take substantial time. The server binds to `127.0.0.1`, and replay should be directed only at a test system you own or are explicitly authorized to test.

## Interpretation and limits

- The original Common Log Format (CLF) files do **not** record request duration. Log-derived P95 response times are therefore unavailable.
- Replay P95 values measure only the **synthetic local test bed**; they are not SIAKAD or NASA/Saskatchewan historical server latencies.
- The historical traces date to **1995**, so they validate the workflow, not current academic traffic.
- One pair of same-weekday, same-hours windows was selected per trace. Block-bootstrap intervals describe **within-window minute variability**, not day-to-day generalization.
- One Saskatchewan break run (`replay_a_s1`) was anomalous and was repeated; both runs are retained.
- The load generator and test bed ran on one laptop. The generator seed fixes its request schedule, but the test bed uses stochastic service times and the host environment can vary. **Latency outputs need not match exactly on another machine.**
- A route is approximated by the first path segment and static assets are identified by file extension.
- The included results are provided as author-supplied outputs, not independently recalculated from the raw 1995 logs in this packaging step.

## Reuse and citation

Use `CITATION.cff` as a starting point for citing this research. Update the final article title, publication metadata, DOI, and license when available. Credit the original trace contributors and respect the archive's terms.
