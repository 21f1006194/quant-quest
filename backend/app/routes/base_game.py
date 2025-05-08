# backend/app/routes/base_game.py
import os
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models.gameplay import Game
from app import db
from app.utils.auth import admin_required


GAMES_DIR = os.path.join(os.path.dirname(__file__), "games")


class BaseGameAPI(Resource):
    def __init__(self, **kwargs):
        super().__init__()
        self.game_name = kwargs.get("game_name")
        self.game = Game.query.filter_by(name=self.game_name).first()

    @jwt_required()
    def get_info(self):
        if not self.game:
            return {"error": "Game not found"}, 404
        return self.game.to_dict()

    @admin_required
    def update_control(self, data):
        """Update game control settings like is_active, config_data,
        max_sessions_per_user, max_bets_per_session"""
        if not self.game:
            return {"error": "Game not found"}, 404

        try:
            changed_fields = []
            if "is_active" in data:
                self.game.is_active = data["is_active"]
                changed_fields.append("is_active")
            if "config_data" in data:
                for k, v in self.game.config_data.items():
                    if k not in data["config_data"]:
                        return {"error": f"Missing config key: {k}"}, 400
                    elif type(data["config_data"][k]) != type(v):
                        return {"error": f"Invalid config value type for key: {k}"}, 400

                self.game.config_data = {
                    k: v
                    for k, v in data["config_data"].items()
                    if k in self.game.config_data
                }
                changed_fields.append("config_data")
            if "difficulty" in data:
                self.game.difficulty = data["difficulty"]
                changed_fields.append("difficulty")
            if "tags" in data:
                self.game.tags = data["tags"]
                changed_fields.append("tags")
            if "max_sessions_per_user" in data:
                self.game.max_sessions_per_user = int(data["max_sessions_per_user"])
                changed_fields.append("max_sessions_per_user")
            if "max_bets_per_session" in data:
                self.game.max_bets_per_session = int(data["max_bets_per_session"])
                changed_fields.append("max_bets_per_session")
            if changed_fields:
                db.session.commit()
                return {
                    "message": "Game control updated successfully",
                    "changed_fields": changed_fields,
                }
            else:
                return {"message": "No changes made to game control"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @jwt_required()
    def template(self):
        template_path = os.path.join(GAMES_DIR, self.game_name, "template.py")
        if not os.path.exists(template_path):
            return {"error": "Template not found"}, 404
        with open(template_path, "r") as f:
            template = f.read()

        return template
