# backend\app\routes\games\coin_toss\api.py

from flask_restful import Resource
from flask import request
from app.utils.auth import get_api_user
from app.utils.rate_limit import play_rate_limited
from .engine import FinalDraw
from app.services import BetService, BetData, GameSessionService, GameService


class GamePlayAPI(Resource):
    def __init__(self):
        self.engine = FinalDraw()

    @play_rate_limited
    def get(self):
        user = get_api_user()
        session = GameSessionService.get_last_game_session_by_user(
            user.id, self.engine.game.id
        )
        if session is None:
            return {"message": "No game session found"}, 200
        if session.session_data["last_pick"] == -1:
            lp = session.session_data["pick"]
        else:
            lp = session.session_data["last_pick"]
        return {
            "session_id": session.id,
            "last_pick": lp,
        }

    @play_rate_limited
    def post(self):
        user = get_api_user()
        session = GameSessionService.get_last_game_session_by_user(
            user.id, self.engine.game.id
        )
        game_pnl = GameService.get_game_pnl_by_user(user.id, self.engine.game.id)

        if (
            session is not None
            and game_pnl.bet_count < self.engine.game.max_bets_per_session
        ):
            session_data = session.session_data
            if session_data["last_pick"] != -1:
                return {
                    "session_id": session.id,
                    "last_pick": session_data["last_pick"],
                    "message": "Continue the game",
                }, 200

        game_data = self.engine.start()
        new_session_id = GameSessionService.create_game_session(
            user.id, self.engine.game.id, game_data
        )
        return {"session_id": new_session_id, "last_pick": game_data["last_pick"]}

    @play_rate_limited
    def patch(self):
        user = get_api_user()
        data = request.get_json()
        session_id = data.get("session_id")
        choice = data.get("choice")
        if choice not in ["select", "skip"]:
            return {
                "error": "Invalid choice, choice must be either select or skip"
            }, 400

        if not all([session_id, choice]):
            return {"error": "Missing fields"}, 400

        session = GameSessionService.validate_game_session(
            user.id, self.engine.game.id, session_id
        )
        if session.session_data["last_pick"] == -1:
            return {"error": "You have already selected your pick for this session_id"}
        session_data_updated = self.engine.next(session.session_data, choice)
        bet, wallet = BetService.create_bet(
            session_id,
            BetData(
                amount=self.engine.minimum_bet,
                choice=choice,
                payout=session_data_updated["payout"],
            ),
        )
        updated_session = GameSessionService.update_session_data(
            session_id, session_data_updated
        )

        session_data_updated.update(
            {
                "session_id": session_id,
                "bet_id": bet.id,
                "bet_count": updated_session.bet_count,
                "current_balance": wallet.current_balance,
            }
        )
        return session_data_updated, 200
