from flask_restful import Resource
from flask import request
from app.utils.auth import api_token_required, get_api_user
from app.utils.rate_limit import session_rate_limit
from .engine import FibreFilesEngine
from app.services import GameSessionService, BetService, BetData, GameService

class FibreFilesAPI(Resource):
    def __init__(self):
        self.engine = FibreFilesEngine()

    @api_token_required
    @session_rate_limit("fibre_files")
    def get(self):
        user = get_api_user()
        return {
            "game_id": self.engine.game.id,
            "game_name": self.engine.game.name,
            "num_suspects": self.engine.num_suspects,
            "min_bet_amount": self.engine.min_bet_amount,
            "payout": self.engine.payout,
        }

    @api_token_required
    @session_rate_limit("fibre_files")
    def post(self):
        user = get_api_user()

        game_pnl = GameService.get_game_pnl_by_user(user.id, self.engine.game.id)
        if game_pnl.bet_count != game_pnl.session_count:
            session = GameSessionService.get_last_game_session_by_user(
                user.id, self.engine.game.id
            )
            return {
                "session_id": session.id,
                "message": "Continue the game"
            }, 200

        session_data = self.engine.new_game()
        session_id = GameSessionService.create_game_session(
            user.id, self.engine.game.id, session_data
        )

        return {"session_id": session_id, "message": "New game started"}, 201

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

        session = GameSessionService.validate_game_session(
            user.id, self.engine.game.id, session_id
        )

        if session.max_bets_per_session <= session.bet_count:
            return {"error": "Max bets reached"}, 400

        result = self.engine.get_result(choice, bet_amount, session.session_data)
        bet, wallet = BetService.create_bet(
            session_id,
            BetData(
                amount=bet_amount,
                choice=choice,
                payout=result["payout"],
            )
        )

        return {
            "game_data": session.session_data,
            "payout": result["payout"],
            "actual": result["actual"],
            "current_balance": wallet.current_balance
        }
