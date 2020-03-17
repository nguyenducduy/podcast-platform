import os
import sqlalchemy

basedir = os.path.abspath(os.path.dirname(__file__))
upload_dir = os.path.join(basedir, 'storage')

MAX_CONTENT_LENGTH = 128 * 1024 * 1024  # 128Mb
ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'jpg', 'jpeg', 'png'])


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/mk'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Missmilano88@35.198.216.121/podcast'
    GOOGLE_CLOUD_STORAGE_ACCESS_KEY = 'GOOGJ7KEGKA5C2M6QEKBWTCD'
    GOOGLE_CLOUD_STORAGE_SECRET_KEY = 'HH6BbrEH+7hdR1UTYcSczZtuFgYI+lC7POteiTCD'
    GOOGLE_CLOUD_STORAGE_BUCKET = 'podcast_audio_dev'


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
