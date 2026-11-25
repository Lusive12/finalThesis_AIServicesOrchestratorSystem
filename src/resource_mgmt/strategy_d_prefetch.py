"""Strategy (d): Prefetch — Speculative background loading for latency hiding."""

import asyncio
import time
from typing import Any, Dict
from src.resource_mgmt.strategy_base import BaseGPUStrategy


class StrategyPrefetch(BaseGPUStrategy):
    def __init__(self):
        super().__init__("strategy_d_prefetch", "Prefetch")

    async def prepare_service(self, service_id: str, **kwargs) -> Dict[str, Any]:
        # Background prefetch overlaps with active model compute
        t0 = time.perf_counter()
        prefetch_hidden_delay = kwargs.get("simulated_prefetch_delay_s", 0.05)
        await asyncio.sleep(prefetch_hidden_delay)
        perceived_swap_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "strategy": self.strategy_id,
            "service_id": service_id,
            "swap_duration_ms": round(perceived_swap_ms, 2),
            "status": "READY",
        }

    async def release_service(self, service_id: str, **kwargs) -> Dict[str, Any]:
        return {
            "strategy": self.strategy_id,
            "service_id": service_id,
            "unloaded": True,
        }

    async def execute_turn(self, service_sequence: list, **kwargs) -> Dict[str, Any]:
        t_start = time.perf_counter()
        total_perceived_swap_ms = 0.0

        for svc in service_sequence:
            prep = await self.prepare_service(svc, **kwargs)
            total_perceived_swap_ms += prep["swap_duration_ms"]
            await self.release_service(svc, **kwargs)

        t_e2e_ms = (time.perf_counter() - t_start) * 1000.0
        return {
            "strategy": self.strategy_id,
            "total_swap_ms": round(total_perceived_swap_ms, 2),
            "turn_duration_ms": round(t_e2e_ms, 2),
        }
