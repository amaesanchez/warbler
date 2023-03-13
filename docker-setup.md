Docker Setup
============

Run docker-compose & start app
---------------------------------
To setup containers:
    1. `docker compose build --no-cache`
    2. `docker compose up -d`
or
    `docker compose up`

To start the app you will need to connect to `localhost:8000`

Check docker database container in terminal
----------------------------------------------
To open psql in container environment:
    `docker exec -it [database container name] psql -U postgres`

In our case, database container name is `db` and `postgres` is our POSTGRES_USER defined in docker-compose.yml.

Confirm that `warbler` database is present with `\l`.

Testing
-------
To run test you will need to connect to the cli of the webserver container.
    `docker exec -it warbler bash`

From here you should be able to run the unittest commands.

Note: you may need to create the test db beforehand to successfully run the tests. See above.

Shutdown
-------
To shut down the containers (best practice if you are running a different dockerized project):
`docker-compose down --volumes`

Troubleshooting
---------------
If the `db` database is not seeded in docker psql, or any Flask operation querying the database throws an internal server error on the browser, try the following commands to redo container setup:

To list running containers:
    `docker ps`

To stop all containers related to numsapi:
    `docker stop [container id]`

To remove all stopped containers:
    `docker container prune` (Type `y` when prompted to confirm)

To stop and remove related volumes in docker-compose.yml
    `docker-compose down --volumes`

To check if volumes have been removed:
    `docker volume ls`
If there are still volumes, run:
    `docker volume prune` (Type `y` when prompted to confirm)

Rerun docker-compose.yml:
    `docker compose build --no-cache` - builds fresh version that disregrads previous caches
