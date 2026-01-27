# config.py
"""
System-wide configuration for a real-time cyber-physical control system.
"""

# Real-Time Constraints
SAMPLE_TIME = 0.05      # 50 ms
DEADLINE = 0.05         # must be <= SAMPLE_TIME
MAX_JITTER = 0.005      # 5 ms

# Safety
SAFE_CONTROL = 0.0      # fail-safe actuator value

# Security
ATTACK_THRESHOLD = 0.3  # sensor deviation threshold