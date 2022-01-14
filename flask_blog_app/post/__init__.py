import markdown
from flask import Blueprint, render_template, g, url_for
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from flask_blog_app import db
from flask_blog_app.post.forms import PostForm
from flask_blog_app.post.models import Post

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
        post.translations['en'].title = post_form.title.data
        post.translations['es'].title = post_form.title_es.data
        post.translations['en'].content = post_form.content.data
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
    post = Post.query.filter_by(human_url=human_url).first()
    post_markdown = markdown.markdown(post.translations[g.lang_code].content)
    return render_template('post/post.html', post=post, post_md=post_markdown)
