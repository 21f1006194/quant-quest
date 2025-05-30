from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSON
from app.extensions import db
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
    difficulty = db.Column(db.String(50), nullable=True)
    tags = db.Column(db.String(255), nullable=True)
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
            "difficulty": self.difficulty,
            "tags": self.tags,
        }


class GamePnL(db.Model):
    __tablename__ = "game_pnls"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(
        db.Integer, db.ForeignKey("games.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    pnl = db.Column(db.Float, nullable=False, default=0.0)
    bet_count = db.Column(db.Integer, nullable=False, default=0)
    session_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "game_id": self.game_id,
            "user_id": self.user_id,
            "pnl": self.pnl,
            "bet_count": self.bet_count,
            "session_count": self.session_count,
            "updated_at": str(self.updated_at),
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

    session_data = db.Column(JSON, nullable=True)  # gameplay-specific data
    bet_count = db.Column(db.Integer, default=0, nullable=False)  # Track number of bets
    max_bets_per_session = db.Column(db.Integer, nullable=False)  # Copied from game
    net_flow = db.Column(db.Float, default=0, nullable=False)
    bets = db.relationship(
        "Bet", back_populates="session", cascade="all, delete", passive_deletes=True
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

            game_pnl = GamePnL.query.filter_by(user_id=user_id, game_id=game_id).first()
            if not game_pnl:
                raise ValueError(
                    f"Game PnL with user_id {user_id} and game_id {game_id} does not exist"
                )

            if game_pnl.session_count >= game.max_sessions_per_user:
                raise ValueError(
                    f"Maximum number of sessions ({game.max_sessions_per_user}) "
                    f"reached for user {user_id} in game {game_id}"
                )

            # Copy max_bets_per_session from game
            kwargs["max_bets_per_session"] = game.max_bets_per_session

        super().__init__(**kwargs)
        game_pnl.session_count += 1


class Bet(db.Model):
    # Usability Not Confirmed
    __tablename__ = "bets"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.Integer,
        db.ForeignKey("game_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    game_id = db.Column(
        db.Integer,
        db.ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    amount = db.Column(db.Float, nullable=False)
    placed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    payout = db.Column(db.Float, nullable=False)
    choice = db.Column(db.String(100), nullable=False)
    bet_details = db.Column(JSON, nullable=True)

    __table_args__ = (db.Index("idx_bet_session", "session_id", "game_id", "user_id"),)

    session = db.relationship("GameSession", back_populates="bets")

    @property
    def net_flow(self):
        """Calculate the net flow (profit/loss) for this bet.
        Returns the difference between payout and amount.
        """
        return self.payout - self.amount

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "placed_at": str(self.placed_at),
            "payout": self.payout,
            "choice": self.choice,
            "bet_details": self.bet_details,
        }
