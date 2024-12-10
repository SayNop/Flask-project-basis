from flask import current_app, request
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer

from . import response
from .time_utils import *


auth = HTTPTokenAuth()


def init_serializer(app) -> TimedJSONWebSignatureSerializer:
    return TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_in=app.config['JWT_EXPIRY_DAYS'] * 24 * 3600)


@auth.verify_token
def verify_token(token: str) -> bool:
    try:
        data = current_app.serializer.loads(token)
    except Exception:
        return False
    # todo check conflict
    # todo check user
    return True


@auth.error_handler
def error_handler() -> dict:
    if not request.headers.get('Authorization'):
        return response.fail_response(response.TOKEN_INVALID)
    try:
        current_app.serializer.loads(request.headers['Authorization'].split(None, 1)[1])
    except Exception:
        return response.fail_response(response.TOKEN_EXPIRY)
    return response.fail_response(response.PERMISSION_DENIED)


def generate_token(payload: dict) -> str:
    _pay_load = {
        'exp': datetime.utcnow() + timedelta(days=current_app.config['JWT_EXPIRY_DAYS']),
        'nbf': datetime.utcnow()
    }
    _pay_load.update(payload)
    return current_app.serializer.dumps(_pay_load).decode()
