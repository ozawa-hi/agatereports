Tests and demos that use MySQL as datasource requires user and database tables created by the following scripts.


Setting up MySQL docker database
----------------------------------
| If you already have MySQL database running, skip to 'Creating User and Tables'.
| Following are steps on setting up MySQL docker to run included tests and demos. It is not steps on setting up MySQL for production use.
| Before executing the following command, docker must be installed and setup.
| Instruction on how to install docker is available from the following site. From the left side menu, select 'Get Docker', 'Docker CE', and then select the OS that you are using.
| https://docs.docker.com/

If you have not yet setup docker network, execute the following command. Setting up a docker network will enable to have a static ip address for MySQL database.

- to setup docker network (to have static ip address)
    docker network create --subnet=172.18.0.0/16 agatenetwork

- to setup mysql database:
    docker run --net agatenetwork --ip 172.18.0.2 --name mysql-5.7.24 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7.24

- to connect:
    docker exec -it mysql-5.7.24 bash

- to login to mysql:
    mysql -u root -p

After logging in to mysql, execute sql commands to `Creating User and Tables`_

Starting and Stopping Docker MySQL Container
------------------------------------------------
- to stop:
    docker stop mysql-5.7.24

- to start:
    docker start mysql-5.7.24

Creating User and Tables
------------------------
Execute scripts in the following order after connecting to MySQL. 
    1. create database schema.
        `create_schema.sql <./create_schema.sql>`_
    2. create test user 'python' with all privileges to database 'agatereports'.
        `create_user.sql <./create_user.sql>`_
    3. create database tables:
        - `create_address.sql <./create_address.sql>`_
        - `create_document.sql <./create_document.sql>`_
        - `create_orders.sql <./create_orders.sql>`_
        - `create_product.sql <./create_product.sql>`_
        - `create_tasks.sql <./create_tasks.sql>`_
	4. run Python script to create table 'pictures' with a blob field containing jpg image data
        - `create_pictures.py <./create_pictures.py>`_

END
