FROM python:3.6.8-alpine as base

FROM base as build
RUN apk add postgresql-dev python3-dev musl-dev gcc --no-cache
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt                                                                                       
RUN pip install --install-option="--prefix=/install" -r /requirements.txt


FROM base
RUN apk --no-cache add libpq

RUN adduser -S cert-gen
USER cert-gen
WORKDIR /home/cert-gen

COPY --from=build /install /usr/local
COPY --chown=cert-gen:root . .
RUN python manage.py makemigrations api
RUN python manage.py migrate

EXPOSE 8000
CMD [ "python","manage.py","runserver"]
