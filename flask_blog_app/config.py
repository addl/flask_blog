import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://pguser:pguser@127.0.0.1:5432/flask_blog'
    TWITTER_CLIENT_ID = "EHfW4CbwNahoyK"
    TWITTER_CLIENT_SECRET = "Dh2q17Pntva1g0BwlYKyW7e"
    UPLOAD_FOLDER = 'C:/Users/andry.diaz/Documents/lion/my_refactor/tmp/posts'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'andrydaniel88@gmail.com'
    MAIL_PASSWORD = 'secret'
    MAIL_ADMIN = 'elion0075@yahoo.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


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
