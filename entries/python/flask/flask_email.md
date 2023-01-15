## Intoduction
Sending emails from a Flask application can be a useful feature for a variety of use cases, such as sending confirmation emails, password reset emails, and more. In this article, we will go over how to send emails from a Flask application using the Gmail SMTP server.

## Requirements
For this tutorial you will need:
1. [A environment already set up for Flask](http://myrefactor.com/en/posts/python-and-flask:-introduction-step-by-step)
2. [An already contact form](http://myrefactor.com/en/posts/flask-contact-form-email-example)
3. Gmail account

## Installing dependencies, Flask-Mail
First, we need to install the extension `Flask-Mail` using **pip**:
````commandline
pip install Flask-Mail
````

## Flask configuration
Next, we will configure Flask to use the Gmail SMTP, set the `MAIL_SERVER` and `MAIL_PORT` to the appropriate values for Gmail, I am using a `config` file as Flask configuration.

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
Next, we will configure Flask to use a `Mail` instance from the `Flask-Mail` extension:

````python
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
mail = Mail(app)
````

Alternatively you can set up your `Mail` instance later at configuration time, using the **init_app** method:
````python
mail = Mail()

app = Flask(__name__)
mail.init_app(app)
````

## Sending emails
With the app configured, we can now create a route that will handle sending the email:
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
This code creates a route called `/contact`, which handles the POST requests for the contact form. In addition, it creates a new `Message` object using the `Flask-Mail` library, and sets the sender, recipients, and message body. Finally, the message is sent by calling **mail.send()**.

## Troubleshooting
If no have done previously, you might require a specific setting for your application. Try to send an email following the step described here I got the error:
````commandline
SMTPAuthenticationError(code, resp)
smtplib.SMTPAuthenticationError: (534, b'5.7.9 Application-specific password required ...
````
The solution is to set up devices that don't support 2-Step Verification, as explained in [Google App Passwords](https://support.google.com/accounts/answer/185833?visit_id=638093857819222551-1157742139&p=InvalidSecondFactor&rd=1).

## Conclusion
In summary, we learned in this post how sending emails from a Flask app is an easy and useful functionality thanks to the `Flask_Mail` library, you just need to configure the app to use the Gmail SMTP server, create a simple form and route it to a view function that actually sends the email.
