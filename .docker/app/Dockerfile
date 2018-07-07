FROM python:3-slim
MAINTAINER Kelvin Li
EXPOSE 9000

RUN mkdir /code

WORKDIR /code

ADD requirements*.txt /code/

RUN pip install -r requirements.txt -r requirements-devel.txt

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code/src:/code/ \
    DJANGO_SETTINGS_MODULE=django_project.settings

ADD . /code/

ENTRYPOINT ["/code/.docker/app/docker-entrypoint.sh"]