FROM python:3-slim
MAINTAINER Kelvin Li <kelvin.li@memodir.com>
EXPOSE 9000

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code/src:/code/ \
    DJANGO_SETTINGS_MODULE=django_project.settings \
    LIBRARY_PATH=/lib:/usr/lib \
    INSTALL_PATH=/code

RUN mkdir $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY . $INSTALL_PATH/

RUN python3 -m pip install -r requirements.txt -r requirements-devel.txt --no-cache-dir

ENTRYPOINT ["/code/.docker/app/docker-entrypoint.sh"]