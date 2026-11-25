#!/usr/bin/env python3
"""run.py — Unified CLI runner for Smart Kiosk Thesis Project.

Usage:
    python run.py server           # Run FastAPI Orchestrator & Gateway
    python run.py kiosk            # Launch Chromium Kiosk (Linux)
    python run.py benchmark        # Run 4-strategy benchmark
    python run.py audit-hardware   # Run M0 Hardware verification
"""

import argparse
import os
import subprocess
import sys


def cmd_server(args):
    print(f"[*] Menjalankan Orchestrator Gateway di {args.host}:{args.port}...")
    try:
        import uvicorn
        uvicorn.run("src.orchestrator.main:app", host=args.host, port=args.port, reload=args.reload)
    except ImportError:
        print("[!] Error: uvicorn belum terpasang. Jalankan: pip install -r requirements.txt")
        sys.exit(1)


def cmd_kiosk(args):
    kiosk_url = f"http://{args.host}:{args.port}/ui/index.html"
    print(f"[*] Meluncurkan Chromium Kiosk Mode menuju: {kiosk_url}")
    cmd = [
        "chromium-browser",
        "--kiosk",
        "--noerrdialogs",
        "--disable-infobars",
        "--check-for-update-interval=31536000",
        kiosk_url,
    ]
    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        print(f"[!] Error: chromium-browser tidak ditemukan di PATH. Buka manual di browser: {kiosk_url}")


def cmd_benchmark(args):
    print(f"[*] Menjalankan Automated Benchmark Harness (Rounds: {args.rounds}, Strategy: {args.strategy})...")
    benchmark_script = os.path.join("experiments", "run_benchmark.py")
    if os.path.exists(benchmark_script):
        cmd = [sys.executable, benchmark_script, "--rounds", str(args.rounds), "--strategy", args.strategy]
        subprocess.run(cmd)
    else:
        print(f"[!] File benchmark {benchmark_script} belum siap.")


def cmd_audit(args):
    print("[*] Melakukan Audit Fisik Hardware Mini PC & Periferal Kiosk (M0)...")
    print("-" * 60)
    # Check GPU
    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv"],
            capture_output=True,
            text=True,
        )
        print("[GPU Info]")
        print(res.stdout.strip())
    except Exception as e:
        print(f"[!] Gagal menjalankan nvidia-smi: {e}")

    # Check CPU / Memory info
    print("\n[Audit selesai. Simpan catatan hasil audit ke docs/checkpoint.md]")


def main():
    parser = argparse.ArgumentParser(
        description="Smart Kiosk AI Service Orchestration — Unified CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-perintah yang tersedia")

    # server
    p_server = subparsers.add_parser("server", help="Jalankan FastAPI Backend Orchestrator")
    p_server.add_argument("--host", default="127.0.0.1", help="Host binding")
    p_server.add_argument("--port", type=int, default=8000, help="Port binding")
    p_server.add_argument("--reload", action="store_true", help="Enable hot reload")

    # kiosk
    p_kiosk = subparsers.add_parser("kiosk", help="Luncurkan Chromium Kiosk Mode")
    p_kiosk.add_argument("--host", default="127.0.0.1")
    p_kiosk.add_argument("--port", type=int, default=8000)

    # benchmark
    p_bench = subparsers.add_parser("benchmark", help="Jalankan benchmark komparasi 4 strategi")
    p_bench.add_argument("--rounds", type=int, default=10, help="Jumlah putaran pengulangan")
    p_bench.add_argument("--strategy", default="all", choices=["all", "resident", "naive", "pinned", "prefetch"])

    # audit-hardware
    subparsers.add_parser("audit-hardware", help="Audit hardware dan status GPU (M0)")

    args = parser.parse_args()

    if args.command == "server":
        cmd_server(args)
    elif args.command == "kiosk":
        cmd_kiosk(args)
    elif args.command == "benchmark":
        cmd_benchmark(args)
    elif args.command == "audit-hardware":
        cmd_audit(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
