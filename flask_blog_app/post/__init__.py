import os

import markdown
from flask import Blueprint, render_template, g, url_for, request, current_app
from flask_login import current_user, login_required
from werkzeug.utils import redirect, secure_filename

from flask_blog_app import db
from flask_blog_app.post.forms import PostForm
from flask_blog_app.post.models import Post, PostTranslation

post_bp = Blueprint('POST_BP', __name__, url_prefix='/<lang_code>')


@post_bp.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' not in g:
        g.lang_code = 'en'
    values.setdefault('lang_code', g.lang_code)


@post_bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@post_bp.route('/posts', methods=['GET'])
def all_posts():
    return render_template('post/all.html', posts=Post.query.all())


@post_bp.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post()
        if 'file_content' not in request.files:
            return redirect(request.url)
        file_content = request.files['file_content']
        if file_content.filename == '':
            return redirect(request.url)
        filename = ''
        if file_content:
            filename = secure_filename(file_content.filename)
            file_content.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        post.translations['en'].title = post_form.title.data
        post.translations['es'].title = post_form.title_es.data
        post.translations['en'].content = filename
        post.translations['es'].content = post_form.content_es.data
        post.translations['en'].human_url = post_form.title.data.replace(' ', '-').lower()
        post.translations['es'].human_url = post_form.title_es.data.replace(' ', '-').lower()
        post.user_id = current_user.id
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.all_posts'))
    return render_template('post/form.html', form=post_form)


@post_bp.route('/<human_url>')
def show_post(human_url):
    post = PostTranslation.query.filter_by(human_url=human_url).first()
    md_file = os.path.join(current_app.config['UPLOAD_FOLDER'], post.content)
    f = open(md_file, 'r')
    post_markdown = markdown.markdown(f.read())
    return render_template('post/post.html', post=Post.query.get(post.id), post_md=post_markdown)
