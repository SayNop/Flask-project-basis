from flask import Flask


def create_flask_app(config: dict) -> Flask:
    """
    :param config: configuration dict
    :return: Flask app
    """
    app = Flask(__name__)
    app.config.from_mapping(config)

    # limiter
    from utils.limiter import limiter
    limiter.init_app(app)

    # logger
    from utils.logging import create_logger
    create_logger(app)

    # redis
    from redis import StrictRedis
    from settings import REDIS_CONFIG
    app.redis_master = StrictRedis(**REDIS_CONFIG)

    # auth
    from utils.auth import init_serializer
    app.serializer = init_serializer(app)

    # MySQL conn init
    from models import db
    db.init_app(app)

    # bluepoints
    from .resources.example import example_bp  # todo: remove example bluepoints
    app.register_blueprint(example_bp)

    # todo: add your bluepoints here

    return app
