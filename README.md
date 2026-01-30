# CPS Real-Time Secure System

## Overview

This project implements a secure real-time Cyber-Physical System (CPS) simulation with attack injection, monitoring, detection, and mitigation mechanisms. The system models a plant controlled by a real-time controller and scheduler, while actively monitoring for faults, attacks, and deadline violations.

The goal is to evaluate system resilience under different attack scenarios and scheduling conditions using state-based security monitoring and residual-based detection.

---

## Features

- Real-time CPS simulation loop  
- Configurable attack injection  
- State machine–based security controller  
- Residual-based attack detection  
- Deadline and scheduling risk analysis  
- Multiple experiment modes (baseline & attacks)  
- Modular and extensible architecture  
- Console-based monitoring and logging  

---

## Project Structure

```text
cps_rt_secure_system/
│
├── attacker.py              # Defines attacker behavior and attack models
├── config.py                # Global configuration and experiment selection
├── controller.py            # Control logic for the CPS
├── fault_injector.py        # Injects faults/attacks into the system
├── main.py                  # Entry point for running experiments
├── monitor.py               # Runtime monitoring and logging
├── observer.py              # State estimation / observer logic
├── plant.py                 # Physical system (plant) model
├── residual_detector.py     # Residual-based anomaly detection
├── rl_policy.py             # (Optional) RL-based or adaptive policy logic
├── scheduler.py             # Real-time task scheduling and analysis
├── security.py              # Security logic and mitigation actions
├── state_machine.py         # CPS security state machine
├── visual_demo.py           # Visualization or demo utilities
├── README.md                # Project documentation
└── __pycache__/             # Python cache files



Experiment Modes

The experiment mode is selected in config.py:

EXPERIMENT_MODE = "random_attack"

Available Modes

baseline
Normal operation without attacks

random_attack
Random fault/attack injection during runtime

stealth_attack
Low-magnitude attacks designed to evade detection

deadline_miss
Induced timing faults to test scheduling robustness

System States

The CPS security state machine transitions between:

NORMAL – System operating safely

DEGRADED – Performance impacted but controlled

ATTACK_DETECTED – Anomaly or attack detected

MITIGATION / RECOVERY – Defensive actions applied

State Transitions Triggered By

Residual threshold violations

Control saturation

Deadline misses

Scheduling risk detection

Scheduling & Timing Analysis

The scheduler evaluates real-time constraints and reports:

Cycle elapsed time

Deadline violations

Worst-Case Execution Time (WCET)

CPU utilization

Scheduling risk detection

Example Output
--- SCHEDULING ANALYSIS ---
WCET: 0.0552s
Utilization: 1.11
Scheduling Risk Detected

Output & Logs

During execution, the system prints:

Control and plant states

Residual values

State transitions

Attack detection events

Scheduling and deadline warnings

This enables real-time inspection of system resilience and security behavior.

Use Cases

CPS security research

Real-time systems experimentation

Attack detection validation

Scheduling and deadline analysis

Academic projects and demonstrations

Future Improvements

Graphical visualization dashboard

Support for network-based attacks

Machine-learning-based detectors

Real hardware-in-the-loop (HIL) integration

Formal verification of state transitions

System Architecture
![CPS Real-Time Secure System Architecture](<images/architecture.png>)

---

## ✅ Now finish the Git fix

After pasting and saving:

```bash
git add README.md
git commit -m "Resolve README.md merge conflict"
git push origin main
