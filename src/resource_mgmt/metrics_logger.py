"""Metrics Logger: records the 5 core thesis evaluation metrics into CSV & JSONL."""

import csv
import json
import os
from pathlib import Path
import time
from typing import Any, Dict, Optional


class MetricsLogger:
    CSV_HEADERS = [
        "run_id",
        "timestamp",
        "strategy",
        "mode",
        "turn_index",
        "swap_duration_ms",
        "infer_duration_ms",
        "e2e_latency_ms",
        "peak_vram_mb",
        "status",
        "error_message",
    ]

    def __init__(self, output_dir: str = "results", filename_prefix: str = "benchmark"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        self.csv_path = self.output_dir / f"{filename_prefix}_{timestamp_str}.csv"
        self.jsonl_path = self.output_dir / f"{filename_prefix}_{timestamp_str}.jsonl"
        self._init_csv()

    def _init_csv(self):
        if not self.csv_path.exists():
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.CSV_HEADERS)

    def log_record(
        self,
        run_id: str,
        strategy: str,
        mode: str,
        turn_index: int,
        swap_duration_ms: float,
        infer_duration_ms: float,
        e2e_latency_ms: float,
        peak_vram_mb: float,
        status: str = "SUCCESS",
        error_message: Optional[str] = None,
    ):
        record = {
            "run_id": run_id,
            "timestamp": time.time(),
            "strategy": strategy,
            "mode": mode,
            "turn_index": turn_index,
            "swap_duration_ms": round(swap_duration_ms, 2),
            "infer_duration_ms": round(infer_duration_ms, 2),
            "e2e_latency_ms": round(e2e_latency_ms, 2),
            "peak_vram_mb": round(peak_vram_mb, 2),
            "status": status,
            "error_message": error_message or "",
        }

        # Write CSV row
        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_HEADERS)
            writer.writerow(record)

        # Write JSONL record
        with open(self.jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
