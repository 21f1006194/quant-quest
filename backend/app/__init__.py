from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config, ConfigValidator
from app.utils import create_admin_if_not_exists
from app.extensions import db, migrate, jwt, cache


def initialize_app(app):
    """Initialize application data after database is ready"""
    with app.app_context():
        create_admin_if_not_exists()
        from .routes.game_router import register_all_games

        register_all_games(app)


def create_app(config_object=None):
    """Create and configure the Flask application.

    Args:
        config_object: Configuration object to use. If None, uses the default Config.
    """
    app = Flask(__name__)

    # Use provided config or default to Config
    app.config.from_object(config_object or Config)

    # Validate environment variables if using default Config
    if config_object is None:
        missing_vars = ConfigValidator.validate()
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    # Configure CORS
    CORS(
        app,
        resources={
            r"/*": {  # Allow CORS for all routes
                "origins": app.config["CORS_ORIGINS"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "Accept"],
                "expose_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "max_age": 3600,
            }
        },
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app)

    # Register blueprints
    from .routes import common_bp, admin_bp, player_bp, game_bp, play_bp

    app.register_blueprint(common_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(play_bp)

    return app
