# Installation

## Using a virtual environment to install dependencies

Using the `venv` module that is now part of the standard library (python 3.3+).
Might not be installed in some Linux distros and in that case `sudo apt-get install python3-venv` should do it for Ubuntu.

```sh
# creating the virtual env
$ python3 -m venv <your_env_dir>
# activating the environment
$ source <your_env_dir>/bin/activate
```

## Installing dependencies

```sh
$ pip install -r requirements.txt
```

# Db migration

The configured database is sqlite (just for demonstration purposes)

```sh
$ python manage.py migrate
# create an administrator account
$ python manage.py createsuperuser --email admin@example.com --username admin
```

# Run the tests

```sh
$ python manage.py test
```

# Run the app

```sh
$ python manage.py runserver
```

This project is using the Django's REST framework api view, so it has also an html ui at `localhost:8000/loans`.

The `admin` has access to everything but it's possible to create other users and
play around with the permissions by accessing `localhost:8000/admin`
