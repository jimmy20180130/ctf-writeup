#!/bin/bash

# Start MariaDB
service mariadb start

# Wait for MariaDB to be ready
until mysqladmin ping -h localhost --silent; do
    echo 'waiting for mariadb to be connectable...'
    sleep 1
done

# Initialize Database
mysql -u root < /opt/init.sql

# Run PHP Seed Script
php /opt/seed.php

# Start Apache in foreground
source /etc/apache2/envvars
exec apache2 -D FOREGROUND
