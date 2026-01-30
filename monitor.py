# monitor.py
# Safety monitoring and fail-safe behavior

import logging
from config import SAFE_CONTROL

logging.basicConfig(level=logging.INFO)

class SystemMonitor:
    def __init__(self):
        # Track worst-case execution time
        self.max_execution_time = 0.0
        self.deadlin_misses = 0
        self.stable_cycles = 0

    def record_stability(self, residual, threshold):
        """Track consecutive stable cycles."""
        if residual < threshold:
            self.stable_cycles += 1
        else:
            self.stable_cycles = 0

    def log_timing(self, elapsed, deadline):
        """Log cycle execution time vs deadline."""
        print(f"[MONITOR] Cycle elapsed={elapsed:.6f}s, Deadline={deadline:.6f}s")

    def activate_fail_safe(self, reason="Unknown"):
        """Trigger fail-safe behavior."""
        logging.error(f"FAIL-SAFE ACTIVATED: {reason}")
        return SAFE_CONTROL
