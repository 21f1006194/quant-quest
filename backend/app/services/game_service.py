from app.models.gameplay import Game, GameSession, GamePnL
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
        game_pnls = GamePnL.query.filter_by(user_id=user_id).all()
        return {game_pnl.game_id: game_pnl.to_dict() for game_pnl in game_pnls}

    @staticmethod
    def get_game_pnl_by_user(user_id):
        return GamePnL.query.filter_by(user_id=user_id).all()

    @staticmethod
    def initialize_game_pnl_for_user(user_id):
        games = Game.query.all()
        for game in games:
            game_pnl = GamePnL(user_id=user_id, game_id=game.id)
            db.session.add(game_pnl)
        db.session.commit()
