import random
from collections import defaultdict
from app.services import GameService


class GameOverError(Exception):
    """Raised when the game cannot continue due to no remaining attempts."""
    pass


class ThreeDoorsMaze:
    def __init__(self):
        self.game = GameService.get_game_by_name("three_doors_maze")
        self.config = self.game.config_data
        self.min_bet_amount = self.config["min_bet_amount"]
        self.payout = self.config["payout"]
        self.depth = self.config.get("depth", 10)
        self.max_attempts_per_door = self.config.get("max_attempts_per_door", 3)
        self.doors = ["A", "B", "C"]
        self.graph = defaultdict(dict)
        self.success_probs = defaultdict(dict)
        self.attempts_left = defaultdict(dict)
        self.end_room = None
        self.priors = defaultdict(lambda: {door: 0.33 for door in self.doors})
        self._build_maze()

    def _build_maze(self):
        room_id_counter = 0
        queue = [(0, 0)]
        visited = set()
        max_depth_room = 0

        while queue:
            room_id, level = queue.pop(0)
            if room_id in visited:
                continue
            visited.add(room_id)
            if level >= self.depth:
                continue

            for door in self.doors:
                next_room = room_id_counter + 1
                room_id_counter += 1
                self.graph[room_id][door] = next_room
                self.success_probs[room_id][door] = round(random.uniform(0.5, 0.9), 2)
                self.attempts_left[room_id][door] = self.max_attempts_per_door
                queue.append((next_room, level + 1))
                if level + 1 == self.depth:
                    max_depth_room = next_room

            if level > 0 and random.random() < 0.3:
                rand_room = random.randint(0, room_id_counter - 2)
                rand_door = random.choice(self.doors)
                self.graph[room_id][rand_door] = rand_room

        self.end_room = room_id_counter + 1
        if max_depth_room:
            end_door = random.choice(self.doors)
            self.graph[max_depth_room][end_door] = self.end_room

    def get_metadata(self):
        return {
            "game_id": self.game.id,
            "game_name": self.game.name,
            "doors": self.doors,
            "min_bet_amount": self.min_bet_amount,
            "payout": self.payout,
            "depth": self.depth,
            "max_attempts_per_door": self.max_attempts_per_door,
        }

    def should_resume_game(self, user_id):
        pnl = GameService.get_game_pnl_by_user(user_id, self.game.id)
        return pnl.bet_count != pnl.session_count

    def new_game(self):
        return {
            "current_room": 0,
            "visited": [],
            "hint": self._generate_hint(0),
            "bayesian_probs": self.priors[0].copy(),
        }

    def check_choice(self, choice, game_data):
        if choice not in self.doors:
            raise ValueError("Invalid door")
        
        room = game_data["current_room"]
        if room not in self.graph:
            raise ValueError("Invalid room state")

        if self.attempts_left[room][choice] <= 0:
            if all(self.attempts_left[room][d] <= 0 for d in self.doors):
                raise GameOverError("No attempts left for any door in this room")
            raise ValueError(f"No attempts left for door {choice}")

        self.attempts_left[room][choice] -= 1
        success_prob = self.success_probs[room][choice]
        success = random.random() < success_prob

        self._update_priors(room, choice, success)

        if success:
            next_room = self.graph[room][choice]
            game_data["visited"].append(room)
            game_data["current_room"] = next_room
            hint = None if next_room == self.end_room else self._generate_hint(next_room)
            game_data["hint"] = hint
            game_data["bayesian_probs"] = self.priors[next_room].copy() if next_room != self.end_room else {}
        else:
            game_data["hint"] = self._generate_hint(room, misleading=random.random() < 0.2)
            game_data["bayesian_probs"] = self.priors[room].copy()

        return game_data

    def _generate_hint(self, room_id, misleading=False):
        if room_id not in self.success_probs or not self.success_probs[room_id]:
            return "No data available for this room."
        probabilities = self.success_probs[room_id]
        sorted_doors = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        if misleading:
            return f"Door {sorted_doors[-1][0]} might be worth trying."
        return f"Door {sorted_doors[0][0]} seems promising."

    def _update_priors(self, room, door, success):
        for d in self.doors:
            prior = self.priors[room][d]
            if d == door:
                likelihood = self.success_probs[room][d] if success else (1 - self.success_probs[room][d])
            else:
                likelihood = (1 - self.success_probs[room][d])  # Assume failure for unchosen doors
            self.priors[room][d] = prior * likelihood
        
        total = sum(self.priors[room].values())
        for d in self.doors:
            self.priors[room][d] = self.priors[room][d] / total if total > 0 else 0.33

    def get_result(self, choice, bet_amount, game_data):
        if choice not in self.doors:
            raise ValueError("Invalid door")
        if bet_amount < self.min_bet_amount:
            raise ValueError(f"Bet amount must be >= {self.min_bet_amount}")

        game_data = self.check_choice(choice, game_data)
        if game_data["current_room"] == self.end_room:
            return bet_amount * self.payout
        return 0