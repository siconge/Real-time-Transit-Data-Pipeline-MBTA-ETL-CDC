FROM mysql:8.0

ENV MYSQL_DATABASE=MBTAdb \
    MYSQL_ROOT_PASSWORD=MyNewPass

# Copy the file mbta.sql from the host's build context into the `/docker-entrypoint-initdb.d` directory inside the container, so it is automatically executed to initialize the database with schema and data
ADD mbta.sql /docker-entrypoint-initdb.d

EXPOSE 3306