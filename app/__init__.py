from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.utils.cache import cache
from app.config import Config
from app.utils.worker import AsyncWorker
from app.utils.zmq_logger import ZMQLogger

db = SQLAlchemy()
worker = AsyncWorker(max_workers=5)
logger = ZMQLogger()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cache.init_app(app)

    from app.routes.api_routes import math_bp
    app.register_blueprint(math_bp, url_prefix='/')

    return app
