import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from helpers import filedrive
from models.filedrive import Filedrive
from models.user import User
from werkzeug.utils import secure_filename
from db import db
from helpers.token import decode_auth_token
from graphene_file_upload.scalars import Upload
from gtypes import CommonDictType
import os
import librosa
import pendulum


class FiledriveNode(SQLAlchemyObjectType):
    class Meta:
        model = Filedrive

    type = graphene.Field(CommonDictType)
    is_common = graphene.Field(CommonDictType)
    path = graphene.String()

    def resolve_type(self, info):
        return self.getType()

    def resolve_is_common(self, info):
        return self.getIsCommon()

    def resolve_path(self, info):
        return filedrive.getPath('audio', self.path)


class FiledriveFilter(FilterSet):
    class Meta:
        model = Filedrive
        fields = {
            'id': [...],
            'type': [...],
            'is_tmp': [...],
            'is_common': [...]
        }

    is_owner = graphene.Boolean()

    @staticmethod
    def is_owner_filter(info, query, value):
        if value:
            auth_resp = decode_auth_token(
                info.context.headers.get('Authorization'))
            return Filedrive.u_id == User.query.filter_by(
                id=auth_resp).first().id


class FiledriveConnection(graphene.Connection):
    class Meta:
        node = FiledriveNode

    total_count = graphene.NonNull(graphene.Int)
    common_list = graphene.List(CommonDictType)

    def resolve_total_count(self, info, **kwargs):
        return self.length

    def resolve_common_list(self, info, **kwargs):
        return Filedrive.getCommonList()


class FiledriveEditField(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        data_index = graphene.String(required=True)
        value = graphene.String(required=True)

    updated = graphene.Boolean()

    def mutate(self, info, **kwargs):
        myFiledrive = Filedrive.query.filter_by(id=kwargs.get('id')).first()
        if not myFiledrive:
            raise Exception('Filedrive not found.')

        setattr(myFiledrive, kwargs.get('data_index'), kwargs.get('value'))
        save(myFiledrive)

        return FiledriveEditField(updated=True)


class FiledriveUpload(graphene.Mutation):
    class Arguments:
        upload_file = Upload()

    path = graphene.String()

    def mutate(self, info, **kwargs):
        uploadFile = kwargs.get('upload_file')
        uploadedPath = filedrive.save('audio', uploadFile)
        filePath = filedrive.getRelativePath('audio', uploadedPath)

        name = secure_filename(uploadFile.filename.rsplit('.', 1)[0].lower())
        ext = uploadFile.filename.rsplit('.', 1)[1].lower()

        if os.path.isfile(filePath):
            # get more file info
            size = os.stat(filePath).st_size
            duration = librosa.get_duration(filename=filePath)

            # store to db
            myFiledrive = Filedrive(u_id=kwargs.get('user').id,
                                    name=name,
                                    ext=ext,
                                    size=size,
                                    duration=duration,
                                    path=uploadedPath,
                                    type=Filedrive.TYPE_FX,
                                    is_tmp=Filedrive.IS_NOT_TMP,
                                    is_common=Filedrive.IS_NOT_COMMON)
            save(myFiledrive)

            return FiledriveUpload(path=myFiledrive.path)

        raise Exception('Upload failed!')


class RecordUpload(graphene.Mutation):
    class Arguments:
        record_file = Upload()

    path = graphene.String()

    def mutate(self, info, **kwargs):
        uploadFile = kwargs.get('record_file')
        uploadedPath = filedrive.save('audio', uploadFile, True)
        filePath = filedrive.getRelativePath('audio', uploadedPath)

        name = secure_filename(uploadFile.filename.rsplit('.', 1)[0].lower())
        ext = uploadFile.filename.rsplit('.', 1)[1].lower()

        if os.path.isfile(filePath):
            # get more file info
            size = os.stat(filePath).st_size
            duration = librosa.get_duration(filename=filePath)

            # store to db
            myFiledrive = Filedrive(u_id=kwargs.get('user').id,
                                    name=name,
                                    ext='mp3',
                                    size=size,
                                    duration=duration,
                                    path=uploadedPath,
                                    type=Filedrive.TYPE_RECORD,
                                    is_tmp=Filedrive.IS_NOT_TMP,
                                    is_common=Filedrive.IS_NOT_COMMON)
            save(myFiledrive)

            return FiledriveUpload(path=myFiledrive.path)

        raise Exception('Upload failed!')


class CommonUpload(graphene.Mutation):
    class Arguments:
        upload_file = Upload()

    path = graphene.String()

    def mutate(self, info, **kwargs):
        uploadFile = kwargs.get('upload_file')
        uploadedPath = filedrive.save('audio', uploadFile)
        filePath = filedrive.getRelativePath('audio', uploadedPath)

        name = secure_filename(uploadFile.filename.rsplit('.', 1)[0].lower())
        ext = uploadFile.filename.rsplit('.', 1)[1].lower()

        if os.path.isfile(filePath):
            # get more file info
            size = os.stat(filePath).st_size
            duration = librosa.get_duration(filename=filePath)

            # store to db
            myFiledrive = Filedrive(u_id=kwargs.get('user').id,
                                    name=name,
                                    ext=ext,
                                    size=size,
                                    duration=duration,
                                    path=uploadedPath,
                                    type=Filedrive.TYPE_FX,
                                    is_tmp=Filedrive.IS_NOT_TMP,
                                    is_common=Filedrive.IS_COMMON)
            save(myFiledrive)

            return CommonUpload(path=myFiledrive.path)

        raise Exception('Upload failed!')


class DeleteFiledrive(graphene.Mutation):
    class Arguments:
        filedrive_id = graphene.Int(required=True)

    deleted = graphene.Boolean()

    def mutate(self, info, **kwargs):
        myFiledrive = Filedrive.query.filter_by(
            id=kwargs.get('filedrive_id')).first()
        if not myFiledrive:
            raise Exception('Filedrive not found.')

        filedrive.delete('audio', myFiledrive.path)
        delete(myFiledrive)

        return DeleteFiledrive(deleted=True)


def save(data):
    db.session.add(data)
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()
