from flask_restplus import Api
from run import app
from .views import welcome, UssdCallback

API = Api(app)
API.add_resource(welcome, '/welcome')
API.add_resource(UssdCallback, '/ussd/callback')
