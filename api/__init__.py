import os

from dotenv import load_dotenv
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    from api.models import employee

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from api.blueprints import emp_api

    app.register_blueprint(emp_api, url_prefix='/api')

    return app
