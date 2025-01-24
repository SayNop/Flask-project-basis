from datetime import datetime
from flask_restful import current_app, Resource
from flask_restful.reqparse import RequestParser

from models import db
from models.user import LoginUser
from utils import parser, response
from utils.auth import TOKEN_PREFIX, CONFLICT_PREFIX


class LoginResource(Resource):
    def post(self):
        rp = RequestParser(parser.CustomArgument)
        rp.add_argument('phone', type=parser.mobile, required=True, location='json', help='phone number error')
        # rp.add_argument('code', type=inputs.regex(r'\d{4}'), required=False, location='json', help='sms code error')
        rp.add_argument('password', type=parser.str_len_range(8, 16), required=False, location='json', help='password error')
        args = rp.parse_args()

        user = LoginUser.query.filter_by(phone=args.phone).first()
        if not user:
            return response.fail_response(code=response.NOT_FOUND, msg='This phone number has not been registered yet!')
        token = current_app.serializer.dumps({'phone': args.phone}).decode()
        old_token = current_app.redis_master.get(TOKEN_PREFIX + args.phone)
        if old_token:
            current_app.redis_master.setex(CONFLICT_PREFIX + old_token,
                                           3600 * 24 * current_app.config['JWT_EXPIRY_DAYS'],
                                           1)
        current_app.redis_master.setex(TOKEN_PREFIX + args.phone,
                                       3600 * 24 * current_app.config['JWT_EXPIRY_DAYS'],
                                       token)

        user.last_login = datetime.now()
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)

        return response.success_response(msg='Login success!', data={
            'token': 'Bearer ' + token
        })


class RegisterResource(Resource):
    def post(self):
        rp = RequestParser(parser.CustomArgument)
        rp.add_argument('phone', type=parser.mobile, required=True, location='json', help='phone number error')
        rp.add_argument('password', type=parser.str_len_range(8, 16), required=True, location='json', help='password error')
        rp.add_argument('username', type=parser.str_len_range(1, 15), required=False, location='json', help='username error')
        args = rp.parse_args()

        user = LoginUser.query.filter_by(phone=args.phone).first()
        if user:
            return response.fail_response(response.PARAMS_ERROR, 'This phone number has been registered')
        user = LoginUser()
        user.phone = args.phone
        user.username = args.username or 'User' + args.phone[-4:]
        user.password = args.password
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
            return response.fail_response(msg='Register fail!')

        return response.success_response(msg='Register success!')
