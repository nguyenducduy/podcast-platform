from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from graphql import GraphQLError
from helper.decorator import require_auth
from helper import filedrive
from model.episode import Episode
from db import db_session
from graphene_file_upload.scalars import Upload
from config import upload_dir
from werkzeug.utils import secure_filename
from datetime import datetime
import graphene
import os


# DEFINE NODE
class EpisodeNode(SQLAlchemyObjectType):
    class Meta:
        model = Episode

    cover = graphene.String()

    def resolve_cover(self, info):
        return filedrive.getPath('episode', self.cover)

# FILTER


class EpisodeFilter(FilterSet):
    class Meta:
        model = Episode
        fields = {
            'id': [...],
            'p_id': [...],
            'status': [...]
        }

# QUERY


class EpisodeConnection(graphene.relay.Connection):
    class Meta:
        node = EpisodeNode
    total_count = graphene.NonNull(graphene.Int)

    def resolve_total_count(self, info, **kwargs):
        return self.length

# MUTATION


class CreateEpisode(graphene.Mutation):
    class Arguments:
        p_id = graphene.Int(required=True)
        cover_img = Upload()
        title = graphene.String(required=True)
        description = graphene.String()
        status = graphene.Int(required=True)
        type = graphene.Int(required=True)
        order_no = graphene.Int()
        season_no = graphene.Int()
        link = graphene.String()
        author = graphene.String()

    episode = graphene.Field(lambda: EpisodeNode)

    @require_auth
    def mutate(self, info, **kwargs):
        coverImg = kwargs.get('cover_img')

        # insert db
        new_episode = Episode(
            u_id=kwargs.get('user').id,
            p_id=kwargs.get('p_id'),
            title=kwargs.get('title'),
            description=kwargs.get('description'),
            status=kwargs.get('status'),
            type=kwargs.get('type'),
            order_no=kwargs.get('order_no'),
            season_no=kwargs.get('season_no'),
            link=kwargs.get('link'),
            author=kwargs.get('author')
        )
        if coverImg != None:
            uploadedPath = filedrive.save('episode', coverImg)
            new_episode.cover = uploadedPath

        save_changes(new_episode)

        return CreateEpisode(episode=new_episode)


class UpdateEpisode(graphene.Mutation):
    class Arguments:
        episode_id = graphene.Int(required=True)
        cover_img = Upload()
        title = graphene.String(required=True)
        description = graphene.String()
        status = graphene.Int(required=True)
        type = graphene.Int(required=True)
        order_no = graphene.Int()
        season_no = graphene.Int()
        link = graphene.String()
        author = graphene.String()

    episode = graphene.Field(lambda: EpisodeNode)

    @require_auth
    def mutate(self, info, **kwargs):
        myEpisode = Episode.query.filter_by(
            id=kwargs.get('episode_id')).first()
        if not myEpisode:
            raise Exception('Episode not found.')

        coverImg = kwargs.get('cover_img')
        if coverImg != None:
            uploadedPath = filedrive.save('episode', coverImg)

            # remove old file
            if myEpisode.cover != '':
                filedrive.delete('episode', myEpisode.cover)

            myEpisode.cover = uploadedPath

        # update db
        myEpisode.title = kwargs.get('title')
        myEpisode.description = kwargs.get('description')
        myEpisode.status = kwargs.get('status')
        myEpisode.type = kwargs.get('type')
        myEpisode.order_no = kwargs.get('order_no')
        myEpisode.season_no = kwargs.get('season_no')
        myEpisode.link = kwargs.get('link')
        myEpisode.author = kwargs.get('author')

        save_changes(myEpisode)

        return UpdateEpisode(episode=myEpisode)


class DeleteEpisode(graphene.Mutation):
    class Arguments:
        episode_id = graphene.Int(required=True)

    deleted = graphene.Boolean()

    @require_auth
    def mutate(self, info, **kwargs):
        myEpisode = Episode.query.filter_by(
            id=kwargs.get('episode_id')).first()
        if not myEpisode:
            raise Exception('Episode not found.')

        filedrive.delete('episode', myEpisode.cover)
        db_session.delete(myEpisode)
        db_session.commit()

        return DeleteEpisode(deleted=True)


def save_changes(data):
    db_session.add(data)
    db_session.commit()
