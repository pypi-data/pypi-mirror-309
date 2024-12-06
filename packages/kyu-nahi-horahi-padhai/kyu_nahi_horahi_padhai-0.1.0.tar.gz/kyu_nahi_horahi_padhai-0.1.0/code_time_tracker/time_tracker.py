# code_time_tracker/time_tracker.py

import time

class TimeTracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()
        print("Tracking started...")

    def stop(self):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print("Tracking stopped...")
        return duration

