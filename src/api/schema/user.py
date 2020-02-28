from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from model.user import User
from graphql import GraphQLError
from db import db_session
from graphene_file_upload.scalars import Upload
from helper.graphtype import CommonDictType
import graphene
import time


class UserNode(SQLAlchemyObjectType):
    class Meta:
        model = User

    group = graphene.Field(CommonDictType)

    def resolve_group(self, info):
        return self.getGroup()


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            # 'id': [...],
            'group_id': [...]
        }


# QUERY
class UserConnection(graphene.Connection):
    class Meta:
        node = UserNode
    total_count = graphene.NonNull(graphene.Int)
    group_list = graphene.List(CommonDictType)

    def resolve_total_count(self, info, **kwargs):
        return self.length

    def resolve_group_list(self, info, **kwargs):
        return User.getGroupList()


# MUTATION
class CreateUser(graphene.Mutation):
    class Arguments:
        screen_name = graphene.String(required=True)
        full_name = graphene.String(required=True)
    user = graphene.Field(lambda: UserNode)

    def mutate(self, info, screen_name, full_name):
        new_user = User(
            screen_name=screen_name,
            full_name=full_name
        )
        save_changes(new_user)

        return CreateUser(user=new_user)


class AvatarUpload(graphene.Mutation):
    class Arguments:
        file_in = Upload()
    ok = graphene.Boolean()

    def mutate(self, info, file_in):
        return AvatarUpload(ok=True)


class SignupUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        full_name = graphene.String(required=True)
    user = graphene.Field(lambda: UserNode)

    def mutate(self, info, **kwargs):
        new_user = User(
            email=kwargs.get('email'),
            password_hash=kwargs.get('password'),
            full_name=kwargs.get('full_name'),
            created_at=int(time.time())
        )
        save_changes(new_user)

        return SignupUser(user=new_user)


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
            print(auth_token)
        else:
            raise GraphQLError("Invalid credentials")

        return LoginUser(user=user, token=auth_token.decode())


def save_changes(data):
    db_session.add(data)
    db_session.commit()
