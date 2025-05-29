from functools import wraps
from flask import request, current_app
import redis
from app.models.gameplay import Game
from app.utils.auth import get_api_user, api_token_required
from app.services.wallet_service import WalletService

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


def play_rate_key(user_id):
    """Generate rate limit key for play endpoints"""
    return f"play_rate:{user_id}"


def custom_rate_limit(f):
    """Custom rate limiter with dynamic expiry times"""

    @wraps(f)
    @api_token_required
    def decorated(*args, **kwargs):
        user_id = get_api_user().id
        key = play_rate_key(user_id)

        # Get current count and TTL
        current_count = redis_client.get(key)
        current_ttl = redis_client.ttl(key)

        if current_count is None or current_ttl <= 0:
            # First request or expired window - start new 5 second window
            redis_client.setex(key, 5, 1)  # Set 5 second expiry with count 1
            return f(*args, **kwargs)

        current_count = int(current_count)

        if current_count >= 20:
            # If we hit 20 requests, extend to 60 seconds and apply penalty
            redis_client.setex(key, 60, current_count)

            # Apply penalty using WalletService
            try:
                current_balance = WalletService.get_balance(user_id)
                penalty_amount = max(50, int(current_balance * 0.05))
                WalletService.create_penalty(
                    user_id=user_id,
                    amount=penalty_amount,
                    description="Speeding Ticket! API Rate limit exceeded.",
                    transaction_info={
                        "rate_limit_key": key,
                        "request_count": current_count,
                        "penalty_reason": "rate_limit_exceeded",
                    },
                )
            except Exception as e:
                current_app.logger.error(
                    f"Failed to apply rate limit penalty: {str(e)}"
                )

            return {
                "error": "Rate limit exceeded. Please try again in 60 seconds."
            }, 429

        # Increment counter while preserving TTL
        redis_client.incr(key)
        return f(*args, **kwargs)

    return decorated


def play_rate_limited(f):
    """Decorator that combines API token requirement and rate limiting"""
    return custom_rate_limit(f)
