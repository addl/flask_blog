## Introducción
FlaskForm es una poderosa biblioteca que le permite crear y validar fácilmente formularios en su aplicación Flask. Se integra a la perfección con el motor de plantillas Jinja2, por lo que puede usarlo para pasar datos de formulario a sus plantillas y representar los formularios en sus páginas HTML.

Para usar FlaskForm en su aplicación Flask, primero deberá instalarlo usando pip:
````commandline
pip install wtforms
````

## Creando el formulario
Deberá crear una clase de formulario en su código de Python. Por ejemplo, aquí hay un formulario de contacto simple con un campo de nombre, correo electrónico y mensaje:

````python
class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[
        DataRequired(), Email(granular_message=True)])
    message = TextAreaField(label='Message',  validators=[DataRequired()])
````
Las clases `StringField` y `TextAreaField` representan campos de entrada para datos de texto, y el módulo de validadores proporciona varias funciones de validación que se pueden usar para garantizar que la entrada del usuario sea válida. En este ejemplo, estamos utilizando el validador `DataRequired` para garantizar que el usuario ingrese un valor para cada campo, y el validador `Email` para garantizar que el campo de correo electrónico contenga una dirección de correo electrónico válida.

## Creación de la URL de vista y enrutamiento
Necesitamos crear una función de ruta para mostrar la página del formulario y validarla usando el método de validación del objeto del formulario:

````python
from flask import request, flash, render_template

@app.route('/contact', methods=['GET', 'POST'])
def contact_us():
    contact_form = ContactForm(request.form)
    if request.method == 'POST' and contact_form.validate():
        # Process the contact information here.
        flash('Thanks for contact us!')
    return render_template('contact.html', form=contact_form)
````
En la `view` de arriba, cuando el método HTTP es GET mostramos el formulario, de lo contrario, si el método HTTP es POST, procedemos a validar y procesar la información enviada por el usuario.

Nuestro nombre de vista es `contact_us` y se ejecutará si la URL es `/contact`, esta información es importante para configurar el formulario en la plantilla HTML.

## Configuración de la plantilla HTML
Para mostrar el formulario en su plantilla, deberá pasar el objeto del formulario al contexto de la plantilla y utilizar la sintaxis de Jinja2 para renderizar elementos HTML. Por ejemplo:

````html
<div class="contact_us">
    <form method="POST" action="{{ url_for('contact_us') }}">
        {{ form.csrf_token }}
        {{ form.name.label }} {{ form.name(size=32) }}
        <br />
        {{ form.email.label }} {{ form.email(size=32) }}
        <br />
        {{ form.message.label }} {{ form.message(cols=50, rows=10) }}
        <br />
        {% if form.errors %}
            <ul class="errors">
                {% for error, msg in form.errors.items() %}
                    <li>{{ error }} : {{ msg[0] }}</li>
                {% endfor %}
            </ul>
        {% endif %}
        <br />
        <button type="submit">Send</button>
    </form>
</div>
````

En el ejemplo anterior, las etiquetas del formulario: `{{ form.name.label }}` y los campos producirán los elementos HTML del formulario.

Una propiedad importante en los formularios es la información de errores. Tenga en cuenta cómo preguntamos si tenemos errores en algún campo o no con `{% if form.errors %}`, si es así, iteramos a través de todos ellos y mostramos el mensaje de error.

Cuando el usuario envía el formulario, los datos se enviarán a la ruta `/contacto` en su aplicación Flask, ya que usamos `url_for` para crear la acción del formulario: `action="{{ url_for('contact_us') }} "`.

## Problemas comunes
Si ve el siguiente error una vez que ejecuta la aplicación:

````commandline
Exception: Install 'email_validator' for email validation support.
````

Está relacionado con una dependencia en el archivo `wtforms/validators.py`, en la línea 9:
````python
import email_validator
````

Entonces necesitamos instalar el paquete `email_validator`, con pip run:
````commandline
pip install email_validator
````

Ahora debería funcionar sin errores.

## Conclusión
FlaskForm es una biblioteca útil para crear y validar formularios en una aplicación Flask. Se integra a la perfección con Jinja2, lo que le permite representar fácilmente formularios en sus plantillas y manejar datos de formularios en sus rutas.

Happy code!
