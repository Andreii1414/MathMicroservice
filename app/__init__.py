from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.utils.cache import cache
from app.config import Config
from app.utils.worker import AsyncWorker
from app.utils.zmq_logger import ZMQLogger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
worker = AsyncWorker(max_workers=5)
logger = ZMQLogger()
limiter = Limiter(
    key_func=get_remote_address
)


def create_app():
    """
    Create and configure the Flask application.
    This function initializes the Flask app, configures it with settings from Config,
    initializes the database and cache, and registers the API routes.
    :return: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    from app.routes.api_routes import register_routes
    register_routes(app)

    return app
