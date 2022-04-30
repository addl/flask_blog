from flask_blog_app import db


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())


class Subscriptor(db.Model):
    __tablename__ = 'subscriptor'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
