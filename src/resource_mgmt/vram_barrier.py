"""VRAM Barrier: ensures GPU memory drops to baseline before exclusive models load."""

import asyncio
import logging
import time
from typing import Optional
from src.resource_mgmt.gpu_monitor import GPUMonitor

logger = logging.getLogger("resource_mgmt.barrier")


class VRAMBarrier:
    def __init__(self, gpu_monitor: GPUMonitor, baseline_vram_threshold_mb: float = 1200.0):
        self.gpu_monitor = gpu_monitor
        self.baseline_threshold_mb = baseline_vram_threshold_mb

    async def wait_for_vram_release(
        self,
        timeout_seconds: float = 5.0,
        poll_interval_s: float = 0.05,
    ) -> bool:
        """Polls NVML memory until VRAM drops below the safe threshold."""
        t_start = time.perf_counter()
        logger.info(
            "Barrier active: waiting for VRAM <= %.1f MB (Timeout: %.1fs)",
            self.baseline_threshold_mb,
            timeout_seconds,
        )

        while (time.perf_counter() - t_start) < timeout_seconds:
            mem = self.gpu_monitor.get_memory_info()
            used = mem["used_mb"]

            if used <= self.baseline_threshold_mb:
                elapsed = time.perf_counter() - t_start
                logger.info("Barrier cleared! VRAM dropped to %.1f MB in %.3fs", used, elapsed)
                return True

            await asyncio.sleep(poll_interval_s)

        current = self.gpu_monitor.get_memory_info()["used_mb"]
        logger.warning(
            "Barrier timeout after %.1fs. VRAM still at %.1f MB (threshold: %.1f MB)",
            timeout_seconds,
            current,
            self.baseline_threshold_mb,
        )
        return False
