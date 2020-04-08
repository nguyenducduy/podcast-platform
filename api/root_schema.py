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

    group = graphene.Field(group_schema.GroupNode, id=graphene.Int())

    def resolve_group(self, info, **kwargs):
        return group_schema.GroupNode.get_query(info).get(kwargs.get('id'))

    permission = graphene.Field(
        permission_schema.PermissionNode, id=graphene.Int())

    def resolve_permission(self, info, **kwargs):
        return permission_schema.PermissionNode.get_query(info).get(kwargs.get('id'))

    user = graphene.Field(user_schema.UserNode, id=graphene.Int())

    def resolve_user(self, info, **kwargs):
        return user_schema.UserNode.get_query(info).get(kwargs.get('id'))

    filedrive = graphene.Field(
        filedrive_schema.FiledriveNode, id=graphene.Int())

    def resolve_filedrive(self, info, **kwargs):
        return filedrive_schema.FiledriveNode.get_query(info).get(kwargs.get('id'))

    podcast = graphene.Field(podcast_schema.PodcastNode, id=graphene.Int())

    def resolve_podcast(self, info, **kwargs):
        return podcast_schema.PodcastNode.get_query(info).get(kwargs.get('id'))

    episode = graphene.Field(episode_schema.EpisodeNode, id=graphene.Int())

    def resolve_episode(self, info, **kwargs):
        return episode_schema.EpisodeNode.get_query(info).get(kwargs.get('id'))


class Mutation(graphene.ObjectType):
    # user
    create_user = user_schema.CreateUser.Field()
    update_user = user_schema.UpdateUser.Field()
    delete_user = user_schema.DeleteUser.Field()
    login_user = user_schema.LoginUser.Field()
    logout_user = user_schema.LogoutUser.Field()
    change_password = user_schema.ChangePassword.Field()
    # group
    create_group = group_schema.CreateGroup.Field()
    update_group = group_schema.UpdateGroup.Field()
    delete_group = group_schema.DeleteGroup.Field()
    grant_permission = group_schema.GrantPermission.Field()
    # permission
    create_permission = permission_schema.CreatePermission.Field()
    update_permission = permission_schema.UpdatePermission.Field()
    delete_permission = permission_schema.DeletePermission.Field()
    # filedrive
    filedrive_upload = filedrive_schema.FiledriveUpload.Field()
    record_upload = filedrive_schema.RecordUpload.Field()
    common_upload = filedrive_schema.CommonUpload.Field()
    filedrive_edit_field = filedrive_schema.FiledriveEditField.Field()
    delete_filedrive = filedrive_schema.DeleteFiledrive.Field()
    delete_user_filedrive = filedrive_schema.DeleteUserFiledrive.Field()
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
