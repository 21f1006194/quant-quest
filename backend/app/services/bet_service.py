from app import db
from app.models.gameplay import GameSession, Bet
from app.services.wallet_service import WalletService
from sqlalchemy.exc import IntegrityError


class BetService:
    @staticmethod
    def validate_bet_amount(user_id, amount):
        """Validate if user has enough balance for the bet"""
        current_balance = WalletService.get_balance(user_id)
        print(f"Current balance: {current_balance}, Amount: {amount}")
        print(f"User ID: {user_id}")
        if current_balance < amount:
            raise ValueError(
                f"Insufficient balance. Required: {amount}, Available: {current_balance}"
            )
        return True

    @staticmethod
    def create_bet(session_id, bet_data, result):
        """
        Create a bet with proper transaction handling.
        This is an atomic operation that:
        1. Validates wallet balance
        2. Creates bet
        3. Updates wallet balance
        4. Updates session bet count

        Args:
            session_id (int): The ID of the game session
            bet_data (dict): The bet data containing bet_amount and choice
            result (dict): The result of the bet from the game engine

        Returns:
            Bet: The created bet instance

        Raises:
            ValueError: If session not found or max bets reached
            RuntimeError: If database error occurs
        """
        try:
            # Validate bet amount
            BetService.validate_bet_amount(bet_data["user_id"], bet_data["bet_amount"])

            with db.session.begin_nested():
                # Lock the session row for safe concurrent updates
                session = GameSession.query.with_for_update().get(session_id)
                if not session:
                    raise ValueError(f"Session {session_id} not found")

                if session.bet_count >= session.max_bets_per_session:
                    raise ValueError(f"Max bets reached for session {session_id}")

                # Create bet
                bet = Bet(
                    session_id=session_id,
                    game_id=session.game_id,
                    user_id=session.user_id,
                    amount=bet_data["bet_amount"],
                    choice=str(bet_data["choice"]),
                    payout=result["payout"],
                    bet_details=result,
                )

                # Update session bet count
                session.bet_count += 1

                # Update wallet balance
                wallet = WalletService.get_wallet(session.user_id)
                wallet.current_balance -= bet_data["bet_amount"]  # Deduct bet amount
                wallet.current_balance += result["payout"]  # Add payout

                # Add all to session
                db.session.add(bet)
                db.session.add(session)
                db.session.add(wallet)

            db.session.commit()
            return bet

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Database error occurred") from e
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error creating bet: {str(e)}") from e
