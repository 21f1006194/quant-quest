import os
from dotenv import load_dotenv
from datetime import timedelta
from typing import List, Optional

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, "../.env"))


class ConfigValidator:
    """Validates that all required environment variables are present."""

    REQUIRED_ENV_VARS = [
        "SECRET_KEY",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
        "JWT_SECRET_KEY",
        "REDIS_HOST",
        "REDIS_PORT",
        "REDIS_DB",
        "ADMIN_EMAIL",
        "ADMIN_USERNAME",
        "ADMIN_PASSWORD",
        "ADMIN_FULL_NAME",
        "CORS_ORIGINS",
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET",
        "GOOGLE_REDIRECT_URI",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GCP_BUCKET_NAME",
    ]

    @classmethod
    def validate(cls) -> Optional[List[str]]:
        """Validate that all required environment variables are present.

        Returns:
            Optional[List[str]]: List of missing environment variables, or None if all are present
        """
        missing_vars = [var for var in cls.REQUIRED_ENV_VARS if not os.environ.get(var)]
        return missing_vars if missing_vars else None


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]

    # Database Configuration
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_NAME = os.environ["DB_NAME"]
    DB_USER = os.environ["DB_USER"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_ERROR_MESSAGE_KEY = "error"

    # Redis Configuration
    REDIS_HOST = os.environ["REDIS_HOST"]
    REDIS_PORT = int(os.environ["REDIS_PORT"])
    REDIS_DB = int(os.environ["REDIS_DB"])

    # Admin Configuration
    ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]
    ADMIN_USERNAME = os.environ["ADMIN_USERNAME"]
    ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
    ADMIN_FULL_NAME = os.environ["ADMIN_FULL_NAME"]

    # CORS Configuration
    CORS_ORIGINS = os.environ["CORS_ORIGINS"].split(",")

    # Google credentials
    GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
    GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
    GOOGLE_REDIRECT_URI = os.environ["GOOGLE_REDIRECT_URI"]
    GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    GCP_BUCKET_NAME = os.environ["GCP_BUCKET_NAME"]
