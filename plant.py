# plant.py
# Physical system model (DC motor speed)

class MotorPlant:
    def __init__(self, a=0.8, b=1.2):
        self.speed = 0.0
        self.a = a  # damping
        self.b = b  # control gain

    def update(self, control_input, dt):
        """
        Discrete-time motor model:
        w(k+1) = w(k) + dt * (-a*w + b*u)
        """
        self.speed += dt * (-self.a * self.speed + self.b * control_input)

        # physical constraint
        if self.speed < 0.0:
            self.speed = 0.0

        return self.speed