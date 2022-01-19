import babel
import sqlalchemy_utils
from elasticsearch import Elasticsearch
from flask import Flask, render_template, g, request, send_from_directory, url_for
from flask_babel import Babel
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from flask_blog_app.config import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()
babel_ext = Babel()
es = Elasticsearch()


def create_app(test_config=None, get_locale=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig)

    # DB settings
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://pguser:postgres@localhost:5432/flask_blog"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Login
    login_manager = LoginManager()
    # Which function to execute when login is required
    login_manager.login_view = 'AUTH_BP.login'
    login_manager.init_app(app)

    from flask_blog_app.auth.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # i18n
    babel_ext.init_app(app)

    @babel_ext.localeselector
    def get_locale():
        # if a user is logged in, use the locale from the user settings
        user = getattr(g, 'user', None)
        if user is not None:
            return user.locale
        # return request.accept_languages.best_match(['en', 'es'])
        return g.get('lang_code', 'en')

    # sqlalchemy-i18n
    sqlalchemy_utils.i18n.get_locale = get_locale

    # a simple page that says hello
    @app.route('/')
    def home():
        return redirect(url_for('BLOG_BP.home'))

    @app.route('/robots.txt')
    @app.route('/sitemap.xml')
    def static_from_root():
        path_ = request.path[1:]
        return send_from_directory(app.static_folder, path_)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html")

    @app.errorhandler(500)
    def not_found(e):
        return render_template("500.html")

    # blueprint registration
    from flask_blog_app.blog import blog_bp
    from flask_blog_app.post import post_bp
    from flask_blog_app.auth import auth_bp
    app.register_blueprint(blog_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        from .post.models import Post

        return app
