from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterSet
from graphql import GraphQLError
from helper.decorator import require_auth
from helper import filedrive
from model.podcast import Podcast
from model.episode import Episode
from model.filedrive import Filedrive
from db import db_session
from graphene_file_upload.scalars import Upload
from config import upload_dir
from werkzeug.utils import secure_filename
from datetime import datetime
import graphene
import os
import urllib.request
import json
from xml.dom import minidom
import librosa


# DEFINE NODE
class PodcastNode(SQLAlchemyObjectType):
    class Meta:
        model = Podcast

    cover = graphene.String()

    def resolve_cover(self, info):
        return filedrive.getPath('podcast', self.cover)

# FILTER


class PodcastFilter(FilterSet):
    class Meta:
        model = Podcast
        fields = {
            'id': [...],
            'status': [...]
        }


# QUERY
class PodcastConnection(graphene.relay.Connection):
    class Meta:
        node = PodcastNode
    total_count = graphene.NonNull(graphene.Int)

    def resolve_total_count(self, info, **kwargs):
        return self.length


# MUTATION
class CreatePodcast(graphene.Mutation):
    class Arguments:
        cover_img = Upload()
        title = graphene.String(required=True)
        description = graphene.String()
        status = graphene.Int(required=True)
        contact_email = graphene.String()
        website_url = graphene.String()
        copyright = graphene.String()

    podcast = graphene.Field(lambda: PodcastNode)

    @require_auth
    def mutate(self, info, **kwargs):
        coverImg = kwargs.get('cover_img')
        uploadedPath = filedrive.save('podcast', coverImg)

        # insert db
        new_podcast = Podcast(
            u_id=kwargs.get('user').id,
            title=kwargs.get('title'),
            description=kwargs.get('description'),
            status=kwargs.get('status'),
            contact_email=kwargs.get('contact_email'),
            website_url=kwargs.get('website_url'),
            copyright=kwargs.get('copyright'),
            cover=uploadedPath,
            language=Podcast.LANGUAGE_VI
        )
        save_changes(new_podcast)

        return CreatePodcast(podcast=new_podcast)


class UpdatePodcast(graphene.Mutation):
    class Arguments:
        podcast_id = graphene.Int(required=True)
        cover_img = Upload()
        title = graphene.String(required=True)
        description = graphene.String()
        status = graphene.Int(required=True)
        contact_email = graphene.String()
        website_url = graphene.String()
        copyright = graphene.String()

    podcast = graphene.Field(lambda: PodcastNode)

    @require_auth
    def mutate(self, info, **kwargs):
        myPodcast = Podcast.query.filter_by(
            id=kwargs.get('podcast_id')).first()
        if not myPodcast:
            raise Exception('Podcast not found.')

        coverImg = kwargs.get('cover_img')
        if coverImg != None:
            uploadedPath = filedrive.save('podcast', coverImg)
            # remove old file
            filedrive.delete('podcast', myPodcast.cover)
            myPodcast.cover = uploadedPath

        # update db
        myPodcast.title = kwargs.get('title')
        myPodcast.description = kwargs.get('description')
        myPodcast.status = kwargs.get('status')
        myPodcast.contact_email = kwargs.get('contact_email')
        myPodcast.website_url = kwargs.get('website_url')
        myPodcast.copyright = kwargs.get('copyright')

        save_changes(myPodcast)

        return UpdatePodcast(podcast=myPodcast)


class DeletePodcast(graphene.Mutation):
    class Arguments:
        podcast_id = graphene.Int(required=True)

    deleted = graphene.Boolean()

    @require_auth
    def mutate(self, info, **kwargs):
        myPodcast = Podcast.query.filter_by(
            id=kwargs.get('podcast_id')).first()
        if not myPodcast:
            raise Exception('Podcast not found.')

        filedrive.delete('podcast', myPodcast.cover)
        db_session.delete(myPodcast)
        db_session.commit()

        return DeletePodcast(deleted=True)


