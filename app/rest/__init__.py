from flask import Flask, request, jsonify, Response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)

api = Api(app)

