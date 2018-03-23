# cv

# start a postgres docker
docker run -i -t -p 5432:5432 postgres


# connect to the dock postgres via psql
psql -h localhost -p 5432 -U postgres

# create a super user
make manage ARGS='createsuperuser'