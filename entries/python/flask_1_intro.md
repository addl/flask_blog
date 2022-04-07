## Requirements
1. PyCharm installed
2. Python installed

## Virtual environments
Use a virtual environment to manage the dependencies for your project, both in development and in production.

### What problem does a virtual environment solve?

The more Python projects you have, the more likely it is that you need to work with different versions of Python libraries, or even Python itself. Newer versions of libraries for one project can break compatibility in another project.

Virtual environments are independent groups of Python libraries, one for each project. Packages installed for one project will not affect other projects or the operating system’s packages.

### Create an environment
Usually virtual environments are created inside the project's folder. Example: if your project folder is 'flask_application', then the virtual environment folder is located inside it, supposing virtual environment folder is 'my_venv' you will end up having the following structure:

```
flask_application/my_venv
```
In order to create the virtual environment, let's run the following commands:
```commandline
$ mkdir flask_application
$ cd flask_application
$ python3 -m venv my_venv
```
In case you are using Windows:
```commandline
> mkdir flask_application
> cd flask_application
> py -3 -m venv my_venv
```
Above we first create project's folder, then we move into the folder and lastly we crate the virtual environment 'my_venv'.

### Activating the virtual environment
We need to activate the just created virtual environment, otherwise we will use the global python interpreter, and we need to use the one inside the virtual environment right? So to activate 'my_venv' we just need to:
```commandline
$ source my_venv/bin/activate
```
or, if you are using Windows
```commandline
my_venv\Scripts\activate
```

## Using PyCharm
Setting up virtual environment and installing dependencies using an IDE like PyCharm makes your life a lot easier, let's get to it

### Creating a project
Open PyCharm and press the button 'New Project', you should see the following screen:
![New Project using PyCharm](https://drive.google.com/uc?id=1YSU-W6Xtxp7KZx3looLXfUNWWGzWY-Zc)

From the picture, you can see the project folder and also PyCharm is suggesting to create a virtual environment automatically, it has also identified the Python version installed in the system. Click in 'Create' button.

## Installing Flask
With 'my_venv' activated, if you install a python package using **pip**, the package will be installed automatically inside our virtual environment: 'my_venv', let's install Flask with the following command:
```commandline
pip install Flask
```

