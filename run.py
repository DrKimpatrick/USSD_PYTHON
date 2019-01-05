from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# it is placed here because it's classes inherit from DB
# Makes the table available for runing migrations

from app.models import User, SessionLevel


# makes the endpoint available for consumption
from app import API


if __name__ == '__main__':
    app.run()
