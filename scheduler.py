# scheduler.py
# Periodic task scheduler for real-time control system

import time

class RealTimeScheduler:
    def __init__(self, period):
        self.period = period

    def wait_for_next_cycle(self, start_time):
        elapsed = time.monotonic() - start_time
        sleep_time = self.period - elapsed

        if sleep_time > 0:
            time.sleep(sleep_time)
            return self.period
        else:
            # deadline miss
            return elapsed