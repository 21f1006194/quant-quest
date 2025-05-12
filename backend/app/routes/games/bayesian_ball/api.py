from flask_restful import Resource
from flask import request
from app.utils.auth import api_token_required, get_api_user
from app.utils.rate_limit import session_rate_limit, bets_rate_limit
from .engine import BayesianBall
from app.services import BetService, BetData, GameSessionService


class GamePlayAPI(Resource):
    def __init__(self):
        self.engine = BayesianBall()

    @api_token_required
    @session_rate_limit("bayesian_ball")
    def get(self):
        user = get_api_user()
        return {
            "game_id": self.engine.game.id,
            "game_name": self.engine.game.name,
            "bags": self.engine.bags,
            "balls": self.engine.balls,
            "min_bet_amount": self.engine.min_bet_amount,
            "payout": self.engine.payout,
        }

    @api_token_required
    @session_rate_limit("bayesian_ball")
    def post(self):
        user = get_api_user()
        data = request.get_json()
        session_data = self.engine.new_game()
        show_balls = session_data["balls"][:-1]
        # TODO: create a new session
        session_id = GameSessionService.create_game_session(
            user.id, self.engine.game.id, session_data
        )
        return {"session_id": session_id, "balls": show_balls}

    @api_token_required
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
        if session.max_bets_per_session >= session.bet_count:
            return {"error": "max_bets_per_session reached"}, 400
        payout = self.engine.get_result(choice, bet_amount, session.session_data)
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
