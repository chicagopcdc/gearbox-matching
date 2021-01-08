docker-compose exec -T mysql-development mysql -uroot -ppassword pedal_dev_v_0 < ../pedal_20191209.sql

docker-compose exec  mysql-development mysql -uroot -ppassword



mysql -h localhost -P 32000 --protocol=tcp -u root -p


clean unused volumes
	docker volume prune

remove container and associated volumes
	docker rm -v [container]


~~~~~~~~~~~~~~~~~~~

config.env sets the environment (set as test).
The env defaults to "dev" if not otherwise set.
Again, the config is set as "test" in the repo, but will default to "dev" if this is removed.

CRUD tests can be run from the app container:

shell into container:
"docker-compose exec app sh"

start pipenv:
"pipenv shell"

run tests:
"pytest"

Tests use (and require) the pre-set data, in db/pedal_populate.sql

Tests reference the data set in this way.
New data is created in the tests themselves,
but the data is flushed from the session at the end of the tests.

Some tables use the "code" field, which can be used as a lookup code.
Those that do not have "code" use primary keys, packages as dash separated ids (int) (format is {}-{}-...).

~~~~~~~~~~~~~~~~~~~

The app container will fail/crash unless Secrets/creds.json is created (in root dir of the app).

creds.json holds the client_id for fence.

{
    "CLIENT_ID":""
}
