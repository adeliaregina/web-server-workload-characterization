#!/usr/bin/env python3
"""Merge Table 5 and Table 6 results of several datasets into one table.
Usage: python3 combine.py NAME1=results_dir1 NAME2=results_dir2 ... > cross_dataset.csv"""
import sys, pandas as pd
rows = []
for arg in sys.argv[1:]:
    name, d = arg.split("=", 1)
    t5 = pd.read_csv(f"{d}/table5_test_parameters.csv", dtype=str).set_index("Parameter")
    t6 = pd.read_csv(f"{d}/table6_intervals.csv", dtype=str).set_index("Measure")
    ci = t6.columns[1]
    rr = t6.index[2]; dd = t6.index[3]
    rows.append({"dataset": name,
                 "regular_median_rate": t5.loc["Median rate (req/min)"].iloc[0], "busy_peak_rate": t5.loc["Peak rate (req/min)"].iloc[1],
                 "ratio_of_medians": t6.loc[rr, "Estimate"], "ratio_95ci": t6.loc[rr, ci],
                 "d5xx_pp": t6.loc[dd, "Estimate"], "d5xx_95ci": t6.loc[dd, ci]})
pd.DataFrame(rows).to_csv(sys.stdout, index=False)
