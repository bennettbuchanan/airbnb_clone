# Creates users and databases for testing of AirBnb Clone.

# Create user airbnb_user_test that can access the database from any IP.
CREATE USER 'airbnb_user_test'@'%' IDENTIFIED BY 'airbnb_user_test';

# Create the databases.
CREATE DATABASE airbnb_test
DEFAULT COLLATE utf8_general_ci;

# Grant privileges to the databases of the user.
GRANT ALL ON airbnb_test.* TO 'airbnb_user_test'@'%' IDENTIFIED BY 'airbnb_user_test';
