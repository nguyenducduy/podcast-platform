import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from graphene_file_upload.scalars import Upload
from gtypes import CommonDictType
from db import db
from models.group import Group
from schemas.permission import PermissionNode


class GroupNode(SQLAlchemyObjectType):
    class Meta:
        model = Group

    permissions = graphene.List(PermissionNode)


class GroupFilter(FilterSet):
    class Meta:
        model = Group
        fields = {
            'id': [...],
            'name': [...],
        }


class GroupConnection(graphene.Connection):
    class Meta:
        node = GroupNode

    total_count = graphene.NonNull(graphene.Int)

    def resolve_total_count(self, info, **kwargs):
        return self.length


def save(data):
    db.session.add(data)
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()
