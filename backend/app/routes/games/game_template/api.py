from flask_restful import Resource
from flask import request
from app.utils.auth import api_token_required, get_api_user
from app.utils.rate_limit import session_rate_limit, bets_rate_limit

## To have custom functions for info, control;
## We can inherit from BaseGameAPI and override the methods
# from app.routes.base_game import BaseGameAPI


# class GameInfoAPI(BaseGameAPI):
#     pass

# class GameControlAPI(BaseGameAPI):
#     pass


class GamePlayAPI(Resource):
    @api_token_required
    def get(self):
        user = get_api_user()
        return {"trials_left": 3, "money_made": 100, "user_id": user.id}

    @api_token_required
    @session_rate_limit("game_template")
    def post(self):
        user = get_api_user()
        data = request.get_json()
        bet_amount = data.get("bet_amount")
        # Create new session logic here and a bet in it.
        return {"result": "played new trial"}

    @api_token_required
    @bets_rate_limit("game_template")
    def put(self):
        user = get_api_user()
        data = request.get_json()
        session_id = data.get("session_id")
        bet_amount = data.get("bet_amount")
        # continue betting in the same session
        return {"result": "continued previous trial"}
