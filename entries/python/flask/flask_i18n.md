## poster
![Visual VM tool](https://drive.google.com/uc?id=1ciyU--Fw3q215AZz-KBKbexRO0wdB6lR)

## Introduction
Internationalization (i18n) and localization (l10n) allow your application to support multiple languages, so that users can interact with your application in their preferred language. Flask-Babel is a Flask extension that can be used to easily add i18n and l10n support to a Flask application. It provides a set of decorators and functions to translate strings in the source code and templates, and also provides support for managing translation catalogs. It is built on top of the Babel library, which provides a set of utilities for internationalizing and localizing Python applications.

In this post I will explain how to get started with i18n and l10n by creating static translation in Flask application using Flask-Babel extension and Babel library.

## Babel and Flask-Babel
Babel and Flask-Babel are both related to internationalization (i18n) and localization (l10n) of applications, but they are different libraries.

Babel is a generic internationalization library for Python. It provides a set of utilities for internationalizing and localizing Python applications. It includes functionality for extracting messages from source code, compiling message catalogs, and managing translations. The core functionality of Babel can be used in any Python application, and it is not limited to web applications.

Flask-Babel, on the other hand, is a Flask extension that adds i18n and l10n support to Flask applications. It uses Babel under the hood and provides a set of decorators and functions that are tailored to work with Flask.

## Installation
The first thing is to install our dependencies using PyPi:
```
pip3 install Flask-Babel
```
> The above command will install `Babel` as well.

## Babel settings
Create `babel.cfg` file inside project directory, next to application directory, with the following content:

```
[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```
For mostly Flask applications that's all you need, Babel will scan your python files and Jinja templates.

## Flask configuration
In case you are using `application factory`. After initializing `Flask-Babel`, configure as follows:

```python
...
babel_ext.init_app(app)

@babel_ext.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # return request.accept_languages.best_match(['en', 'es'])
    return g.get('lang_code', 'en')
...
```
This code defines a function called **get_locale** and decorates it with **@babel_ext.localeselector**, which is a decorator provided by the `Flask-Babel` extension. This decorator tells `Flask-Babel` that this function should be used to determine the locale for the current request. 

The function determines the user's preferred language/locale either from user's settings or from the global context object `g`. If none of the above is available it returns `en` as default.

## The functions "gettext" and "lazy_gettext"
In order to understand Babel we have to begin with two key functions `gettext` and `lazy_gettext`. 

The `gettext` function returns the translation of a string in a given language, immediately. It takes a string as an argument and returns the corresponding translated string in the current language. For example:
````python
translated_string = gettext("Hello World")
````

The `lazy_gettext` function is similar to `gettext`, but it doesn't translate the string immediately, instead it returns a **proxy object** that will be translated when it is needed. This can be useful for performance when working with a lot of strings. It can be used in the same way as `gettext`:
````python
translated_string = lazy_gettext("Hello World")
````

## Marking strings
You can mark certain strings as translatable and a tool will pick all those up, collect them in a separate file for you to translate. At runtime the original strings (which should be English) will be replaced by the language you selected.

### Inside Python files
Import `lazy_gettext`:
```
from flask.ext.babelpkg import lazy_gettext as _
```
Let;s take for example a simple form, and specify that the label is translatable, so that we can provide the English and Spanish versions:
```python
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField(_('Name'), validators=[DataRequired()])
    content = TextAreaField(_('Content'), validators=[DataRequired()])
```
The above code defines a class called `PostForm` that inherits from the "FlaskForm" class. The class has two attributes, "title" and "content". The `_` function is a shortcut for `lazy_gettext`, by using `_` function we mark the string fields `Name` and `Content` for translation. So, these fields will be translated based on the user's preferred language.

### Marking Jinja templates texts
Mark texts in Jinja template:
```html
...
<li><a href="/">{{ _('Home') }}</a></li>
...
```
This code snippet is a Jinja template, and it is used to create an HTML element that represents a link to the homepage of the application. The link text is "Home" and it is marked for translation using the `_` function, similar to how it was used in the previous Python code snippet.

## Extracting translatable strings
Let's extract the text we marked as translatable and create a `messages.pot` file, this file will serve us as template to later create the actual translations, execute:

```commandline
pybabel extract -F babel.cfg -o messages.pot flask_app
```
The command is composed of several options:

1. `extract`: specifies that the `pybabel` tool should extract translatable strings.
2. `-F babel.cfg`: specifies the configuration file that contains the settings: `babel.cfg`.
3. `-o messages.pot`: specifies the output file that should be used to store the extracted strings.
4. `flask_app`: specifies the Flask application (app folder) to look for the strings inside.

After executing the command, we will see a new file created: `messages.pot` containing all marked strings:
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

## Generating translations
Now we are ready to create translations, for example to generate a translation for Spanish from the strings in `messages.pot` we could execute:

```commandline
pybabel init -i messages.pot -d flask_app/translations -l es
```

The above command do the following:

1. `init`: specifies that the `pybabel` tool should initialize a new translation catalog.
2. `-i messages.pot`: specifies the input file that should be used as a template for the new catalog.
3. `-d flask_app/translations`: specifies the directory where the new catalog should be created.
4. `-l es`: specifies the language code of the new catalog, in this case `es` for Spanish.

The default folder where **Flask-Babel** will look for translations is `your_app/translations` directory. In my case is `flask_app/translations`, so the command will create a `es` subdirectory inside this directory for the Spanish data files.
Look for the file`flask_app/translations/es/LC_MESSAGES/messages.po`. Now we just need to modify the file by providing actual translation to Spanish:

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
The `.po` files is like a source of translations, while `.pot` is like a template to create sources, we need to compile `.po` fies to create  `.mo`, `.mo` files are compiled version, this is the actual file used by **Flask-Babel** to load translations.

What if you add more strings or they change? Keep in mind we need to update sometimes, otherwise we will lose the translation we have made before, to update the source after **extracting** the new texts added if that the case.

````commandline
pybabel update -i messages.pot -d flask_app/translations -l es
````

Let's compile our sources so that the translation get reflected in our application, to create the compiled file `.mo` from a `.po` source:

```
pybabel compile -d flask_app/translations
```
This command will generate a `.mo` file just next to the `.po` file. This will be the actual file used by Babel to pick the value of the translatable string based on the language returned by the function **get_locale()**.

## Running the application
Set default locale to `es`, just for testing purpose:
```python
@babel_ext.localeselector
def get_locale():
    return 'es'
```
Then run the command `flask run` and go to your form where the text where marked as translatable. You should see the text in Spanish.

## Conclusion
We have discussed the usage of Flask-Babel library for internationalization and localization of a Flask application. We went through various code snippets and commands that demonstrated how to use the library for translating strings in the source code, templates and how to extract and initialize translation catalogs.

Happy code ;)