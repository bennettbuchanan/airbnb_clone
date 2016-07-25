'''Configures the variables for Airbnb clone based on the current value of the
environment variable AIRBNB_ENV. The default mode is that of user
'airbnb_user_dev'.
'''
import os

env = os.environ.get("AIRBNB_ENV")

DEBUG = True
HOST = "localhost"
PORT = 3333
DATABASE = dict(host="158.69.92.186",
                port=3306,
                charset="utf8",
                user="airbnb_user_dev",
                database="airbnb_dev",
                password="airbnb_user_dev")

if env == "production":
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 3000
    DATABASE.update({"user": "airbnb_user_prod",
                     "database": "airbnb_prod",
                     "password": "airbnb_user_prod"})

elif env == "test":
    DEBUG = False
    PORT = 5556
    DATABASE.update({"user": "airbnb_user_test",
                     "database": "airbnb_test",
                     "password": os.environ.get("AIRBNB_DATABASE_PWD_TEST")})
