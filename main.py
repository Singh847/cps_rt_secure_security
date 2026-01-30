# main.py
# Secure Real-Time Cyber-Physical System (Simulation Only)

import time
import logging
import random

from residual_detector import ResidualDetector
from state_machine import StateMachine, SystemState
from plant import MotorPlant
from controller import PIDController
from scheduler import RealTimeScheduler
from monitor import SystemMonitor
from fault_injector import FaultInjector
from config import *

# =============================
# EXPERIMENT SELECTION
# =============================
EXPERIMENT_MODE = "random_attack"

# Options:
# "baseline"
# "random_attack"
# "stealth_attack"
# "deadline_miss"
# "recovery_test"

# =============================
# CONSTANTS
# =============================
DEGRADED_CONTROL_LIMIT = 0.4
SAFE_CONTROL = 0.0
RECOVERY_STABLE_CYCLES = 10

# =============================
# LOGGING
# =============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    # =============================
    # INITIALIZATION
    # =============================
    plant = MotorPlant()
    controller = PIDController(kp=1.0, ki=0.1, kd=0.01)
    scheduler = RealTimeScheduler(SAMPLE_TIME)
    monitor = SystemMonitor()
    state_machine = StateMachine()
    residual_detector = ResidualDetector(threshold=1.5)

    # Configure attack model
    if EXPERIMENT_MODE == "baseline":
        fault_injector = FaultInjector(attack_probability=0.0)
    elif EXPERIMENT_MODE == "random_attack":
        fault_injector = FaultInjector(attack_probability=0.2)
    else:
        fault_injector = FaultInjector(attack_probability=0.0)

    setpoint = 10.0

    logging.info(f"Starting CPS Experiment: {EXPERIMENT_MODE}")

    try:
        while True:
            cycle_start = time.monotonic()
            wcet_start = time.perf_counter()

            # =============================
            # SENSOR READ
            # =============================
            true_speed = plant.speed
            sensed_speed = fault_injector.inject(true_speed)

            # Stealth attack (slow bias)
            if EXPERIMENT_MODE == "stealth_attack":
                sensed_speed += 0.02

            expected_speed = plant.speed

            # =============================
            # RESIDUAL DETECTION
            # =============================
            attack, residual = residual_detector.is_attack(
                expected_speed, sensed_speed
            )

            monitor.record_stability(residual, residual_detector.threshold)

            if attack:
                state_machine.transition(
                    SystemState.ATTACK_DETECTED,
                    f"Residual {residual:.2f}"
                )

            # =============================
            # RECOVERY LOGIC
            # =============================
            if (
                state_machine.state == SystemState.DEGRADED
                and monitor.stable_cycles >= RECOVERY_STABLE_CYCLES
            ):
                state_machine.transition(
                    SystemState.RECOVERY,
                    "System stable, recovering"
                )

            # =============================
            # CONTROL LOGIC
            # =============================
            if state_machine.state == SystemState.NORMAL:
                control_signal = controller.compute(
                    setpoint, sensed_speed, SAMPLE_TIME
                )

            elif state_machine.state == SystemState.ATTACK_DETECTED:
                state_machine.transition(
                    SystemState.DEGRADED,
                    "Limiting control"
                )
                raw = controller.compute(setpoint, sensed_speed, SAMPLE_TIME)
                control_signal = max(
                    min(raw, DEGRADED_CONTROL_LIMIT),
                    -DEGRADED_CONTROL_LIMIT
                )

            elif state_machine.state == SystemState.DEGRADED:
                raw = controller.compute(setpoint, sensed_speed, SAMPLE_TIME)
                control_signal = max(
                    min(raw, DEGRADED_CONTROL_LIMIT),
                    -DEGRADED_CONTROL_LIMIT
                )

            elif state_machine.state == SystemState.RECOVERY:
                control_signal = controller.compute(
                    setpoint, sensed_speed, SAMPLE_TIME
                )
                state_machine.transition(
                    SystemState.NORMAL,
                    "Recovered"
                )

            elif state_machine.state == SystemState.FAIL_SAFE:
                control_signal = SAFE_CONTROL

            else:
                control_signal = SAFE_CONTROL

            # =============================
            # DEADLINE MISS EXPERIMENT
            # =============================
            if EXPERIMENT_MODE == "deadline_miss":
                time.sleep(DEADLINE * 1.5)

            # =============================
            # WCET TRACKING
            # =============================
            wcet = time.perf_counter() - wcet_start
            monitor.max_execution_time = max(
                monitor.max_execution_time, wcet
            )

            # =============================
            # ACTUATION
            # =============================
            plant.update(control_signal, SAMPLE_TIME)

            # =============================
            # REAL-TIME SCHEDULING
            # =============================
            elapsed = scheduler.wait_for_next_cycle(cycle_start)
            monitor.log_timing(elapsed, DEADLINE)

            if elapsed > DEADLINE:
                state_machine.transition(
                    SystemState.DEGRADED,
                    "Deadline missed"
                )

            if elapsed > DEADLINE + MAX_JITTER:
                state_machine.transition(
                    SystemState.FAIL_SAFE,
                    "Hard real-time violation"
                )

            # =============================
            # LOGGING
            # =============================
            logging.info(
                f"State={state_machine.state.name}, "
                f"Speed={sensed_speed:.2f}, "
                f"Control={control_signal:.2f}, "
                f"Residual={residual:.2f}, "
                f"StableCycles={monitor.stable_cycles}"
            )

    except KeyboardInterrupt:
        logging.info("Experiment stopped")

        utilization = monitor.max_execution_time / SAMPLE_TIME

        print("\n--- SCHEDULING ANALYSIS ---")
        print(f"WCET: {monitor.max_execution_time:.6f}s")
        print(f"Utilization: {utilization:.2f}")

        if utilization < 0.69:
            print("Rate Monotonic Schedulable")
        else:
            print("Scheduling Risk Detected")

if __name__ == "__main__":
    main()
