## Reference
https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-debian-10

## Installing nginx and ufw
```commandline
sudo apt install ufw nginx
```
## Enabling nginx in firewall
List the application configurations that ufw knows how to work with by typing:

```sudo ufw app list```
 
You should get a listing of the application profiles:

```
Available applications:
...
  Nginx Full
  Nginx HTTP
  Nginx HTTPS
...
```

You can enable HTTP (Https for another entry) by typing:
```sudo ufw allow 'Nginx HTTP'```

To verify if nginx is running and the port 80 is open, you can point your web browser to the address of your vps:
```commandline
http://161.35.103.255/
```
And a nginx welcome message should be visualized:
```
Welcome to nginx!
If you see this page, the nginx web server is successfully installed and working. Further configuration is required.

For online documentation and support please refer to nginx.org.
Commercial support is available at nginx.com.

Thank you for using nginx.
```

## Managing nginx server
Let's check the status of nginx
```commandline
systemctl status nginx
```
the output should be similar to:
```commandline
● nginx.service - A high performance web server and a reverse proxy server
   Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2022-01-21 08:40:32 UTC; 8min ago
     Docs: man:nginx(8)
 Main PID: 15563 (nginx)
    Tasks: 2 (limit: 2377)
   Memory: 3.5M
   CGroup: /system.slice/nginx.service
           ├─15563 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
           └─15565 nginx: worker process
```
> Alternative you could use 'systemctl' to **stop**, **start** or **restart** your server:
```commandline
systemctl restart nginx
```

## Setting up nginx with project config file
Cretae a config file for our project
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

If you encounter any errors, try checking the following:

sudo less /var/log/nginx/error.log: checks the Nginx error logs.
sudo less /var/log/nginx/access.log: checks the Nginx access logs.
sudo journalctl -u nginx: checks the Nginx process logs.
sudo journalctl -u myproject: checks your Flask app’s uWSGI logs.