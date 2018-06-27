FROM python:3-slim
MAINTAINER Kelvin Li
#EXPOSE 9000

RUN mkdir /code
WORKDIR /code

ADD requirements*.txt /code/
RUN pip install -r requirements.txt -r requirements-devel.txt


ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code/src:/code/
ENV DJANGO_SETTINGS_MODULE django_project.settings
#ENV DATABASE_URL postgres://postgres@db/postgres

ADD . /code/

#CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
ENTRYPOINT ["./docker-entrypoint.sh"]