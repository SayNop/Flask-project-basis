from json import dumps
from flask import make_response, current_app, request
from flask_restful.utils import PY3

from .response import FRAMEWORK, SUCCESS


def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    if 'message' not in data:
        data = {
            'message': 'OK',
            'data': data
        }

    if 'code' not in data:
        if str(code) != 200:
            data['code'] = FRAMEWORK
            if type(data['message'] != str):
                data['message'] = str(data['message'])
        else:
            data['code'] = SUCCESS

    if 'success' not in data:
        data['success'] = True if data['code'] == SUCCESS else False

    settings = current_app.config.get('RESTFUL_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
