from flask import Flask
from flask_json import FlaskJSON
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
json = FlaskJSON(app)

env = os.environ.get("AIRBNB_ENV")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

"""List of origins for cross-origin connection in production."""
if env == "production":
    cors = CORS(app, resources={r"/*": {"origins": ["https://127.0.0.1/",
                                                    "http://158.69.92.186/"]}})
