docker build . -t doc-flask:v1

docker run -p 5000:5000 doc-flask:v1




DB connection for local DEV env
CREATE USER 'pcdc'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON pedal_dev_v_0 . * TO 'pcdc'@'localhost';
flush privileges;
SHOW GRANTS FOR 'pcdc'@'localhost';

CREATE USER 'pcdc_dev'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON pedal_dev_v_0 . * TO 'pcdc'@'%';


CREATE USER 'newuser'@'%' IDENTIFIED BY 'newpassword';
GRANT ALL PRIVILEGES ON pedal_dev_v_0.* to 'pedal'@'%';