import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base configuration class for the application.
    This class loads environment variables and sets up configuration
    parameters for the Flask application.
    """
    SECRET_KEY = os.getenv("SECRET_KEY")  # not used, just for example
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
