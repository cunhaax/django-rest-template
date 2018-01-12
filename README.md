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


# Development

Starting the project for development.

```sh
$ python manage.py migrate
```
