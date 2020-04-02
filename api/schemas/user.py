import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from graphene_file_upload.scalars import Upload
from gtypes import CommonDictType
from db import db
from models.user import User
from models.group import Group
from models.blacklist_token import BlacklistToken
from schemas.group import GroupNode


class UserNode(SQLAlchemyObjectType):
    class Meta:
        model = User

    group = graphene.Field(GroupNode)


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {'id': [...], 'group_id': [...],
                  'email': [...], 'full_name': [...]}


class UserConnection(graphene.Connection):
    class Meta:
        node = UserNode

    total_count = graphene.NonNull(graphene.Int)
    group_list = graphene.List(GroupNode)

    def resolve_total_count(self, info, **kwargs):
        return self.length

    def resolve_group_list(self, info, **kwargs):
        return Group.query.all()


class CreateUser(graphene.Mutation):
    class Arguments:
        full_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        group_id = graphene.Int(required=True)

    user = graphene.Field(lambda: UserNode)

    def mutate(self, info, **kwargs):
        myUser = User(
            email=kwargs.get('email'),
            full_name=kwargs.get('full_name'),
            password_hash=kwargs.get('password'),
            group_id=kwargs.get('group_id')
        )
        save(myUser)

        return CreateUser(user=myUser)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        full_name = graphene.String(required=True)
        email = graphene.String(required=True)
        group_id = graphene.Int(required=True)

    user = graphene.Field(lambda: UserNode)

    def mutate(self, info, **kwargs):
        myUser = User.query.get(kwargs.get('id'))
        if not myUser:
            raise Exception('User not found')

        myUser.full_name = kwargs.get('full_name')
        myUser.email = kwargs.get('email')
        myUser.group_id = kwargs.get('group_id')
        save(myUser)

        return UpdateUser(user=myUser)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    deleted = graphene.Boolean()

    def mutate(self, info, **kwargs):
        myUser = User.query.get(kwargs.get('id'))
        if not myUser:
            raise Exception('User not found')

        delete(myUser)

        return DeleteUser(deleted=True)


class LoginUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(lambda: UserNode)
    token = graphene.String()

    def mutate(self, info, **kwargs):
        user = User.query.filter_by(email=kwargs.get('email')).first()
        if user and user.check_password(kwargs.get('password')):
            auth_token = user.encode_auth_token(user.id)
        else:
            raise Exception("Invalid credentials")

        return LoginUser(user=user, token=auth_token.decode())


class LogoutUser(graphene.Mutation):
    logged_out = graphene.Boolean()

    def mutate(self, info, **kwargs):
        myBlacklistToken = BlacklistToken(
            token=kwargs.get('token')
        )
        save(myBlacklistToken)

        return LogoutUser(logged_out=True)


class ChangePassword(graphene.Mutation):
    class Arguments:
        password = graphene.String(required=True)

    user = graphene.Field(lambda: UserNode)

    def mutate(self, info, **kwargs):
        myUser = User.query.get(kwargs.get('user').id)
        if not myUser:
            raise Exception('User not found')

        myUser.password_hash = kwargs.get('password')
        save(myUser)

        return ChangePassword(user=myUser)


def save(data):
    db.session.add(data)
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()
