"""Mode Controller: handles high-level kiosk mode transitions and exclusivity barriers."""

import logging
from pathlib import Path
import time
from typing import Dict, List, Optional
import yaml

from src.orchestrator.models import ModeSwitchResponse
from src.orchestrator.registry import ServiceRegistry
from src.orchestrator.lifecycle import LifecycleStateMachine

logger = logging.getLogger("orchestrator.mode")


class ModeController:
    def __init__(
        self,
        registry: ServiceRegistry,
        lifecycle: LifecycleStateMachine,
        config_path: str = "configs/modes.yaml",
    ):
        self.registry = registry
        self.lifecycle = lifecycle
        self.config_path = Path(config_path)
        self.modes: Dict[str, dict] = {}
        self.current_mode: str = "standby"
        self.load_modes()

    def load_modes(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Modes config not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        self.modes = raw.get("modes", {})

    async def switch_mode(self, target_mode: str, force: bool = False) -> ModeSwitchResponse:
        t_start = time.perf_counter()

        if target_mode not in self.modes:
            raise ValueError(f"Unknown mode: {target_mode}. Valid modes: {list(self.modes.keys())}")

        prev_mode = self.current_mode
        target_info = self.modes[target_mode]
        target_services = target_info.get("active_services", [])
        is_exclusive = target_info.get("exclusive_mode", False)

        logger.info(
            "Switching mode from '%s' to '%s' (Exclusive: %s)",
            prev_mode,
            target_mode,
            is_exclusive,
        )

        # Jika mode target bersifat eksklusif, hentikan layanan sebelumnya terlebih dahulu
        if is_exclusive:
            logger.info("Executing barrier shutdown for previous services...")
            # Simulasi penghentian layanan aktif sebelumnya
            for s_id in self.modes.get(prev_mode, {}).get("active_services", []):
                if s_id not in target_services:
                    logger.info("Unloading non-target service: %s", s_id)

        self.current_mode = target_mode
        t_duration_ms = (time.perf_counter() - t_start) * 1000.0

        return ModeSwitchResponse(
            status="SUCCESS",
            previous_mode=prev_mode,
            current_mode=target_mode,
            transition_duration_ms=round(t_duration_ms, 2),
            active_services=target_services,
        )
