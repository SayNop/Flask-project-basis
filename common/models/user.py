from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class LoginUser(db.Model):
    """
    Login User Table Example

    Create a data table
    1. Write a create table SQL statement
    2. Use the SQL script in step 1 to create a data table in mysql cli
    3. Write ORM according to the data table field type
    """

    __tablename__ = 'login_user'

    phone = db.Column(db.String(11), primary_key=True, doc='phone number')
    username = db.Column(db.String(15), doc='nickname')
    _password = db.Column('password', db.String, doc='password')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='create time')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, doc='update time')
    last_login = db.Column(db.DateTime, doc='last login time')

    def __repr__(self):
        return '<User %r>' % self.phone

    @property
    def password(self):
        raise Exception('The password cannot be read')

    @password.setter
    def password(self, value: str):
        self._password = generate_password_hash(value)

    def check_password(self, pwd: str) -> bool:
        """
        :return: True or False
        """
        return check_password_hash(self._password, pwd)
