import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from graphene_file_upload.scalars import Upload
from gtypes import CommonDictType
from db import db
from models.permission import Permission


class PermissionNode(SQLAlchemyObjectType):
    class Meta:
        model = Permission


class PermissionFilter(FilterSet):
    class Meta:
        model = Permission
        fields = {
            'id': [...],
            'name': [...],
        }


class PermissionConnection(graphene.Connection):
    class Meta:
        node = PermissionNode

    total_count = graphene.NonNull(graphene.Int)

    def resolve_total_count(self, info, **kwargs):
        return self.length


def save(data):
    db.session.add(data)
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()
