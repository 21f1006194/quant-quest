from flask_restful import Resource
from flask import request
from app.utils.auth import get_api_user
from app.utils.rate_limit import play_rate_limited
from .engine import SignalSequence
from app.services import BetService, BetData, GameSessionService, GameService


class GamePlayAPI(Resource):
    def __init__(self):
        self.engine = SignalSequence()

    @play_rate_limited
    def get(self):
        return {
            "game_id": self.engine.game.id,
            "game_name": self.engine.game.name,
            "min_bet_amount": self.engine.min_bet_amount,
        }

    @play_rate_limited
    def post(self):
        user = get_api_user()
        session = GameSessionService.get_last_game_session_by_user(
            user.id, self.engine.game.id
        )
        if "streak" not in session.session_data:
            return {
                "session_id": session.id,
                "message": "Continue the game",
            }, 200

        session_data = self.engine.start_game()
        session_id = GameSessionService.create_game_session(
            user.id, self.engine.game.id, session_data
        )
        return {
            "session_id": session_id,
            "message": "Game started, now place your bet.",
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
        sequence = session.session_data["sequence"]
        if "streak" in session.session_data:
            return {"error": "Game already ended"}, 400
        payout = self.engine.get_result(choice, bet_amount, sequence, session.bet_count)
        if payout == 0:
            updated_session = {
                "sequence": sequence,
                "streak": session.bet_count + 1,
            }
            new_session = GameSessionService.update_game_session(
                session_id, updated_session
            )
        bet, wallet = BetService.create_bet(
            session_id,
            BetData(amount=bet_amount, choice=choice, payout=payout),
        )
        return {
            "session_id": new_session.id,
            "payout": payout,
            "sequence": sequence[: session.bet_count + 1],
            "streak": new_session.bet_count,
            "current_balance": wallet.current_balance,
        }, 200
