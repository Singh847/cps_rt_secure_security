# state_machine.py
from enum import Enum, auto
import logging

logging.basicConfig(level=logging.INFO)

class SystemState(Enum):
    NORMAL = auto()
    ATTACK_DETECTED = auto()
    DEGRADED = auto()
    FAIL_SAFE = auto()
    RECOVERY = auto()

class StateMachine:
    def __init__(self):
        self.state = SystemState.NORMAL

    def transition(self, new_state, reason=""):
        logging.warning(
            f"State transition: {self.state.name} -> {new_state.name} Reason: {reason}"
        )
        self.state = new_state

    # Helper methods
    def is_normal(self):
        return self.state == SystemState.NORMAL

    def is_fail_safe(self):
        return self.state == SystemState.FAIL_SAFE

    def is_attack_detected(self):
        return self.state == SystemState.ATTACK_DETECTED

    def is_degraded(self):
        return self.state == SystemState.DEGRADED

    def is_recovery(self):
        return self.state == SystemState.RECOVERY
