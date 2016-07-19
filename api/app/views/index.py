'''Defines the flask function to run when a GET request is made to the root
directory '/'. Handles the behavior for a 404 error.
'''
from flask import Flask, jsonify, request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from app import app
import datetime
import time
from app.models.base import BaseModel
from peewee import *


@app.route('/', methods=['GET'])
@as_json
def index():
    '''Return a JSON object with the status code of the server, and UTC time
    and the server time.
    '''
    return jsonify(status="OK",
                   utc_time=datetime.datetime
                                    .utcnow()
                                    .strftime("%Y/%m/%d %H:%M:%S"),
                   time=datetime.datetime
                                .now()
                                .strftime("%Y/%m/%d %H:%M:%S"))

def before_request():
    '''Connect to the database defined in BaseModel.'''
    BaseModel.database.connect()


def after_request():
    '''Close the connection to the database defined in the BaseModel.'''
    BaseModel.database.close()


@app.errorhandler(404)
def page_not_found(error):
    '''Return a JSON object with the code 404, and a message "not found".'''
    return jsonify(code=404,
                   msg="not found")
