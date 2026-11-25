"""Request Router: forwards infer/health requests to backend service adapters."""

import logging
from typing import Any, Dict
import httpx

from src.orchestrator.registry import ServiceRegistry
from src.orchestrator.lifecycle import LifecycleStateMachine

logger = logging.getLogger("orchestrator.router")


class RequestRouter:
    def __init__(self, registry: ServiceRegistry, lifecycle: LifecycleStateMachine):
        self.registry = registry
        self.lifecycle = lifecycle
        self.client = httpx.AsyncClient(timeout=30.0)

    async def forward_infer(self, service_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        service = self.registry.get_service(service_id)
        if not service:
            raise ValueError(f"Service '{service_id}' not found in registry.")

        url = f"{service.endpoint.rstrip('/')}/infer"
        logger.info("Routing infer request to '%s' at %s", service_id, url)

        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("HTTP error while calling service '%s': %s", service_id, str(e))
            raise

    async def close(self):
        await self.client.aclose()
