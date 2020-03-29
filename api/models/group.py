import pendulum
from db import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.event import listens_for
from models.permission import Permission
from models.rel_group_permission import RelGroupPermission


class Group(db.Model):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    screen_name = Column(String(100), nullable=False, index=True)
    color = Column(String(10))
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer)
    permissions = relationship('Permission',
                               secondary='rel_group_permission',
                               back_populates='groups')


@listens_for(Group, 'before_insert')
def generate_created_at(mapper, connect, self):
    self.created_at = int(pendulum.now().timestamp())
    return self.created_at


@listens_for(Group, 'before_update')
def generate_updated_at(mapper, connect, self):
    self.updated_at = int(pendulum.now().timestamp())
    return self.updated_at
