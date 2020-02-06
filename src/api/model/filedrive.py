from db import Base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.event import listens_for
import pendulum


class Filedrive(Base):
    __tablename__ = 'file_drive'

    u_id = Column(Integer)
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(155))
    ext = Column(String(30))
    path = Column(String(512), nullable=False, index=True)
    size = Column(Integer)
    duration = Column(Float)
    type = Column(Integer)
    is_tmp = Column(Integer)
    is_common = Column(Integer)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer)

    TYPE_FX = 1
    TYPE_RECORD = 3
    TYPE_TRIMMED = 5
    TYPE_CROSSFADED = 7
    TYPE_MIXED = 9
    TYPE_EPISODE = 11
    IS_TMP = 1
    IS_NOT_TMP = 3
    IS_COMMON = 1
    IS_NOT_COMMON = 3

@listens_for(Filedrive, 'before_insert')
def generate_created_at(mapper, connect, self):
    self.created_at = int(pendulum.now().timestamp())
    return self.created_at

@listens_for(Filedrive, 'before_update')
def generate_updated_at(mapper, connect, self):
    self.updated_at = int(pendulum.now().timestamp())
    return self.updated_at
