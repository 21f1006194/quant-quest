from app.models.gameplay import GameSession, Bet
from app import db


def validate_bet_data(bet_data):
    # check for choice to be an integer between 10 and 60
    if "choice" not in bet_data or "bet_amount" not in bet_data:
        raise ValueError("Bet data must contain choice and bet_amount")
    if bet_data["choice"] not in range(10, 60):
        raise ValueError("Invalid bet data")
    return True


def get_bets_for_user(user_id, game):
    bets = Bet.query.filter_by(user_id=user_id, game_id=game.id).all()
    return [bet.to_dict() for bet in bets]


def create_game_session_and_bet(user_id, game, bet_data, result):
    """
    Create a game session and bet for the user.

    Args:
        user_id (int): The ID of the user
        game_name (str): The name of the game
        bet_data (dict): The bet data containing choice and bet_amount
        result (dict): The result of the bet from the game engine

    Returns:
        tuple: (GameSession, Bet) objects created
    """
    # Create a new session
    session = GameSession(
        user_id=user_id,
        game_id=game.id,
    )
    # commit to get the session id
    db.session.add(session)
    db.session.flush()

    try:
        # Create the bet
        bet = Bet.create(
            session_id=session.id,
            amount=bet_data["bet_amount"],
            choice=str(bet_data["choice"]),
            payout=result["payout"],
            bet_details=result,
        )

        return session, bet
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Failed to create bet: {str(e)}")
