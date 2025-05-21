import random
from app.services import GameService
import numpy as np


class MeanMangos:
    def __init__(self):
        self.game = GameService.get_game_by_name("mean_mangos")
        self.config = self.game.config_data
        self.min_qty = self.config["min_qty"]

    def new_game(self, decision_day=50, days_total=60):
        S0 = 50
        mu = 50
        theta = 0.15
        sigma = 0.9
        dt = 1  # daily step
        prices = [S0]
        show_price, entry_price, future_price = "", None, ""
        for day in range(days_total + 1):
            S_prev = prices[-1]
            dS = theta * (mu - S_prev) * dt + sigma * np.random.normal()
            prices.append(float(S_prev + dS))
            if day < decision_day:
                show_price += f"{prices[-1]};"
            elif day == decision_day:
                show_price += f"{prices[-1]};"
                entry_price = prices[-1]
            else:
                future_price += f"{prices[-1]};"

        return {
            "show_price": show_price,
            "entry_price": entry_price,
            "future_price": future_price,
            "exit_price": prices[-1],
        }

    def get_cost(self, qty, game_data):
        entry_price = float(game_data["entry_price"])
        return qty * entry_price

    def get_current_value(self, choice, qty, game_data):
        if qty < self.min_qty:
            raise ValueError(f"Qty must be greater than or equal to {self.min_qty}")
        value = qty * float(game_data["exit_price"])
        cost = self.get_cost(qty, game_data)
        if choice.lower() == "buy":
            pnl = value - cost
        else:
            pnl = cost - value
        return cost, value, pnl
