import threading
import traceback
from datetime import datetime
import os
import json

class LocalArena:
    def __init__(self, num_rounds, players, timeout, handin, logging_path, save_path):
        self.num_rounds = num_rounds
        self.players = players
        self.timeout = timeout
        self.handin_mode = handin
        self.logging_path = logging_path
        self.save_path = save_path
        self.timeout_tolerance = 5
        self.game_reports = {}

        if self.logging_path:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.logging_path = os.path.join(logging_path, f"{timestamp}_log.txt")

    def run_func_w_time(self, func, timeout, name, alt_ret=None):
        ret = None

        def target_wrapper():
            nonlocal ret
            try:
                ret = func()
            except Exception as e:
                self._log_exception(e, name)

        thread = threading.Thread(target=target_wrapper)
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            self._handle_timeout(name)

        return ret or alt_ret

    def _log_exception(self, exception, name):
        msg = f"Exception for {name}: {exception}"
        if self.logging_path:
            with open(self.logging_path, "a") as f:
                f.write(msg + "\n")
        else:
            print(msg)

    def _handle_timeout(self, name):
        if name in self.game_reports:
            self.game_reports[name].setdefault('timeout_count', 0)
            self.game_reports[name]['timeout_count'] += 1

        msg = f"{name} timed out"
        if self.logging_path:
            with open(self.logging_path, "a") as f:
                f.write(msg + "\n")
        else:
            print(msg)

    def run_game(self):
        raise NotImplementedError
