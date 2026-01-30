# residual_detector.py
class ResidualDetector:
    def __init__(self, threshold):
        self.threshold = threshold

    def compute_residual(self, expected, measured):
        return abs(expected - measured)

    def is_attack(self, expected, measured):
        residual = self.compute_residual(expected, measured)
        attack = residual > self.threshold
        return attack, residual  # <-- return tuple
