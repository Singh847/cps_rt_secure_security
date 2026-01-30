# visual_demo.py
import time
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.patches import Rectangle

from attacker import SensorAttacker
from plant import MotorPlant
from controller import PIDController
from scheduler import RealTimeScheduler
from security import SecurityMonitor
from monitor import SystemMonitor
from config import *

# Initialize system
plant = MotorPlant()
controller = PIDController(kp=1.0, ki=0.1, kd=0.01)
scheduler = RealTimeScheduler(SAMPLE_TIME)
security = SecurityMonitor(ATTACK_THRESHOLD)
monitor = SystemMonitor()
attacker = SensorAttacker()

setpoint = 10.0

# For plotting
max_points = 200
time_data = deque(maxlen=max_points)
speed_data = deque(maxlen=max_points)
setpoint_data = deque(maxlen=max_points)
attack_data = deque(maxlen=max_points)
fail_safe_flags = deque(maxlen=max_points)

plt.ion()
fig, ax = plt.subplots()
line_speed, = ax.plot([], [], label="Motor Speed",color='blue')
line_setpoint, = ax.plot([], [], label="Setpoint",color='green', linestyle='--')
line_attack, = ax.plot([], [], label="Sensor Reading", linestyle=':')
fail_safe_patches = []

ax.set_ylim(0, setpoint * 1.5)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Speed")
ax.legend()
ax.grid(True)

start_time = time.monotonic()
t = 0

try:
    while True:
        cycle_start = time.monotonic()
        true_speed = plant.speed
        sensed_speed = attacker.attack(true_speed)

        fail_safe_active = False
        if security.sensor_attack_detected(true_speed, sensed_speed):
            control_signal = monitor.activate_fail_safe("Sensor attack")
            fail_safe_active = True
        else:
            control_signal = controller.compute(setpoint, sensed_speed, SAMPLE_TIME)

        plant.update(control_signal, SAMPLE_TIME)

        elapsed = scheduler.wait_for_next_cycle(cycle_start)
        monitor.log_timing(elapsed, DEADLINE)

        if elapsed > DEADLINE + MAX_JITTER:
            monitor.activate_fail_safe("Deadline violation")
            fail_safe_active = True

        # Update plotting data
        t += SAMPLE_TIME
        time_data.append(t)
        speed_data.append(plant.speed)
        setpoint_data.append(setpoint)
        attack_data.append(sensed_speed)
        fail_safe_flags.append(fail_safe_active)

        # Update main lines
        line_speed.set_data(time_data, speed_data)
        line_setpoint.set_data(time_data, setpoint_data)
        line_attack.set_data(time_data, attack_data)

        # Clear old fail-safe patches
        for patch in fail_safe_patches:
            patch.remove()
        fail_safe_patches.clear()

        # Highlight fail-safe periods with red translucent rectangles
        for i in range(len(time_data)):
            if fail_safe_flags[i]:
                rect = Rectangle(
                    (time_data[i], 0),
                    SAMPLE_TIME,
                    setpoint*1.5,
                    color='red',
                    alpha=0.2
                )
                ax.add_patch(rect)
                fail_safe_patches.append(rect)

        ax.set_xlim(max(0, t - max_points*SAMPLE_TIME), t + SAMPLE_TIME)
        plt.pause(0.001)

except KeyboardInterrupt:
    print("Visualization stopped.")