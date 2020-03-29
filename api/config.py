import os
from dotenv import load_dotenv

dotenv_path = os.path.join('.env')
load_dotenv(dotenv_path)


class Config:
    """Base config vars."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    LANGUAGES = ['en', 'vi']
    GOOGLE_CLOUD_STORAGE_ACCESS_KEY = os.environ.get(
        'GOOGLE_CLOUD_STORAGE_ACCESS_KEY')
    GOOGLE_CLOUD_STORAGE_SECRET_KEY = os.environ.get(
        'GOOGLE_CLOUD_STORAGE_SECRET_KEY')
    GOOGLE_CLOUD_STORAGE_BUCKET = os.environ.get('GOOGLE_CLOUD_STORAGE_BUCKET')


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEVELOPMENT_SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'PRODUCTION_SQLALCHEMY_DATABASE_URI')
