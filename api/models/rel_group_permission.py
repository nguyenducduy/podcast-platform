from db import db
from sqlalchemy import Column, Integer, String, ForeignKey


class RelGroupPermission(db.Model):
    __tablename__ = 'rel_group_permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)
    permission_id = Column(Integer,
                           ForeignKey('permission.id'),
                           primary_key=True)
