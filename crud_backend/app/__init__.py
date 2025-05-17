from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://igor:igor@cluster0.upqn1.mongodb.net/biblioteca_db?retryWrites=true&w=majority"

mongodb_client = PyMongo(app)
db = mongodb_client.db

from app import routes