class ImportFromApple(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    imported = graphene.Boolean()

    @require_auth
    def mutate(self, info, **kwargs):
        appleId = kwargs.get('id')
        req = urllib.request.Request(
            "https://itunes.apple.com/lookup?id=%s&entity=podcast" % appleId)

        try:
            # get xml link
            with urllib.request.urlopen(req) as response:
                content = json.loads(response.read())
                appleRssLink = content['results'][0]['feedUrl']

                req = urllib.request.Request(appleRssLink)
                try:
                    # get xml content
                    with urllib.request.urlopen(req) as response:
                        content = response.read().decode('utf-8')

                        new_podcast = Podcast.query.filter_by(
                            apple_rss_link=appleRssLink
                        ).first()

                        if new_podcast:
                            print(new_podcast.title)
                            doc = minidom.parse(filedrive.getRelativePath(
                                'rss', new_podcast.apple_rss_file))
                        else:
                            xmlFilePath = filedrive.saveToFile(
                                'rss',
                                appleRssLink,
                                'xml',
                                str(content).encode('utf-8)
                            )
                            doc = minidom.parse(
                                filedrive.getRelativePath('rss', xmlFilePath))

                            title = doc.getElementsByTagName(
                                'title')[0].encode("utf-8")
                            description = doc.getElementsByTagName('description')[
                                0].encode("utf-8")
                            language = doc.getElementsByTagName('language')[0]
                            website_url = doc.getElementsByTagName('link')[0]
                            if doc.getElementsByTagName('itunes:keywords').length > 0:
                                keywords = doc.getElementsByTagName('itunes:keywords')[
                                    0].firstChild.data.encode("utf-8")
                            else:
                                keywords = ''
                            image = doc.getElementsByTagName('itunes:image')[0]
                            author = doc.getElementsByTagName(
                                'itunes:author')[0].encode("utf-8")
                            category = doc.getElementsByTagName(
                                'itunes:category')[0]
                            coverFilePath = filedrive.downloadFromUrl(
                                'podcast', image.getAttribute('href'))

                            new_podcast = Podcast(
                                u_id=kwargs.get('user').id,
                                title=title.firstChild.data,
                                description=description.firstChild.data,
                                keywords=keywords,
                                status=Podcast.STATUS_DRAFT,
                                website_url=website_url.firstChild.data,
                                cover=coverFilePath,
                                apple_rss_link=appleRssLink,
                                apple_rss_file=xmlFilePath
                            )
                            if language.firstChild.data == 'en':
                                new_podcast.language = Podcast.LANGUAGE_EN
                            else:
                                new_podcast.language = Podcast.LANGUAGE_VI

                            save_changes(new_podcast)
                            print('Podcast: ' + new_podcast.title)

                        i = 0
                        episodes = doc.getElementsByTagName('item')
                        for episode in reversed(episodes):
                            i = i + 1
                            title = episode.getElementsByTagName(
                                'title')[0].encode("utf-8")
                            if episode.getElementsByTagName('description').length > 0:
                                description = episode.getElementsByTagName('description')[
                                    0].firstChild.data.encode("utf-8")
                            else:
                                description = ''

                            if episode.getElementsByTagName('link').length > 0:
                                link = episode.getElementsByTagName(
                                    'link')[0].firstChild.data
                            else:
                                link = ''

                            if episode.getElementsByTagName('itunes:image').length > 0:
                                image = episode.getElementsByTagName('itunes:image')[
                                    0]
                                coverFilePath = filedrive.downloadFromUrl(
                                    'episode', image.getAttribute('href'))
                            else:
                                coverFilePath = ''

                            audio = episode.getElementsByTagName('enclosure')[
                                0]

                            new_episode = Episode(
                                p_id=new_podcast.id,
                                u_id=kwargs.get('user').id,
                                title=title.firstChild.data,
                                description=description,
                                link=link,
                                order_no=i,
                                season_no=1,
                                cover=coverFilePath,
                                external_file_path=audio.getAttribute(
                                    'url').split('?')[0],
                                status=Episode.STATUS_DRAFT,
                                type=Episode.TYPE_FULL
                            )

                            save_changes(new_episode)
                            print('Episode: ' + new_episode.title)

                        return ImportFromApple(imported=True)

                except urllib.error.URLError as e:
                    print('get XML link fail')
                    raise GraphQLError(e.reason)

        except urllib.error.URLError as e:
            print('get RSS link fail')
            raise GraphQLError(e.reason)

        return null


def save_changes(data):
    db_session.add(data)
    db_session.commit()
