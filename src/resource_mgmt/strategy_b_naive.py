"""Strategy (b): Naive Load/Unload — Cold load from Disk SSD & immediate unload."""

import asyncio
import time
from typing import Any, Dict
from src.resource_mgmt.strategy_base import BaseGPUStrategy


class StrategyNaiveLoadUnload(BaseGPUStrategy):
    def __init__(self):
        super().__init__("strategy_b_naive", "Naive Load/Unload")

    async def prepare_service(self, service_id: str, **kwargs) -> Dict[str, Any]:
        t0 = time.perf_counter()
        # Simulate loading from disk SSD
        load_delay = kwargs.get("simulated_load_s", 0.8)
        await asyncio.sleep(load_delay)
        swap_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "strategy": self.strategy_id,
            "service_id": service_id,
            "swap_duration_ms": round(swap_ms, 2),
            "status": "READY",
        }

    async def release_service(self, service_id: str, **kwargs) -> Dict[str, Any]:
        t0 = time.perf_counter()
        # Simulate unloading & VRAM cleanup
        unload_delay = kwargs.get("simulated_unload_s", 0.2)
        await asyncio.sleep(unload_delay)
        unload_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "strategy": self.strategy_id,
            "service_id": service_id,
            "unload_duration_ms": round(unload_ms, 2),
            "unloaded": True,
        }

    async def execute_turn(self, service_sequence: list, **kwargs) -> Dict[str, Any]:
        t_start = time.perf_counter()
        total_swap_ms = 0.0

        for svc in service_sequence:
            prep = await self.prepare_service(svc, **kwargs)
            total_swap_ms += prep["swap_duration_ms"]
            await self.release_service(svc, **kwargs)

        t_e2e_ms = (time.perf_counter() - t_start) * 1000.0
        return {
            "strategy": self.strategy_id,
            "total_swap_ms": round(total_swap_ms, 2),
            "turn_duration_ms": round(t_e2e_ms, 2),
        }
