from db import db
from sqlalchemy.event import listens_for
import pendulum


class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255))
    created_at = db.Column(db.Integer, nullable=False)


@listens_for(BlacklistToken, 'before_insert')
def generate_created_at(mapper, connect, self):
    self.created_at = int(pendulum.now().timestamp())
    return self.created_at
