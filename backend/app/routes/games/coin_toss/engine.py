# backend\app\routes\games\coin_toss\engine.py

import random
from app.services import GameService


class CoinToss:
    def __init__(self):
        self.game = GameService.get_game_by_name("coin_toss")
        self.config = self.game.config_data
        self.min_bet_amount = self.config["min_bet_amount"]
        self.payout = self.config["payout"]
        self.bias = self.config["bias"]  # e.g., {"H": 0.6, "T": 0.4}

    def toss(self):
        return random.choices(
            ["H", "T"], weights=[self.bias["H"], self.bias["T"]], k=1
        )[0]

    def get_result(self, choice, bet_amount, toss_result):
        if choice not in ["H", "T"]:
            raise ValueError("Invalid choice")
        if bet_amount < self.min_bet_amount:
            raise ValueError(f"Minimum bet is {self.min_bet_amount}")
        return bet_amount * self.payout if choice == toss_result else 0
