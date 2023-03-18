from flask import Flask, Blueprint
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from server.settings.environment import Environment

environment = Environment()

api_blueprint = Blueprint('api', __name__, url_prefix='/v1')

api = Api(
    api_blueprint,
    title=f'{environment.api_name} Flask API',
    version='1.0',
    description='Backend Application',
)
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environment.database_connection
