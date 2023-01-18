from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectMultipleField, TextAreaField, HiddenField, EmailField, SelectField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    post_id = HiddenField()
    title = StringField(_('Title EN'), validators=[DataRequired()])
    title_es = StringField('Title ES', validators=[DataRequired()])
    file_content = FileField('Select English MD file')
    file_content_es = FileField('Select Spanish MD file')
    description = TextAreaField('Description EN', validators=[Length(max=180)])
    description_es = TextAreaField('Description ES', validators=[Length(max=180)])
    tags = SelectMultipleField('Tags', coerce=int, validators=[DataRequired()])
    category = SelectField('Category', coerce=int)


class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
    post_id = HiddenField(validators=[DataRequired()])
    comment_id = HiddenField()
