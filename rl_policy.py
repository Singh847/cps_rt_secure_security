# rl_policy.py
# RL-style Recovery Policy for CPS Control Loop
# Lightweight, explainable policy using thresholds

class RecoveryPolicy:
    """
    Lightweight, explainable recovery policy for CPS control.
    """

    def __init__(self):
        # Discrete gain multipliers for control
        self.actions = [0.5, 1.0, 1.5]

    def select_action(self, residual: float) -> float:
        """
        Selects a control gain based on the magnitude of the residual.
        residual: absolute difference between estimated and measured state
        Returns: float, gain multiplier
        """
        if residual > 2.0:
            return 0.5  # Minimal control (aggressive damping)
        elif residual > 1.0:
            return 1.0  # Moderate control
        else:
            return 1.5  # Normal/default control
