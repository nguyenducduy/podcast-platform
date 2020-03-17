from db import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import (relationship, backref)
from sqlalchemy.event import listens_for
import pendulum
from model.filedrive import Filedrive


class Episode(Base):
    __tablename__ = 'episode'

    p_id = Column(Integer)
    u_id = Column(Integer)
    fd_id = Column(Integer, ForeignKey('file_drive.id'))
    audio_file = relationship(
        Filedrive,
        backref=backref('filedrive', uselist=False)
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String)
    cover = Column(String(255))
    status = Column(Integer)
    type = Column(Integer)
    order_no = Column(Integer)
    season_no = Column(Integer)
    link = Column(String(255))
    author = Column(String(155))
    external_file_path = Column(String(255))
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer)

    STATUS_PUBLISH = 1
    STATUS_DRAFT = 3
    TYPE_FULL = 1
    TYPE_TRAILER = 3
    TYPE_BONUS = 5


@listens_for(Episode, 'before_insert')
def generate_created_at(mapper, connect, self):
    self.created_at = int(pendulum.now().timestamp())
    return self.created_at


@listens_for(Episode, 'before_update')
def generate_updated_at(mapper, connect, self):
    self.updated_at = int(pendulum.now().timestamp())
    return self.updated_at
