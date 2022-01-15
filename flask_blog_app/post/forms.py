from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField(_('Title'), validators=[DataRequired()])
    title_es = StringField(_('Title'), validators=[DataRequired()])
    content = TextAreaField(_('Content'), validators=[DataRequired()])
    content_es = TextAreaField(_('Content'), validators=[DataRequired()])
    file_content = FileField('Select file content')
