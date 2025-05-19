# ===== FLASK API CONTROLLER =====
from flask_restful import Resource
from flask import request
from app.utils.auth import api_token_required, get_api_user
from app.utils.rate_limit import session_rate_limit
from app.services import BetService, BetData, GameSessionService
from .engine import TripleOrNothing


class TripleOrNothingAPI(Resource):
    def __init__(self):
        self.engine = TripleOrNothing()

    @api_token_required
    @session_rate_limit("triple_or_nothing")
    def get(self):
        return {
            "game_id": self.engine.game.id,
            "game_name": self.engine.game.name,
            "min_bet_amount": self.engine.min_bet_amount,
            "payouts": {
                "first": self.engine.payout_first,
                "second": self.engine.payout_second,
            },
            "bias": self.engine.bias,
        }

    @api_token_required
    @session_rate_limit("triple_or_nothing")
    def post(self):
        user = get_api_user()
        game_data = self.engine.new_game()
        toss_result = self.engine.toss()
        game_data["result"] = toss_result
        session_id = GameSessionService.create_game_session(
            user.id, self.engine.game.id, game_data
        )
        return {"session_id": session_id, "message": "First toss done. Place your bet."}, 201

    @api_token_required
    def patch(self):
        user = get_api_user()
        data = request.get_json()
        session_id = data.get("session_id")
        choice = data.get("choice")
        bet_amount = data.get("bet_amount")
        step = data.get("step")  # 1 or 2

        if not all([session_id, choice, bet_amount, step]):
            return {"error": "Missing required fields"}, 400

        session = GameSessionService.validate_game_session(
            user.id, self.engine.game.id, session_id
        )

        self.engine.check_choice(choice, step)
        toss_result = session.session_data["result"]
        payout = self.engine.get_result(choice, bet_amount, step, toss_result)

        bet, wallet = BetService.create_bet(
            session_id,
            BetData(amount=bet_amount, choice=choice, payout=payout),
        )

        return {
            "toss_result": toss_result,
            "step": step,
            "payout": payout,
            "current_balance": wallet.current_balance,
        }
