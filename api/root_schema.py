import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy_filter import FilterableConnectionField
from graphene_file_upload.scalars import Upload

# MODELS
from models.user import User
from models.group import Group
from models.filedrive import Filedrive
from models.podcast import Podcast
from models.episode import Episode

# SCHEMAS
import schemas.user as user_schema
import schemas.group as group_schema
import schemas.filedrive as filedrive_schema
import schemas.revision as revision_schema
import schemas.podcast as podcast_schema
import schemas.episode as episode_schema
import schemas.permission as permission_schema


class Query(graphene.ObjectType):
    node = graphene.Node.Field()

    userList = FilterableConnectionField(
        user_schema.UserConnection, filters=user_schema.UserFilter())
    groupList = FilterableConnectionField(
        group_schema.GroupConnection, filters=group_schema.GroupFilter())
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
    permissionList = FilterableConnectionField(
        permission_schema.PermissionConnection, filters=permission_schema.PermissionFilter())

    filedrive = graphene.Field(
        filedrive_schema.FiledriveNode, id=graphene.Int())

    def resolve_filedrive(self, info, **kwargs):
        query = filedrive_schema.FiledriveNode.get_query(info)
        return query.filter(Filedrive.id == kwargs.get('id')).first()

    podcast = graphene.Field(podcast_schema.PodcastNode, id=graphene.Int())

    def resolve_podcast(self, info, **kwargs):
        query = podcast_schema.PodcastNode.get_query(info)
        return query.filter(Podcast.id == kwargs.get('id')).first()

    episode = graphene.Field(episode_schema.EpisodeNode, id=graphene.Int())

    def resolve_episode(self, info, **kwargs):
        query = episode_schema.EpisodeNode.get_query(info)
        return query.filter(Episode.id == kwargs.get('id')).first()


class Mutation(graphene.ObjectType):
    create_user = user_schema.CreateUser.Field()
    login_user = user_schema.LoginUser.Field()
    # avatar_upload = user_schema.AvatarUpload.Field()
    # filedrive
    filedrive_upload = filedrive_schema.FiledriveUpload.Field()
    record_upload = filedrive_schema.RecordUpload.Field()
    common_upload = filedrive_schema.CommonUpload.Field()
    filedrive_edit_field = filedrive_schema.FiledriveEditField.Field()
    delete_filedrive = filedrive_schema.DeleteFiledrive.Field()
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


schema = graphene.Schema(query=Query, mutation=Mutation, types=[Upload])
