from agt_server.local_games.base import LocalArena
from itertools import combinations
import numpy as np
import os
import json
import pandas as pd
from datetime import datetime


class RPSArena(LocalArena):
    def __init__(self, num_rounds=1000, players=[], timeout=1, handin=False, 
                 logging_path=None, summary_path=None, detailed_reports_path=None):
        super().__init__(num_rounds, players, timeout, handin, logging_path, summary_path)
        self.game_name = "Rock, Paper, Scissors"
        self.valid_actions = [0, 1, 2]
        self.action_map = {0: "Rock", 1: "Paper", 2: "Scissors"}  # Map numbers to actions
        self.utils = [[0, -1, 1],  # Payoff matrix: [P1, P2]
                      [1, 0, -1],
                      [-1, 1, 0]]
        self.invalid_move_penalty = -1
        self.detailed_reports_path = detailed_reports_path

        if not self.handin_mode:
            assert len(self.players) >= 2, "Arena must have at least 2 players"

        for idx, player in enumerate(self.players):
            self.game_reports[player.name] = {
                "action_history": [],
                "util_history": [],
                "index": idx,
                "timeout_count": 0,
                "global_timeout_count": 0,
                "disconnected": False
            }

        self.result_table = np.zeros((len(players), len(players)))
        self.game_num = 1

    def calculate_utils(self, p1_action, p2_action):
        if p1_action not in self.valid_actions and p2_action not in self.valid_actions:
            return [0, 0]
        if p1_action not in self.valid_actions:
            return [self.invalid_move_penalty, 0]
        if p2_action not in self.valid_actions:
            return [0, self.invalid_move_penalty]
        return [self.utils[p1_action][p2_action], self.utils[p2_action][p1_action]]

    def reset_game_reports(self):
        for player in self.players:
            self.game_reports[player.name]["action_history"] = []
            self.game_reports[player.name]["util_history"] = []

    def run_game(self, p1, p2):
        for round_num in range(self.num_rounds):
            p1_action = self.run_func_w_time(p1.get_action, self.timeout, p1.name, -1)
            p2_action = self.run_func_w_time(p2.get_action, self.timeout, p2.name, -1)

            self.game_reports[p1.name]['action_history'].append(p1_action)
            self.game_reports[p2.name]['action_history'].append(p2_action)

            p1_util, p2_util = self.calculate_utils(p1_action, p2_action)
            self.game_reports[p1.name]['util_history'].append(p1_util)
            self.game_reports[p2.name]['util_history'].append(p2_util)

            # Translate actions for interpretability
            p1_action_str = self.action_map.get(p1_action, "Invalid")
            p2_action_str = self.action_map.get(p2_action, "Invalid")

            # Log or print round results
            self._log_or_print(
                f"Game {self.game_num}, Round {round_num + 1}: "
                f"{p1.name} -> {p1_action_str}, {p2.name} -> {p2_action_str}. "
                f"Utilities: {p1.name} {p1_util}, {p2.name} {p2_util}"
            )

        # Save detailed game report
        if self.detailed_reports_path:
            self._save_detailed_game_report(p1, p2)

    def run(self):
        for p1, p2 in combinations(self.players, 2):
            self.run_func_w_time(p1.setup, self.timeout, p1.name)
            self.run_func_w_time(p2.setup, self.timeout, p2.name)
            self.run_game(p1, p2)

        return self.summarize_results()

    def summarize_results(self):
        agent_names = [player.name for player in self.players]
        df = pd.DataFrame(self.result_table, columns=agent_names, index=agent_names)

        # Log or print summary
        summary_message = f"Summary Results:\n{df}"
        self._log_or_print(summary_message)

        if self.save_path:
            df.to_csv(self.save_path)

        return df

    def _save_detailed_game_report(self, p1, p2):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_game_{self.game_num}.json"
        report_path = os.path.join(self.detailed_reports_path, filename)

        report = {
            "game_number": self.game_num,
            "players": [p1.name, p2.name],
            "p1_history": self.game_reports[p1.name],
            "p2_history": self.game_reports[p2.name],
        }

        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)

        self._log_or_print(f"Saved detailed report for Game {self.game_num} at {report_path}")
        self.game_num += 1

    def _log_or_print(self, message):
        """
        Helper function to log messages if logging_path is set, otherwise print them.
        """
        if self.logging_path:
            with open(self.logging_path, "a") as log_file:
                log_file.write(message + "\n")
        else:
            print(message)
