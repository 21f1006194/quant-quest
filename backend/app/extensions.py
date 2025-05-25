from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cache = Cache(
    config={
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_HOST": Config.REDIS_HOST,
        "CACHE_REDIS_PORT": Config.REDIS_PORT,
        "CACHE_REDIS_DB": Config.REDIS_DB,
        "CACHE_DEFAULT_TIMEOUT": 300,  # 5 minutes default timeout
    }
)
