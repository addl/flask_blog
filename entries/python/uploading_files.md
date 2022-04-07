# Uploading Files to the server with Flask

## Path Configuration
We need to tell flask where to store the files that areuploaded to the server

```
...
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://pguser:postgres@127.0.0.1:5432/flask_blog'
    UPLOAD_FOLDER = '/home/lion/Public'
...
```

Why do we limit the extensions that are allowed? You probably don’t want your users to be able to upload everything there if the server is directly sending out the data to the client. That way you can make sure that users are not able to upload HTML files that would cause XSS problems (see Cross-Site Scripting (XSS)). Also make sure to disallow .php files if the server executes them, but who has PHP installed on their server, right?


## Updating the WTForm

```
...
file_content = FileField('Select file content')
...
```

## Updating the HTML page with the form and the new file
```
...
<form method="POST" action="{{ url_for('POST_BP.create_post') }}" enctype="multipart/form-data">
...
{{ form.file_content.label }} {{ form.file_content }}
...
```
## Changing the view function to validate and accept the file
```
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file_content' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_content = request.files['file_content']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file_content.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file_content and allowed_file(file_content.filename):
            filename = secure_filename(file_content.filename)
            file_content.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect('/')
```

## Testing the app