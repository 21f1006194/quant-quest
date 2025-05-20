import random
from app.services import GameService


class SpinnerWinner:
    def __init__(self):
        self.game = GameService.get_game_by_name("spinner_winner")
        self.game_config = self.game.config_data
        self.min_bet_amount = self.game_config["min_bet_amount"]

    def new_game(self, num_segments=5):
        colors_pool = [
            "Red",
            "Blue",
            "Green",
            "Yellow",
            "Purple",
            "Orange",
            "Cyan",
            "Pink",
        ]
        colors = random.sample(colors_pool, k=num_segments)

        raw_angles = [random.randint(30, 120) for _ in range(num_segments)]
        total_angle = sum(raw_angles)
        angles = [round(a * 360 / total_angle) for a in raw_angles]
        probs = [a / 360 for a in angles]

        payouts = []
        evs = []
        for prob in probs:
            base_ev = random.uniform(0.6, 1.0)
            payout = round(base_ev / prob, 2)
            payouts.append(payout)
            evs.append(base_ev)

        # Boost EV for 1 or 2 segments
        boost_indices = random.sample(range(num_segments), k=random.choice([1, 2]))
        for i in boost_indices:
            better_ev = random.uniform(1.05, 1.15)
            payouts[i] = round(better_ev / probs[i], 2)
            evs[i] = better_ev

        wheel = []
        start_angle = 0
        for color, angle, payout, prob, ev in zip(colors, angles, payouts, probs, evs):
            wheel.append(
                {
                    "color": color,
                    "angle": angle,
                    "payout": payout,
                    # "probability": round(prob, 3),
                    # "ev": round(ev, 3),
                    "start_angle": start_angle,
                    "end_angle": start_angle + angle,
                }
            )
            start_angle += angle

        # Simulate spin
        spin_angle = random.uniform(0, 360)
        result_color = None
        for segment in wheel:
            if segment["start_angle"] <= spin_angle < segment["end_angle"]:
                result_color = segment["color"]
                break

        game_data = {
            "wheel": wheel,
            "spin_angle": round(spin_angle, 2),
            "result_color": result_color,
        }
        print("Game data", game_data)
        return game_data

    def check_choice(self, choice, game_data):
        return any(segment["color"] == choice for segment in game_data["wheel"])

    def get_result(self, choice, bet_amount, game_data):
        if not self.check_choice(choice, game_data):
            raise ValueError("Invalid color choice.")

        if bet_amount < self.min_bet_amount:
            raise ValueError(
                f"Bet amount must be greater than or equal to {self.min_bet_amount}."
            )

        result_color = game_data["result_color"]
        won = choice == result_color
        payout_multiplier = 0

        if won:
            payout_multiplier = next(
                segment["payout"]
                for segment in game_data["wheel"]
                if segment["color"] == choice
            )
            final_tokens = round(bet_amount * payout_multiplier, 2)
        else:
            final_tokens = 0

        payout_multiplier = 0 if not won else payout_multiplier
        return {
            "won": won,
            "result_color": result_color,
            "payout": payout_multiplier * bet_amount,
            "final_tokens": final_tokens,
        }
