from flask_restful import current_app, Resource, inputs
from flask_restful.reqparse import RequestParser

from models.user import LoginUser
from utils import auth, parser, response


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

        return response.success_response(msg='Login success!', data={
            'token': 'Bearer ' + token
        })
