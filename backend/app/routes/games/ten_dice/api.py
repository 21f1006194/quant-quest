from flask_restful import Resource
from flask import request
from app.utils.auth import get_api_user
from app.utils.rate_limit import session_rate_limit, play_rate_limited
from .engine import TenDiceEngine
from .utils import validate_bet_data, create_game_session_and_bet, get_bets_for_user


class GamePlayAPI(Resource):
    def __init__(self):
        self.engine = TenDiceEngine()

    @play_rate_limited
    def get(self):
        user = get_api_user()
        # TODO: Get game status for the user
        bets = get_bets_for_user(user.id, self.engine.game)
        return {"bets": bets}

    @play_rate_limited
    @session_rate_limit("ten_dice")
    def post(self):
        try:
            user = get_api_user()
            play_data = request.get_json()
            validate_bet_data(play_data, self.engine.config_data)

            # Get result from game engine
            result = self.engine.get_result(
                play_data["choice"], play_data["bet_amount"]
            )

            # Create session and bet
            session, bet, wallet = create_game_session_and_bet(
                user_id=user.id,
                game=self.engine.game,
                bet_data=play_data,
                result=result,
            )

            return {
                "result": result,
                "current_balance": wallet.current_balance,
            }
        except Exception as e:
            return {"error": str(e)}, 400
