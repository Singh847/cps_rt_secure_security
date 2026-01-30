# observer.py
import numpy as np

class KalmanObserver:
    def __init__(self, a, b, q=0.01, r=0.1):
        self.a = a
        self.b = b
        self.q = q
        self.r = r
        self.x_hat = 0.0
        self.p = 1.0

    def update(self, u, z):
        # Predict
        x_hat_pred = self.a * self.x_hat + self.b * u
        p_pred = self.a * self.p * self.a + self.q

        # Update
        k = p_pred / (p_pred + self.r)
        self.x_hat = x_hat_pred + k * (z - x_hat_pred)
        self.p = (1 - k) * p_pred

        residual = abs(self.x_hat - z)
        return self.x_hat, residual
