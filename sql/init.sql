# Creates users and databases for production and development for AirBnb Clone.

# Create user airbnb_user_dev that can access the database from any IP and
# user airbnb_user_prod that can access the database from only localhost.
CREATE USER 'airbnb_user_dev'@'%' IDENTIFIED BY 'airbnb_user_dev';
CREATE USER 'airbnb_user_prod'@'localhost' IDENTIFIED BY 'airbnb_user_prod';

# Create the databases.
CREATE DATABASE airbnb_dev;
CREATE DATABASE airbnb_prod;

# Grant privileges to the databases of the respective users.
GRANT ALL ON airbnb_dev.* TO 'airbnb_user_dev'@'%' IDENTIFIED BY 'airbnb_user_dev';
GRANT ALL ON airbnb_prod.* TO 'airbnb_user_prod'@'localhost' IDENTIFIED BY 'airbnb_user_prod';
