import os
from flask import request, make_response
from flask_restplus import Resource, reqparse
from flask import jsonify, json, current_app, request, make_response
from run import db
from .models import User, SessionLevel


def respond(menu_text):
    response = make_response(menu_text, 200)
    response.headers['Content-Type'] = "text/plain"
    return response


# def get_phone(phone_number, session_id):
#         # insert the phone number and then request for the name
#         new_user = User(phone_number=phone_number)
        
#         # also insert phone number and session_id to the sessionLevel table
#         user = SessionLevel(phone_number=phone_number, session_id=session_id)

#         db.session.add(new_user)
#         db.session.commit()
#         db.session.add(user)
#         db.session.commit()

#         response = "CON Please enter your name"
#         return respond(response)


class RegisterUser:
    """
    Collect user info
    :phone_number
    :name
    :city
    :pin
    """

    def __init__(self, phone_number, session_id, optional_param='None'):
        self.phone_number = phone_number
        self.session_id = session_id
        self.optional_param = optional_param

    def get_phone(self):
        # insert the phone number and then request for the name
        new_user = User(phone_number=self.phone_number)
        
        # also insert phone number and session_id to the sessionLevel table
        user = SessionLevel(phone_number=self.phone_number, session_id=self.session_id)

        db.session.add(new_user)
        db.session.add(user)
        db.session.commit()

        response = "CON Please enter your name"
        return respond(response)

    def get_name(self):
        """ add name to the user """
        # insert user name into db request for city
        user = User.query.filter_by(phone_number=self.phone_number).first()
        user.name = self.optional_param
        
        db.session.add(user)
        db.session.commit()

        # Promote session level to 1
        session_level = SessionLevel.query.filter_by(session_id=self.session_id).first()
        session_level.promote_level(1)  # default is 1
        db.session.add(session_level)
        db.session.commit()

        # respond to user
        response = "CON You can now enter your city"
        return respond(response)

    def get_city(self):
        # insert city then request for pin
        user = User.query.filter_by(phone_number=self.phone_number).first()
        user.city = self.optional_param

        db.session.add(user)
        db.session.commit()

        # promote user to level 2
        session_level = SessionLevel.query.filter_by(session_id=self.session_id).first()
        session_level.promote_level(2)
        db.session.add(session_level)
        db.session.commit()

        # respond to user
        response = "CON Please create a Pin number \n"
        response += "Pin should be 4 integers long \n"
        response += "You will use this pin whenever \n"
        response += "you're trasacting"

        return respond(response)

    def get_pin(self):
        # insert in and then request for >>>>>>>>>
        user = User.query.filter_by(phone_number=self.phone_number).first()
        user.pin = self.optional_param

        db.session.add(user)
        db.session.commit()

        # promote user to level 10
        session_level = SessionLevel.query.filter_by(session_id=self.session_id).first()
        session_level.promote_level(10)
        db.session.add(session_level)
        db.session.commit()

        response = "END Promoted to level 10"
        return respond(response)


class UssdCallback(Resource):

    """ Class that handles customer requests from AT API"""

    def post(self):
        """ Method that handles responses from customers"""

        session_id = request.values.get("sessionId", None)
        serviceCode = request.values.get("serviceCode", None)
        phone_number = request.values.get("phoneNumber", None)
        text = request.values.get("text", "default")

        text_array = text.split("*")
        user_response = text_array[len(text_array) - 1]

        # Menu levels and items

        # register_user = {
        #     # Menu for creating a new user
        #     0: "Enter name",
        #     1: "Enter city",
        #     2: "Enter pin"
        # }

        # reset_pin = {
        #     # Menu for reseting pin / password
        #     0: "Enter old pin",
        #     1: "Enter new pin"
        # }

        # transact = {
        #     # Menu for performing transactions
        #     0: "Deposit",
        #     1: "Withdraw",
        #     2: "Account Balance",
        #     3: "Get loan",
        #     4: "Pay loan",
        #     5: "Debt"
        # }

        # The keys correspond to the values of the menus
        # methods = {
        #     # register new user
        #     "Enter name": enter_name,
        #     "Enter city": enter_city,
        #     "Enter pin": enter_pin,

        #     # reset pin
        #     "Enter old pin": enter_old_pin,
        #     "Enter new pin": enter_new_pin,

        #     # transact
        #     "Deposit": deposit,
        #     "Withdraw": withdraw,
        #     "Account Balance": account_balance,
        #     "Get loan": get_loan,
        #     "Pay loan": pay_loan,
        #     "Debt": debt
        # }

        # check if user exists
        user = User.query.filter_by(phone_number=phone_number).first()

        # if user does not exist create one
        if user:
            # check for the level of the user
            session_level = SessionLevel.query.filter_by(session_id=session_id).first()

            level = session_level.level

            if level < 10:
                menu = RegisterUser(phone_number, session_id, user_response)
                if level == 0:   
                    return menu.get_name() # enter city
                elif level == 1:
                    return menu.get_city() # enter pin
                elif level == 2:
                    return menu.get_pin() # promoted to level 10
            else:
                return respond("END you are at level 10 now")
        else:
            menu = RegisterUser(phone_number, session_id)
            return menu.get_phone() # enter name
           

