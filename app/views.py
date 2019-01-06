import os
from flask import request, jsonify, json, current_app, request, make_response
from run import db
from flask_restplus import Resource, reqparse
from .models import User, SessionLevel
from .utils import RegisterUser, respond


class UssdCallback(Resource):

    """ Class that handles customer requests from AT API"""

    def post(self):
        """ Method that handles responses from customers"""

        # session_id = '078778877737v3g44fbbyy23jgb4r5665h'
        session_id = request.values.get("sessionId", None)
        serviceCode = request.values.get("serviceCode", None)
        
        # phone_number = '078778445457'
        phone_number = request.values.get("phoneNumber", None)
        text = request.values.get("text", "default")

        text_array = text.split("*")
        user_response = text_array[len(text_array) - 1]

        # check if user exists
        user = User.query.filter_by(phone_number=phone_number).first()

        # if user does not exist create one
        if user:
            # check for the level of the user
            session_level = SessionLevel.query.filter_by(
                session_id=session_id).first()

            # Handling user registration

            if not user.pin or not user.is_pin_confirmed:
                # user does not have pin set or if pin is not confirmed

                # check if session_id exists in sessionLevel table
                if session_level:

                    level = session_level.level

                    if level < 10:
                        menu = RegisterUser(
                            phone_number, session_id, user_response)
                        if level == 0:
                            return menu.get_name()  # enter city
                        if level == 1:
                            return menu.get_city()  # enter pin
                        if level == 2:
                            return menu.get_pin()  # promoted to level 3
                        if level == 3:
                            # confirm pin
                            return menu.confirm_pin()  # promoted to level 10
                else:
                    # After promoting user registration | is done in the if statement above
                    # This is because a new the session will be the same

                    # check if user does not have name
                    if not user.name:
                        response = "CON Please enter your name"

                        # demote user to level 0

                        # also insert phone number and session_id to the sessionLevel table
                        session_level = SessionLevel(
                            phone_number=phone_number, session_id=session_id)

                        db.session.add(session_level)
                        db.session.commit()

                        return respond(response)

                    # check if user does not have city
                    if not user.city:
                        response = "CON You  can now enter your city"

                        # promote user to level 1

                        # also insert phone number and session_id to the sessionLevel table
                        session_level = SessionLevel(
                            phone_number=phone_number, session_id=session_id, level=1)

                        db.session.add(session_level)
                        db.session.commit()

                        return respond(response)

                    # check if user does not have pin
                    if not user.pin:

                        # promote user to level 2

                        # also insert phone number and session_id to the sessionLevel table
                        session_level = SessionLevel(
                            phone_number=phone_number, session_id=session_id, level=2)

                        db.session.add(session_level)
                        db.session.commit()

                        # respond to user
                        response = "CON Please create a Pin number \n"
                        response += "Pin should be 4 integers long \n"
                        response += "You will use this pin whenever \n"
                        response += "you're trasacting"

                        return respond(response)

                    # if user has pin but is not confirmed
                    if not user.is_pin_confirmed:
                        # also insert phone number and session_id to the sessionLevel table
                        session_level = SessionLevel(
                            phone_number=phone_number, session_id=session_id, level=3)

                        db.session.add(session_level)
                        db.session.commit()

                        response = "CON Please re-enter your Pin \n"
                        response += "to confirm it"
                        return respond(response)

            else:
                response = "CON 1. Deposit \n"
                response += "2. Withdraw \n"
                response += "3. Balance \n"
                response += "4. Debt \n"
                response += "5. Get loan \n"
                response += "6. Pay loan \n"
                response += "7. Account information"

                return respond(response)
        else:
            menu = RegisterUser(phone_number, session_id)
            return menu.get_phone()  # enter name
