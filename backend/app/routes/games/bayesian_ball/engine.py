import random
from app.services import GameService


class BayesianBall:
    def __init__(self):
        self.game = GameService.get_game_by_name("bayesian_ball")
        self.config = self.game.config_data
        self.min_bet_amount = self.config["min_bet_amount"]
        self.payout = self.config["payout"]
        self.bags = ["A", "B", "C", "D"]
        self.balls = ["R", "G", "B"]
        self.bag_probabilities = [0.3, 0.35, 0.2, 0.15]
        self.bag_contents_probabilities = {
            "A": {"R": 0.3, "G": 0.4, "B": 0.3},
            "B": {"R": 0.4, "G": 0.3, "B": 0.3},
            "C": {"R": 0.25, "G": 0.5, "B": 0.25},
            "D": {"R": 0.2, "G": 0.2, "B": 0.6},
        }

    def new_game(self):
        bag = random.choices(self.bags, weights=self.bag_probabilities, k=1)[0]
        # pick 10 balls from the bag with replacement
        balls = random.choices(
            self.balls, weights=self.bag_contents_probabilities[bag].values(), k=10
        )
        return {"bag": bag, "balls": balls}

    def check_choice(self, choice, game_data):
        if choice[0] not in self.bags:
            raise ValueError("Invalid bag")
        if choice[1] not in self.balls:
            raise ValueError("Invalid ball")
        last_ball = game_data["bag"] + game_data["balls"][-1]
        if last_ball == choice:
            return True
        else:
            return False

    def get_result(self, choice, bet_amount, game_data):
        if len(choice) != 2:
            raise ValueError("Choice must be a two character string")
        if bet_amount < self.min_bet_amount:
            raise ValueError(
                f"Bet amount must be greater than or equal to {self.min_bet_amount}"
            )
        if self.check_choice(choice, game_data):
            return bet_amount * self.payout
        else:
            return 0
