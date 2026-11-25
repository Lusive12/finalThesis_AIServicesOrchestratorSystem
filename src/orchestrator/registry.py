"""Service Registry: loads and manages definitions from configs/services.yaml."""

from pathlib import Path
from typing import Dict, List, Optional
import yaml

from src.orchestrator.models import ServiceMetadata


class ServiceRegistry:
    def __init__(self, config_path: str = "configs/services.yaml"):
        self.config_path = Path(config_path)
        self.services: Dict[str, ServiceMetadata] = {}
        self.load_registry()

    def load_registry(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found at: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        raw_services = raw.get("services", {})
        for s_id, s_data in raw_services.items():
            self.services[s_id] = ServiceMetadata(
                id=s_id,
                name=s_data.get("name", s_id),
                owner=s_data.get("owner", "unknown"),
                runtime=s_data.get("runtime", "python_process"),
                endpoint=s_data.get("endpoint", "http://127.0.0.1:8000"),
                estimated_vram_mb=s_data.get("estimated_vram_mb", 0),
                load_time_estimate_ms=s_data.get("load_time_estimate_ms", 1000),
                exclusive_gpu=s_data.get("exclusive_gpu", False),
                can_resident=s_data.get("can_resident", True),
                models=s_data.get("models", {}),
            )

    def get_service(self, service_id: str) -> Optional[ServiceMetadata]:
        return self.services.get(service_id)

    def list_services(self) -> List[ServiceMetadata]:
        return list(self.services.values())

    def get_exclusive_services(self) -> List[ServiceMetadata]:
        return [s for s in self.services.values() if s.exclusive_gpu]
