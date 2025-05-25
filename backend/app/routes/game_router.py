from flask import Blueprint, request
from flask_restful import Api
import importlib
from .base_game import BaseGameAPI
from app.services.game_service import GameService
from app.extensions import db


game_bp = Blueprint("game", __name__)
play_bp = Blueprint("play", __name__)
play_api = Api(play_bp)
game_api = Api(game_bp)


def add_game_routes(game_name, mod):
    """Add common game routes (status, description, control)"""
    try:
        # Define default API classes outside the if blocks
        class DefaultGameControlAPI(BaseGameAPI):
            def post(self):
                return self.update_control(request.get_json())

        class DefaultGameInfoAPI(BaseGameAPI):
            def get(self):
                return self.get_info()

        class DefaultGameTemplateAPI(BaseGameAPI):
            def get(self):
                return self.template()

        # Info API
        GameInfoAPI = (
            mod.GameInfoAPI if hasattr(mod, "GameInfoAPI") else DefaultGameInfoAPI
        )
        game_api.add_resource(
            GameInfoAPI,
            f"/game/{game_name}/info",
            endpoint=f"{game_name}_info",
            resource_class_kwargs={"game_name": game_name},
        )
        # Control API
        GameControlAPI = (
            mod.GameControlAPI
            if hasattr(mod, "GameControlAPI")
            else DefaultGameControlAPI
        )
        game_api.add_resource(
            GameControlAPI,
            f"/game/{game_name}/control",
            endpoint=f"{game_name}_control",
            resource_class_kwargs={"game_name": game_name},
        )

        # Template API
        GameTemplateAPI = (
            mod.GameTemplateAPI
            if hasattr(mod, "GameTemplateAPI")
            else DefaultGameTemplateAPI
        )
        game_api.add_resource(
            GameTemplateAPI,
            f"/game/{game_name}/template",
            endpoint=f"{game_name}_template",
            resource_class_kwargs={"game_name": game_name},
        )
        print(f"Added game routes for {game_name}")
        return True
    except Exception as e:
        print(f"Error adding game routes: {e}")
        return False


def add_game_play_routes(game_name, mod):
    """Add game-specific play routes"""
    try:
        if hasattr(mod, "GamePlayAPI"):
            play_api.add_resource(
                mod.GamePlayAPI, f"/play/{game_name}", endpoint=f"{game_name}_play"
            )
            print(f"Added play routes for {game_name}")
        return True
    except Exception as e:
        print(f"Error adding play routes: {e}")
        return False


def register_game(game_name):
    """Register a single game in the system"""
    try:

        # 1. Import game module
        mod = importlib.import_module(f"app.routes.games.{game_name}.api")

        # 2. Add common game routes
        if not add_game_routes(game_name, mod):
            return False

        # 3. Add play routes
        if not add_game_play_routes(game_name, mod):
            return False

        return True

    except Exception as e:
        print(f"Error registering game {game_name}: {e}")
        db.session.rollback()
        return False


def register_all_games(app):
    """Register all games in the games directory"""
    with app.app_context():
        games = GameService.get_all_games()
        for game in games:
            game_name = game.name
            if register_game(game_name):
                print(f"Successfully registered game: {game_name}")
            else:
                print(f"Failed to register game: {game_name}")
