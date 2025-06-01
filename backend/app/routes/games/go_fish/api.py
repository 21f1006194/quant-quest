from flask_restful import Resource
from flask import request
from app.utils.auth import get_api_user
from app.utils.rate_limit import play_rate_limited
from .engine import GoFish
from app.services import GameSessionService, BetService, BetData, GameService


class GamePlayAPI(Resource):
    def __init__(self):
        self.engine = GoFish()

    @play_rate_limited
    def get(self):
        user = get_api_user()
        # return the current session info
        game_pnl = GameService.get_game_pnl_by_user(user.id, self.engine.game.id)
        return {
            "game_id": self.engine.game.id,
            "game_name": self.engine.game.name,
            "max_bet_per_session": self.engine.max_bet_per_session,
            "half_guess_payout": self.engine.half_guess_payout,
            "full_guess_payout": self.engine.full_guess_payout,
            "last_session_id": GameSessionService.get_last_game_session_by_user(
                user.id, self.engine.game.id
            ).id,
        }

    @play_rate_limited
    def post(self):
        user = get_api_user()
        game_pnl = GameService.get_game_pnl_by_user(user.id, self.engine.game.id)
        if (
            game_pnl.bet_count
            != game_pnl.session_count * self.engine.max_bet_per_session
        ):
            session = GameSessionService.get_last_game_session_by_user(
                user.id, self.engine.game.id
            )
            initial_cards = session.session_data["initial_cards"]
            fish_cards = session.session_data["fish_cards"][
                : game_pnl.bet_count % self.engine.max_bet_per_session
            ]

            return {
                "session_id": session.id,
                "initial_cards": initial_cards,
                "revealed_cards": fish_cards,
                "message": f"Continue the game, you have {self.engine.max_bet_per_session - len(fish_cards)} bets left",
            }, 200
        session_data = self.engine.new_game()
        initial_cards = session_data["initial_cards"]
        session_id = GameSessionService.create_game_session(
            user.id, self.engine.game.id, session_data
        )
        return {"session_id": session_id, "initial_cards": initial_cards}, 201

    @play_rate_limited
    def patch(self):
        try:
            user = get_api_user()
            data = request.get_json()
            session_id = data.get("session_id")
            session = GameSessionService.get_game_session(session_id)
            this_bet_count = session.bet_count + 1
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
            session_data = session.session_data
            if this_bet_count > len(session_data["fish_cards"]):
                return {"error": "no more bets"}, 400
            # base_bet :  return the player hand
            # second_bet : return the house hand and the result
            bet_amount = data["bet_amount"]
            choice = data["choice"]
            res = self.engine.get_result(
                session_data, this_bet_count, choice, bet_amount
            )
            bet_data = BetData(
                amount=bet_amount,
                choice=choice,
                payout=res["payout"],
                bet_details=res,
            )
            bet, wallet = BetService.create_bet(session_id, bet_data)
            return {
                "bet_id": bet.id,
                "fishing_count": this_bet_count,
                "result": res,
                "current_balance": wallet.current_balance,
            }
        except Exception as e:
            return {"error": str(e)}, 500
