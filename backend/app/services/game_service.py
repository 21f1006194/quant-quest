from app.models.gameplay import Game, GameSession
from app import db
from sqlalchemy import case


class GameService:
    @staticmethod
    def get_all_games():
        return Game.query.all()

    @staticmethod
    def get_game_by_id(game_id):
        return Game.query.get(game_id)

    @staticmethod
    def get_active_games():
        return Game.query.filter_by(is_active=True).all()

    @staticmethod
    def get_games_played_data_by_user(user_id):
        """
        Get the number of times a user has played each game and the PnL for each game

        Returns:
            dict: {game_id: number_of_plays}
        """
        # TODO: This is a temporary solution, we should use a more efficient query later
        games_sessions = GameSession.query.filter_by(user_id=user_id).all()
        session_count = {}
        pnl = {}
        for game_session in games_sessions:
            session_count[game_session.game_id] = (
                session_count.get(game_session.game_id, 0) + 1
            )
            pnl[game_session.game_id] = (
                pnl.get(game_session.game_id, 0) + game_session.net_flow
            )

        return session_count, pnl
