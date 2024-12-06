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
        self.timeout_tolerance = 5
        self.game_reports = {}

        # Initialize logging and save paths
        self.logging_path = logging_path
        self.save_path = save_path

        # Create a timestamped log file if logging_path is provided
        if self.logging_path:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.logging_path = os.path.join(logging_path, f"{timestamp}_log.txt")

    def run_func_w_time(self, func, timeout, name, alt_ret=None):
        """
        Runs a function with a timeout, capturing exceptions and handling timeouts.
        """
        result = {"ret": None, "timed_out": False, "exception": None}

        def target_wrapper():
            try:
                result["ret"] = func()
            except Exception as e:
                result["exception"] = e

        # Run the function in a separate thread
        thread = threading.Thread(target=target_wrapper)
        thread.start()
        thread.join(timeout)

        # Handle timeout
        if thread.is_alive():
            result["timed_out"] = True
            thread.join()
            self._handle_timeout(name)

        # Handle exceptions
        if result["exception"]:
            self._log_or_print_exception(result["exception"], name)

        # Return the function result or fallback to `alt_ret` if needed
        if result["timed_out"] or result["exception"] or result["ret"] is None:
            return alt_ret
        return result["ret"]

    def _log_or_print_exception(self, exception, name):
        """
        Logs or prints exceptions during function execution.
        """
        stack_trace = traceback.format_exc()
        message = f"Exception in {name}: {exception}\n{stack_trace}"
        self._log_or_print(message)

        # Mark the player as disconnected if in handin mode
        if self.handin_mode and name in self.game_reports:
            self.game_reports[name]["disconnected"] = True

    def _handle_timeout(self, name):
        """
        Handles timeout events for a player.
        """
        if name in self.game_reports:
            self.game_reports[name].setdefault("timeout_count", 0)
            self.game_reports[name].setdefault("global_timeout_count", 0)
            self.game_reports[name]["timeout_count"] += 1
            self.game_reports[name]["global_timeout_count"] += 1

        message = f"{name} timed out after {self.timeout} seconds."
        self._log_or_print(message)

    def run_game(self):
        """
        Placeholder for the game logic. Must be implemented in subclasses.
        """
        raise NotImplementedError

    def _log_or_print(self, message):
        """
        Helper function to log messages to a file if logging_path is set, otherwise print them.
        """
        if self.logging_path:
            with open(self.logging_path, "a") as log_file:
                log_file.write(message + "\n")
        else:
            print(message)
