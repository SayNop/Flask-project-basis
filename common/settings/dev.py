from pathlib import Path


_host = '127.0.0.1'

Dev_flask_config = dict(
    TESTING=True,

    # logs
    LOGGING_FILE_DIR=str(Path(__file__).resolve().parents[2] / 'log'),

    # todo: database
    SQLALCHEMY_DATABASE_URI=f'mysql+pymysql://root:mysql123@{_host}:3306/test',
)


Dev_redis_config = dict(
    host=_host,
    port=6379,
    decode_responses=True
)
