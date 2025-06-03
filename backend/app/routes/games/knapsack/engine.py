import random
from app.services import GameService
import numpy as np


class KnapSack:
    def __init__(self):
        self.game = GameService.get_game_by_name("knapsack")
        self.config = self.game.config_data

    def generate_base_assets(self):
        base_assets = [
            {"name": "Gold Coin", "value": 100, "weight": 5},
            {"name": "Silver Bar", "value": 80, "weight": 10},
            {"name": "Painting", "value": 150, "weight": 15},
            {"name": "Laptop", "value": 120, "weight": 7},
            {"name": "Diamond", "value": 200, "weight": 3},
            {"name": "Rare Stamp", "value": 90, "weight": 2},
            {"name": "Smartphone", "value": 130, "weight": 6},
            {"name": "Antique Vase", "value": 170, "weight": 9},
        ]
        random.shuffle(base_assets)
        return base_assets[:6]

    def new_game(self, decision_day=50, days_total=60):
        # 14,17, 22, 29, 25, 30 -- select a capacity from this
        session_data = {
            "capacity": random.choice([14, 17, 20, 22, 29, 25, 30]),
            "assets": self.generate_base_assets(),
            "result": "nil",
        }

    def get_result(self, session_data, sack):
        total_weight = sum(item["weight"] for item in sack)
        total_value = sum([item["value"] for item in sack])
        if total_weight > session_data["capacity"]:
            # Over weight - loose
            return {"bet_amount": total_value, "payout": 0, "result": "Over weight"}
        elif total_weight == session_data["capacity"]:
            # Success
            return {
                "bet_amount": total_value,
                "payout": total_value * 2,
                "result": "success",
            }
        else:
            return {
                "bet_amount": total_value,
                "payout": total_value,
                "result": "Under weight",
            }
