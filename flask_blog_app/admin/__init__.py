import os
from datetime import datetime

from flask import Blueprint, render_template, request, current_app, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect, secure_filename

from flask_blog_app import db, es
from flask_blog_app.blog.models import Tag
from flask_blog_app.post.models import Post
from flask_blog_app.post import PostForm

admin_bp = Blueprint('ADMIN_BP', __name__)


@admin_bp.before_request
def intercept():
    if not current_user.is_admin:
        return abort(404)


@login_required
@admin_bp.route("/admin")
def admin_home():
    return render_template('admin/home.html')


@admin_bp.route('/admin/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    post_form = PostForm()
    post_form.tags.choices = [(t.id, t.name) for t in Tag.query.all()]
    post_id = request.args.get('post_id')
    if post_id:
        current_post = Post.query.get_or_404(post_id)
        post_form.post_id.data = post_id
        post_form.title.data = current_post.translations['en'].title
        post_form.title_es.data = current_post.translations['es'].title
        post_form.description.data = current_post.translations['en'].description
        post_form.description_es.data = current_post.translations['es'].description
    if post_form.validate_on_submit():
        post = Post()
        if post_form.post_id.data:
            post = Post.query.get_or_404(int(post_form.post_id.data))
        if 'file_content' not in request.files or 'file_content_es' not in request.files:
            return redirect(request.url)
        file_content = request.files['file_content']
        file_content_es = request.files['file_content_es']
        if file_content.filename == '' or file_content_es.filename == '':
            return redirect(request.url)
        filename = ''
        filename_es = ''
        if file_content and file_content_es:
            # when updating delete old files
            if post.id and file_content and file_content_es:
                delete_post_files_from_disk(post.id)
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
    return render_template('admin/post_form.html', form=post_form)


@admin_bp.route('/admin/posts/all', methods=['GET'])
@login_required
def all_posts():
    return render_template('admin/all_posts.html', posts=Post.query.all())


@admin_bp.route('/admin/posts/delete/<post_id>', methods=['GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.all_posts'))


# helpers:
def delete_post_files_from_disk(post_id):
    post = Post.query.get(post_id)
    en_file = post.translations['en'].content
    es_file = post.translations['es'].content
    md_file_en = os.path.join(current_app.config['UPLOAD_FOLDER'], en_file)
    md_file_es = os.path.join(current_app.config['UPLOAD_FOLDER'], es_file)
    if os.path.exists(md_file_en):
        current_app.logger.info(f"Deleting file: {md_file_en}")
        os.remove(md_file_en)
    if os.path.exists(md_file_es):
        current_app.logger.info(f"Deleting file: {md_file_es}")
        os.remove(md_file_es)
