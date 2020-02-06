from model.user import User
from helper.decorator import require_auth
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from model.revision import Revision
from model.filedrive import Filedrive
from datetime import datetime
from helper import filedrive
import graphene
from db import db_session
import os
import subprocess
from config import upload_dir
import json
import librosa
from shutil import copyfile
import random


def r(): return random.randint(0, 255)


def g(): return random.randint(0, 255)


def b(): return random.randint(0, 255)

# DEFINE NODE


class RevisionNode(SQLAlchemyObjectType):
    """Revision node."""

    class Meta:
        model = Revision


# FILTER
class RevisionFilter(FilterSet):
    class Meta:
        model = Revision
        fields = {
            'id': [...],
            'session_id': [...],
            'version': [...]
        }

    is_owner = graphene.Boolean()

    @staticmethod
    def is_owner_filter(info, query, value):
        if value:
            auth_resp = User.decode_auth_token(info.context)
            return Revision.u_id == User.query.filter_by(id=auth_resp).first().id


# QUERY
class RevisionConnection(graphene.relay.Connection):
    class Meta:
        node = RevisionNode

    total_count = graphene.NonNull(graphene.Int)

    def resolve_total_count(self, info, **kwargs):
        return self.length


# MUTATION
class CreateRevision(graphene.Mutation):
    class Arguments:
        session_id = graphene.String(required=True)
        content = graphene.String(required=True)

    revision = graphene.Field(lambda: RevisionNode)
    tmp_file = graphene.String()

    @require_auth
    def mutate(self, info, **kwargs):
        sessionId = kwargs.get('session_id')
        uId = kwargs.get('user').id
        content = kwargs.get('content')
        defaultOverlapDuration = 2
        segment = json.loads(content)

        # check file exist
        myFile = Filedrive.query.filter_by(id=segment['fdId']).first()
        if not myFile:
            raise Exception("File not found.")

        # get last revision
        myLastRevision = Revision.query.filter(
            Revision.u_id == uId,
            Revision.session_id == sessionId
        ).order_by(Revision.version.desc()).first()

        if segment['action'] == 'crossfade':
            if not myLastRevision:
                # first revision
                new_revision = Revision(
                    u_id=uId,
                    session_id=sessionId,
                    version=1,
                    content=json.dumps([
                        {
                            "fdId": myFile.id,
                            "start": 0,
                            "end": myFile.duration,
                            "color": 'rgba(%s, %s, %s, 0.1)' % (r(), g(), b()),
                            "label": myFile.name,
                            "durationOverlap": defaultOverlapDuration,
                            "type": "crossfade"
                        }
                    ]),
                    mixed_id=myFile.id,
                    files_used=myFile.id
                )
                save_changes(new_revision)

                return CreateRevision(revision=new_revision)
            else:
                myLastRevisionFile = Filedrive.query.filter_by(
                    id=myLastRevision.mixed_id).first()
                if not myLastRevisionFile:
                    raise Exception("Last revision file not found.")

                # run ffmpeg command then save to revision table.
                currentEpDir = os.path.join(
                    upload_dir, ("audio/%s/%s" % (uId, sessionId)))
                os.makedirs(currentEpDir, exist_ok=True)
                mixedFilePath = os.path.join(
                    currentEpDir, ("%sx%s.mp3" % (myLastRevisionFile.id, myFile.id)))

                out = subprocess.Popen([
                    'ffmpeg',
                    '-y',
                    '-i',
                    filedrive.getRelativePath(
                        'audio', myLastRevisionFile.path),
                    '-i',
                    filedrive.getRelativePath('audio', myFile.path),
                    '-filter_complex',
                    '[0][1]acrossfade=d=2:o=1:c1=tri:c2=tri',
                    '-ar',
                    '44100',
                    '-ac',
                    '2',
                    '-b:a',
                    '128k',
                    '-acodec',
                    'libmp3lame',
                    '-f',
                    'mp3',
                    mixedFilePath
                ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)

                # waiting for command run complete
                stdout, stderr = out.communicate()
                print(stdout)

                # success command
                if os.path.isfile(mixedFilePath):
                    size = os.stat(mixedFilePath).st_size
                    duration = librosa.get_duration(filename=mixedFilePath)

                    # create mixed file
                    new_filedrive = Filedrive(
                        u_id=uId,
                        name=("%sx%s.mp3" %
                              (myLastRevisionFile.id, myFile.id)),
                        path=("%s/%s/%sx%s.mp3" % (uId, sessionId,
                                                   myLastRevisionFile.id, myFile.id)),
                        size=size,
                        duration=duration,
                        type=Filedrive.TYPE_CROSSFADED,
                        is_tmp=Filedrive.IS_NOT_TMP,
                        is_common=Filedrive.IS_NOT_COMMON
                    )
                    save_changes(new_filedrive)

                    # create revision
                    revisionContent = json.loads(myLastRevision.content)

                    revisionContent.append({
                        "fdId": myFile.id,
                        "start": myLastRevisionFile.duration,
                        "end": duration,
                        "color": 'rgba(%s, %s, %s, 0.1)' % (r(), g(), b()),
                        "label": myFile.name,
                        "durationOverlap": defaultOverlapDuration,
                        "type": "crossfade"
                    })

                    new_revision = Revision(
                        session_id=sessionId,
                        u_id=uId,
                        version=myLastRevision.version + 1,
                        content=json.dumps(revisionContent),
                        mixed_id=new_filedrive.id,
                        files_used=("%s,%s" %
                                    (myLastRevision.mixed_id, myFile.id))
                    )
                    save_changes(new_revision)

                return CreateRevision(revision=new_revision)
        elif segment['action'] == 'mix':
            myLastRevisionFile = Filedrive.query.filter_by(
                id=myLastRevision.mixed_id).first()
            if not myLastRevisionFile:
                raise Exception("Last revision file not found.")

            # run ffmpeg command then save to revision table.
            currentEpDir = os.path.join(
                upload_dir, ("audio/%s/%s" % (uId, sessionId)))
            os.makedirs(currentEpDir, exist_ok=True)
            mixedFilePath = os.path.join(
                currentEpDir, ("%sx%s.mp3" % (myLastRevisionFile.id, myFile.id)))

            out = subprocess.Popen([
                'ffmpeg',
                '-y',
                '-i',
                filedrive.getRelativePath('audio', myLastRevisionFile.path),
                '-i',
                filedrive.getRelativePath('audio', myFile.path),
                '-filter_complex',
                ("[0:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[a0];[1:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[a1];[a1]atrim=%s:%s[a1trim];[a1trim]adelay=%s|%s[aud1];[aud1]amix=1,apad[a];[a0][a]amerge[a]" % (
                    segment['duration'][0], segment['duration'][1], int(segment['start'])*1000, int(segment['start'])*1000)),
                '-map',
                '[a]',
                '-ar',
                '44100',
                '-ac',
                '2',
                '-b:a',
                '128k',
                '-acodec',
                'libmp3lame',
                '-f',
                'mp3',
                mixedFilePath
            ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

            # waiting for command run complete
            stdout, stderr = out.communicate()
            print(stdout)

            # success command
            if os.path.isfile(mixedFilePath):
                size = os.stat(mixedFilePath).st_size
                duration = librosa.get_duration(filename=mixedFilePath)

                if segment['type'] == 'try':
                    is_tmp = Filedrive.IS_TMP
                else:
                    is_tmp = Filedrive.IS_NOT_TMP

                # create mixed file
                new_filedrive = Filedrive(
                    u_id=uId,
                    name=("%sx%s.mp3" % (myLastRevisionFile.id, myFile.id)),
                    path=("%s/%s/%sx%s.mp3" %
                          (uId, sessionId, myLastRevisionFile.id, myFile.id)),
                    size=size,
                    duration=duration,
                    type=Filedrive.TYPE_MIXED,
                    is_tmp=is_tmp,
                    is_common=Filedrive.IS_NOT_COMMON
                )
                save_changes(new_filedrive)

                # fake return old revision if type = try
                if segment['type'] == 'try':
                    return CreateRevision(tmp_file=new_filedrive.path)

                # create revision
                revisionContent = json.loads(myLastRevision.content)

                revisionContent.append({
                    "fdId": myFile.id,
                    "start": segment['start'],
                    "end": int(segment['start']) + (int(segment['duration'][1]) - int(segment['duration'][0])),
                    "color": 'rgba(%s, %s, %s, 0.1)' % (r(), g(), b()),
                    "label": myFile.name,
                    "durationRange": segment['duration'],
                    "type": "mix"
                })

                new_revision = Revision(
                    session_id=sessionId,
                    u_id=uId,
                    version=myLastRevision.version + 1,
                    content=json.dumps(revisionContent),
                    mixed_id=new_filedrive.id,
                    files_used=("%s,%s" % (myLastRevision.mixed_id, myFile.id))
                )
                save_changes(new_revision)

            return CreateRevision(revision=new_revision)


class DetachRevision(graphene.Mutation):
    class Arguments:
        session_id = graphene.String(required=True)
        version = graphene.Int(required=True)
        detachIndex = graphene.Int(required=True)

    revision = graphene.Field(lambda: RevisionNode)

    @require_auth
    def mutate(self, info, **kwargs):
        sessionId = kwargs.get('session_id')
        version = kwargs.get('version')
        uId = kwargs.get('user').id
        detachIndex = kwargs.get('detachIndex')

        # get last revision
        myLastRevision = Revision.query.filter(
            Revision.session_id == sessionId,
            Revision.u_id == uId,
            Revision.version == version,
        ).order_by(Revision.version.desc()).first()

        revisionContent = json.loads(myLastRevision.content)
        detachSegment = [index for index, segment in enumerate(
            revisionContent) if index == detachIndex]
        del revisionContent[detachSegment[0]]
        cmd, fileName = buildCmd(revisionContent, uId, sessionId)

        # print(cmd.split(" "))
        out = subprocess.Popen(
            cmd.split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        # waiting for command run complete
        stdout, stderr = out.communicate()
        print(stdout)

        currentEpDir = os.path.join(
            upload_dir, ("audio/%s/%s" % (uId, sessionId)))
        os.makedirs(currentEpDir, exist_ok=True)
        mixedFilePath = os.path.join(currentEpDir, ("%s.mp3" % fileName))

        # success command
        if os.path.isfile(mixedFilePath):
            size = os.stat(mixedFilePath).st_size
            duration = librosa.get_duration(filename=mixedFilePath)

            # create mixed file
            new_filedrive = Filedrive(
                u_id=uId,
                name=("%s.mp3" % fileName),
                path=("%s/%s/%s.mp3" % (uId, sessionId, fileName)),
                size=size,
                duration=duration,
                type=Filedrive.TYPE_MIXED,
                is_tmp=Filedrive.IS_NOT_TMP,
                is_common=Filedrive.IS_NOT_COMMON
            )
            save_changes(new_filedrive)

            new_revision = Revision(
                session_id=sessionId,
                u_id=uId,
                version=myLastRevision.version + 1,
                content=json.dumps(revisionContent),
                mixed_id=new_filedrive.id,
                files_used=("%s" % myLastRevision.mixed_id)
            )
            save_changes(new_revision)

        return CreateRevision(revision=new_revision)


def buildCmd(data, uId, sessionId):
    inputTrackString = ''
    filterComplexString = ''
    mapString = ''
    crossfadeString = ''
    mixString = ''
    crossfadeList = []
    mixList = []
    lastCrossfadeIdx = 0
    mixItemsString = ''

    fileName = ''
    for idx, rev in enumerate(data):
        myFile = Filedrive.query.filter_by(id=rev['fdId']).first()
        if not myFile:
            raise Exception("File not found.")

        fileName += str(myFile.id) + 'x'

        inputTrackString += "-i %s " % os.path.join(
            upload_dir, filedrive.getRelativePath('audio', myFile.path))

        if rev['type'] == 'crossfade':
            lastCrossfadeIdx = idx
            crossfadeList.append(rev)
            crossfadeString += "[%s]acrossfade=d=2:c1=tri:c2=tri[aud%s]%s%s" % (str(idx), str(idx), ';' if len(
                crossfadeList) < len(data) else '', '[aud' + str(idx) + ']' if len(crossfadeList) < len(data) else '')
        if rev['type'] == 'mix':
            mixList.append(rev)
            mixString += "[%s]atrim=%s:%s[%strim];[%strim]adelay=%s|%s[aud%s];" % (str(
                idx), rev['durationRange'][0], rev['durationRange'][1], str(idx), str(idx), rev['start'], rev['start'], str(idx))
            mixItemsString += "[aud%s]" % idx

    if len(mixList) > 0:
        crossfadeString = crossfadeString[:-len("[aud%s]" % lastCrossfadeIdx)]
        mixString += mixItemsString
        mixString += "amix=%s,apad[mixed];" % len(mixList)
        if len(crossfadeList) > 0:
            mixString += "[aud%s][mixed]amerge[mixed]" % lastCrossfadeIdx
            mixString += ' -map [mixed]'
    else:
        if len(crossfadeList) > len(data):
            crossfadeString = crossfadeString[:-1]
        crossfadeString += "\" -map [aud%s]" % lastCrossfadeIdx

    currentEpDir = os.path.join(upload_dir, ("audio/%s/%s" % (uId, sessionId)))
    os.makedirs(currentEpDir, exist_ok=True)
    mixedFilePath = os.path.join(currentEpDir, ("%s.mp3" % fileName))
    # print(crossfadeString)
    # print(mixString)

    filterComplexString += crossfadeString + mixString
    cmd = 'ffmpeg -y %s -filter_complex %s ' % (
        inputTrackString.rstrip(), filterComplexString)
    cmd += "-ar 44100 -ac 2 -b:a 128k -acodec libmp3lame -f mp3 " + mixedFilePath
    # print(cmd)
    return cmd, fileName


def save_changes(data):
    db_session.add(data)
    db_session.commit()
