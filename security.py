# security.py
# Cyber-physical security monitoring

import logging
logging.basicConfig(level=logging.INFO)

class SecurityMonitor:
    def __init__(self, threshold):
        self.threshold = threshold

    def sensor_attack_detected(self, expected, measured):
        deviation = abs(expected - measured)
        if deviation > self.threshold:
            logging.warning(f"Sensor attack detected! deviation={deviation:.3f}")
            return True
        return False