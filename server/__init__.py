from flask import Flask
from flask_cors import CORS
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
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://signup:6BWdGl0r21q5TQYxGsn33bgWZ46r5ptr@dpg-cgu0l9aut4mcfrg3teig-a/db_signup_i5l3"
