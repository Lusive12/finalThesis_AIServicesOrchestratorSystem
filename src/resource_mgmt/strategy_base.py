"""Base class for GPU Lifecycle Management Strategies."""

from abc import ABC, abstractmethod
import logging
from typing import Any, Dict

logger = logging.getLogger("resource_mgmt.strategy")


class BaseGPUStrategy(ABC):
    def __init__(self, strategy_id: str, name: str):
        self.strategy_id = strategy_id
        self.name = name

    @abstractmethod
    async def prepare_service(self, service_id: str, **kwargs) -> Dict[str, Any]:
        """Prepares or swaps in the requested service model to GPU VRAM."""
        pass

    @abstractmethod
    async def release_service(self, service_id: str, **kwargs) -> Dict[str, Any]:
        """Releases the service model from GPU VRAM."""
        pass

    @abstractmethod
    async def execute_turn(self, service_sequence: list, **kwargs) -> Dict[str, Any]:
        """Executes a complete multi-model turn under this strategy."""
        pass
