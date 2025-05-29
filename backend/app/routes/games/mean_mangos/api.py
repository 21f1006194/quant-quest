from flask_restful import Resource
from flask import request
from app.utils.auth import get_api_user
from app.utils.rate_limit import play_rate_limited
from .engine import MeanMangos
from app.services import BetService, BetData, GameSessionService, GameService


class GamePlayAPI(Resource):
    def __init__(self):
        self.engine = MeanMangos()

    @play_rate_limited
    def get(self):
        user = get_api_user()
        return {
            "game_id": self.engine.game.id,
            "game_name": self.engine.game.name,
        }

    @play_rate_limited
    def post(self):
        user = get_api_user()
        game_pnl = GameService.get_game_pnl_by_user(user.id, self.engine.game.id)
        if game_pnl.bet_count != game_pnl.session_count:
            session = GameSessionService.get_last_game_session_by_user(
                user.id, self.engine.game.id
            )
            show_price = session.session_data["show_price"]
            entry_price = session.session_data["entry_price"]
            return {
                "session_id": session.id,
                "price_data": show_price,
                "entry_price": entry_price,
                "message": "Continue the game",
            }, 200
        session_data = self.engine.new_game()
        show_price = session_data["show_price"]
        entry_price = session_data["entry_price"]
        session_id = GameSessionService.create_game_session(
            user.id, self.engine.game.id, session_data
        )
        return {
            "session_id": session_id,
            "price_data": show_price,
            "entry_price": entry_price,
        }, 201

    @play_rate_limited
    def patch(self):
        user = get_api_user()
        data = request.get_json()
        session_id = data.get("session_id")
        qty = int(data.get("qty"))
        choice = data.get("choice")
        if not session_id:
            return {"error": "session_id is required"}, 400
        if not qty:
            return {"error": "qty is required"}, 400
        if not choice:
            return {"error": "choice is required"}, 400
        # TODO: get the session
        session = GameSessionService.validate_game_session(
            user.id, self.engine.game.id, session_id
        )
        if session.max_bets_per_session <= session.bet_count:
            return {"error": "max_bets_per_session reached"}, 400
        cost, value, pnl = self.engine.get_current_value(
            choice, qty, session.session_data
        )
        bet, wallet = BetService.create_bet(
            session_id,
            BetData(
                amount=cost,
                choice=choice,
                payout=cost + pnl,
            ),
        )
        return {
            "game_data": {
                "price_data": session.session_data["show_price"],
                "entry_price": session.session_data["entry_price"],
                "future_price": session.session_data["future_price"],
                "exit_price": session.session_data["exit_price"],
            },
            "side": choice,
            "cost": cost,
            "value": value,
            "pnl": pnl,
            "current_balance": wallet.current_balance,
        }
