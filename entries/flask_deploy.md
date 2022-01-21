Flask deployment with uWSGI and Nginx

## Create User in VPS
Follow this article:
https://phoenixnap.com/kb/create-a-sudo-user-on-debian

## Installation of packages
```commandline
sudo apt-get install python3-venv uwsgi uwsgi-src python3-pip python3-dev libpq-dev
```

## Create VENV and installing dependencies
Move into the project folder:
```commandline
cd flask_blog
```
ANd create the venv and install dependencies:
```commandline
python3 -m venv flask-env
...
source flask-env/bin/activate
...
python3 -m pip install -r requirements.txt
```

## Trying to run the app
```commandline
uwsgi --http-socket :5000 --plugin python3 --module app:app --virtualenv /home/myrefactor/flask_blog/flask-env/
```

## Installing PostgresSql
Refer to another post

## Setting up DB
With venv activated:
```commandline
flask db init
flask db migrate
flask db upgrade
```

## Setting up wsgi
```commandline
[uwsgi]
chdir = /home/myrefactor/flask_blog/
module = app:app

plugin = python3
virtualenv = /home/myrefactor/flask_blog/flask-env/

master = true
socket = /home/myrefactor/myrefactor.sock
chmod-socket = 666
vacuum = true

die-on-term = true
```
vacuum = true will removed the socket when the process is finished or we exit it by pressing Ctrl + C.
That's much better. As an added bonus, the presence of die-on-term = true in our config means that our uWSGI process will end when we Control+C, for convenience's sake.

## Running the app
```commandline
uwsgi flask_blog/myrefactor.ini
```

## Setting up nginx with project config file
You should have Nginx installed. Cretae a config file for our project
```commandline
sudo nano /etc/nginx/sites-available/myrefactor
```
Put inside this file the following:
```commandline
server {
    listen 80;
    server_name 161.35.103.255;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:///home/myrefactor/myrefactor.sock;
    }
}

```

Save and close the file when you’re finished.

To enable the Nginx server block configuration you’ve just created, link the file to the sites-enabled directory:
```
sudo ln -s /etc/nginx/sites-available/myrefactor /etc/nginx/sites-enabled
```
With the file in that directory, you can test for syntax errors by running the following:

```sudo nginx -t```

If this returns without indicating any issues, restart the Nginx process to read the new configuration:

```sudo systemctl restart nginx```

You should now be able to navigate to your server’s domain name in your web browser:

```http://161.35.103.255```