# Historical data sources and redistribution notes

This study uses two **public historical web-server traces** distributed by the Internet Traffic Archive:

1. **University of Saskatchewan HTTP** trace, June–December 1995, `usask_access_log` (2,408,625 input lines in the author-provided results).
2. **NASA Kennedy Space Center HTTP** trace, July 1995, `NASA_access_log_Jul95` (1,891,715 input lines in the author-provided results).

Source portal: https://ita.ee.lbl.gov/

The uploaded research kit contained raw and compressed copies of both logs. **They are deliberately not included in the GitHub package**, both to keep the repository manageable and to avoid rehosting raw client-level records. Download them from their original source if permitted, verify source conditions, and keep them locally. The `.gitignore` excludes the raw log filenames.

Derived aggregate tables and scenario files are included under `hasil_SASK/` and `hasil_NASA/`. The replay request-level CSVs contain the synthetic test-bed request paths, response status and measured duration, **not the original client IP addresses**.

The manuscript does **not** analyze any Universitas Lamappapoleonro SIAKAD access log. Do not label these files as SIAKAD data.
