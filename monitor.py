# monitor.py
# Safety monitoring and fail-safe behavior

import logging
from config import SAFE_CONTROL

logging.basicConfig(level=logging.INFO)

class SystemMonitor:
    def __init__(self):
        self.jitter_log = []

    def log_timing(self, elapsed, deadline):
        jitter = elapsed - deadline
        self.jitter_log.append(jitter)

        if jitter > 0:
            logging.warning(f"Deadline miss: jitter={jitter:.6f}s")

    def activate_fail_safe(self, reason="Unknown"):
        logging.error(f"FAIL-SAFE ACTIVATED: {reason}")
        return SAFE_CONTROL