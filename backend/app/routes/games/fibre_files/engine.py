# engine.py
import numpy as np
from app.models.gameplay import Game

class FibreFilesEngine:
    def __init__(self):
        self.game = Game.query.filter_by(name="fibre_files").first()
        self.config_data = self.game.config_data
        self.num_suspects = 10
        self.min_bet_amount = self.config_data["min_bet_amount"]
        self.payout = self.config_data["payout"]

    def new_game(self):
        priors = np.full(self.num_suspects, 1 / self.num_suspects).tolist()
        likelihoods = np.random.uniform(0.1, 0.9, self.num_suspects).tolist()
        return {
            "priors": priors,
            "likelihoods": likelihoods
        }

    def calculate_posteriors(self, priors, likelihoods):
        numerators = np.array(likelihoods) * np.array(priors)
        denominator = np.sum(numerators)
        return (numerators / denominator).tolist()

    def get_result(self, choice, bet_amount, session_data):
        if bet_amount < self.min_bet_amount:
            raise ValueError("Bet amount too low")

        posteriors = self.calculate_posteriors(
            session_data["priors"], session_data["likelihoods"]
        )
        predicted = int(np.argmax(posteriors))

        if choice == predicted:
            return {
                "result": "correct",
                "payout": bet_amount * self.payout,
                "actual": predicted,
                "posteriors": posteriors
            }
        else:
            return {
                "result": "incorrect",
                "payout": 0,
                "actual": predicted,
                "posteriors": posteriors
            }
