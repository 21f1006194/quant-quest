from flask_restful import Resource
from app.utils.auth import api_token_required, get_api_user

## To have custom functions for status, description, control;
## We can inherit from BaseGameAPI and override the methods
# from app.routes.base_game import BaseGameAPI

# class GameStatusAPI(BaseGameAPI):
#     pass

# class GameDescriptionAPI(BaseGameAPI):
#     pass

# class GameControlAPI(BaseGameAPI):
#     pass


class GamePlayAPI(Resource):
    @api_token_required
    def get(self):
        user = get_api_user()
        return {"trials_left": 3, "money_made": 100, "user_id": user.id}

    @api_token_required
    def post(self):
        return {"result": "played new trial"}

    @api_token_required
    def put(self):
        return {"result": "continued previous trial"}
