FROM nginx
MAINTAINER Kelvin Li <kelvin.li@memodir.com>
EXPOSE 80

RUN rm /etc/nginx/conf.d/default.conf; \
    rm /etc/nginx/nginx.conf; \
    mkdir /static

COPY .docker/nginx/* /static/
COPY staticfiles/ /static/

RUN cp /static/memodir.conf /etc/nginx/conf.d/; \
    cp /static/nginx.conf /etc/nginx/; \
    rm /static/memodir.conf; \
    rm /static/nginx.conf
