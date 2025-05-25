from app.models.gameplay import GameSession
from app.extensions import db


class GameSessionService:
    @staticmethod
    def create_game_session(user_id, game_id, session_data=None):
        if session_data is None:
            session = GameSession(user_id=user_id, game_id=game_id)
        elif isinstance(session_data, dict):
            session = GameSession(
                user_id=user_id, game_id=game_id, session_data=session_data
            )
        else:
            raise ValueError("Invalid session data")
        db.session.add(session)
        db.session.commit()
        return session.id

    @staticmethod
    def get_game_session(session_id):
        return GameSession.query.get(session_id)

    @staticmethod
    def validate_game_session(user_id, game_id, session_id):
        session = GameSession.query.filter_by(
            user_id=user_id, game_id=game_id, id=session_id
        ).first()
        if not session:
            raise ValueError("Invalid session")
        return session

    @staticmethod
    def get_last_game_session_by_user(user_id, game_id):
        return (
            GameSession.query.filter_by(user_id=user_id, game_id=game_id)
            .order_by(GameSession.id.desc())
            .first()
        )
