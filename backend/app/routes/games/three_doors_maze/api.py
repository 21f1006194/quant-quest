# api.py
from flask_restful import Resource
from flask import request
from app.utils.auth import api_token_required, get_api_user
from app.utils.rate_limit import session_rate_limit
from app.services import BetService, BetData, GameSessionService, GameService
from .engine import ThreeDoorsMaze

class ThreeDoorsMazeAPI(Resource):
    def __init__(self):
        self.engine = ThreeDoorsMaze()

    @api_token_required
    @session_rate_limit("three_doors_maze")
    def get(self):
        user = get_api_user()
        return self.engine.get_metadata()

    @api_token_required
    @session_rate_limit("three_doors_maze")
    def post(self):
        user = get_api_user()
        if self.engine.should_resume_game(user.id):
            session = GameSessionService.get_last_game_session_by_user(user.id, self.engine.game.id)
            return {
                "session_id": session.id,
                "game_data": session.session_data,
                "message": "Continue the game",
            }, 200
        session_data = self.engine.new_game()
        session_id = GameSessionService.create_game_session(user.id, self.engine.game.id, session_data)
        return {"session_id": session_id, "game_data": session_data}, 201

    @api_token_required
    def patch(self):
        user = get_api_user()
        data = request.get_json()
        session_id = data.get("session_id")
        bet_amount = data.get("bet_amount")
        choice = data.get("choice")

        if not session_id or not bet_amount or not choice:
            return {"error": "session_id, bet_amount, and choice are required"}, 400

        session = GameSessionService.validate_game_session(user.id, self.engine.game.id, session_id)
        if session.max_bets_per_session <= session.bet_count:
            return {"error": "max_bets_per_session reached"}, 400

        updated_data, payout = self.engine.make_choice(session.session_data, choice, bet_amount)
        bet, wallet = BetService.create_bet(session_id, BetData(amount=bet_amount, choice=choice, payout=payout))
        GameSessionService.update_game_session(session.id, updated_data)

        return {
            "game_data": updated_data,
            "payout": payout,
            "current_balance": wallet.current_balance,
        }
