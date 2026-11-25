"""Lifecycle State Machine for AI microservices."""

import logging
import time
from typing import Dict
from src.orchestrator.models import ServiceState

logger = logging.getLogger("orchestrator.lifecycle")


class LifecycleStateMachine:
    """Manages service state transitions: STOPPED -> STARTING -> READY -> STOPPING -> STOPPED."""

    VALID_TRANSITIONS = {
        ServiceState.STOPPED: [ServiceState.STARTING, ServiceState.ERROR],
        ServiceState.STARTING: [ServiceState.READY, ServiceState.ERROR, ServiceState.STOPPED],
        ServiceState.READY: [ServiceState.BUSY, ServiceState.STOPPING, ServiceState.ERROR],
        ServiceState.BUSY: [ServiceState.READY, ServiceState.STOPPING, ServiceState.ERROR],
        ServiceState.STOPPING: [ServiceState.STOPPED, ServiceState.ERROR],
        ServiceState.ERROR: [ServiceState.STOPPED, ServiceState.STARTING],
    }

    def __init__(self):
        self._states: Dict[str, ServiceState] = {}
        self._transition_timestamps: Dict[str, float] = {}

    def get_state(self, service_id: str) -> ServiceState:
        return self._states.get(service_id, ServiceState.STOPPED)

    def transition_to(self, service_id: str, new_state: ServiceState) -> bool:
        current = self.get_state(service_id)
        valid_next = self.VALID_TRANSITIONS.get(current, [])

        if new_state not in valid_next and new_state != current:
            logger.error(
                "Invalid transition for service '%s': %s -> %s",
                service_id,
                current.value,
                new_state.value,
            )
            return False

        self._states[service_id] = new_state
        self._transition_timestamps[service_id] = time.perf_counter()
        logger.info(
            "Service '%s' transitioned: %s -> %s",
            service_id,
            current.value,
            new_state.value,
        )
        return True

    def is_ready(self, service_id: str) -> bool:
        return self.get_state(service_id) == ServiceState.READY
