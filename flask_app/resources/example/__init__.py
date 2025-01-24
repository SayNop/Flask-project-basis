from flask import Blueprint
from flask_restful import Api

from . import ex_passport
from utils.output import output_json


example_bp = Blueprint('user', __name__)
example_api = Api(example_bp, catch_all_404s=True)
example_api.representation('application/json')(output_json)


example_api.add_resource(ex_passport.LoginResource, '/api/login', endpoint='GetAuth')
example_api.add_resource(ex_passport.LoginResource, '/api/register', endpoint='Register')