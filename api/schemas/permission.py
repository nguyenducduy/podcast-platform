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


class CreatePermission(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    permission = graphene.Field(lambda: PermissionNode)

    def mutate(self, info, **kwargs):
        myPermission = Permission(
            name=kwargs.get('name'),
            description=kwargs.get('description')
        )
        save(myPermission)

        return CreatePermission(permission=myPermission)


class UpdatePermission(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    permission = graphene.Field(lambda: PermissionNode)

    def mutate(self, info, **kwargs):
        myPermission = Permission.query.get(kwargs.get('id'))
        if not myPermission:
            raise Exception('Permission not found')

        myPermission.name = kwargs.get('name')
        myPermission.description = kwargs.get('description')
        save(myPermission)

        return UpdatePermission(permission=myPermission)


class DeletePermission(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    deleted = graphene.Boolean()

    def mutate(self, info, **kwargs):
        myPermission = Permission.query.get(kwargs.get('id'))
        if not myPermission:
            raise Exception('Permission not found')

        delete(myPermission)

        return DeletePermission(deleted=True)


def save(data):
    db.session.add(data)
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()
