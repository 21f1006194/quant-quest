from flask_restful import Resource
from flask import request
from app.utils.auth import get_api_user
from app.utils.rate_limit import play_rate_limited
from .engine import SniperShotEngine
from .utils import validate_bet_data, create_game_session_and_bet
from app.services.bet_service import BetService


class GamePlayAPI(Resource):
    def __init__(self):
        self.engine = SniperShotEngine()

    @play_rate_limited
    def get(self):
        user = get_api_user()
        bets = BetService.get_bets_for_user(user.id, self.engine.game)
        return {"bets": bets}

    @play_rate_limited
    def post(self):
        try:
            user = get_api_user()
            data = request.get_json()
            validate_bet_data(data, self.engine.config_data)

            # Get result from game engine
            result = self.engine.get_result(data["choice"], data["bet_amount"])

            # Create session and bet
            session, bet, wallet = create_game_session_and_bet(
                user.id, self.engine.game, data, result
            )

            return {
                "result": result,
                "current_balance": wallet.current_balance,
            }
        except Exception as e:
            return {"error": str(e)}, 400
