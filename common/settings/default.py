Prod_flask_config = dict(
    # todo: logs dir
    LOGGING_FILE_DIR='/data/logs/flask-basis/',

    # todo: database
    SQLALCHEMY_DATABASE_URI=f'mysql+pymysql://root:mysql123@127.0.0.1:3306/example',
)

# todo: prod redis
Prod_redis_config = dict(
    host='127.0.0.1',
    port=6379,
    decode_responses=True
)
