"""calculate_stats.py — Descriptive Statistics Calculator for Benchmark CSV Results."""

import argparse
from pathlib import Path
import pandas as pd


def calculate_descriptive_stats(csv_path: str):
    p = Path(csv_path)
    if not p.exists():
        print(f"[!] File not found: {csv_path}")
        return

    df = pd.read_csv(p)
    print(f"\n{'='*70}\nSTATISTIK DESKRIPTIF BENCHMARK: {p.name}\n{'='*70}")

    metrics = ["swap_duration_ms", "infer_duration_ms", "e2e_latency_ms", "peak_vram_mb"]

    grouped = df.groupby("strategy")
    for strat, group in grouped:
        print(f"\n[Strategi: {strat}] (Total Sampel: {len(group)})")
        summary = group[metrics].agg(["mean", "median", "std", "min", "max"]).T
        summary.columns = ["Rata-rata", "Median", "Std Dev", "Min", "Max"]
        print(summary.round(2).to_string())

    print("\n" + "="*70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate descriptive stats from benchmark CSV")
    parser.add_argument("csv_path", help="Path to results CSV file")
    args = parser.parse_args()
    calculate_descriptive_stats(args.csv_path)
