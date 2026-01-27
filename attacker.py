# attacker.py
# Simulates cyber attacks on sensor data

import random

class SensorAttacker:
    def __init__(self, attack_probability=0.2, attack_strength=0.5):
        self.attack_probability = attack_probability
        self.attack_strength = attack_strength

    def attack(self, true_value):
        if random.random() < self.attack_probability:
            return true_value + self.attack_strength
        return true_value