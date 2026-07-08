FROM php:8.2-apache

# Install MariaDB server + csvtool
RUN apt-get update && apt-get install -y --no-install-recommends \
    mariadb-server \
    csvtool \
    && rm -rf /var/lib/apt/lists/*

# Enable PHP mysqli extension
RUN docker-php-ext-install mysqli

# SUID on csvtool — privesc vector
RUN chmod u+s /usr/bin/csvtool

# Part2 flag — only root can read → requires privesc via csvtool
COPY part2.txt /part2.txt
RUN chmod 0400 /part2.txt && chown root:root /part2.txt

# MySQL config: allow INTO OUTFILE anywhere
COPY mysql.cnf /etc/mysql/mariadb.conf.d/99-ctf.cnf

# Configure Apache to listen on port 2412
RUN sed -i 's/Listen 80/Listen 2412/' /etc/apache2/ports.conf \
    && sed -i 's/:80/:2412/g' /etc/apache2/sites-available/000-default.conf

# Copy application source to webroot
COPY src/ /var/www/html/

# Remove default index.html
RUN rm -f /var/www/html/index.html

# Create uploads directory — writable by both www-data and mysql (for INTO OUTFILE)
RUN mkdir -p /var/www/html/uploads \
    && echo "Seed CV for recruitment review." > /var/www/html/uploads/seed_cv.txt \
    && chmod 777 /var/www/html/uploads

# Copy init files (not in webroot)
COPY init.sql /opt/init.sql
COPY seed.php /opt/seed.php
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Create MySQL runtime directory
RUN mkdir -p /var/run/mysqld && chown mysql:mysql /var/run/mysqld

EXPOSE 2412

CMD ["/start.sh"]
