#!/bin/bash
python manage.py migrate
python manage.py makemigrations api
python manage.py migrate api

