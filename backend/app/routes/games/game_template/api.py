from flask_restful import Resource

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
    def get(self):
        return {"trials_left": 3, "money_made": 100}

    def post(self):
        return {"result": "played new trial"}

    def put(self):
        return {"result": "continued previous trial"}
