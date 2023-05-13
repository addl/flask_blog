from flask import Blueprint, render_template, flash, url_for, request
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import redirect
from flask_blog_app.auth.forms import LoginForm
from flask_blog_app.auth.models import User

auth_bp = Blueprint('AUTH_BP', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        existing_user = User.query.filter_by(email=login_form.email.data).first()
        if existing_user is None or not existing_user.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('.login'))
        login_user(existing_user, remember=login_form.remember_me.data)
        if existing_user.is_admin:
            return redirect(url_for('ADMIN_BP.admin_home'))
        return redirect('/')
    return render_template('auth/login.html', form=login_form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

