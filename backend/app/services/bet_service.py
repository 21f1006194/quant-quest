from app import db
from app.models.gameplay import GameSession, Bet
from app.services.wallet_service import WalletService
from sqlalchemy.exc import IntegrityError
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class BetData:
    """Standardized bet data structure for all games"""

    amount: float
    choice: str
    payout: float
    bet_details: Optional[dict[str, Any]] = None

    def validate(self):
        """Validate bet data"""
        if self.amount <= 0:
            raise ValueError("Bet amount must be positive")
        if not self.choice:
            raise ValueError("Bet choice is required")
        if self.payout < 0:
            raise ValueError("Payout cannot be negative")


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
    def create_bet(session_id: int, bet_data: BetData) -> Bet:
        """
        Create a bet with proper transaction handling.

        Args:
            session_id: The ID of the game session
            bet_data: Standardized bet data

        Returns:
            Bet: The created bet instance
        """
        try:
            # Validate bet data
            bet_data.validate()

            with db.session.begin_nested():
                session = GameSession.query.with_for_update().get(session_id)
                if not session:
                    raise ValueError(f"Session {session_id} not found")

                # Validate wallet balance
                BetService.validate_bet_amount(session.user_id, bet_data.amount)

                if session.bet_count >= session.max_bets_per_session:
                    raise ValueError(f"Max bets reached for session {session_id}")

                # Create bet
                bet = Bet(
                    session_id=session_id,
                    game_id=session.game_id,
                    user_id=session.user_id,
                    amount=bet_data.amount,
                    choice=bet_data.choice,
                    payout=bet_data.payout,
                    bet_details=bet_data.bet_details,
                )

                # Update session and wallet
                session.bet_count += 1
                wallet = WalletService.get_wallet(session.user_id)
                wallet.current_balance -= bet_data.amount
                wallet.current_balance += bet_data.payout

                db.session.add_all([bet, session, wallet])

            db.session.commit()
            return bet, wallet

        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error creating bet: {str(e)}") from e
