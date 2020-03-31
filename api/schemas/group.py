import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from graphene_file_upload.scalars import Upload
from gtypes import CommonDictType
from db import db
from models.group import Group
from models.permission import Permission
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


class CreateGroup(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        screen_name = graphene.String(required=True)
        color = graphene.String(required=True)

    group = graphene.Field(lambda: GroupNode)

    def mutate(self, info, **kwargs):
        myGroup = Group(
            name=kwargs.get('name'),
            screen_name=kwargs.get('screen_name'),
            color=kwargs.get('color')
        )
        save(myGroup)

        return CreateGroup(group=myGroup)


class UpdateGroup(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        screen_name = graphene.String(required=True)
        color = graphene.String(required=True)

    group = graphene.Field(lambda: GroupNode)

    def mutate(self, info, **kwargs):
        myGroup = Group.query.get(kwargs.get('id'))
        if not myGroup:
            raise Exception('Group not found')

        myGroup.name = kwargs.get('name')
        myGroup.screen_name = kwargs.get('screen_name')
        myGroup.color = kwargs.get('color')
        save(myGroup)

        return UpdateGroup(group=myGroup)


class DeleteGroup(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    deleted = graphene.Boolean()

    def mutate(self, info, **kwargs):
        myGroup = Group.query.get(kwargs.get('id'))
        if not myGroup:
            raise Exception('Group not found')

        delete(myGroup)

        return DeleteGroup(deleted=True)


class GrantPermission(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        permissions = graphene.List(graphene.String, required=True)

    granted = graphene.Boolean()

    def mutate(self, info, **kwargs):
        myGroup = Group.query.get(kwargs.get('id'))
        if not myGroup:
            raise Exception('Group not found')

        currentPermissions = []
        for perm in myGroup.permissions:
            currentPermissions.append(perm.id)

        # add new permission
        for permId in kwargs.get('permissions'):
            if permId not in currentPermissions:
                myPerm = Permission.query.get(permId)
                myGroup.permissions.append(myPerm)

        # remove old permission which are not include in new permission
        for permId in currentPermissions:
            if permId not in kwargs.get('permissions'):
                myPerm = Permission.query.get(permId)
                myGroup.permissions.remove(myPerm)

        db.session.commit()

        return GrantPermission(granted=True)


def save(data):
    db.session.add(data)
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()
