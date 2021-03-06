from flask import Blueprint, g, url_for, render_template, request
from flask_login import login_required
from werkzeug.utils import redirect

from flask_blog_app import db
from flask_blog_app.blog.forms import TagForm
from flask_blog_app.blog.models import Subscriptor, Tag
from flask_blog_app.post import Post

blog_bp = Blueprint('BLOG_BP', __name__, url_prefix='/<lang_code>')


@blog_bp.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' not in g:
        g.lang_code = 'en'
    values.setdefault('lang_code', g.lang_code)


@blog_bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@blog_bp.route('/')
def home():
    return render_template('index.html', posts=Post.query.all())


@blog_bp.route("/tag/create", methods=['GET', 'POST'])
@login_required
def create_tag():
    tag_form = TagForm()
    if tag_form.validate_on_submit():
        tag = Tag(name=tag_form.name.data)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('ADMIN_BP.create_post'))
    return render_template('tag/form.html', form=tag_form)


@blog_bp.route("<tag>")
def filter_by_tag(tag):
    return render_template('tag/filter_posts.html', tag=Tag.query.filter_by(name=tag).first_or_404())


@blog_bp.route("/terms")
def show_terms():
    return render_template('terms.html')


@blog_bp.route("/subscribe", methods=['POST'])
def subscribe():
    email = request.form.get('email')
    sub = Subscriptor(email=email)
    db.session.add(sub)
    db.session.commit()
    return {"email": email}
