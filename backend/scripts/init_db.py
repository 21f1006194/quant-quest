import os
import sys

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(backend_dir)

from app import create_app, db
from app.utils import create_admin_if_not_exists
from app.models import Game
from flask_migrate import upgrade
import json

GAMES_DIR = os.path.join(backend_dir, "app", "routes", "games")


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
                difficulty=metadata.get("default_difficulty", "easy"),
                tags=metadata.get("default_tags", ""),
                config_data=metadata.get("default_config", {}),
            )
            db.session.add(game)
            print("Game created")
        else:
            game.description = description
            print("Game description updated")

        db.session.commit()
        return game
    except Exception as e:
        print(f"Error creating/updating game in database: {e}")
        db.session.rollback()
        return None


def games_migration(app):
    with app.app_context():
        count = 0
        for game_name in os.listdir(GAMES_DIR):
            if not os.path.isdir(os.path.join(GAMES_DIR, game_name)):
                continue
            print("--------------------------------")
            print(f"Processing game: {game_name}")
            metadata, description = load_game_metadata(
                os.path.join(GAMES_DIR, game_name)
            )
            if metadata is None:
                continue
            # Create/update game in database
            game = create_or_update_game(game_name, metadata, description)
            if game:
                count += 1
        print("-------------------------------------------")
        print(f"Successfully created/updated {count} games")
        print("-------------------------------------------")


def init_database():
    """Initialize the database with migrations, admin user, and games"""
    app = create_app()

    with app.app_context():
        print("Running database migrations...")
        upgrade()

        print("Creating admin user if not exists...")
        create_admin_if_not_exists()

        print("Migrating games...")
        games_migration(app)

        print("Database initialization complete!")
        print("= " * 30, "\n\n")


if __name__ == "__main__":
    init_database()
