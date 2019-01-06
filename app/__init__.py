from flask_restplus import Api
from run import app
from .views import UssdCallback

API = Api(app)
API.add_resource(UssdCallback, '/ussd/callback')
