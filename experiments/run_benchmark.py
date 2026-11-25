"""run_benchmark.py — Automated 4-Strategy Benchmark Harness."""

import argparse
import asyncio
import time
from experiments.runlog import Run
from src.resource_mgmt.gpu_monitor import GPUMonitor
from src.resource_mgmt.metrics_logger import MetricsLogger
from src.resource_mgmt.strategy_a_resident import StrategyAllResident
from src.resource_mgmt.strategy_b_naive import StrategyNaiveLoadUnload
from src.resource_mgmt.strategy_c_pinned import StrategyPinnedMemorySwap
from src.resource_mgmt.strategy_d_prefetch import StrategyPrefetch


async def run_strategy_benchmark(strategy_obj, rounds: int, logger: MetricsLogger, gpu_monitor: GPUMonitor):
    service_seq = ["speech_stt", "speech_llm", "speech_tts"]
    print(f"\n--- Testing Strategy: {strategy_obj.name} ({rounds} rounds) ---")

    for r in range(1, rounds + 1):
        run_id = f"{strategy_obj.strategy_id}_r{r:03d}"
        gpu_monitor.start_sampling()

        t0 = time.perf_counter()
        res = await strategy_obj.execute_turn(service_seq)
        t_e2e_ms = (time.perf_counter() - t0) * 1000.0

        peak_vram = gpu_monitor.stop_sampling()

        logger.log_record(
            run_id=run_id,
            strategy=strategy_obj.name,
            mode="conversation",
            turn_index=r,
            swap_duration_ms=res.get("total_swap_ms", 0.0),
            infer_duration_ms=t_e2e_ms - res.get("total_swap_ms", 0.0),
            e2e_latency_ms=t_e2e_ms,
            peak_vram_mb=peak_vram,
            status="SUCCESS",
        )
        print(f"  Round {r}/{rounds} | Swap: {res.get('total_swap_ms', 0):.1f}ms | Latency: {t_e2e_ms:.1f}ms | Peak VRAM: {peak_vram:.1f}MB")


def main():
    parser = argparse.ArgumentParser(description="Run GPU Strategy Benchmarks")
    parser.add_argument("--rounds", type=int, default=10, help="Number of repetitions (N>=10)")
    parser.add_argument("--strategy", default="all", choices=["all", "resident", "naive", "pinned", "prefetch"])
    args = parser.parse_args()

    with Run("benchmark_strategies", args={"rounds": args.rounds, "strategy": args.strategy}) as run:
        metrics_logger = MetricsLogger(output_dir=str(run.run_dir), filename_prefix="benchmark_data")
        gpu_monitor = GPUMonitor()

        strategies = []
        if args.strategy in ["all", "resident"]:
            strategies.append(StrategyAllResident())
        if args.strategy in ["all", "naive"]:
            strategies.append(StrategyNaiveLoadUnload())
        if args.strategy in ["all", "pinned"]:
            strategies.append(StrategyPinnedMemorySwap())
        if args.strategy in ["all", "prefetch"]:
            strategies.append(StrategyPrefetch())

        loop = asyncio.get_event_loop()
        for strat in strategies:
            loop.run_until_complete(run_strategy_benchmark(strat, args.rounds, metrics_logger, gpu_monitor))

        gpu_monitor.close()


if __name__ == "__main__":
    main()
