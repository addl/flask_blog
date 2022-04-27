Flask deployment with uWSGI and Nginx

## Create User in VPS
Follow this article:
https://phoenixnap.com/kb/create-a-sudo-user-on-debian

## Installation of packages
```commandline
sudo apt-get install python3-venv uwsgi uwsgi-plugin-python3 uwsgi-src python3-pip python3-dev libpq-dev
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

## CReate deamon with UWsgi emperor mode
```commandline
sudo cp /home/myrefactor/flask_blog/myrefactor.ini /etc/uwsgi/apps-available/myapp.ini
$ sudo ln -s /etc/uwsgi/apps-available/myrefactor.ini /etc/uwsgi/apps-enabled/myrefactor.ini
```
nce it is enabled, start emperor mode:
```commandline
sudo uwsgi --emperor /etc/uwsgi/apps-enabled/
```
##Start on Machine Start-up
The best part about running uWSGI in emperor mode is we can have our apps launch upon machine startups without writing any services. Add a file called /etc/rc.local and include the following:
```commandline
/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites-enabled --daemonize /var/log/uwsgi-emperor.log
```
restart your vps and confirm

## Elastic search

## Install elastic
```commandline
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.16.3-amd64.deb
sudo dpkg -i elasticsearch-7.16.3-amd64.deb
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
sudo service elasticsearch start
sudo service elasticsearch status
```
Onc ES is runnig, we need to make sure our app will work.
By default indexes are not created in Elasticsearch, so if you are using ES and try to store data in ES, you might want to create indexes before sending data to ES or to tell ES to create indexes automatically. I would prefer to create indexes automatically:

## Updating app
In case you need to update your app.you will need to restart uwsgi
```commandline
sudo systemctl restart uwsgi
```

## create upload foler
We need to create a folder to store the uploaded files
```commandline
mkdir /home/myrefactor/uploads
```
### Asign permission
```commandline
sudo chmod -R 777 /home/myrefactor/uploads
```