import logging
import logging.handlers
from pathlib import Path
from flask import request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


def create_logger(app):
    """
    :param app: Flask app
    :return:
    """
    logging_level = app.config['LOGGING_LEVEL']
    logging_file_dir = app.config['LOGGING_FILE_DIR']
    logging_file_max_bytes = app.config['LOGGING_FILE_MAX_BYTES']
    logging_file_backup = app.config['LOGGING_FILE_BACKUP']

    flask_console_handler = logging.StreamHandler()
    flask_console_handler.setFormatter(logging.Formatter('%(levelname)s %(module)s %(lineno)d %(message)s'))

    request_formatter = RequestFormatter('[%(asctime)s] %(remote_addr)s %(url)s\n'
                                         '%(levelname)s in %(module)s %(lineno)d: %(message)s')

    flask_file_handler = logging.handlers.RotatingFileHandler(
        filename=str(Path(logging_file_dir) / 'flask.log'),
        maxBytes=logging_file_max_bytes,
        backupCount=logging_file_backup
    )
    flask_file_handler.setFormatter(request_formatter)

    limit_file_handler = logging.handlers.RotatingFileHandler(
        filename=str(Path(logging_file_dir) / 'limit.log'),
        maxBytes=logging_file_max_bytes,
        backupCount=logging_file_backup
    )
    limit_file_handler.setFormatter(request_formatter)

    log_flask_app = logging.getLogger('flask.app')
    log_flask_app.addHandler(flask_file_handler)
    log_flask_app.setLevel(logging_level)

    log_flask_limiter = logging.getLogger('flask-limiter')
    log_flask_limiter.addHandler(limit_file_handler)
    log_flask_limiter.setLevel(logging_level)

    if app.debug:
        log_flask_app.addHandler(flask_console_handler)
        log_flask_limiter.addHandler(flask_console_handler)
