FROM python:3-slim
LABEL maintainer="Kelvin Li<kelvin.li@memodir.com>"
EXPOSE 9000

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code/src:/code/ \
    DJANGO_SETTINGS_MODULE=django_project.settings \
    LIBRARY_PATH=/lib:/usr/lib \
    INSTALL_PATH=/code
    
RUN mkdir $INSTALL_PATH

WORKDIR $INSTALL_PATH

#COPY . $INSTALL_PATH/
COPY requirements* .docker/app/docker-entrypoint.sh  $INSTALL_PATH/
ADD staticfiles/templates $INSTALL_PATH/static/templates
ADD staticfiles/dist/webpack-stats.json $INSTALL_PATH/staticfiles/dist/
ADD django_project $INSTALL_PATH/django_project
ADD locale $INSTALL_PATH/locale
ADD logs $INSTALL_PATH/logs
ADD src $INSTALL_PATH/src

RUN python3 -m pip install -r requirements.txt -r requirements-devel.txt --no-cache-dir

ENTRYPOINT ["/code/docker-entrypoint.sh"]
