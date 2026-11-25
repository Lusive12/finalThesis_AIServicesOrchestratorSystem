"""Pydantic schemas and dataclasses for Orchestrator."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ServiceState(str, Enum):
    STOPPED = "STOPPED"
    STARTING = "STARTING"
    READY = "READY"
    BUSY = "BUSY"
    STOPPING = "STOPPING"
    ERROR = "ERROR"


class ServiceMetadata(BaseModel):
    id: str
    name: str
    owner: str
    runtime: str
    endpoint: str
    estimated_vram_mb: int = 0
    load_time_estimate_ms: int = 1000
    exclusive_gpu: bool = False
    can_resident: bool = True
    models: Dict[str, Any] = Field(default_factory=dict)


class ModeSwitchRequest(BaseModel):
    target_mode: str
    force: bool = False


class ModeSwitchResponse(BaseModel):
    status: str
    previous_mode: str
    current_mode: str
    transition_duration_ms: float
    active_services: List[str]


class TelemetryEvent(BaseModel):
    event_type: str = "TELEMETRY_UPDATE"
    timestamp: float
    vram_used_mb: float
    vram_total_mb: float
    vram_free_mb: float
    gpu_utilization_pct: Optional[float] = None
    cpu_utilization_pct: Optional[float] = None
