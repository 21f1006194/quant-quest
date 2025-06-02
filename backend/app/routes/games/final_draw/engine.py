import random
import numpy as np
from app.services import GameService


def next_pick():
    # Uniform: 10 integers between 1 and 2000
    uniform_nums = np.random.randint(1, 2001, size=10)

    # Normal distribution (mean=1000, std=200), 10 samples, clipped to 1-2000 and integers
    normal_nums = np.clip(np.random.normal(1000, 200, 10), 1, 2000).astype(int)

    # Bimodal: mix 5 samples from N(700, 100) and 5 samples from N(1300, 100), clipped
    bimodal_part1 = np.random.normal(700, 100, 5)
    bimodal_part2 = np.random.normal(1300, 100, 5)
    bimodal_nums = np.concatenate([bimodal_part1, bimodal_part2])
    bimodal_nums = np.clip(bimodal_nums, 1, 2000).astype(int)

    # Exponential (scale=300), shifted and clipped to 1-2000, 10 samples
    exp_nums = np.random.exponential(300, 10) + 1
    exp_nums = np.clip(exp_nums, 1, 2000).astype(int)

    # Combine all
    combined = np.concatenate([uniform_nums, normal_nums, bimodal_nums, exp_nums])

    # Pick one random number from combined and convert to Python int
    chosen = int(np.random.choice(combined))

    return chosen


class FinalDraw:
    def __init__(self):
        self.game = GameService.get_game_by_name("final_draw")
        self.config = self.game.config_data

    def start(self):
        return {
            "last_pick": next_pick(),
        }

    def next(self, game_data, choice):
        # return an integer from 1-2000 randomly
        if choice == "select":
            return {
                "last_pick": -1,
                "pick": game_data["last_pick"],
                "payout": game_data["last_pick"],
            }
        if game_data["last_pick"] != -1:
            return {
                "last_pick": next_pick(),
                "previous_pick": game_data["last_pick"],
                "payout": 0,
            }
        else:
            raise Exception("You have already selected your pick")
