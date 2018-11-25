# Certificate Generator Server

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/06bd6acff9cd4506985192596642ef5f)](https://www.codacy.com/app/JBossOutreach/certificate-generator-server?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JBossOutreach/certificate-generator-server&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/JBossOutreach/certificate-generator-server.svg?branch=master)](https://travis-ci.org/JBossOutreach/certificate-generator-server)

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

- Setup environmental variables using:

```sh
cp .env.sample .env
```

Now edit .env fill the generated `.env` file with your credentials to run it locally.

## Database 

For the Database to be used(in Production),
you can export the connection url in `DATABASE_URL`,
eg,
```sh
$ export DATABASE_URL=postgres://postgres:mysecretpassword@127.0.0.1:5432/test
```

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

## License

This project is currently licensed under the **[GNU General Public License v3](LICENSE.md)**.
i.e we guarantee end users the freedom to run, study, share and modify the software.

> To obtain the software under a different license, please contact [JBossOutreach](https://gitter.im/JBossOutreach/gci).
