#!/usr/bin/env python

'''Configures the environment variables for AirBnb clone based on the current
value of the env varibale AIRBNB_ENV
'''

import os

status = os.environ.get('AIRBNB_ENV')

if status == 'development':
    os.environ["DEBUG"] = "True"
    os.environ["HOST"] = "localhost"
    os.environ["PORT"] = "3333"
    os.environ["DATABASE"] = '{"host": "158.69.92.186", "user": "airbnb_user_dev", "database":"airbnb_dev", "port": "3306", "charset": "utf8", "password": "airbnb_user_dev"}'

if status == 'production':
    os.environ["DEBUG"] = "False"
    os.environ["HOST"] = "0.0.0.0"
    os.environ["PORT"] = "3000"
    os.environ["DATABASE"] = '{"host": "158.69.92.186", "user": "airbnb_user_prod", "database":"airbnb_prod", "port": "3306", "charset": "utf8", "password": "airbnb_user_prod"}'
