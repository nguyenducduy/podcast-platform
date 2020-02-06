from db import Base, flask_bcrypt
from sqlalchemy import Column, Integer, String
from sqlalchemy.event import listens_for
from flask_security import UserMixin
import pendulum
import datetime
import jwt
from config import key


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    screen_name = Column(String(32), nullable=False, index=True)
    full_name = Column(String(50))
    avatar = Column(String(255))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), index=True)
    group_id = Column(Integer)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer)

    GROUPID_GUEST = 0
    GROUPID_ADMIN = 1
    GROUPID_MODERATOR = 5
    GROUPID_EMPLOYEE = 16
    GROUPID_MEMBER = 20

    def getGroup(self):
        group = {}
        if self.group_id == self.GROUPID_GUEST:
            group = { "text": "Guest", "value" : self.GROUPID_GUEST }
        elif self.group_id == self.GROUPID_ADMIN:
            group = { "text": "Administrator", "value" : self.GROUPID_ADMIN }
        elif self.group_id == self.GROUPID_MODERATOR:
            group = { "text": "Moderator", "value" : self.GROUPID_MODERATOR }
        elif self.group_id == self.GROUPID_EMPLOYEE:
            group = { "text": "Employee", "value" : self.GROUPID_EMPLOYEE }
        elif self.group_id == self.GROUPID_MEMBER:
            group = { "text": "Member", "value" : self.GROUPID_MEMBER }
        else:
            group = {}

        return group

    @staticmethod
    def getGroupList():
        return [
            { "text": "Guest", "value": User.GROUPID_GUEST },
            { "text": "Administrator", "value": User.GROUPID_ADMIN },
            { "text": "Moderator", "value": User.GROUPID_MODERATOR },
            { "text": "Employee", "value": User.GROUPID_EMPLOYEE },
            { "text": "Member", "value": User.GROUPID_MEMBER },
        ]

    @property
    def password_hash(self):
        raise AttributeError('password: write-only field')

    @password_hash.setter
    def password_hash(self, password):
        self.password = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(request):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        try:
            payload = jwt.decode(auth_token, key, algorithms='HS256')
            return payload['sub']
            # is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            # if is_blacklisted_token:
            #     return 'Token blacklisted. Please log in again.'
            # else:
            #     return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

@listens_for(User, 'before_insert')
def generate_created_at(mapper, connect, self):
    self.created_at = int(pendulum.now().timestamp())
    return self.created_at

@listens_for(User, 'before_update')
def generate_updated_at(mapper, connect, self):
    self.updated_at = int(pendulum.now().timestamp())
    return self.updated_at
