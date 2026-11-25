"""Kiosk service facade. Mock behavior is isolated from real adapter calls."""
import asyncio
import os
from typing import Any, Dict
import httpx

from src.orchestrator.models import ServiceState
from src.orchestrator.registry import ServiceRegistry
from src.orchestrator.lifecycle import LifecycleStateMachine
from src.orchestrator.request_router import RequestRouter


SERVICE_MAP = {
    "ai_photobooth": "ai_photobooth",
    "virtual_tryon": "virtual_tryon",
    "fashion_recommender": "fashion_recommender",
    "speech_llm": "speech_llm",
}


class KioskServices:
    def __init__(self, registry: ServiceRegistry, lifecycle: LifecycleStateMachine, router: RequestRouter):
        self.registry = registry
        self.lifecycle = lifecycle
        self.router = router
        self.mock_mode = os.getenv("KIOSK_MOCK_MODE", "true").lower() in {"1", "true", "yes", "on"}
        self.load_delay = max(0.1, float(os.getenv("KIOSK_MOCK_LOAD_SECONDS", "1.4")))
        self._tasks: Dict[str, asyncio.Task] = {}
        self._activation_lock = asyncio.Lock()
        self._inference_locks: Dict[str, asyncio.Lock] = {}

    def resolve(self, service_id: str) -> str:
        resolved = SERVICE_MAP.get(service_id)
        if not resolved or not self.registry.get_service(resolved):
            raise ValueError(f"Unknown kiosk service: {service_id}")
        return resolved

    def state(self, service_id: str) -> dict:
        resolved = self.resolve(service_id)
        return {"id": service_id, "state": self.lifecycle.get_state(resolved).value, "mock_mode": self.mock_mode}

    async def start(self, service_id: str) -> dict:
        resolved = self.resolve(service_id)
        state = self.lifecycle.get_state(resolved)
        if state in (ServiceState.READY, ServiceState.STARTING, ServiceState.BUSY):
            return self.state(service_id)
        if state == ServiceState.ERROR:
            self.lifecycle.transition_to(resolved, ServiceState.STOPPED)
        self.lifecycle.transition_to(resolved, ServiceState.STARTING)
        self._tasks[resolved] = asyncio.create_task(self._initialize(resolved))
        return self.state(service_id)

    async def _initialize(self, service_id: str) -> None:
        service = self.registry.get_service(service_id)
        try:
            async with self._activation_lock:
                # Keep exclusive GPU services serialized and release conflicts through
                # their adapter contract; this facade never manipulates processes.
                for other in self.registry.list_services():
                    if other.id == service_id:
                        continue
                    other_state = self.lifecycle.get_state(other.id)
                    conflicts = service.exclusive_gpu or other.exclusive_gpu
                    if conflicts and other_state in (ServiceState.READY, ServiceState.BUSY):
                        self.lifecycle.transition_to(other.id, ServiceState.STOPPING)
                        if not self.mock_mode:
                            async with httpx.AsyncClient(timeout=20.0) as client:
                                response = await client.post(f"{other.endpoint.rstrip('/')}/unload", json={"force_cleanup": True})
                                response.raise_for_status()
                        self.lifecycle.transition_to(other.id, ServiceState.STOPPED)

                if self.mock_mode:
                    await asyncio.sleep(self.load_delay)
                    self.lifecycle.transition_to(service_id, ServiceState.READY)
                    return
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.post(f"{service.endpoint.rstrip('/')}/load", json={})
                    response.raise_for_status()
                    deadline = asyncio.get_running_loop().time() + float(os.getenv("ORCHESTRATOR_READY_TIMEOUT", "90"))
                    while asyncio.get_running_loop().time() < deadline:
                        try:
                            health = await client.get(f"{service.endpoint.rstrip('/')}/health")
                            if health.is_success and str(health.json().get("status", "")).upper() == "READY":
                                self.lifecycle.transition_to(service_id, ServiceState.READY)
                                return
                        except (httpx.HTTPError, ValueError):
                            pass
                        await asyncio.sleep(1)
                    raise TimeoutError("Service readiness timed out")
        except Exception:
            self.lifecycle.transition_to(service_id, ServiceState.ERROR)

    async def health(self, service_id: str) -> dict:
        resolved = self.resolve(service_id)
        state = self.lifecycle.get_state(resolved)
        if self.mock_mode:
            return {**self.state(service_id), "healthy": state == ServiceState.READY, "source": "mock"}
        service = self.registry.get_service(resolved)
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{service.endpoint.rstrip('/')}/health")
                response.raise_for_status()
                return {**response.json(), "id": service_id, "mock_mode": False, "healthy": True}
        except (httpx.HTTPError, ValueError) as exc:
            return {**self.state(service_id), "healthy": False, "error": str(exc)}

    async def infer(self, service_id: str, payload: Dict[str, Any]) -> dict:
        resolved = self.resolve(service_id)
        if self.lifecycle.get_state(resolved) != ServiceState.READY:
            raise RuntimeError("Service is not ready")
        lock = self._inference_locks.setdefault(resolved, asyncio.Lock())
        async with lock:
            self.lifecycle.transition_to(resolved, ServiceState.BUSY)
            try:
                if self.mock_mode:
                    await asyncio.sleep(float(os.getenv("KIOSK_MOCK_INFER_SECONDS", "1.1")))
                    label = {"ai_photobooth": "photobooth", "virtual_tryon": "virtual try-on", "fashion_recommender": "fashion recommendation", "speech_llm": "conversation"}[service_id]
                    if service_id == "fashion_recommender":
                        return {"mock": True, "message": "Simulasi rekomendasi gaya.", "outfits": [["Urban santai", "Jaket ringan, kaus netral, dan denim."], ["Rapi modern", "Kemeja bersih dengan celana warna bumi."], ["Weekend hangat", "Layer rajut dengan aksen warna natural."], ["Minimal harian", "Siluet sederhana yang mudah dipadukan."]]}
                    if service_id == "speech_llm":
                        message = payload.get("message", "")
                        return {"mock": True, "message": f"Ini balasan simulasi untuk: “{message[:180]}”. Layanan percakapan AI belum terhubung."}
                    return {"mock": True, "message": f"Permintaan {label} diterima dalam mode simulasi. Hasil visual AI belum dibuat.", "result": "Mock response"}
                return await self.router.forward_infer(resolved, payload)
            finally:
                if self.lifecycle.get_state(resolved) == ServiceState.BUSY:
                    self.lifecycle.transition_to(resolved, ServiceState.READY)

    async def stop(self, service_id: str) -> dict:
        resolved = self.resolve(service_id)
        state = self.lifecycle.get_state(resolved)
        if state in (ServiceState.STOPPED, ServiceState.STOPPING):
            return self.state(service_id)
        if state == ServiceState.STARTING:
            task = self._tasks.get(resolved)
            if task and not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            self.lifecycle.transition_to(resolved, ServiceState.STOPPED)
            return self.state(service_id)
        if state == ServiceState.ERROR:
            self.lifecycle.transition_to(resolved, ServiceState.STOPPED)
            return self.state(service_id)
        if state == ServiceState.BUSY:
            async with self._inference_locks.setdefault(resolved, asyncio.Lock()):
                pass
            state = self.lifecycle.get_state(resolved)
            if state == ServiceState.READY:
                self.lifecycle.transition_to(resolved, ServiceState.STOPPING)
            else:
                return self.state(service_id)
        else:
            self.lifecycle.transition_to(resolved, ServiceState.STOPPING)
        try:
            if not self.mock_mode:
                service = self.registry.get_service(resolved)
                async with httpx.AsyncClient(timeout=20.0) as client:
                    response = await client.post(f"{service.endpoint.rstrip('/')}/unload", json={"force_cleanup": True})
                    response.raise_for_status()
            self.lifecycle.transition_to(resolved, ServiceState.STOPPED)
            return self.state(service_id)
        except Exception:
            self.lifecycle.transition_to(resolved, ServiceState.ERROR)
            raise
