from flask import current_app
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser

from models import db
from models.user import LoginUser
from utils import response, parser
from utils.auth import auth, TOKEN_PREFIX, CONFLICT_PREFIX


class PasswordResource(Resource):
    method_decorators = {
        'post': [auth.login_required],
        'put': [auth.login_required]
    }
    def post(self):
        rp = RequestParser(parser.CustomArgument)
        rp.add_argument('phone', type=parser.mobile, required=True, location='json', help='phone format error')
        rp.add_argument('pwd', type=parser.str_len_range(8, 16), required=True, location='json', help='password format error')
        args = rp.parse_args()
        user = LoginUser.query.filter_by(phone=args.phone).first()
        if not user:
            return response.fail_response(response.PARAMS_ERROR, 'User does not exist')

        user.password = args.pwd
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            return response.fail_response(response.PARAMS_ERROR, 'Set password fail')

        old_token = current_app.redis_master.get(TOKEN_PREFIX + args.phone)
        if old_token:
            current_app.redis_master.setex(CONFLICT_PREFIX + old_token,
                                           3600 * 24 * current_app.config['JWT_EXPIRY_DAYS'],
                                           1)

        return response.success_response("Set password success")

    def put(self):
        rp = RequestParser(parser.CustomArgument)
        rp.add_argument('phone', type=parser.mobile, required=True, location='json', help='phone format error')
        rp.add_argument('old_pwd', type=parser.str_len_range(8, 16), required=True, location='json', help='password format error')
        rp.add_argument('new_pwd', type=parser.str_len_range(8, 16), required=True, location='json', help='password format error')
        args = rp.parse_args()

        user = LoginUser.query.filter_by(phone=args.phone).first()
        if not user:
            return response.fail_response(response.PARAMS_ERROR, 'User does not exist')

        if not user.check_password(args.old_pwd):
            return response.fail_response(response.PARAMS_ERROR, 'Password incorrect')

        user.password = args.new_pwd
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.exception(e)
            return response.fail_response(response.PARAMS_ERROR, 'Change Password fail')

        old_token = current_app.redis_master.get(TOKEN_PREFIX + args.phone)
        if old_token:
            current_app.redis_master.setex(CONFLICT_PREFIX + old_token,
                                           3600 * 24 * current_app.config['JWT_EXPIRY_DAYS'],
                                           1)

        return response.success_response("Change password success")
