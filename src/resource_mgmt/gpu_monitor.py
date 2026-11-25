"""PyNVML GPU Monitor for real-time VRAM, Temperature, and Power Telemetry."""

import logging
import threading
import time
from typing import Callable, Dict, Optional

logger = logging.getLogger("resource_mgmt.gpu")

try:
    import pynvml
    PYNVML_AVAILABLE = True
except ImportError:
    PYNVML_AVAILABLE = False
    logger.warning("pynvml is not installed; running GPU monitor in simulation/fallback mode.")


class GPUMonitor:
    def __init__(self, device_index: int = 0, sample_interval_ms: int = 50):
        self.device_index = device_index
        self.sample_interval = sample_interval_ms / 1000.0
        self._is_running = False
        self._thread: Optional[threading.Thread] = None
        self._nvml_initialized = False
        self._handle = None
        self.peak_vram_mb: float = 0.0
        self.current_vram_mb: float = 0.0

        if PYNVML_AVAILABLE:
            try:
                pynvml.nvmlInit()
                self._handle = pynvml.nvmlDeviceGetHandleByIndex(self.device_index)
                self._nvml_initialized = True
                logger.info("NVML initialized successfully for GPU device %d.", self.device_index)
            except Exception as e:
                logger.warning("Failed to initialize NVML: %s. Using fallback.", e)

    def get_memory_info(self) -> Dict[str, float]:
        """Returns {used_mb, total_mb, free_mb}."""
        if self._nvml_initialized and self._handle:
            try:
                info = pynvml.nvmlDeviceGetMemoryInfo(self._handle)
                used_mb = info.used / (1024 ** 2)
                total_mb = info.total / (1024 ** 2)
                free_mb = info.free / (1024 ** 2)
                return {"used_mb": round(used_mb, 2), "total_mb": round(total_mb, 2), "free_mb": round(free_mb, 2)}
            except Exception as e:
                logger.error("Error reading NVML memory: %s", e)

        # Fallback simulation
        return {"used_mb": 1024.0, "total_mb": 8192.0, "free_mb": 7168.0}

    def start_sampling(self, callback: Optional[Callable[[Dict[str, float]], None]] = None):
        if self._is_running:
            return

        self._is_running = True
        self.peak_vram_mb = 0.0

        def _sample_loop():
            while self._is_running:
                mem = self.get_memory_info()
                used = mem["used_mb"]
                self.current_vram_mb = used
                if used > self.peak_vram_mb:
                    self.peak_vram_mb = used

                if callback:
                    callback(mem)

                time.sleep(self.sample_interval)

        self._thread = threading.Thread(target=_sample_loop, daemon=True)
        self._thread.start()
        logger.info("Continuous GPU sampling started (interval: %.3fs)", self.sample_interval)

    def stop_sampling(self) -> float:
        self._is_running = False
        if self._thread:
            self._thread.join(timeout=1.0)
        logger.info("GPU sampling stopped. Peak VRAM observed: %.2f MB", self.peak_vram_mb)
        return self.peak_vram_mb

    def close(self):
        self.stop_sampling()
        if self._nvml_initialized:
            try:
                pynvml.nvmlShutdown()
            except Exception:
                pass
