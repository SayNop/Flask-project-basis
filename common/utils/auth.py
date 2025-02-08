from flask import current_app, request, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer

from . import response
from .time_utils import *


TOKEN_PREFIX = 'login:token:'
CONFLICT_PREFIX = 'conflict:'

auth = HTTPTokenAuth()


def init_serializer(app) -> TimedJSONWebSignatureSerializer:
    return TimedJSONWebSignatureSerializer(app.config['JWT_SECRET'], expires_in=app.config['JWT_EXPIRY_DAYS'] * 24 * 3600)


@auth.verify_token
def verify_token(token: str) -> bool:
    try:
        data = current_app.serializer.loads(token)
    except Exception:
        return False
    if _check_conflict(token):
        return False
    # todo check user
    g.phone = data['phone']
    return True


@auth.error_handler
def error_handler() -> dict:
    if not request.headers.get('Authorization'):
        return response.fail_response(response.TOKEN_INVALID, 'token error')
    try:
        token = request.headers['Authorization'].split(None, 1)[1]
        current_app.serializer.loads(token)
    except Exception:
        return response.fail_response(response.TOKEN_EXPIRY, 'token expiry')
    if _check_conflict(token):
        return response.fail_response(response.TOKEN_CONFLICT, msg='Log in on other platforms.')
    return response.fail_response(response.PERMISSION_DENIED, 'no permission')


def generate_token(payload: dict) -> str:
    _pay_load = {
        'exp': datetime.utcnow() + timedelta(days=current_app.config['JWT_EXPIRY_DAYS']),
        'nbf': datetime.utcnow()
    }
    _pay_load.update(payload)
    return current_app.serializer.dumps(_pay_load).decode()


def _check_conflict(token: str) -> bool:
    return True if current_app.redis_master.get(CONFLICT_PREFIX + token) else False
