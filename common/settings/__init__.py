from socket import gethostname


FLASK_CONFIG = dict(
    ERROR_404_HELP=False,

    # CORS - flask_cors
    CORS_ORIGINS='*',

    # 日志
    LOGGING_LEVEL='DEBUG',
    LOGGING_FILE_DIR='',  # filled in default/dev
    LOGGING_FILE_MAX_BYTES=300 * 1024 * 1024,
    LOGGING_FILE_BACKUP=10,

    SQLALCHEMY_DATABASE_URI='',  # filled in default/dev
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
    SQLALCHEMY_ECHO=False,

    # JWT
    JWT_SECRET='',  # todo: fill secret
    JWT_EXPIRY_DAYS=7
)


# todo: proc server host name - 1. single server `== 'prod'` 2. multi server `in ['prod1', 'prod2']`
if gethostname() in ['prod']:
    from .default import Prod_flask_config, Prod_redis_config
    FLASK_CONFIG.update(Prod_flask_config)
    REDIS_CONFIG = Prod_redis_config
else:
    from .dev import Dev_flask_config, Dev_redis_config
    FLASK_CONFIG.update(Dev_flask_config)
    REDIS_CONFIG = Dev_redis_config
