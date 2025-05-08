import numpy as np
from app.models.gameplay import Game


class SniperShotEngine:
    def __init__(self):
        self.n = 27
        self.p = 0.7
        self.game = Game.query.filter_by(name="sniper_shot").first()
        self.config_data = self.game.config_data

    def simulate_game(self):
        hits = np.random.binomial(self.n, self.p)
        return hits

    def get_result(self, choice, bet_amount):
        total_hits = self.simulate_game()
        payout = float(self.config_data["payout"])
        if choice == total_hits:
            return {"result": "win", "payout": bet_amount * payout}
        else:
            return {"result": "loss", "payout": 0}


if __name__ == "__main__":
    engine = SniperShotEngine()
    print(engine.simulate_game())
