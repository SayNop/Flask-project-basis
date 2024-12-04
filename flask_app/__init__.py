from flask import Flask


def create_flask_app(config: dict) -> Flask:
    """
    :param config: configuration dict
    :return: Flask app
    """
    app = Flask(__name__)
    app.config.from_mapping(config)

    # limiter
    # from utils.limiter import limiter as lmt
    # lmt.init_app(app)

    # redis
    from redis import StrictRedis
    from settings import REDIS_CONFIG
    app.redis_master = StrictRedis(**REDIS_CONFIG)

    # MySQL conn init
    from models import db
    db.init_app(app)

    # bluepoints

    return app
