from flask_wtf import FlaskForm
from wtforms import StringField


class TagForm(FlaskForm):
    name = StringField('Tag name')
