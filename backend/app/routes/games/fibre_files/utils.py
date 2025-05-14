from app.services.bet_service import BetService, BetData
from app.models.gameplay import GameSession
from app import db


def validate_bet_data(bet_data, config=None):
    """
    Validates the bet data sent by the frontend.
    For Fibre Files, 'choice' must be between 0 and 9 and 'bet_amount' must be provided.
    """
    if "choice" not in bet_data or "bet_amount" not in bet_data:
        raise ValueError("Bet data must contain 'choice' and 'bet_amount'")

    try:
        choice = int(bet_data["choice"])
    except (ValueError, TypeError):
        raise ValueError("Choice must be an integer")

    if choice not in range(0, 10):
        raise ValueError("Choice must be between 0 and 9")

    try:
        bet_amount = float(bet_data["bet_amount"])
        if bet_amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError("Bet amount must be a positive number")

    return True


def create_game_session_and_bet(user_id, game, bet_data, result):
    """
    Creates a new game session and a bet entry for the Fibre Files game.
    Each bet in Fibre Files gets its own game session.
    """
    try:
        # Create a new session for this bet
        session = GameSession(user_id=user_id, game_id=game.id)
        db.session.add(session)
        db.session.flush()  # To get session.id before commit

        # Prepare bet data in standardized format
        bet_data_obj = BetData(
            amount=bet_data["bet_amount"],
            choice=str(bet_data["choice"]),
            payout=result["payout"],
            bet_details=result,
        )

        # Create the bet and update wallet
        bet, wallet = BetService.create_bet(session.id, bet_data_obj)

        # Commit transaction
        db.session.commit()

        return session, bet, wallet

    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Error creating bet: {str(e)}") from e
