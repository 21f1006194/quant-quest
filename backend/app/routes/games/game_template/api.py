from flask_restful import Resource


class GameStatusAPI(Resource):
    def get(self):
        return {"status": "active"}


class GameDescriptionAPI(Resource):
    def get(self):
        return {"description": "Your game description here"}


class GameControlAPI(Resource):
    def get(self):
        return {"control": {"rate_limit": 5, "max_trials": 10}}


class GamePlayAPI(Resource):
    def get(self):
        return {"trials_left": 3, "money_made": 100}

    def post(self):
        return {"result": "played new trial"}

    def put(self):
        return {"result": "continued previous trial"}
