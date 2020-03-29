import pendulum
import jwt
import datetime
from db import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy.event import listens_for
from flask_bcrypt import Bcrypt
from flask import current_app
from models.group import Group


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    screen_name = db.Column(db.String(32), nullable=False, index=True)
    full_name = db.Column(db.String(50))
    avatar = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), index=True)
    created_at = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.Integer)

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group', backref='user')

    @property
    def password_hash(self):
        raise AttributeError('password: write-only field')

    @password_hash.setter
    def password_hash(self, password):
        self.password = Bcrypt().generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e


@listens_for(User, 'before_insert')
def generate_created_at(mapper, connect, self):
    self.created_at = int(pendulum.now().timestamp())
    return self.created_at


@listens_for(User, 'before_update')
def generate_updated_at(mapper, connect, self):
    self.updated_at = int(pendulum.now().timestamp())
    return self.updated_at
