from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSON
from app import db


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50), nullable=True)  # e.g., 'quiz', 'puzzle', 'prediction'
    metadata = db.Column(JSON, nullable=True)  # game configuration, rules, etc.
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    sessions = db.relationship("GameSession", backref="game", cascade="all, delete", passive_deletes=True)


class GameSession(db.Model):
    __tablename__ = "game_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id", ondelete="CASCADE"), nullable=False)

    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = db.Column(db.DateTime)
    duration = db.Column(db.Interval)

    result = db.Column(db.String(20))  # e.g., 'win', 'loss', 'draw'
    score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default="in_progress")  # 'in_progress', 'completed', 'forfeited'
    metadata = db.Column(JSON, nullable=True)  # gameplay-specific data

    bets = db.relationship("Bet", backref="session", cascade="all, delete", passive_deletes=True)

    __table_args__ = (
        db.Index('idx_session_user_game', 'user_id', 'game_id'),
    )


class Bet(db.Model):
    # Usability Not Confirmed
    __tablename__ = "bets"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False)

    amount = db.Column(db.Float, nullable=False)
    placed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    outcome = db.Column(db.String(20))  # e.g., 'win', 'loss'
    payout = db.Column(db.Float)  # positive or negative money flow
    choice = db.Column(db.String(100))  # what the user bet on
    is_successful = db.Column(db.Boolean)
    metadata = db.Column(JSON, nullable=True)  # e.g., event odds, details

    __table_args__ = (
        db.Index('idx_bet_session', 'session_id'),
    )
