# fault_injector.py
import random

class FaultInjector:
    def __init__(self, attack_probability=0.05):
        self.attack_probability = attack_probability

    def inject(self, signal):
        """
        Inject probabilistic faults into the sensor signal.
        """
        if random.random() < self.attack_probability:
            return signal + random.uniform(-5.0, 5.0)  # Inject fault
        return signal
