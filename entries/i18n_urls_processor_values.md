# URLs an code language 

```
post_bp = Blueprint('POST_BP', __name__, url_prefix='/<lang_code>')


@post_bp.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@post_bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@post_bp.route('/', methods=['GET'])
def all_posts():
    return render_template('post/all.html', posts=Post.query.all())
```