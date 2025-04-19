# backend/app/routes/base_game.py
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models.gameplay import Game
from app import db
from app.utils.auth import admin_required


class BaseGameAPI(Resource):
    def __init__(self, **kwargs):
        super().__init__()
        self.game_name = kwargs.get("game_name")
        self.game = Game.query.filter_by(name=self.game_name).first()

    @jwt_required()
    def get_status(self):
        if not self.game:
            return {"error": "Game not found"}, 404
        return {
            "name": self.game.name,
            "is_active": self.game.is_active,
        }

    def get_description(self):
        if not self.game:
            return {"error": "Game not found"}, 404
        return {
            "name": self.game.name,
            "is_active": self.game.is_active,
            "description": self.game.description,
        }

    @admin_required
    def get_control(self):
        if not self.game:
            return {"error": "Game not found"}, 404
        return {
            "is_active": self.game.is_active,
            "config": self.game.config_data,
        }

    @admin_required
    def update_control(self, data):
        """Update game control settings"""
        if not self.game:
            return {"error": "Game not found"}, 404

        try:
            if "is_active" in data:
                self.game.is_active = data["is_active"]
            if "config" in data:
                ## TODO: Validate config data format with existing config
                self.game.config_data.update(data["config"])

            db.session.commit()
            return {"message": "Game control updated successfully"}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
