from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flask_blog_app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)
    picture = db.Column(db.String(512))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)
