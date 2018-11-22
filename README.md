# Certificate Generator Server

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/06bd6acff9cd4506985192596642ef5f)](https://www.codacy.com/app/JBossOutreach/certificate-generator-server?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JBossOutreach/certificate-generator-server&amp;utm_campaign=Badge_Grade)

An automatic certificate generator for events according to multiple input files like csv, xlsx, numbers and shoot emails with generated certificates.

## Setting up environment

- Install pipenv

```sh
pip install pipenv
```

- Create a pipenv

```sh
pipenv shell
```

As soon as the shell is ready,

- Run the following command to install the dependencies

```sh
pipenv install
```

The above command install all the dependencies.

- Create .env file with
  - SECRET_KEY
  - DEBUG
  - ALLOWED_HOSTS (separated by comma)

Check [Sample .env file](.env.sample)

## Running

```sh
python manage.py migrate
python manage.py makemigrations api
python manage.py migrate
python manage.py runserver
```

To stop the server, press `Ctrl + C` and deactivate the virtual environment using `deactivate` command.

## Post setup instructions

Instead of adding new dependencies to requirements.txt, simply run:

```sh
pipenv install <package-name>
```

to install it inside pipenv and add it to Pipfile.

To lock the dependencies for deployment, run:

```sh
pipenv lock
```
