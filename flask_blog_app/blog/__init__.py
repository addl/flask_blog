from flask import Blueprint, g, url_for, render_template, request, flash, current_app
from flask_mail import Mail, Message
from flask_login import login_required
from werkzeug.utils import redirect

from flask_blog_app import db, mail
from flask_blog_app.blog.forms import TagForm, ContactForm
from flask_blog_app.blog.models import Subscriptor, Tag, Category
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
    return render_template('index.html', posts=Post.query.order_by("timestamp").all()[:6])


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


@blog_bp.route("/contact", methods=['GET', 'POST'])
def contact_us():
    contact_form = ContactForm(request.form)
    if request.method == 'POST' and contact_form.validate():
        # Process the contact information here.
        msg = Message("Message from " + contact_form.name.data,
                      sender=("My Refactor", current_app.config['MAIL_USERNAME']),
                      recipients=[current_app.config['MAIL_ADMIN']])
        msg.body = contact_form.message.data if contact_form.message.data else "Hello,from Flask and Gmail SMTP server."
        msg.reply_to = contact_form.email.data
        mail.send(msg)
        flash('Thanks for contact us! We will message you soon.')
        return redirect(url_for('.contact_us'))
    return render_template('contact.html', form=contact_form)


@blog_bp.route("<category>")
def filter_by_category(category):
    return render_template('category/filter_posts.html', category=Category.query.filter_by(name=category).first_or_404())


@blog_bp.route("/terms")
def show_terms():
    return render_template('terms.html')


@blog_bp.route("/privacy")
def show_privacy():
    return render_template('privacy.html')


@blog_bp.route("/subscribe", methods=['POST'])
def subscribe():
    email = request.form.get('email')
    sub = Subscriptor(email=email)
    db.session.add(sub)
    db.session.commit()
    return {"email": email}
