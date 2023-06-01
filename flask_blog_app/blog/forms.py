from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email


class SerieForm(FlaskForm):
    name = StringField('Name EN', validators=[DataRequired()])
    name_es = StringField('Name ES', validators=[DataRequired()])


class TagForm(FlaskForm):
    name = StringField('Tag name')


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[
        DataRequired(), Email(granular_message=True)])
    message = TextAreaField(label='Message',  validators=[DataRequired()])
