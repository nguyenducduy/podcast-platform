from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy_filter import FilterableConnectionField
from graphql import GraphQLError
from helper.decorator import require_auth
from graphene_file_upload.scalars import Upload
from model.filedrive import Filedrive
from model.user import User
from model.podcast import Podcast
from model.episode import Episode
import graphene
import schema.user as user_schema
import schema.filedrive as filedrive_schema
import schema.revision as revision_schema
import schema.podcast as podcast_schema
import schema.episode as episode_schema


class Viewer (graphene.ObjectType):
    userList = FilterableConnectionField(
        user_schema.UserConnection, filters=user_schema.UserFilter())
    filedriveList = FilterableConnectionField(
        filedrive_schema.FiledriveConnection, filters=filedrive_schema.FiledriveFilter())
    revisionList = FilterableConnectionField(
        revision_schema.RevisionConnection, filters=revision_schema.RevisionFilter())
    historyList = FilterableConnectionField(
        revision_schema.RevisionConnection, filters=revision_schema.RevisionFilter())
    podcastList = FilterableConnectionField(
        podcast_schema.PodcastConnection, filters=podcast_schema.PodcastFilter())
    episodeList = FilterableConnectionField(
        episode_schema.EpisodeConnection, filters=episode_schema.EpisodeFilter())

    filedrive = graphene.Field(
        filedrive_schema.FiledriveNode, id=graphene.Int())

    def resolve_filedrive(self, info, id):
        query = filedrive_schema.FiledriveNode.get_query(info)
        return query.filter(Filedrive.id == id).first()

    podcast = graphene.Field(podcast_schema.PodcastNode, id=graphene.Int())

    def resolve_podcast(self, info, id):
        query = podcast_schema.PodcastNode.get_query(info)
        return query.filter(Podcast.id == id).first()

    episode = graphene.Field(episode_schema.EpisodeNode, id=graphene.Int())

    def resolve_episode(self, info, id):
        query = episode_schema.EpisodeNode.get_query(info)
        return query.filter(Episode.id == id).first()


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    viewer = graphene.Field(Viewer)

    @staticmethod
    def resolve_viewer(self, info):
        auth_resp = User.decode_auth_token(info.context)

        if not isinstance(auth_resp, str):
            return Viewer()
        raise GraphQLError(auth_resp)


class Mutation(graphene.ObjectType):
    # user
    signup_user = user_schema.SignupUser.Field()
    login_user = user_schema.LoginUser.Field()
    create_user = user_schema.CreateUser.Field()
    avatar_upload = user_schema.AvatarUpload.Field()
    # filedrive
    filedrive_upload = filedrive_schema.FiledriveUpload.Field()
    record_upload = filedrive_schema.RecordUpload.Field()
    # revision
    create_revision = revision_schema.CreateRevision.Field()
    detach_revision = revision_schema.DetachRevision.Field()
    change_file_order_in_revision = revision_schema.ChangeFileOrderInRevision.Field()
    # podcast
    create_podcast = podcast_schema.CreatePodcast.Field()
    update_podcast = podcast_schema.UpdatePodcast.Field()
    delete_podcast = podcast_schema.DeletePodcast.Field()
    import_from_apple = podcast_schema.ImportFromApple.Field()
    # episode
    create_episode = episode_schema.CreateEpisode.Field()
    update_episode = episode_schema.UpdateEpisode.Field()
    delete_episode = episode_schema.DeleteEpisode.Field()


# schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription, types=[Upload])
schema = graphene.Schema(query=Query, mutation=Mutation, types=[Upload])
