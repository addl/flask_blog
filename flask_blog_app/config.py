import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://pguser:pguser@127.0.0.1:5432/flask_blog'
    UPLOAD_FOLDER = 'C:/Users/JoanPablo/Documents/my_refactor/tmp/posts'
    TWITTER_CLIENT_ID = "EHfW4CbYluj6xOKLp1wNahoyK"
    TWITTER_CLIENT_SECRET = "Dh2q17PntvO8jIjn8HRAiAb8LnKqPKbeFA5CTa1g0BwlYKyW7e"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
