"""runlog.py — Structured Experiment Runner & Provenance Logger.

Inspired by Ferdie's disciplined runlog pattern:
Creates results/<YYYYMMDD_HHMMSS>_<name>_<tag>/ with:
- meta.json (arguments, SHA-256 of inputs, python/git version, GPU info, status)
- run.log (terminal copy)
- results.csv / summary.json
"""

import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional


def compute_sha256(filepath: str) -> Optional[str]:
    p = Path(filepath)
    if not p.exists() or not p.is_file():
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def get_git_commit() -> str:
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "unknown"


def get_gpu_info() -> str:
    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"],
            capture_output=True,
            text=True,
        )
        return res.stdout.strip()
    except Exception:
        return "no_nvidia_gpu_detected"


class Run:
    def __init__(self, name: str, args: Optional[Dict[str, Any]] = None, inputs: Optional[List[str]] = None, tag: str = "exp"):
        self.name = name
        self.args = args or {}
        self.inputs = inputs or []
        self.tag = tag
        self.start_time = time.time()
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        self.dir_name = f"{timestamp_str}_{self.name}_{self.tag}"
        self.run_dir = Path("results") / self.dir_name
        self.meta_file = self.run_dir / "meta.json"
        self.log_file = self.run_dir / "run.log"

    def __enter__(self):
        self.run_dir.mkdir(parents=True, exist_ok=True)
        # Compute input SHA-256
        input_hashes = {}
        for inp in self.inputs:
            h = compute_sha256(inp)
            if h:
                input_hashes[inp] = h

        self.meta = {
            "name": self.name,
            "tag": self.tag,
            "status": "running",
            "start_time": self.start_time,
            "command": " ".join(sys.argv),
            "args": self.args,
            "git_commit": get_git_commit(),
            "gpu_info": get_gpu_info(),
            "python_version": platform.python_version(),
            "os": f"{platform.system()} {platform.release()}",
            "input_hashes": input_hashes,
        }
        # Tulis meta.json di AWAL run (status: running)
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, indent=2)

        print(f"[*] Experiment run started: {self.run_dir}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.meta["duration_seconds"] = round(duration, 3)
        if exc_type is None:
            self.meta["status"] = "ok"
            print(f"[✓] Experiment run completed successfully in {duration:.2f}s")
        else:
            self.meta["status"] = "error"
            self.meta["error_message"] = str(exc_val)
            print(f"[✗] Experiment run failed with error: {exc_val}")

        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, indent=2)
        return False
