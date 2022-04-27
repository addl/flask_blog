# I18N con Flask y Babel

1. Instalar extension flask-babel extension

2. To notice that flask-bable is just an extension, the package Babel is an standalone module to work with i18n

3. Creating Babel config file

4. Generating files using only Babel (not the extension)

5. Configure project to work with Babel by using flask-babel(the extension)

6. Marking translatable texts




Interesting article: https://flask-babel.tkte.ch/

## Installation

```
pip3 install Flask-Babel
```

## About the difference between Babel and Flask Babel

## Create 'babel.cfg' inside project directory, next to application directory, put this inside:


```
[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```

## Generating (only .pot) files, norice this file is a  placeholder, the actual translation cames later (.po files).

By default Babel uses English (en) and when generating files the English is the base, so generating a file for Spanish, will generated a file with the par EN-ES.

```
pybabel extract -F babel.cfg -o messages.pot .
```

-F configuration file (babel.cfg)

-o output file location 'messages.pot'

. scan from this path on (more in a sec)

The reult of above oprtation is a file 'messages.pot'

```
# Translations template for PROJECT.
# Copyright (C) 2022 ORGANIZATION
# This file is distributed under the same license as the PROJECT project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2022.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PROJECT VERSION\n"
"Report-Msgid-Bugs-To: EMAIL@ADDRESS\n"
"POT-Creation-Date: 2022-01-11 23:13+0200\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel 2.9.1\n"
```
Now we are going to include some text inside this file.


## Configure project and flask-babel extension, the followingcode inside 'app.__init__.py' within create_app, in case you are using 'application factory'
```
@babel.localeselector
    def get_locale():
        # if a user is logged in, use the locale from the user settings
        user = getattr(g, 'user', None)
        if user is not None:
            return user.locale
        # otherwise try to guess the language from the user accept
        # header the browser transmits.  We support de/fr/en in this
        # example.  The best match wins.
        return request.accept_languages.best_match(['en', 'es'])
```

Initilizing extension, inside create_app or in __init__.py:
```python
babel_ext = Babel()
...
create_app():
    ...
    babel_ext.init_app(app)
```

## Marking string

The idea of gettext is that you can mark certain strings as translatable and a tool will pick all those up, collect them in a separate file for you to translate. At runtime the original strings (which should be English) will be replaced by the language you selected.

### Inside python files and Jinja templates

Import lazy_text:
```
from flask.ext.babelpkg import lazy_gettext as _
```
Let;s take for example a simple form, and specify that the label is translatable, so that we can provide the English and Spanish version in our pot file:
```python
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField(_('Name'), validators=[DataRequired()])
    content = TextAreaField(_('Content'), validators=[DataRequired()])
```
Mark texts in Jinja template:
```html
...
<li><a href="/">{{ _('Home') }}</a></li>
...
```

Let's extract the text by generating again 'messages.pot' file, execute in console:
```
pybabel extract -F babel.cfg -o messages.pot .
```

Now you can see that the file changed, by including new entries:
```
...
#: flask_blog_app/post/forms.py:8
msgid "Name"
msgstr ""

#: flask_blog_app/post/forms.py:9
msgid "Content"
msgstr ""

#: flask_blog_app/templates/common/navigation.html:3
msgid "Home"
msgstr ""
...
```
Now we are ready to create the '.po' translation files:
```
pybabel init -i messages.pot -d app/translations -l es
```
The pybabel init command takes the messages.pot file as input and writes a new language catalog to the directory given in the -d option for the language specified in the -l option. I'm going to be installing all the translations in the app/translations directory, because that is where Flask-Babel will expect translation files to be by default. The command will create a es subdirectory inside this directory for the Spanish data files. In particular, there will be a new file named app/translations/es/LC_MESSAGES/messages.po, that is where the translations need to be made.
Now we just need to modify the file by providing actual translation to Spanish:
```
#: flask_blog_app/post/forms.py:8
msgid "Name"
msgstr "Nombre"

#: flask_blog_app/post/forms.py:9
msgid "Content"
msgstr "Contenido"

#: flask_blog_app/templates/common/navigation.html:3
msgid "Home"
msgstr "Inicio"
...
```
'.po' files is like a source of translations, while '.pot' is like a template, we need to compile '.po' fies to create '.mo', '.mo' files are compiled version, means to be used by a computer, this is the actual file used by flask-babel to load translations.
```
pybabel compile -d app/translations
```
This command will generate a '.mo' file just next to the '.po' file

## Running the application
Set default locale to "es", just to test:
```
@babel_ext.localeselector
def get_locale():
    return 'es'
```
Then run flask:
```
flask run
``

We are done!