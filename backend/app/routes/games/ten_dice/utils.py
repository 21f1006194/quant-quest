from app.models.gameplay import GameSession, Bet
from app.services.bet_service import BetService, BetData
from app.extensions import db


def validate_bet_data(bet_data, config):
    # check for choice to be an integer between 10 and 60
    if "choice" not in bet_data or "bet_amount" not in bet_data:
        raise ValueError("Bet data must contain choice and bet_amount")
    if bet_data["choice"] not in range(10, 60):
        raise ValueError("Invalid bet data")
    min_bet_amount = config["min_bet_amount"]
    if bet_data["bet_amount"] < min_bet_amount:
        raise ValueError(f"Bet amount must be greater than {min_bet_amount}")
    return True


def get_bets_for_user(user_id, game):
    bets = Bet.query.filter_by(user_id=user_id, game_id=game.id).all()
    return [bet.to_dict() for bet in bets]


def create_game_session_and_bet(user_id, game, bet_data, result):
    """
    Create a game session and bet for the user.
    For ten_dice game, we create a new session for each bet.

    Args:
        user_id (int): The ID of the user
        game_name (str): The name of the game
        bet_data (dict): The bet data containing choice and bet_amount
        result (dict): The result of the bet from the game engine

    Returns:
        tuple: (GameSession, Bet) objects created
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
        raise ValueError(f"Failed to create bet: {str(e)}")
