from datetime import datetime

from flask_blog_app import db

from sqlalchemy_i18n import make_translatable, translation_base, Translatable


make_translatable(options={'locales': ['en', 'es']})


class Post(Translatable, db.Model):
    __tablename__ = 'post'

    __translatable__ = {'locales': ['en', 'es']}
    locale = 'en'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.title)


class PostTranslation(translation_base(Post)):
    __tablename__ = 'post_translation'
    title = db.Column(db.String())
    content = db.Column(db.String())
    human_url = db.Column(db.String(), unique=True, nullable=False)
