# Debugging Flask Applications

CReate app.py only for this purpose

```
from flask_blog_app import create_app

APP = create_app()

if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=5000, debug=True)
    APP.run(debug=True)
```

Create a configuration excecution for PyCharm, select the 'app.py' file

Debug!!
