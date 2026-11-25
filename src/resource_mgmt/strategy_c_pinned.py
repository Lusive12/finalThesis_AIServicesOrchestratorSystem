"""Strategy (c): Pinned-Memory Swap — Weights held in Host RAM, DMA transfer via PCIe."""

import asyncio
import time
from typing import Any, Dict
from src.resource_mgmt.strategy_base import BaseGPUStrategy


class StrategyPinnedMemorySwap(BaseGPUStrategy):
    def __init__(self):
        super().__init__("strategy_c_pinned", "Pinned-Memory Swap")

    async def prepare_service(self, service_id: str, **kwargs) -> Dict[str, Any]:
        t0 = time.perf_counter()
        # Fast transfer over PCIe Gen4 x8 (~15.8 GB/s)
        pcie_transfer_delay = kwargs.get("simulated_pcie_delay_s", 0.15)
        await asyncio.sleep(pcie_transfer_delay)
        swap_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "strategy": self.strategy_id,
            "service_id": service_id,
            "swap_duration_ms": round(swap_ms, 2),
            "status": "READY",
        }

    async def release_service(self, service_id: str, **kwargs) -> Dict[str, Any]:
        # Fast release; weights retained in Host RAM
        return {
            "strategy": self.strategy_id,
            "service_id": service_id,
            "kept_in_host_ram": True,
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
