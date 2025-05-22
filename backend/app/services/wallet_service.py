from app import db
from app.models.wallet import Wallet, Transaction, TransactionType, TransactionCategory
from sqlalchemy.exc import IntegrityError
from app.services.sse_service import SSEService
from datetime import datetime, timezone


class WalletService:
    @staticmethod
    def get_wallet(user_id):
        """Get wallet for a user"""
        return Wallet.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_balance(user_id):
        """Get current balance for a user"""
        wallet = WalletService.get_wallet(user_id)
        return wallet.current_balance if wallet else 0.0

    @staticmethod
    def _publish_transaction_event(user_id, wallet, amount, category, description):
        """Helper method to publish transaction events to SSE"""
        sse_service = SSEService()
        sse_service.publish_event(
            user_id,
            "transaction_update",
            {
                "balance": wallet.current_balance,
                "transaction": {
                    "amount": amount,
                    "category": category.value,
                    "description": description,
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @staticmethod
    def create_bonus(user_id, amount, description, transaction_info=None):
        """
        Create a bonus transaction and update wallet balance.
        This is an atomic operation.
        """
        try:
            wallet = WalletService.get_wallet(user_id)
            if not wallet:
                raise ValueError(f"No wallet found for user {user_id}")

            # Create transaction
            transaction = Transaction(
                wallet_id=wallet.id,
                amount=amount,
                category=TransactionCategory.BONUS,
                description=description,
                transaction_info=transaction_info,
            )

            # Update wallet balance
            wallet.current_balance += amount

            # Add both to session
            db.session.add(transaction)
            db.session.add(wallet)

            # Commit transaction
            db.session.commit()

            # Publish wallet update event
            WalletService._publish_transaction_event(
                user_id, wallet, amount, TransactionCategory.BONUS, description
            )

            return transaction

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Database error occurred") from e
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error creating bonus transaction: {str(e)}") from e

    @staticmethod
    def create_penalty(user_id, amount, description, transaction_info=None):
        """
        Create a penalty transaction and update wallet balance.
        This is an atomic operation.
        """
        try:
            wallet = WalletService.get_wallet(user_id)
            if not wallet:
                raise ValueError(f"No wallet found for user {user_id}")

            # Create transaction
            transaction = Transaction(
                wallet_id=wallet.id,
                amount=amount,
                category=TransactionCategory.PENALTY,
                description=description,
                transaction_info=transaction_info,
            )

            # Update wallet balance
            wallet.current_balance -= amount

            # Add both to session
            db.session.add(transaction)
            db.session.add(wallet)

            # Commit transaction
            db.session.commit()

            # Publish wallet update event
            WalletService._publish_transaction_event(
                user_id, wallet, amount, TransactionCategory.PENALTY, description
            )

            return transaction

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Database error occurred") from e
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error creating penalty transaction: {str(e)}") from e

    @staticmethod
    def create_bonus_for_all_users(amount, description, transaction_info=None):
        """
        Create bonus transactions for all users.
        Returns a list of successful transactions and failed user IDs.
        """
        successful_transactions = []
        failed_users = []

        # Get all wallets
        wallets = Wallet.query.all()

        for wallet in wallets:
            try:
                transaction = WalletService.create_bonus(
                    user_id=wallet.user_id,
                    amount=amount,
                    description=description,
                    transaction_info=transaction_info,
                )
                successful_transactions.append(transaction)
            except Exception as e:
                failed_users.append(wallet.user_id)
                continue

        return {
            "successful_transactions": successful_transactions,
            "failed_users": failed_users,
            "total_successful": len(successful_transactions),
            "total_failed": len(failed_users),
        }

    @staticmethod
    def get_transactions_by_user(user_id):
        """Get all transactions for a user"""
        return Wallet.query.filter_by(user_id=user_id).first().transactions
