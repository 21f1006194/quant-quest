from flask import Blueprint
from flask_restful import Api
import importlib
import os

game_bp = Blueprint("game", __name__)
play_bp = Blueprint("play", __name__)
play_api = Api(play_bp)
game_api = Api(game_bp)

GAMES_DIR = os.path.join(os.path.dirname(__file__), "games")

for game_name in os.listdir(GAMES_DIR):
    if game_name.startswith("__") or not os.path.isdir(
        os.path.join(GAMES_DIR, game_name)
    ):
        continue

    try:
        mod = importlib.import_module(f"app.routes.games.{game_name}.api")
        if hasattr(mod, "GameStatusAPI"):
            game_api.add_resource(
                mod.GameStatusAPI,
                f"/game/{game_name}/status",
                endpoint=f"{game_name}_status",
            )
        if hasattr(mod, "GameDescriptionAPI"):
            game_api.add_resource(
                mod.GameDescriptionAPI,
                f"/game/{game_name}/description",
                endpoint=f"{game_name}_description",
            )
        if hasattr(mod, "GameControlAPI"):
            game_api.add_resource(
                mod.GameControlAPI,
                f"/game/{game_name}/control",
                endpoint=f"{game_name}_control",
            )
        if hasattr(mod, "GamePlayAPI"):
            play_api.add_resource(
                mod.GamePlayAPI, f"/play/{game_name}", endpoint=f"{game_name}_play"
            )
    except Exception as e:
        print(f"Error loading {game_name}: {e}")
