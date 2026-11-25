"""FastAPI REST & WebSocket Gateway."""

import asyncio
import logging
import time
from typing import Dict, List
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from src.orchestrator.models import ModeSwitchRequest, ModeSwitchResponse, TelemetryEvent
from src.orchestrator.registry import ServiceRegistry
from src.orchestrator.lifecycle import LifecycleStateMachine
from src.orchestrator.mode_controller import ModeController
from src.orchestrator.request_router import RequestRouter

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
        services_list = []
        for s in registry.list_services():
            services_list.append({
                **s.model_dump(),
                "state": lifecycle.get_state(s.id).value,
            })
        return {"services": services_list}

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
