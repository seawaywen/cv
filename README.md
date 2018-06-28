# cv

# Dockered Postgres db management 
## pull a postgres docker 
$ docker pull postgres

## start a postgres docker
$ docker run -i -t -p 5432:5432 postgres

## attach a shell to the docker instance
$ docker exec -it inst-name /bin/bash

## connect to the dock postgres via psql
$ psql -h localhost -p 5432 -U postgres


# DB operation
## init database with all migrations applied
$ make setup-db

## stop database (keep the data)
$ make stop-db

## start database
$ make start-db

## terminate the database
$ make destroy-db

## create a super user
$ make createsuperuser


# FrontEnd
## Install and manage the Node
Use nvm to manage the different node version
Install the long term support version node:
$ nvm install node --lts
Display all installed node version
$ nvm list
Use the specfic version
$ nvm use v10.3.0

## Install the required packages
$ yarn

## Use the webpack to build the asset
$ yarn run build

if you need the build automatically with the file changes 
$ yarn run watch

A task is defined to run the build with the running server
$ yarn dev


# Use the docker start service
$ docker-compose up [--build]

## some useful commands:
$ docker container exec -it cv_web_1 bash
$ docker rmi `docker images -q -f dangling=true`
