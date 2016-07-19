'''Defines the run method of the Flask application. Registers the functions
`before_request()` and `after_request()` to run before and after each request,
respectively (both functions located in app/views/index). Essentially, these
functions open and close a connection to the MySQL database with each request
made to the server.
'''
from flask import Flask
from flask_json import FlaskJSON
import app
from config import *
from app import app
from app.views import *

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
