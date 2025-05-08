from .common import common_bp
from .admin import admin_bp
from .player import player_bp
from .game_router import game_bp, play_bp

__all__ = ["common_bp", "admin_bp", "player_bp", "game_bp", "play_bp"]
