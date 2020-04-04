import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from helpers import filedrive
from models.episode import Episode
from models.filedrive import Filedrive
from db import db
from graphene_file_upload.scalars import Upload
from depot.manager import DepotManager
import os


class EpisodeNode(SQLAlchemyObjectType):
    class Meta:
        model = Episode

    cover = graphene.String()

    def resolve_cover(self, info):
        if self.cover != None:
            return filedrive.getPath('episode', self.cover)
        else:
            return ''


class EpisodeFilter(FilterSet):
    class Meta:
        model = Episode
        fields = {'id': [...], 'p_id': [...], 'status': [...]}


class EpisodeConnection(graphene.relay.Connection):
    class Meta:
        node = EpisodeNode

    total_count = graphene.NonNull(graphene.Int)

    def resolve_total_count(self, info, **kwargs):
        return self.length


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
        fd_id = graphene.Int()

    episode = graphene.Field(lambda: EpisodeNode)

    def mutate(self, info, **kwargs):
        coverImg = kwargs.get('cover_img')

        # insert db
        myEpisode = Episode(u_id=kwargs.get('user').id,
                            p_id=kwargs.get('p_id'),
                            title=kwargs.get('title'),
                            description=kwargs.get('description'),
                            status=kwargs.get('status'),
                            type=kwargs.get('type'),
                            order_no=kwargs.get('order_no'),
                            season_no=kwargs.get('season_no'),
                            link=kwargs.get('link'),
                            author=kwargs.get('author'),
                            fd_id=kwargs.get('fd_id'))
        if coverImg != None:
            uploadedPath = filedrive.save('episode', coverImg)
            myEpisode.cover = uploadedPath

        save(myEpisode)

        return CreateEpisode(episode=myEpisode)


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
        fd_id = graphene.Int()

    episode = graphene.Field(lambda: EpisodeNode)

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

        if kwargs.get('status') == Episode.STATUS_PUBLISH:
            if kwargs.get('fd_id') != None:
                myFiledrive = Filedrive.query.filter_by(
                    id=kwargs.get('fd_id')).first()
                if myFiledrive:
                    myFiledrivePath = filedrive.getRelativePath(
                        'audio', myFiledrive.path)
                    depot = DepotManager.get()
                    fileid = depot.create(open(myFiledrivePath, 'rb'))
                    myFiledrive.gcs_id = fileid

        # update db
        myEpisode.title = kwargs.get('title')
        myEpisode.description = kwargs.get('description')
        myEpisode.status = kwargs.get('status')
        myEpisode.type = kwargs.get('type')
        myEpisode.order_no = kwargs.get('order_no')
        myEpisode.season_no = kwargs.get('season_no')
        myEpisode.link = kwargs.get('link')
        myEpisode.author = kwargs.get('author')
        myEpisode.fd_id = kwargs.get('fd_id')

        save(myEpisode)

        return UpdateEpisode(episode=myEpisode)


class DeleteEpisode(graphene.Mutation):
    class Arguments:
        episode_id = graphene.Int(required=True)

    deleted = graphene.Boolean()

    def mutate(self, info, **kwargs):
        myEpisode = Episode.query.filter_by(
            id=kwargs.get('episode_id')).first()
        if not myEpisode:
            raise Exception('Episode not found.')

        filedrive.delete('episode', myEpisode.cover)
        delete(myEpisode)

        return DeleteEpisode(deleted=True)


def save(data):
    db.session.add(data)
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()
