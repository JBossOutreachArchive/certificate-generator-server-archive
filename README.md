# Certificate Generator Server

An automatic certificate generator for events according to multiple input files like csv, xslx, numbers and shoot emails with generated certificates.

## Setting up environment

- Install virtual environment

```sh
pip install virtualenv
```

- Create a virtual environment named env using the following command

```sh
virtualenv env -p python3
```

- To activate the virtual environment in Windows, run:

```sh
env\Scripts\activate.bat
```

- To activate the virtual environment in Linux or MacOS, run:

```sh
source env/bin/activate
```

- Run the following command to install the dependencies

```sh
pip install -r requirements.txt
```

- Create .env file with
  - SECRET_KEY
  - DEBUG
  - ALLOWED_HOSTS (separated by comma)

Check [Example .env file](.env.sample)

## Running

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

To stop the server, press `Ctrl + C` and deactivate the virtual environmenat using `deactivate` command.
