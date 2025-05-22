from flask_restful import Resource
from flask import request
from app.utils.auth import get_api_user
from app.utils.rate_limit import session_rate_limit, play_rate_limited
from .engine import ThreeCardPoker, HAND_TYPES
from app.services import GameSessionService, BetService, BetData


class GamePlayAPI(Resource):
    def __init__(self):
        self.engine = ThreeCardPoker()

    @play_rate_limited
    def get(self):
        user = get_api_user()
        # return the current session info
        return {"result": "current session info"}

    @play_rate_limited
    @session_rate_limit("three_card_poker")
    def post(self):
        user = get_api_user()
        data = request.get_json()
        session_data = self.engine.new_game()
        session_id = GameSessionService.create_game_session(
            user.id, self.engine.game.id, session_data
        )
        return {"session_id": session_id}

    @play_rate_limited
    def patch(self):
        user = get_api_user()
        data = request.get_json()
        session_id = data.get("session_id")
        session = GameSessionService.get_game_session(session_id)
        if not session:
            return {"error": "session not found"}, 404
        if session.user_id != user.id:
            return {"error": "unauthorized"}, 401
        if session.game_id != self.engine.game.id:
            return {"error": "invalid session"}, 400
        if session.bet_count >= self.engine.max_bet_per_session:
            return {
                "error": f"You have played {session.bet_count} bets, max is {self.engine.max_bet_per_session} per game."
            }, 400
        bet_details = session.session_data[str(session.bet_count)]
        # base_bet :  return the player hand
        # second_bet : return the house hand and the result
        if "base_bet" in data:
            bet_details["base_bet"] = data["base_bet"]
            bet_data = BetData(
                amount=data["base_bet"],
                choice="base_bet",
                payout=0.0,
                bet_details=bet_details,
            )
            bet, wallet = BetService.create_bet(session_id, bet_data)
            return {
                "bet_id": bet.id,
                "hand": bet_details["player_hand"],
                "hand_type": HAND_TYPES[bet_details["player_hand_value"][0]],
            }

        elif "raise_bet" in data and "bet_id" in data:
            bet = BetService.get_bet(data["bet_id"])
            if not bet:
                return {"error": "bet not found"}, 404
            if bet.session_id != session_id:
                return {"error": "invalid bet"}, 400
            if bet.user_id != user.id:
                return {"error": "unauthorized"}, 401
            if bet.game_id != self.engine.game.id:
                return {"error": "invalid bet"}, 400
            if bet.choice == "fold" or bet.choice == "raise":
                return {"error": "invalid raise, this has already been played!!"}, 400

            bet_details = bet.bet_details
            bet_details["raise_bet"] = data["raise_bet"]
            bet_data = BetData(
                amount=bet_details["base_bet"] + bet_details["raise_bet"],
                choice="fold" if data["raise_bet"] <= 0 else "raise",
                payout=(
                    0.0 if data["raise_bet"] <= 0 else self.engine.result(bet_details)
                ),
                bet_details=bet_details,
            )
            bet, wallet = BetService.update_bet(bet.id, session_id, bet_data)
            return {
                "bet_id": bet.id,
                "hand": bet_details["player_hand"],
                "hand_type": HAND_TYPES[bet_details["player_hand_value"][0]],
                "house_hand": bet_details["house_hand"],
                "house_hand_type": HAND_TYPES[bet_details["house_hand_value"][0]],
                "total_bet": bet_details["base_bet"] + bet_details["raise_bet"],
                "action": bet.choice,
                "payout": bet_data.payout,
            }
        else:
            return {"error": "invalid request"}
