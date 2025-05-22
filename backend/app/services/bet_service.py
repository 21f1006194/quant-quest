from app import db
from app.models.gameplay import GameSession, Bet, GamePnL
from app.services.wallet_service import WalletService
from app.services.sse_service import SSEService
from sqlalchemy.exc import IntegrityError
from dataclasses import dataclass
from typing import Optional, Any
from datetime import datetime, timezone


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
    def get_bet(bet_id: int) -> Bet:
        return Bet.query.get(bet_id)

    @staticmethod
    def validate_bet_amount(user_id, amount):
        """Validate if user has enough balance for the bet"""
        current_balance = WalletService.get_balance(user_id)
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
                game_pnl = GamePnL.query.filter_by(
                    user_id=session.user_id, game_id=session.game_id
                ).first()
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

                ## TODO: May be keeping both session.netflow and game pnl is not a good idea.
                ## We should only keep one of them. (gamepnl is more useful), optimize later.
                # Update session and wallet
                session.bet_count += 1
                session.net_flow += bet_data.payout - bet_data.amount
                wallet = WalletService.get_wallet(session.user_id)
                wallet.current_balance -= bet_data.amount
                wallet.current_balance += bet_data.payout
                # update the pnl for the game
                game_pnl.pnl += bet_data.payout - bet_data.amount
                game_pnl.bet_count += 1
                db.session.add_all([bet, session, wallet, game_pnl])

            db.session.commit()

            # Publish bet event
            sse_service = SSEService()
            sse_service.publish_event(
                session.user_id,
                "bet_update",
                {
                    "game_id": session.game_id,
                    "bet_id": bet.id,
                    "amount": bet_data.amount,
                    "payout": bet_data.payout,
                    "balance": wallet.current_balance,
                    "pnl": game_pnl.pnl,
                    "bet_count": game_pnl.bet_count,
                    "session_count": game_pnl.session_count,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

            return bet, wallet

        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error creating bet: {str(e)}") from e

    @staticmethod
    def get_bets_for_user(user_id, game):
        bets = Bet.query.filter_by(user_id=user_id, game_id=game.id).all()
        return [bet.to_dict() for bet in bets]

    @staticmethod
    def update_bet(bet_id: int, session_id: int, bet_data: BetData) -> Bet:
        """
        Update an existing bet with proper transaction handling.

        Args:
            bet_id: The ID of the bet to update
            session_id: The ID of the game session
            bet_data: Standardized bet data for the update

        Returns:
            Bet: The updated bet instance
        """
        try:
            # Validate bet data
            bet_data.validate()

            with db.session.begin_nested():
                # Get the existing bet and session with lock
                bet = Bet.query.with_for_update().get(bet_id)
                session = GameSession.query.with_for_update().get(session_id)
                game_pnl = (
                    GamePnL.query.filter_by(
                        user_id=session.user_id, game_id=session.game_id
                    )
                    .with_for_update()
                    .first()
                )

                if not bet:
                    raise ValueError(f"Bet {bet_id} not found")
                if not session:
                    raise ValueError(f"Session {session_id} not found")
                if bet.session_id != session_id:
                    raise ValueError("Bet does not belong to the specified session")

                # Calculate the difference in amount and payout
                amount_diff = bet_data.amount - bet.amount
                payout_diff = bet_data.payout - bet.payout
                total_diff = payout_diff - amount_diff

                # Validate wallet balance if amount is increasing
                if amount_diff > 0:
                    BetService.validate_bet_amount(session.user_id, amount_diff)

                # Update bet details
                bet.amount = bet_data.amount
                bet.choice = bet_data.choice
                bet.payout = bet_data.payout
                bet.bet_details = bet_data.bet_details

                # Update session and wallet
                session.net_flow += total_diff
                wallet = WalletService.get_wallet(session.user_id)
                wallet.current_balance -= amount_diff
                wallet.current_balance += payout_diff

                # Update game PnL
                game_pnl.pnl += total_diff

                db.session.add_all([bet, session, wallet, game_pnl])

            db.session.commit()

            # Publish bet update event
            sse_service = SSEService()
            sse_service.publish_event(
                session.user_id,
                "bet_update",
                {
                    "game_id": session.game_id,
                    "bet_id": bet.id,
                    "amount": bet_data.amount,
                    "payout": bet_data.payout,
                    "balance": wallet.current_balance,
                    "pnl": game_pnl.pnl,
                    "bet_count": game_pnl.bet_count,
                    "session_count": game_pnl.session_count,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

            return bet, wallet

        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error updating bet: {str(e)}") from e
