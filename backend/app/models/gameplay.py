from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSON
from app import db
from sqlalchemy import and_, CheckConstraint
from sqlalchemy.exc import IntegrityError


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    type = db.Column(
        db.String(50), nullable=True
    )  # e.g., 'quiz', 'puzzle', 'prediction'
    max_sessions_per_user = db.Column(db.Integer, nullable=False)
    max_bets_per_session = db.Column(db.Integer, nullable=False)
    config_data = db.Column(JSON, nullable=True)  # game configuration, rules, etc.
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    sessions = db.relationship(
        "GameSession",
        back_populates="game",
        cascade="all, delete",
        passive_deletes=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "max_sessions_per_user": self.max_sessions_per_user,
            "max_bets_per_session": self.max_bets_per_session,
            "config_data": self.config_data,
            "is_active": self.is_active,
        }


class GameSession(db.Model):
    __tablename__ = "game_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    game_id = db.Column(
        db.Integer, db.ForeignKey("games.id", ondelete="CASCADE"), nullable=False
    )

    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = db.Column(db.DateTime)
    duration = db.Column(db.Interval)

    result = db.Column(db.String(20))  # e.g., 'win', 'loss', 'draw'
    score = db.Column(db.Float, default=0.0)
    status = db.Column(
        db.String(20), default="in_progress"
    )  # 'in_progress', 'completed', 'forfeited'
    session_data = db.Column(JSON, nullable=True)  # gameplay-specific data
    bet_count = db.Column(db.Integer, default=0, nullable=False)  # Track number of bets
    max_bets_per_session = db.Column(db.Integer, nullable=False)  # Copied from game

    bets = db.relationship(
        "Bet", backref="session", cascade="all, delete", passive_deletes=True
    )

    game = db.relationship("Game", back_populates="sessions")

    __table_args__ = (
        db.Index("idx_session_user_game", "user_id", "game_id"),
        CheckConstraint(
            "bet_count <= max_bets_per_session", name="check_bet_count_limit"
        ),
    )

    def __init__(self, **kwargs):
        user_id = kwargs.get("user_id")
        game_id = kwargs.get("game_id")

        if user_id is not None and game_id is not None:
            game = Game.query.get(game_id)
            if not game:
                raise ValueError(f"Game with id {game_id} does not exist")

            current_sessions_count = self.query.filter(
                and_(
                    self.__class__.user_id == user_id, self.__class__.game_id == game_id
                )
            ).count()

            if current_sessions_count >= game.max_sessions_per_user:
                raise ValueError(
                    f"Maximum number of sessions ({game.max_sessions_per_user}) "
                    f"reached for user {user_id} in game {game_id}"
                )

            # Copy max_bets_per_session from game
            kwargs["max_bets_per_session"] = game.max_bets_per_session

        super().__init__(**kwargs)


class Bet(db.Model):
    # Usability Not Confirmed
    __tablename__ = "bets"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.Integer,
        db.ForeignKey("game_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )

    amount = db.Column(db.Float, nullable=False)
    placed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    outcome = db.Column(db.String(20))  # e.g., 'win', 'loss'
    payout = db.Column(db.Float)  # positive or negative money flow
    choice = db.Column(db.String(100))  # what the user bet on
    is_successful = db.Column(db.Boolean)
    bet_details = db.Column(JSON, nullable=True)  # e.g., event odds, details

    __table_args__ = (db.Index("idx_bet_session", "session_id"),)

    @staticmethod
    def create(**kwargs):
        """
        Create a new bet with proper transaction handling and row locking.
        This method ensures thread-safe bet creation and counter updates.
        Args:
            **kwargs: Bet attributes including
        Returns:
            The created Bet instance
        Raises:
            ValueError: If session not found or max bets reached
            RuntimeError: If database error occurs
        """
        session_id = kwargs.get("session_id")
        if not session_id:
            raise ValueError("session_id is required")

        try:
            with db.session.begin_nested():
                # Lock the session row for safe concurrent updates
                session = GameSession.query.with_for_update().get(session_id)

                if not session:
                    raise ValueError(f"Session {session_id} not found")

                if session.bet_count >= session.max_bets_per_session:
                    raise ValueError(f"Max bets reached for session {session_id}")

                # Increment counter & create bet
                session.bet_count += 1

                bet = Bet(**kwargs)
                db.session.add(bet)

            db.session.commit()
            return bet

        except IntegrityError as e:
            db.session.rollback()
            raise RuntimeError("Database error occurred") from e
        except Exception:
            db.session.rollback()
            raise
