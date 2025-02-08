from flask import Blueprint
from flask_restful import Api

from . import ex_passport, ex_profile
from utils.output import output_json


example_bp = Blueprint('user', __name__)
example_api = Api(example_bp, catch_all_404s=True)
example_api.representation('application/json')(output_json)


example_api.add_resource(ex_passport.LoginResource, '/api/login', endpoint='GetAuth')
example_api.add_resource(ex_passport.RegisterResource, '/api/register', endpoint='Register')

example_api.add_resource(ex_profile.PasswordResource, '/my/pwd', endpoint='Password')

example_api.add_resource(ex_profile.UserInfoResource, '/my/info', endpoint='UserInfo')
