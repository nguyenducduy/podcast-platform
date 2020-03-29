import pendulum
from db import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.event import listens_for
from sqlalchemy.orm import relationship
# from models.group import Group
from models.rel_group_permission import RelGroupPermission


class Permission(db.Model):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=False, index=True)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer)
    groups = relationship('Group',
                          secondary='rel_group_permission',
                          back_populates='permissions')


@listens_for(Permission, 'before_insert')
def generate_created_at(mapper, connect, self):
    self.created_at = int(pendulum.now().timestamp())
    return self.created_at


@listens_for(Permission, 'before_update')
def generate_updated_at(mapper, connect, self):
    self.updated_at = int(pendulum.now().timestamp())
    return self.updated_at
