"""FastAPI REST & WebSocket Gateway."""

import asyncio
import logging
import os
import time
from typing import Dict, List
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from src.orchestrator.models import ModeSwitchRequest, ModeSwitchResponse, TelemetryEvent
from src.orchestrator.registry import ServiceRegistry
from src.orchestrator.lifecycle import LifecycleStateMachine
from src.orchestrator.mode_controller import ModeController
from src.orchestrator.request_router import RequestRouter
from src.orchestrator.kiosk_services import KioskServices

logger = logging.getLogger("orchestrator.gateway")


class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("WebSocket client connected. Total clients: %d", len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("WebSocket client disconnected. Total clients: %d", len(self.active_connections))

    async def broadcast_json(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)


def create_gateway_router(
    registry: ServiceRegistry,
    lifecycle: LifecycleStateMachine,
    mode_controller: ModeController,
    router: RequestRouter,
    ws_manager: WebSocketConnectionManager,
    kiosk_services: KioskServices,
) -> APIRouter:
    api = APIRouter()

    @api.get("/health")
    async def get_health():
        return {
            "status": "healthy",
            "current_mode": mode_controller.current_mode,
            "timestamp": time.time(),
        }

    @api.get("/services")
    async def list_services():
        return {"services": [{**service.model_dump(), "state": lifecycle.get_state(service.id).value} for service in registry.list_services()]}

    @api.get("/api/services")
    async def kiosk_services_list():
        kiosk_ids = ["ai_photobooth", "virtual_tryon", "fashion_recommender", "speech_llm"]
        services_list = []
        for service_id in kiosk_ids:
            try:
                state = kiosk_services.state(service_id)
                metadata = registry.get_service(kiosk_services.resolve(service_id))
                services_list.append({**state, "name": metadata.name, "available": True})
            except ValueError:
                services_list.append({"id": service_id, "state": "ERROR", "available": False})
        return {"services": services_list, "mock_mode": kiosk_services.mock_mode}

    @api.get("/api/kiosk-config")
    async def kiosk_config():
        return {
            "idle_timeout_ms": int(float(os.getenv("KIOSK_IDLE_TIMEOUT_SECONDS", "180")) * 1000),
            "ready_timeout_ms": int(float(os.getenv("ORCHESTRATOR_READY_TIMEOUT", "90")) * 1000),
        }

    @api.get("/api/services/{service_id}/status")
    async def kiosk_service_status(service_id: str):
        try:
            return kiosk_services.state(service_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc))

    @api.post("/api/services/{service_id}/start", status_code=202)
    async def kiosk_service_start(service_id: str):
        try:
            return await kiosk_services.start(service_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc))

    @api.post("/api/services/{service_id}/stop")
    async def kiosk_service_stop(service_id: str):
        try:
            return await kiosk_services.stop(service_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc))
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Service stop request failed: {exc}")

    @api.get("/api/services/{service_id}/health")
    async def kiosk_service_health(service_id: str):
        try:
            return await kiosk_services.health(service_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc))

    @api.post("/api/services/{service_id}/infer")
    async def kiosk_service_infer(service_id: str, payload: dict):
        try:
            return await kiosk_services.infer(service_id, payload)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc))
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc))
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Inference request failed: {exc}")

    @api.post("/api/v1/mode/switch", response_model=ModeSwitchResponse)
    async def switch_mode(request: ModeSwitchRequest):
        try:
            res = await mode_controller.switch_mode(request.target_mode, request.force)
            # Broadcast update via WebSocket
            await ws_manager.broadcast_json({
                "event_type": "MODE_CHANGED",
                "current_mode": res.current_mode,
                "previous_mode": res.previous_mode,
                "transition_duration_ms": res.transition_duration_ms,
            })
            return res
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @api.post("/api/v1/infer/{service_id}")
    async def infer(service_id: str, payload: dict):
        try:
            return await router.forward_infer(service_id, payload)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Service gateway error: {str(e)}")

    return api
