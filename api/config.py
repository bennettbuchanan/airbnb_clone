'''Configures the variables for Airbnb clone based on the current value of the
environment variable AIRBNB_ENV. The default mode is that of user
'airbnb_user_dev'.
'''
import os

status = os.environ.get("AIRBNB_ENV")

DEBUG = True
HOST = "localhost"
PORT = 3333
DATABASE = {"host": "158.69.92.186",
            "user": "airbnb_user_dev",
            "database": "airbnb_dev",
            "port": 3306,
            "charset": "utf8",
            "password": "airbnb_user_dev"}

if status == "production":
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 3000
    DATABASE = {"host": "158.69.92.186",
                "user": "airbnb_user_prod",
                "database": "airbnb_prod",
                "port": 3306,
                "charset": "utf8",
                "password": "airbnb_user_prod"}

elif status == "test":
    DEBUG = False
    HOST = "localhost"
    PORT = 5555
    DATABASE = {"host": "158.69.92.186",
                "user": "airbnb_user_test",
                "database": "airbnb_test",
                "port": 3306,
                "charset": "utf8",
                "password": os.environ.get("AIRBNB_DATABASE_PWD_TEST")}
