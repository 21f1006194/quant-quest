# ===== ENGINE (server-side logic) =====
import random
from app.services import GameService


class TripleOrNothing:
    def __init__(self):
        self.game = GameService.get_game_by_name("triple_or_nothing")
        self.config = self.game.config_data
        self.min_bet_amount = self.config["min_bet_amount"]
        self.payout_first = self.config["payout_first"]
        self.payout_second = self.config["payout_second"]
        self.bias = self.config["bias"]  # {"H": 0.5, "T": 0.5}

    def new_game(self):
        return {"step": 1, "result": None, "winnings": 0}

    def check_choice(self, choice, step):
        if choice not in ["H", "T"]:
            raise ValueError("Invalid choice: must be 'H' or 'T'")
        if step not in [1, 2]:
            raise ValueError("Invalid game step")

    def get_result(self, choice, bet_amount, step, toss_result):
        if bet_amount < self.min_bet_amount:
            raise ValueError(f"Minimum bet is {self.min_bet_amount}")

        if step == 1:
            if choice == toss_result:
                return bet_amount * self.payout_first  # win x
            else:
                return 0  # lost

        elif step == 2:
            if choice == toss_result:
                return bet_amount * self.payout_second  # win 3x
            else:
                return 0  # lost all winnings

    def toss(self):
        return random.choices(["H", "T"], weights=[self.bias["H"], self.bias["T"]], k=1)[0]
