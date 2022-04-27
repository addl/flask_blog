import babel
import sqlalchemy_utils
from elasticsearch import Elasticsearch
from flask import Flask, render_template, g, request, send_from_directory, url_for, session, jsonify
from flask_babel import Babel
from flask_login import LoginManager, login_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from authlib.integrations.flask_client import OAuth

from flask_blog_app.config import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()
babel_ext = Babel()
es = Elasticsearch()
oauth = OAuth()

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

    @app.route('/')
    def home():
        return redirect(url_for('BLOG_BP.home'))

    @app.route('/robots.txt')
    @app.route('/sitemap.xml')
    def static_from_root():
        path_ = request.path[1:]
        return send_from_directory(app.static_folder, path_)

    # Social login
    oauth.init_app(app)

    @app.route('/twitter')
    def login_twitter():
        oauth.register(
            name='twitter',
            api_base_url='https://api.twitter.com/1.1/',
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authenticate',
            client_kwargs={
                "include_email": True,
            },
            fetch_token=lambda: session.get('token'),  # DON'T DO IT IN PRODUCTION
        )
        return oauth.twitter.authorize_redirect(url_for('auth_twitter', _external=True))

    @app.route('/tcallback')
    def auth_twitter():
        token = oauth.twitter.authorize_access_token()
        url = 'account/verify_credentials.json'
        resp = oauth.twitter.get(url, params={'skip_status': True})
        twitter_user = resp.json()
        tuser_email = f"{twitter_user.get('screen_name')}@twitter.com"
        user = User.query.filter_by(email=tuser_email).first()
        if not user:
            user = User(name=twitter_user.get('name'), email=tuser_email, picture=twitter_user.get('profile_image_url'))
            db.session.add(user)
            db.session.commit()
        # Login user
        login_user(user)
        return redirect('/')

    @app.route('/linkedin/')
    def linkedin():
        LINKEDIN_CLIENT_ID = "773gub81e3fli6"
        LINKEDIN_CLIENT_SECRET = "8usba9vBkUsiZttE"
        oauth.register(
            name='linkedin',
            client_id=LINKEDIN_CLIENT_ID,
            client_secret=LINKEDIN_CLIENT_SECRET,
            grant_type='client_credentials',
            access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
            request_token_url='https://www.linkedin.com/oauth/v2/requestToken',
            authorize_url='https://www.linkedin.com/oauth/v2/authorization',
            access_token_method='POST',
            client_kwargs={
                'scope': 'r_basicprofile',
                'state': 'RandomString',
                'grant_type': 'client_credentials'
            }
        )
        # Redirect to callback function
        redirect_uri = url_for('linkedin_auth', _external=True)
        return oauth.linkedin.authorize_redirect(redirect_uri)

    @app.route('/lcallback')
    def linkedin_auth():
        resp = linkedin.authorized_response()
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        session['linkedin_token'] = (resp['access_token'], '')
        me = linkedin.get('people/~')
        return jsonify(me.data)

    @app.route('/facebook/')
    def facebook():
        # Facebook Oauth Config
        #FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID')
        #FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET')
        FACEBOOK_CLIENT_ID = "915487802553036"
        FACEBOOK_CLIENT_SECRET = "1c9237a58fe6ad038cfc635c8a36ff36"
        oauth.register(
            name='facebook',
            client_id=FACEBOOK_CLIENT_ID,
            client_secret=FACEBOOK_CLIENT_SECRET,
            access_token_url='https://graph.facebook.com/oauth/access_token',
            access_token_params=None,
            authorize_url='https://www.facebook.com/dialog/oauth',
            authorize_params=None,
            api_base_url='https://graph.facebook.com/',
            client_kwargs={'scope': 'email'},
        )
        redirect_uri = url_for('facebook_auth', _external=True)
        return oauth.facebook.authorize_redirect(redirect_uri)

    @app.route('/fcallback')
    def facebook_auth():
        token = oauth.facebook.authorize_access_token()
        resp = oauth.facebook.get(
            'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
        profile = resp.json()
        print("Facebook User ", profile)
        return redirect('/')

    @app.route('/google/')
    def google():
        # Google Oauth Config
        # Get client_id and client_secret from environment variables
        # GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
        # GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
        GOOGLE_CLIENT_ID = "140728854919-7j25htfcau37o3th1rl72qrejjogtkvj.apps.googleusercontent.com"
        GOOGLE_CLIENT_SECRET = "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"

        CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
        oauth.register(
            name='google',
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            server_metadata_url=CONF_URL,
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
        # Redirect to google_auth function
        redirect_uri = url_for('google_auth', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)

    @app.route('/gcallback')
    def google_auth():
        token = oauth.google.authorize_access_token()
        google_user = oauth.google.parse_id_token(token, nonce=None)

        # Doesn't exist? Add it to the database.
        user = User.query.filter_by(email=google_user.get('email')).first()
        if not user:
            user = User(name=google_user.get('name'), email=google_user.get('email'),
                        picture=google_user.get('picture'))
            db.session.add(user)
            db.session.commit()

        # Begin user session by logging the user in
        login_user(user)
        return redirect('/')

    # Error handlers registering
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_error)

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


# Error handlers
def not_found(e):
    return render_template("404.html"), 404


def internal_error(e):
    return render_template("500.html"), 500
