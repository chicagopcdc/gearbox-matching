docker-compose exec -T mysql-development mysql -uroot -ppassword pedal_dev_v_0 < ../pedal_20191209.sql

docker-compose exec  mysql-development mysql -uroot -ppassword



mysql -h localhost -P 32000 --protocol=tcp -u root -p


clean unused volumes
	docker volume prune

remove container and associated volumes
	docker rm -v [container]