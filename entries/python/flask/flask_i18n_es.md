## poster
![Visual VM tool](https://drive.google.com/uc?id=1w2XKd4u1g1XIhiBMGBlnoTXZFDdRFHFT)

## Introducción
La internacionalización (i18n) y la localización (l10n) permiten que su aplicación admita varios idiomas, de modo que los usuarios puedan interactuar con su aplicación en su idioma preferido. Flask-Babel es una extensión de Flask que se puede usar para agregar fácilmente compatibilidad con i18n y l10n a una aplicación de Flask. 

Proporciona un conjunto de decoradores y funciones para traducir cadenas en el código fuente y las plantillas, y también brinda soporte para administrar catálogos de traducción. Está construido sobre la biblioteca de Babel, que proporciona un conjunto de utilidades para internacionalizar y localizar aplicaciones de Python.

En esta publicación, explicaré cómo comenzar con i18n y l10n creando una traducción estática en la aplicación Flask usando la extensión Flask-Babel y la biblioteca Babel.

## Babel y Frasco-Babel
Babel y Flask-Babel están relacionados con la internacionalización (i18n) y la localización (l10n) de aplicaciones, pero son bibliotecas diferentes.

Babel es una biblioteca de internacionalización genérica para Python. Proporciona un conjunto de utilidades para internacionalizar y localizar aplicaciones de Python. Incluye funcionalidad para extraer mensajes del código fuente, compilar catálogos de mensajes y administrar traducciones. La funcionalidad principal de Babel se puede utilizar en cualquier aplicación de Python y no se limita a las aplicaciones web.

Flask-Babel, por otro lado, es una extensión de Flask que agrega compatibilidad con i18n y l10n a las aplicaciones de Flask. Utiliza Babel bajo el capó y proporciona un conjunto de decoradores y funciones que se adaptan para trabajar con Flask.

## Instalación
Lo primero es instalar nuestras dependencias usando PyPi:
```
pip3 install Flask-Babel
```
> El comando anterior también instalará `Babel`.

## Configuración de Babel
Cree el archivo `babel.cfg` dentro del directorio del proyecto, al nivel del directorio del proyecto, con el siguiente contenido:

```
[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```
Para la mayoría de las aplicaciones de Flask, eso es todo lo que necesita, Babel escaneará sus archivos de python y las plantillas de Jinja.

## Configuración de Flak
En caso de que esté utilizando `fábrica de aplicaciones`. Después de inicializar `Flask-Babel`, configure la extensión de la siguiente manera:

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
El código anterior define una función llamada **get_locale** y la decora con **@babel_ext.localeselector**, que es un decorador provisto por la extensión `Flask-Babel`. Este decorador le dice a `Flask-Babel` que esta función debe usarse para determinar la configuración regional para la solicitud actual.

La función determina el idioma o la configuración regional preferidos por el usuario, ya sea desde la configuración del usuario o desde el objeto de contexto global `g`. Si ninguno de los anteriores está disponible, devuelve `en` por defecto.

## Las funciones "gettext" y "lazy_gettext"
Para entender Babel tenemos que empezar con dos funciones claves `gettext` y `lazy_gettext`.

La función `gettext` devuelve la traducción de una cadena en un idioma dado, **inmediatamente**. Toma una cadena como argumento y devuelve la cadena traducida correspondiente en el idioma actual. Por ejemplo:
````python
translated_string = gettext("Hello World")
````

La función `lazy_gettext` es similar a `gettext`, pero no traduce la cadena inmediatamente, sino que devuelve un **objeto proxy** que se traducirá cuando sea necesario. Esto puede ser útil para el rendimiento cuando se trabaja con muchas cadenas. Se puede usar de la misma forma que `gettext`:
````python
translated_string = lazy_gettext("Hello World")
````

## Marcado de texto
Este proceso consiste en marcar ciertas cadenas como traducibles y luego `Flask-Babel` las recopilará en un archivo para que las traduzca. En tiempo de ejecución, las cadenas originales (que deben ser en inglés) serán reemplazadas por el idioma que seleccionó.

### Dentro de los archivos de Python
Importe `lazy_gettext` as follows:
```
from flask.ext.babelpkg import lazy_gettext as _
```

Tomemos, por ejemplo, un formulario simple y especifiquemos que la etiqueta es traducible, de modo que podamos proporcionar la versión en inglés y español:

```python
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField(_('Name'), validators=[DataRequired()])
    content = TextAreaField(_('Content'), validators=[DataRequired()])
```
El código anterior define una clase llamada `PostForm` que hereda de la clase `FlaskForm`. La clase tiene dos atributos, `title` y `content`. La función `_` es un atajo para `lazy_gettext`, al usar la función `_` marcamos los campos de cadena `Name` y `Content` para la traducción. Por lo tanto, estos campos se traducirán según el idioma preferido del usuario.

### Marcado de textos de plantillas Jinja
Marcar textos en la plantilla Jinja:
```html
...
<li><a href="/">{{ _('Home') }}</a></li>
...
```
Este fragmento de código es una plantilla de Jinja y se utiliza para crear un elemento HTML que representa un enlace a la página de inicio de la aplicación. El texto del vínculo es "Home" y está marcado para traducir mediante la función `_`, similar a cómo se usó en el fragmento de código de Python anterior.

## Extrayendo cadenas traducibles
Extraigamos el texto que marcamos como traducible y creemos un archivo `messages.pot`, este archivo nos servirá como plantilla para luego crear las traducciones reales, ejecutamos:

```commandline
pybabel extract -F babel.cfg -o messages.pot flask_app
```
El comando se compone de varias opciones:

1. `extract`: especifica que la herramienta `pybabel` debe extraer cadenas marcadas como traducibles.
2. `-F babel.cfg`: especifica el archivo de configuración que contiene los ajustes: `babel.cfg`.
3. `-o message.pot`: especifica el archivo de salida que debe usarse para almacenar las cadenas extraídas.
4. `flask_app`: especifica la aplicación Flask (carpeta de la aplicación) para buscar las cadenas dentro.

Después de ejecutar el comando, veremos un nuevo archivo creado: `messages.pot` que contiene todas las cadenas marcadas:
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

## Generando traducciones
Ahora estamos listos para crear traducciones, por ejemplo para generar una traducción para español a partir de las cadenas en `messages.pot` podríamos ejecutar:
```commandline
pybabel init -i messages.pot -d flask_app/translations -l es
```
El comando anterior hace lo siguiente:

1. `init`: especifica que la herramienta `pybabel` debe inicializar un nuevo catálogo de traducción.
2. `-i mensajes.pot`: especifica el archivo de entrada que debe usarse como plantilla para el nuevo catálogo.
3. `-d matraz_app/translations`: especifica el directorio donde se debe crear el nuevo catálogo.
4. `-l es`: especifica el código de idioma del nuevo catálogo, en este caso `es` para español.

La carpeta predeterminada donde **Flask-Babel** buscará las traducciones es el directorio `tu_aplicación/traducciones`. En mi caso es `flask_app/translations`, por lo que el comando creará un subdirectorio `es` dentro de este directorio para los archivos de datos en español.
Busque el archivo `flask_app/translations/es/LC_MESSAGES/messages.po`. Ahora solo necesitamos modificar el archivo proporcionando una traducción real al español, por ejemplo:

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
Los archivos `.po` son como una fuente de traducciones, mientras que `.pot` es como una plantilla para crear fuentes, necesitamos compilar archivos `.po` para crear `.mo`, los archivos `.mo` son una versión compilada , este es el archivo real utilizado por **Flask-Babel** para cargar las traducciones.

¿Qué pasa si agregas más cadenas o cambian? Tenga en cuenta que necesitamos actualizar a veces, de lo contrario perderemos la traducción que hemos hecho antes, para actualizar la fuente después de **extraer** los nuevos textos agregados si ese es el caso.
````commandline
pybabel update -i messages.pot -d flask_app/translations -l es
````

Vamos a compilar nuestras fuentes para que la traducción se refleje en nuestra aplicación, para crear el archivo compilado `.mo` a partir de una fuente `.po`:

```
pybabel compile -d flask_app/translations
```
Este comando generará un archivo `.mo` justo al lado del archivo `.po`. Este será el archivo real utilizado por Babel para elegir el valor de la cadena traducible en función del idioma devuelto por la función **get_locale()**.

## Ejecutando la aplicación
Establezca la configuración regional predeterminada en `es`, solo para fines de prueba:
```python
@babel_ext.localeselector
def get_locale():
    return 'es'
```
Luego ejecute el comando `flask run` y vaya a su formulario donde el texto se marcó como traducible. Debería ver el texto en español.

## Conclusión
Hemos discutido el uso de la biblioteca Flask-Babel para la internacionalización y localización de una aplicación Flask. Revisamos varios fragmentos de código y comandos que demostraban cómo usar la biblioteca para traducir cadenas en el código fuente, plantillas y cómo extraer e inicializar catálogos de traducción.

Happy Code ;)