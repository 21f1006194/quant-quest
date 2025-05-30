# backend\app\routes\games\coin_toss\engine.py

import random
from app.services import GameService


class NDicesEngine:
    def __init__(self):
        self.game = GameService.get_game_by_name("n_dices")
        self.config_data = self.game.config_data
        self.min_bet_amount = self.config_data["min_bet_amount"]
        self.payout = self.config_data["payout"]

    def roll(self):
        n = random.randint(5, 15)
        roll = [random.randint(1, 6) for _ in range(n)]
        n_sum = sum(roll)
        return {"dice_sum": n_sum, "roll": roll, "n": n}

    def get_result(self, choice, bet_amount, game_data):
        payout = float(self.config_data["payout"])
        if int(choice) == int(game_data["dice_sum"]):
            return {
                "dice_sum": game_data["dice_sum"],
                "roll": game_data["roll"],
                "result": "win",
                "payout": bet_amount * payout,
            }
        else:
            return {
                "dice_sum": game_data["dice_sum"],
                "roll": game_data["roll"],
                "result": "loss",
                "payout": 0,
            }
