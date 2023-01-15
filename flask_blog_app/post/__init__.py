import os

import markdown
from flask import Blueprint, render_template, g, request, current_app
from werkzeug.utils import redirect

from flask_blog_app import db, es
from flask_blog_app.auth import User
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


@post_bp.route('/posts/<human_url>')
def show_post(human_url):
    post = PostTranslation.query.filter_by(human_url=human_url).first_or_404()
    md_file = os.path.join(current_app.config['UPLOAD_FOLDER'], post.content)
    f = open(md_file, 'r')
    md_text = f.read()
    # post_markdown = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])
    post_markdown = markdown.markdown(f"[TOC]\n{md_text}", extensions=['toc', 'fenced_code', 'codehilite'])
    # comment form
    comment_form = CommentForm()
    comment_form.post_id.data = post.id
    return render_template('post/post.html', post=Post.query.get(post.id), post_md=post_markdown, form=comment_form)


@post_bp.route('/posts/comment', methods=['POST'])
def create_comment():
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        user_email = comment_form.email.data
        user = User.query.filter_by(email=user_email).first()
        if not user:
            user = User(name=comment_form.name.data, email=user_email, picture=None)
            db.session.add(user)
            db.session.commit()
        db.session.flush()

        comment = Comment()
        comment.user_id = user.id
        comment.post_id = comment_form.post_id.data
        if comment_form.comment_id.data:
            comment.parent_id = comment_form.comment_id.data
        comment.content = markdown.markdown(comment_form.content.data, extensions=['fenced_code', 'codehilite'])
        db.session.add(comment)
        db.session.commit()
    referrer = request.referrer
    return redirect(referrer)


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
