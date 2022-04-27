import os
from datetime import datetime

import markdown
from flask import Blueprint, render_template, g, url_for, request, current_app
from flask_login import current_user, login_required
from werkzeug.utils import redirect, secure_filename

from flask_blog_app import db, es
from flask_blog_app.blog.models import Tag
from flask_blog_app.post.forms import PostForm, CommentForm
from flask_blog_app.post.models import Post, PostTranslation, Comment

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
    post_form.tags.choices = [(t.id, t.name) for t in Tag.query.all()]
    if post_form.validate_on_submit():
        post = Post()
        if 'file_content' not in request.files or 'file_content_es' not in request.files:
            return redirect(request.url)
        file_content = request.files['file_content']
        file_content_es = request.files['file_content_es']
        if file_content.filename == '' or file_content_es.filename == '':
            return redirect(request.url)
        filename = ''
        filename_es = ''
        if file_content and file_content_es:
            filename = secure_filename(file_content.filename)
            filename_es = secure_filename(file_content_es.filename)
            file_content.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            file_content_es.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename_es))
        post.translations['en'].title = post_form.title.data
        post.translations['es'].title = post_form.title_es.data
        post.translations['en'].content = filename
        post.translations['es'].content = filename_es
        human_url_en = post_form.title.data.replace(' ', '-').lower()
        human_url_es = post_form.title_es.data.replace(' ', '-').lower()
        post.translations['en'].human_url = human_url_en
        post.translations['es'].human_url = human_url_es
        post.translations['en'].description = post_form.description.data
        post.translations['es'].description = post_form.description_es.data
        post.tags = [Tag.query.get(t) for t in post_form.tags.data]
        post.user_id = current_user.id
        db.session.add(post)
        db.session.commit()
        # ES insert

        body = {
            'id': human_url_en,
            'title': post_form.title.data.lower(),
            'description': post_form.description.data.lower(),
            'timestamp': datetime.now()
        }

        body_es = {
            'id': human_url_es,
            'title': post_form.title_es.data.lower(),
            'description': post_form.description_es.data.lower(),
            'timestamp': datetime.now()
        }

        es.index(index='post_en', id=human_url_en, body=body)
        es.index(index='post_es', id=human_url_es, body=body_es)
        return redirect(url_for('.all_posts'))
    return render_template('post/form.html', form=post_form)


@post_bp.route('/posts/<human_url>')
def show_post(human_url):
    post = PostTranslation.query.filter_by(human_url=human_url).first_or_404()
    md_file = os.path.join(current_app.config['UPLOAD_FOLDER'], post.content)
    f = open(md_file, 'r')
    post_markdown = markdown.markdown(f.read(), extensions=['fenced_code', 'codehilite'])
    # comment form
    comment_form = CommentForm()
    comment_form.post_id.data = post.id
    return render_template('post/post.html', post=Post.query.get(post.id), post_md=post_markdown, form=comment_form)


@post_bp.route('/posts/comment', methods=['POST'])
@login_required
def create_comment():
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment()
        comment.user_id = current_user.id
        comment.post_id = comment_form.post_id
    referrer = request.referrer
    return redirect(referrer)


@post_bp.route('/posts/comments/<post_id>')
def get_post_comment(post_id):
    pass


@post_bp.route('/posts/search')
def search_posts():
    query = request.args.get('query')
    body = {
        "query": {
            "multi_match": {
                "query": query.lower(),
                "fields": ["title", "description"]
            }
        }
    }
    res = es.search(index="post_"+g.lang_code, body=body)
    # to use dict to avoid duplicated post, due to language
    posts_result = []
    for hit in res['hits']['hits']:
        posts_result.append(Post.query.filter_by(human_url=hit['_id']).first())
    return render_template('search/result.html', query=query, posts=posts_result)
