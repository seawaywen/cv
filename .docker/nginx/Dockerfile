FROM nginx
MAINTAINER Kelvin Li
EXPOSE 80

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir /static

ADD .docker/nginx/memodir.conf /static/
COPY staticfiles/ /static/

RUN cp /static/memodir.conf /etc/nginx/conf.d/
RUN rm /static/memodir.conf
