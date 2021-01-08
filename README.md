docker-compose exec -T mysql-development mysql -uroot -ppassword pedal_dev_v_0 < ../pedal_20191209.sql

docker-compose exec  mysql-development mysql -uroot -ppassword



mysql -h localhost -P 32000 --protocol=tcp -u root -p


clean unused volumes
	docker volume prune

remove container and associated volumes
	docker rm -v [container]


~~~~~~~~~~~~~~~~~~~

The app will fail unless Secrets/creds.json is created (in root dir of the app).

creds.json holds the client_id for fence.

{
    "CLIENT_ID":""
}
