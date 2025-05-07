import numpy as np
from app.models.gameplay import Game

class FiberFilesEngine:
    def __init__(self):
        self.game = Game.query.filter_by(name="fiber_files").first()
        self.config_data = self.game.config_data
        self.num_suspects = 10

        # Priors: P(H_i)
        self.priors = np.full(self.num_suspects, 1 / self.num_suspects)

        # Likelihoods: P(E | H_i)
        self.likelihoods = np.random.uniform(0.1, 0.9, self.num_suspects)
    
    def calculate_posteriors(self):
        numerators = self.likelihoods * self.priors
        denominator = np.sum(numerators)
        return numerators / denominator

    def get_result(self, choice, bet_amount):
        posteriors = self.calculate_posteriors()
        predicted = np.argmax(posteriors)

        if choice == predicted:
            payout = float(self.config_data["payout"])
            return {"result": "correct", "payout": bet_amount * payout, "actual": predicted}
        else:
            return {"result": "incorrect", "payout": 0, "actual": predicted}
