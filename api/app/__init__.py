from flask import Flask, request
from flask_json import FlaskJSON

app = Flask(__name__)
json = FlaskJSON(app)
