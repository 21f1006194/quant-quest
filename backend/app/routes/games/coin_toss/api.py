# backend\app\routes\games\coin_toss\api.py

from flask_restful import Resource
from flask import request
from app.utils.auth import get_api_user
from app.utils.rate_limit import session_rate_limit, play_rate_limited
from .engine import CoinToss
from app.services import BetService, BetData, GameSessionService, GameService


class GamePlayAPI(Resource):
    def __init__(self):
        self.engine = CoinToss()

    @play_rate_limited
    @session_rate_limit("coin_toss")
    def get(self):
        return {
            "game_id": self.engine.game.id,
            "game_name": self.engine.game.name,
            "min_bet_amount": self.engine.min_bet_amount,
            "payout": self.engine.payout,
        }

    @play_rate_limited
    @session_rate_limit("coin_toss")
    def post(self):
        user = get_api_user()
        game_pnl = GameService.get_game_pnl_by_user(user.id, self.engine.game.id)
        if game_pnl.bet_count != game_pnl.session_count:
            session = GameSessionService.get_last_game_session_by_user(
                user.id, self.engine.game.id
            )
            return {
                "session_id": session.id,
                "message": "Continue the game",
            }, 200

        toss_result = self.engine.toss()
        session_data = {"result": toss_result}
        session_id = GameSessionService.create_game_session(
            user.id, self.engine.game.id, session_data
        )
        return {
            "session_id": session_id,
            "message": "Toss completed, now place your bet.",
        }, 201

    @play_rate_limited
    def patch(self):
        user = get_api_user()
        data = request.get_json()
        session_id = data.get("session_id")
        bet_amount = data.get("bet_amount")
        choice = data.get("choice")

        if not all([session_id, bet_amount, choice]):
            return {"error": "Missing fields"}, 400

        session = GameSessionService.validate_game_session(
            user.id, self.engine.game.id, session_id
        )
        toss_result = session.session_data["result"]

        payout = self.engine.get_result(choice, bet_amount, toss_result)
        bet, wallet = BetService.create_bet(
            session_id,
            BetData(amount=bet_amount, choice=choice, payout=payout),
        )

        return {
            "toss_result": toss_result,
            "payout": payout,
            "current_balance": wallet.current_balance,
        }
