from flask import Blueprint, current_app, request
from flask_restful import Api
import importlib
import os
import json
from .base_game import BaseGameAPI
from app.models.gameplay import Game
from app import db

game_bp = Blueprint("game", __name__)
play_bp = Blueprint("play", __name__)
play_api = Api(play_bp)
game_api = Api(game_bp)

GAMES_DIR = os.path.join(os.path.dirname(__file__), "games")


def load_game_metadata(game_dir):
    """Load game metadata and description from files"""
    try:
        # Load basic metadata
        metadata_path = os.path.join(game_dir, "metadata.json")
        if not os.path.exists(metadata_path):
            print(f"Warning: No metadata.json found")
            return None, None

        with open(metadata_path) as f:
            metadata = json.load(f)

        # Check if game should be ignored
        if metadata.get("ignore", False):
            print(f"Game is marked to be ignored")
            return None, None

        # Load description from markdown file
        description = ""
        desc_path = os.path.join(game_dir, "description.md")
        if os.path.exists(desc_path):
            with open(desc_path, "r") as f:
                description = f.read()

        return metadata, description
    except Exception as e:
        print(f"Error loading game metadata: {e}")
        return None, None


def create_or_update_game(game_name, metadata, description):
    """Create or update game in database"""
    try:
        game = Game.query.filter_by(name=game_name).first()
        if not game:
            game = Game(
                name=game_name,
                description=description,
                type=metadata.get("type", "game"),
                max_sessions_per_user=metadata.get("default_max_sessions_per_user"),
                max_bets_per_session=metadata.get("default_max_bets_per_session"),
                is_active=metadata.get("default_is_active", True),
                config_data=metadata.get("default_config", {}),
            )
            db.session.add(game)
        else:
            game.description = description

        db.session.commit()
        return game
    except Exception as e:
        print(f"Error creating/updating game in database: {e}")
        db.session.rollback()
        return None


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


def register_game(game_name, game_dir, metadata, description):
    """Register a single game in the system"""
    try:

        # 1. Create/update game in database
        game = create_or_update_game(game_name, metadata, description)
        if not game:
            return False

        # 2. Import game module
        mod = importlib.import_module(f"app.routes.games.{game_name}.api")

        # 3. Add common game routes
        if not add_game_routes(game_name, mod):
            return False

        # 4. Add play routes
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
        for game_name in os.listdir(GAMES_DIR):
            if not os.path.isdir(os.path.join(GAMES_DIR, game_name)):
                continue

            game_dir = os.path.join(GAMES_DIR, game_name)
            metadata, description = load_game_metadata(game_dir)

            if metadata is None:
                if os.path.exists(os.path.join(game_dir, "metadata.json")):
                    print(f"Game '{game_name}' is ignored or has invalid metadata")
                else:
                    print(f"Game '{game_name}' has no metadata.json")
                continue

            if register_game(game_name, game_dir, metadata, description):
                print(f"Successfully registered game: {game_name}")
            else:
                print(f"Failed to register game: {game_name}")
