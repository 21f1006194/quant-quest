from flask_restful import Resource
from flask import request
from app.utils.auth import get_api_user
from app.utils.rate_limit import play_rate_limited
from .engine import KnapSack
from app.services import BetService, BetData, GameSessionService, GameService


class GamePlayAPI(Resource):
    def __init__(self):
        self.engine = KnapSack()

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
        # If not solved  - session.session_data["result"] !="success"
        if game_pnl and game_pnl.bet_count != game_pnl.session_count:
            session = GameSessionService.get_last_game_session_by_user(
                user.id, self.engine.game.id
            )
            assets = session.session_data["assets"]
            return {
                "session_id": session.id,
                "assets": assets,
                "attempts": game_pnl.bet_count,
                "message": "Continue the game",
            }, 200
        session_data = self.engine.new_game()
        session_id = GameSessionService.create_game_session(
            user.id, self.engine.game.id, session_data
        )
        return {
            "session_id": session_id,
            "assets": session_data["assets"],
        }, 201

    @play_rate_limited
    def patch(self):
        user = get_api_user()
        data = request.get_json()
        session_id = data.get("session_id")
        sack = data.get("sack")
        if not session_id:
            return {"error": "session_id is required"}, 400
        if not sack:
            return {"error": "sack is required"}, 400

        # TODO: get the session
        session = GameSessionService.validate_game_session(
            user.id, self.engine.game.id, session_id
        )
        if (
            session.max_bets_per_session <= session.bet_count
            and session.session_data["result"] != "success"
        ):
            return {"error": "Game completed, create new session to play"}, 400
        result = self.engine.get_result(session.session_data, sack)
        bet, wallet = BetService.create_bet(
            session_id,
            BetData(
                amount=result["bet_amount"],
                # TODO: make suer that choice can handle long text
                choice=str(",".join([asset["name"] for asset in sack])),
                payout=result["payout"],
            ),
        )
        # update game session
        new_session_data = session.session_data
        new_session_data["result"] = result["result"]
        new_session = GameSessionService.update_session_data(
            session_id, new_session_data
        )
        return {
            "session_id": session_id,
            "result": result,
            "current_balance": wallet.current_balance,
        }
