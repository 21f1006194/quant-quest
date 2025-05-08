from functools import wraps
from flask import request, current_app
import redis
from app import db
from app.models.gameplay import Game, GameSession
from app.utils.auth import get_api_user

# Initialize Redis client with configuration
redis_client = redis.Redis(
    host=current_app.config["REDIS_HOST"],
    port=current_app.config["REDIS_PORT"],
    db=current_app.config["REDIS_DB"],
)


## TODO: cache later
def get_game(game_name):
    """Get game from request"""
    game = Game.query.filter_by(name=game_name).first()
    if not game:
        raise ValueError(f"Game {game_name} not found")
    return game


# TODO: use in admin api to clear limits for a specific user for a game
def clear_user_limits(user_id, game_name):
    """Clear rate limits for a specific user and game"""
    game = get_game(game_name)
    key = f"session_count:{game.id}:{user_id}"
    redis_client.delete(key)
    key = f"bets_count:{game.id}:{user_id}"
    redis_client.delete(key)


# TODO: use in game api(or player api) to get remaining bets and sessions for a user
def get_remaining_bets(user_id, game_name):
    """Get remaining bets for a specific user and game"""
    game = get_game(game_name)
    key1 = f"bets_count:{game.id}:{user_id}"
    key2 = f"session_count:{game.id}:{user_id}"
    return {
        "sessions": game.max_sessions_per_user - redis_client.get(key2),
        "bets": game.max_bets_per_session - redis_client.get(key1),
    }


def session_rate_limit(game_name):
    """Rate limit for game sessions"""

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            game = get_game(game_name)
            user_id = get_api_user().id
            key = f"session_count:{game.id}:{user_id}"

            # Check current count first
            current_count = redis_client.get(key)
            if current_count and int(current_count) >= game.max_sessions_per_user:
                return {"error": "Rate limit exceeded"}, 429

            # Try to increment
            if redis_client.incr(key) > game.max_sessions_per_user:
                # Decrement if we exceeded the limit
                redis_client.decr(key)
                return {"error": "Rate limit exceeded"}, 429

            try:
                # Execute the function
                response = f(*args, **kwargs)

                # Check if response is successful
                if isinstance(response, tuple):
                    status_code = response[1]
                    if status_code not in [200, 201]:
                        # Decrement count if not successful
                        redis_client.decr(key)
                return response

            except Exception as e:
                # Decrement count on any error
                redis_client.decr(key)
                raise e

        return decorated

    return decorator


def bets_rate_limit(game_name):
    """Rate limit for bets"""

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            game = get_game(game_name)
            user_id = get_api_user().id
            key = f"bets_count:{game.id}:{user_id}"
            if redis_client.incr(key) > game.max_bets_per_session:
                return {"error": "Rate limit exceeded"}, 429
            return f(*args, **kwargs)

        return decorated

    return decorator
