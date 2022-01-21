
## Installing packages
```commandline
sudo apt install postgresql postgresql-contrib
```

By installing postgresql a new user is added to the system 'postgres', this is the super userof the database. Login as postgres:
```commandline
sudo su - postgres
```
PSQL is the postgres language, using it we can create DB, users, etc
```commandline
psql
```
You can also enter directly to psql:
```commandline
sudo -u postgres psql
```
## creating DB
```commandline
create database mydb;
create user myuser with encrypted password 'mypass';
grant all privileges on database mydb to myuser;
```
To confirm the atabase was created successfully, run the following:
```commandline
\l
```
The result:
```commandline
                                  List of databases
    Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
------------+----------+----------+-------------+-------------+-----------------------
 flask_blog | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 postgres   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
            |          |          |             |             | postgres=CTc/postgres
 template1  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
            |          |          |             |             | postgres=CTc/postgres

```
## creating users
```commandline
create user pguser with encrypted password 'pguser';
```
After creating an user we need to assign permission to access to our database:
```commandline
grant all privileges on database flask_blog to pguser;
```
Confirming our user 'pguser' has access to the database 'flask_blog'
```commandline
                                  List of databases
    Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
------------+----------+----------+-------------+-------------+-----------------------
 flask_blog | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =Tc/postgres         +
            |          |          |             |             | postgres=CTc/postgres+
            |          |          |             |             | pguser=CTc/postgres
 postgres   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
            |          |          |             |             | postgres=CTc/postgres
 template1  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
            |          |          |             |             | postgres=CTc/postgres

```
In the last column, notice how 'pguser=CTc/postgres' is listed in the row for 'flask_blog', so we are good.

## Switching Databases
Most Postgres servers have three databases defined by default: template0, template1 and postgres. template0 and template1 are skeleton databases that are or can be used by the CREATE DATABASE command. postgres is the default database you will connect to before you have created any other databases. Once you have created another database you will want to switch to it in order to create tables and insert data. Often, when working with servers that manage multiple databases, you’ll find the need to jump between databases frequently. This can be done with the \connect meta-command or its shortcut \c.
```commandline
postgres=# \c flask_blog
You are now connected to database "flask_blog" as user "postgres".
flask_blog=#
```
## Listing Tables
Once you’ve connected to a database, you will want to inspect which tables have been created there. This can be done with the \dt meta-command. However, if there are no tables you will get no output.

```commandline
flask_blog=# \dt
             List of relations
 Schema |       Name       | Type  | Owner
--------+------------------+-------+--------
 public | alembic_version  | table | pguser
 public | post             | table | pguser
 public | post_tag         | table | pguser
 public | post_translation | table | pguser
 public | subscriptor      | table | pguser
 public | tag              | table | pguser
 public | user             | table | pguser
(7 rows)
flask_blog=#
```

## Executing .SQL files
We might want to execute an SQL file to put some basic data into databases, for example one user.
To execute an SQL log in and connect to database:
```commandline
\c flask_blog
\i /home/user/folder/file.sql
```

### Another option could be:
```commandline
psql pguser -h 127.0.0.1 -d flask_blog -f /path/to/file.sql
```

Done!