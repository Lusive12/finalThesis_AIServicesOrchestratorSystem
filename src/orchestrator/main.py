"""Main FastAPI application factory and runner for Orchestrator."""

from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.orchestrator.gateway import WebSocketConnectionManager, create_gateway_router
from src.orchestrator.lifecycle import LifecycleStateMachine
from src.orchestrator.mode_controller import ModeController
from src.orchestrator.registry import ServiceRegistry
from src.orchestrator.request_router import RequestRouter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("orchestrator.main")


def create_app() -> FastAPI:
    registry = ServiceRegistry()
    lifecycle = LifecycleStateMachine()
    mode_controller = ModeController(registry, lifecycle)
    router = RequestRouter(registry, lifecycle)
    ws_manager = WebSocketConnectionManager()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("Orchestrator Gateway starting up...")
        yield
        logger.info("Orchestrator Gateway shutting down...")
        await router.close()

    app = FastAPI(
        title="Smart Kiosk AI Service Orchestrator",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS setup for web kiosk
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Attach REST endpoints
    gateway_router = create_gateway_router(
        registry, lifecycle, mode_controller, router, ws_manager
    )
    app.include_router(gateway_router)

    # Attach WebSocket endpoint
    @app.websocket("/ws/events")
    async def websocket_endpoint(websocket: WebSocket):
        await ws_manager.connect(websocket)
        try:
            while True:
                # Keep alive and receive commands
                msg = await websocket.receive_text()
                logger.debug("Received WS message: %s", msg)
        except WebSocketDisconnect:
            ws_manager.disconnect(websocket)

    # Mount UI static files if directory exists
    try:
        app.mount("/ui", StaticFiles(directory="src/kiosk_ui", html=True), name="ui")
    except Exception as e:
        logger.warning("Could not mount static UI directory: %s", e)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.orchestrator.main:app", host="0.0.0.0", port=8000, reload=True)
