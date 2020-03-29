import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from graphene_file_upload.scalars import Upload
from gtypes import CommonDictType
from db import db
from models.user import User
from models.group import Group
from schemas.group import GroupNode


class UserNode(SQLAlchemyObjectType):
    class Meta:
        model = User

    group = graphene.Field(GroupNode)


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {'id': [...], 'group_id': [...]}


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
        email = graphene.String(required=True)
        screen_name = graphene.String(required=True)
        full_name = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(lambda: UserNode)

    def mutate(self, info, **kwargs):
        myUser = User(
            email=kwargs.get('email'),
            screen_name=kwargs.get('screen_name'),
            full_name=kwargs.get('full_name'),
            # password_hash=kwargs.get('password')
        )

        try:
            save(myUser)
        except Exception as err:
            print(err)
            raise Exception('Error create user.')

        return CreateUser(user=myUser)


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


def save(data):
    db.session.add(data)
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()
