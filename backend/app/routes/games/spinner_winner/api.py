from flask_restful import Resource
from flask import request
from app.utils.auth import get_api_user
from app.utils.rate_limit import play_rate_limited
from .engine import SpinnerWinner
from app.services import BetService, BetData, GameSessionService, GameService


class GamePlayAPI(Resource):
    def __init__(self):
        self.engine = SpinnerWinner()

    @play_rate_limited
    def get(self):
        user = get_api_user()
        return {
            "game_id": self.engine.game.id,
            "game_name": self.engine.game.name,
            "min_bet_amount": self.engine.min_bet_amount,
        }

    @play_rate_limited
    def post(self):
        user = get_api_user()
        game_pnl = GameService.get_game_pnl_by_user(user.id, self.engine.game.id)
        if game_pnl and game_pnl.bet_count != game_pnl.session_count:
            session = GameSessionService.get_last_game_session_by_user(
                user.id, self.engine.game.id
            )
            show_wheel = session.session_data["wheel"]

            return {
                "session_id": session.id,
                "wheel": show_wheel,
                "message": "Continue the game",
            }, 200
        session_data = self.engine.new_game()
        show_wheel = session_data["wheel"]
        session_id = GameSessionService.create_game_session(
            user.id, self.engine.game.id, session_data
        )
        return {"session_id": session_id, "wheel": show_wheel}, 201

    @play_rate_limited
    def patch(self):
        user = get_api_user()
        data = request.get_json()
        session_id = data.get("session_id")
        bet_amount = data.get("bet_amount")
        choice = data.get("choice")
        if not session_id:
            return {"error": "session_id is required"}, 400
        if not bet_amount:
            return {"error": "bet_amount is required"}, 400
        if not choice:
            return {"error": "choice is required"}, 400
        # TODO: get the session
        session = GameSessionService.validate_game_session(
            user.id, self.engine.game.id, session_id
        )
        if session.max_bets_per_session <= session.bet_count:
            return {"error": "max_bets_per_session reached"}, 400
        result = self.engine.get_result(choice, bet_amount, session.session_data)
        payout = result["payout"]
        bet, wallet = BetService.create_bet(
            session_id,
            BetData(
                amount=bet_amount,
                choice=choice,
                payout=payout,
            ),
        )
        return {
            "game_data": session.session_data,
            "payout": payout,
            "current_balance": wallet.current_balance,
        }
