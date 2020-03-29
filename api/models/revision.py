import pendulum
from db import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.event import listens_for
from models.filedrive import Filedrive


class Revision(db.Model):
    __tablename__ = 'revision'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(30), nullable=False, index=True)
    u_id = Column(Integer, nullable=False, index=True)
    version = Column(Integer, nullable=False, index=True)
    content = Column(String, nullable=False)
    files_used = Column(String, nullable=False)
    mixed_id = Column(Integer, ForeignKey('file_drive.id'))
    mixed_file = relationship(Filedrive,
                              backref=backref('revision', uselist=True))
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer)


@listens_for(Revision, 'before_insert')
def generate_created_at(mapper, connect, self):
    self.created_at = int(pendulum.now().timestamp())
    return self.created_at


@listens_for(Revision, 'before_update')
def generate_updated_at(mapper, connect, self):
    self.updated_at = int(pendulum.now().timestamp())
    return self.updated_at
