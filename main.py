# main.py
# Real-time cyber-physical control loop

import time

from attacker import SensorAttacker
from plant import MotorPlant
from controller import PIDController
from scheduler import RealTimeScheduler
from security import SecurityMonitor
from monitor import SystemMonitor
from config import *

def main():
    plant = MotorPlant()
    controller = PIDController(kp=1.0, ki=0.1, kd=0.01)
    scheduler = RealTimeScheduler(SAMPLE_TIME)
    security = SecurityMonitor(ATTACK_THRESHOLD)
    monitor = SystemMonitor()
    attacker = SensorAttacker()

    setpoint = 10.0  # desired speed

    while True:
        cycle_start = time.monotonic()

        # Sensor read
        true_speed = plant.speed
        sensed_speed = attacker.attack(true_speed)

        # Security check
        if security.sensor_attack_detected(true_speed, sensed_speed):
            control_signal = monitor.activate_fail_safe("Sensor attack")
        else:
            control_signal = controller.compute(
                setpoint,
                sensed_speed,
                SAMPLE_TIME
            )

        # Actuation
        plant.update(control_signal, SAMPLE_TIME)

        # Real-time enforcement
        elapsed = scheduler.wait_for_next_cycle(cycle_start)
        monitor.log_timing(elapsed, DEADLINE)

        if elapsed > DEADLINE + MAX_JITTER:
            monitor.activate_fail_safe("Deadline violation")

if __name__ == "__main__":
    main()