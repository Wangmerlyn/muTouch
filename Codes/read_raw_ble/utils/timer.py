import threading
import time


class Timer:
    def __init__(self):
        self.start_time = None
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            self.start_time = time.time()

    def elapsed_time(self):
        with self.lock:
            if self.start_time is None:
                return 0
            return time.time() - self.start_time
