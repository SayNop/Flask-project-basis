SUCCESS = 0

# framework
FRAMEWORK = 1

# auth
TOKEN_INVALID = 1000
TOKEN_EXPIRY = 1001
TOKEN_CONFLICT = 1002
PERMISSION_DENIED = 1003

# request
PARAMS_ERROR = 2000
NOT_FOUND = 2001
DUPLICATE = 2002


def success_response(msg='OK', data={}) -> dict:
    return {'code': SUCCESS, 'message': msg, 'data': data}


def fail_response(code=FRAMEWORK, msg='请求失败', data={}) -> dict:
    return {'code': code, 'message': msg, 'data': data}
