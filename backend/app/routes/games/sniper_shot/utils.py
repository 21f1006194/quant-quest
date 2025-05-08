from app.services.bet_service import BetService, BetData
from app.models.gameplay import GameSession
from app import db


def validate_bet_data(bet_data, config):
    if "choice" not in bet_data or "bet_amount" not in bet_data:
        raise ValueError("Bet data must contain choice and bet_amount")
    if bet_data["choice"] not in range(0, 28):
        raise ValueError("Invalid bet data")
    return True


def create_game_session_and_bet(user_id, game, bet_data, result):
    """
    Create a game session and bet for the user.
    For sniper_shot game, we create a new session for each bet.
    """
    try:
        # Create session
        session = GameSession(user_id=user_id, game_id=game.id)
        db.session.add(session)
        db.session.flush()

        # Convert game-specific data to standardized format
        bet_data = BetData(
            amount=bet_data["bet_amount"],
            choice=str(bet_data["choice"]),
            payout=result["payout"],
            bet_details=result,
        )

        # Create bet
        bet, wallet = BetService.create_bet(session.id, bet_data)
        return session, bet, wallet

    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Error creating bet: {str(e)}") from e
