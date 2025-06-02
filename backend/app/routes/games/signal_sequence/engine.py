# backend\app\routes\games\coin_toss\engine.py

import random
from app.services import GameService


class SignalSequence:
    def __init__(self):
        self.game = GameService.get_game_by_name("signal_sequence")
        self.config = self.game.config_data
        self.min_bet_amount = self.config["min_bet_amount"]
        self.colors = ["Red", "Blue", "Green", "Yellow", "Purple"]
        # self.probabilities = [0.3, 0.25, 0.2, 0.15, 0.1]
        self.probabilities = [0.5, 0.2, 0.15, 0.1, 0.05]

    def start_game(self):
        sequence = []
        available_colors = self.colors[:]
        available_probs = self.probabilities[:]

        for _ in range(4):
            # Normalize current probabilities
            total = sum(available_probs)
            normalized_probs = [p / total for p in available_probs]

            # Sample one item using current weights
            chosen_index = random.choices(
                range(len(available_colors)), weights=normalized_probs, k=1
            )[0]
            chosen_color = available_colors.pop(chosen_index)
            available_probs.pop(chosen_index)

            sequence.append(chosen_color)
        print(sequence)
        return {"sequence": sequence}

    def get_result(self, choice, bet_amount, sequence, bet_count):
        if choice not in self.colors:
            raise ValueError("Invalid choice")
        if bet_amount < self.min_bet_amount:
            raise ValueError(f"Minimum bet is {self.min_bet_amount}")
        if choice == sequence[bet_count]:
            return (bet_count + 1) * bet_amount
        else:
            return 0
