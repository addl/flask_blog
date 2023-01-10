## Introduction
FlaskForm is a powerful library that allows you to easily create and validate forms in your Flask application. It integrates seamlessly with the Jinja2 templating engine, so you can use it to pass form data to your templates and render the forms in your HTML pages.

To use FlaskForm in your Flask application, you will first need to install it using pip:
````commandline
pip install wtforms
````

## Creating the form
You will need to create a form class in your Python code. For example, here is a simple contact form with a name, email, and message field:
````python
class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[
        DataRequired(), Email(granular_message=True)])
    message = TextAreaField(label='Message',  validators=[DataRequired()])
````
The `StringField` and `TextAreaField` classes represent input fields for text data, and the validators module provides various validator functions that can be used to ensure that the user's input is valid. In this example, we are using the `DataRequired` validator to ensure that the user enters a value for each field, and the `Email` validator to ensure that the email field contains a valid email address.

## Creating the view and routing URL
We need to create a route function to show the form page and validate it using the validate method of the form object:
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
In the above view, when the HTTP method is GET we show the form, otherwise, if the HTTP method is POST we proceed with validation and processing the information sent by the user.

Our view name is `contact_us` and will be executed if the URL is `/contact`, this information is important to set up the form on the HTML template.

## Setting up the HTML template
To render the form in your template, you will need to pass the form object to the template context and render it using Jinja2 syntax. For example:
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
In the above example, the form fields and labels will be rendered in your HTML page. 

One important property in forms is the information for errors note how we ask whether we have errors in any field or not with `{% if form.errors %}`, if so, we iterate through all of them and show the error's message.
When the user submits the form, the data will be sent to the `/contact` route in your Flask application, as we use `url_for` to create the form action: `action="{{ url_for('contact_us') }}"`.

## Common issues
If you see the following error once you execute the application:
````commandline
Exception: Install 'email_validator' for email validation support.
````
It is related to a dependency in `wtforms/validators.py` file, in line 9:
````python
import email_validator
````

So we need to install the package `email_validator`, with pip run:
````commandline
pip install email_validator
````

Now it should run with no errors.

## Conclusion
FlaskForm is a useful library for creating and validating forms in a Flask application. It integrates seamlessly with Jinja2, allowing you to easily render forms in your templates and handle form data in your routes

Happy code!
