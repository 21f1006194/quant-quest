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
            if "is_active" in data:
                self.game.is_active = data["is_active"]
            if "config" in data:
                ## TODO: Validate config data format with existing config
                self.game.config_data.update(data["config"])
            if "max_sessions_per_user" in data:
                self.game.max_sessions_per_user = int(data["max_sessions_per_user"])
            if "max_bets_per_session" in data:
                self.game.max_bets_per_session = int(data["max_bets_per_session"])

            db.session.commit()
            return {"message": "Game control updated successfully"}
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
