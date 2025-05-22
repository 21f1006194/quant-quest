from flask_restful import Resource
from flask import request
from app.utils.auth import get_api_user
from app.utils.rate_limit import session_rate_limit, bets_rate_limit, play_rate_limited

## To have custom functions for info, control;
## We can inherit from BaseGameAPI and override the methods
# from app.routes.base_game import BaseGameAPI


# class GameInfoAPI(BaseGameAPI):
#     pass

# class GameControlAPI(BaseGameAPI):
#     pass


class GamePlayAPI(Resource):
    @play_rate_limited
    def get(self):
        user = get_api_user()
        return {"trials_left": 3, "money_made": 100, "user_id": user.id}

    @play_rate_limited
    @session_rate_limit("game_template")
    def post(self):
        user = get_api_user()
        data = request.get_json()
        bet_amount = data.get("bet_amount")
        # Create new session logic here and a bet in it.
        return {"result": "played new trial"}

    @play_rate_limited
    @bets_rate_limit("game_template")
    def put(self):
        user = get_api_user()
        data = request.get_json()
        session_id = data.get("session_id")
        bet_amount = data.get("bet_amount")
        # continue betting in the same session
        return {"result": "continued previous trial"}
