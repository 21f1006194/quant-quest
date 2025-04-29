from random import randint
import json
from app.models.gameplay import Game


class TenDiceEngine:
    def __init__(self):
        self.game = Game.query.filter_by(name="ten_dice").first()
        self.config_data = self.game.config_data

    def roll_10_dice(self):
        ten_dice_sum = sum([randint(1, 6) for _ in range(10)])
        return ten_dice_sum

    def get_result(self, choice, bet_amount):
        ten_dice_sum = self.roll_10_dice()
        payout = float(self.config_data["payout"])
        if choice == ten_dice_sum:
            return {
                "dice_sum": ten_dice_sum,
                "result": "win",
                "payout": bet_amount * payout,
            }
        else:
            return {"dice_sum": ten_dice_sum, "result": "loss", "payout": 0}
