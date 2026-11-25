"""Strategy (a): All-Resident — All models permanently resident in VRAM."""

import time
from typing import Any, Dict
from src.resource_mgmt.strategy_base import BaseGPUStrategy


class StrategyAllResident(BaseGPUStrategy):
    def __init__(self):
        super().__init__("strategy_a_resident", "All-Resident")
        self.resident_services = set()

    async def prepare_service(self, service_id: str, **kwargs) -> Dict[str, Any]:
        # Under Strategy A, models are already in VRAM; swap duration is virtually 0
        self.resident_services.add(service_id)
        return {
            "strategy": self.strategy_id,
            "service_id": service_id,
            "swap_duration_ms": 0.0,
            "status": "READY",
        }

    async def release_service(self, service_id: str, **kwargs) -> Dict[str, Any]:
        # Under Strategy A, models are NOT unloaded between turns
        return {
            "strategy": self.strategy_id,
            "service_id": service_id,
            "unloaded": False,
        }

    async def execute_turn(self, service_sequence: list, **kwargs) -> Dict[str, Any]:
        t0 = time.perf_counter()
        total_swap_ms = 0.0
        # Instant turnaround
        t_e2e_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "strategy": self.strategy_id,
            "total_swap_ms": total_swap_ms,
            "turn_duration_ms": t_e2e_ms,
        }
