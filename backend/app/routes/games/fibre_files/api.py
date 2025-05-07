from flask_restful import Resource
from flask import request
from app.utils.auth import api_token_required, get_api_user
from app.utils.rate_limit import session_rate_limit, bets_rate_limit
from .engine import FiberFilesEngine
from .utils import validate_bet_data, create_game_session_and_bet
from app.services.bet_service import BetService

class FiberFilesAPI(Resource):
    def __init__(self):
        self.engine = FiberFilesEngine()

    @api_token_required
    def get(self):
        user = get_api_user()
        bets = BetService.get_bets_for_user(user.id, self.engine.game)
        return {"bets": bets}

    @api_token_required
    @session_rate_limit("fiber_files")
    def post(self):
        try:
            user = get_api_user()
            data = request.get_json()
            validate_bet_data(data, self.engine.config_data)

            result = self.engine.get_result(data["choice"], data["bet_amount"])
            session, bet, wallet = create_game_session_and_bet(
                user.id, self.engine.game, data, result
            )

            return {
                "result": result,
                "current_balance": wallet.current_balance
            }
        except Exception as e:
            return {"error": str(e)}, 400
