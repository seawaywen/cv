# cv

# Docker management 
### pull a postgres docker 
$ docker pull postgres

### start a postgres docker
$ docker run -i -t -p 5432:5432 postgres

### attach a shell to the docker instance
$ docker exec -it inst-name /bin/bash

### connect to the dock postgres via psql
$ psql -h localhost -p 5432 -U postgres


# DB operation
### init database with all migrations applied
$ make setup-db

### stop database (keep the data)
$ make stop-db

### start database
$ make start-db

### terminate the database
$ make destroy-db

### create a super user
$ make createsuperuser


# FrontEnd
Use the webpack to buuild the asset

$ yarn run build

if you need the build automatically with the file changes 
$ yarn run watch