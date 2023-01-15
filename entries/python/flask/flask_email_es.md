## Introducción
Enviar correos electrónicos desde una aplicación Flask puede ser una función útil para una variedad de casos de uso, como enviar correos electrónicos de confirmación, correos electrónicos de restablecimiento de contraseña y más. En este artículo, veremos cómo enviar correos electrónicos desde una aplicación Flask utilizando el servidor SMTP de Gmail.

## Requisitos
Para este tutorial necesitarás:
1. [Un entorno ya configurado para Flask](http://myrefactor.com/es/posts/python-y-flask:-introducci%C3%B3n-paso-a-pso)
2. [Un formulario de contacto](http://myrefactor.com/es/posts/formulario-de-contacto-con-email-in-flask)
3. Una cuenta de Gmail

## Instalación de dependencias, Flask-Mail
Primero, necesitamos instalar la extensión `Flask-Mail` usando **pip**:

````commandline
pip install Flask-Mail
````

## Configuración de Flask
A continuación, configuraremos Flask para usar el SMTP de Gmail, estableceremos `MAIL_SERVER` y `MAIL_PORT` en los valores apropiados para Gmail, estoy usando un archivo `config` como configuración de Flask.

````python
class Config(object):
    # more settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'example@gmail.com'
    MAIL_PASSWORD = '*******'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
````
A continuación, configuraremos Flask para usar una instancia de `Mail` de la extensión `Flask-Mail`:

````python
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
mail = Mail(app)
````

Alternativamente, puede configurar su instancia de `Mail` más tarde en el momento de la configuración, utilizando el método **init_app**:

````python
mail = Mail()

app = Flask(__name__)
mail.init_app(app)
````

## Enviando correos electrónicos
Con la aplicación configurada, ahora podemos crear una ruta que manejará el envío del correo electrónico:

````python
@blog_bp.route("/contact", methods=['GET', 'POST'])
def contact_us():
    contact_form = ContactForm(request.form)
    if request.method == 'POST' and contact_form.validate():
        # Process the contact information here.
        msg = Message('Test Email', sender='youremail@gmail.com', recipients=['recipient@example.com'])
        msg.body = "Hello, this is a test email sent from a Flask app using the Gmail SMTP server."
        mail.send(msg)
        flash('Thanks for contact us!')
    return render_template('contact.html', form=contact_form)
````
Este código crea una ruta llamada `/contact`, que maneja las solicitudes POST para el formulario de contacto. Además, crea un nuevo objeto `Message` utilizando la biblioteca `Flask-Mail` y establece el remitente, los destinatarios y el cuerpo del mensaje. Finalmente, el mensaje se envía llamando a **mail.send()**.

## Solución de problemas
Si no lo ha hecho anteriormente, es posible que necesite una configuración específica para su aplicación. Intente enviar un correo electrónico siguiendo el paso descrito aquí. Obtuve el error:
````línea de comandos
SMTPAuthenticationError (código, respuesta)
smtplib.SMTPAuthenticationError: (534, b'5.7.9 Se requiere contraseña específica de la aplicación...
````
La solución es configurar dispositivos que no admitan la verificación en dos pasos, como se explica en [Contraseñas de aplicaciones de Google](https://support.google.com/accounts/answer/185833?visit_id=638093857819222551-1157742139&p=InvalidSecondFactor&rd=1).

## Conclusión
En resumen, aprendimos en esta publicación cómo enviar correos electrónicos desde una aplicación Flask es una funcionalidad fácil y útil gracias a la biblioteca `Flask_Mail`, solo necesita configurar la aplicación para usar el servidor SMTP de Gmail, crear un formulario simple y enrutarlo a una función de vista que realmente envía el correo electrónico.