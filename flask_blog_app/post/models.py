from datetime import datetime

import sqlalchemy_utils
from flask_babel import get_locale

from flask_blog_app import db

from sqlalchemy_i18n import make_translatable, translation_base, Translatable

make_translatable(options={'locales': ['en', 'es']})


post_tags = db.Table('post_tag',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Post(Translatable, db.Model):
    __tablename__ = 'post'
    __translatable__ = {'locales': ['en', 'es']}
    locale = 'en'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship("Tag", secondary=post_tags, backref=db.backref('posts', lazy='dynamic'), lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.title)


class PostTranslation(translation_base(Post)):
    __tablename__ = 'post_translation'
    title = db.Column(db.String())
    content = db.Column(db.String())
    description = db.Column(db.String())
    human_url = db.Column(db.String(), unique=True, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.String())
