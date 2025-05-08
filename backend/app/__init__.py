from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.utils import create_admin_if_not_exists

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def initialize_app(app):
    """Initialize application data after database is ready"""
    with app.app_context():
        create_admin_if_not_exists()
        from .routes.game_router import register_all_games

        register_all_games(app)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    jwt.init_app(app)

    # Register blueprints
    from .routes import common_bp, admin_bp, player_bp, game_bp, play_bp

    app.register_blueprint(common_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(play_bp)

    return app
