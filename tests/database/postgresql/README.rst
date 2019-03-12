Tests and demos that use PostgreSQL as datasource requires user and database tables created by the following scripts.

Setting up PostgreSQL docker database
------------------------------------------------
If you already have PostgreSQL database running, skip to 'Creating User and Tables'.
Following are steps on setting up PostgreSQL docker to run included tests and demos. It is not steps on setting up Postgresql for production use.
Before executing the following command, docker must be installed and setup.
Instruction on how to install docker is available from the following site. From the left side menu, select 'Get Docker', 'Docker CE', and then select the OS that you are using.
https://docs.docker.com/

If you have not yet setup docker network, execute the following command. Setting up a docker network will enable to have a static ip address for PostgreSQL database.

- to setup docker network (to have static ip address) NOTE: this step is unnecessary if docker network is already setup during MySQL installation
    docker network create --subnet=172.18.0.0/16 agatenetwork

- to setup postgresql database
    docker run --net agatenetwork --ip 172.18.0.4 --name postgresql-11.2 -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -d postgres:11.2

- to connect:
    docker run --net agatenetwork -it --rm --link postgresql-11.2:postgres postgres psql -h postgres -U postgres

After logging in to PostgreSQL, execute sql commands to create users and database tables.

Starting and Stopping Docker PostgreSQL Container
------------------------------------------------------------
- to stop:
    docker stop postgresql-11.2

- to start:
    docker start postgresql-11.2

Creating User and Tables
-----------------------------------
Execute scripts in the following order after connecting to Postgres.
    1. create database schema.
        `create_schema.sql <./create_schema.sql>`_
    2. create test user 'python' with all privileges to database 'agatereports'.
        `create_user.sql <./create_user.sql>`_
    3. create database tables:
        - `create_address.sql <./create_address.sql>`_
        - `create_document.sql <./create_document.sql>`_
        - `create_orders.sql <./create_orders.sql>`_
        - `create_product.sql <./create_product.sql>`_
        - `create_tasks.sql <create_tasks.sql>`_
    4. grant privileges to access the tables by the user
        - `grant_priv_to_user.sql <./grant_priv_to_user.sql>`_

END
