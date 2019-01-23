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

        # # session_id = '078778877737v3g44fbbyy23jgb4r5665h'
        # session_id = request.values.get("sessionId", None)
        # serviceCode = request.values.get("serviceCode", None)

        # # phone_number = '078778445457'
        # phone_number = request.values.get("phoneNumber", None)
        # text = request.values.get("text", "default")

        # text_array = text.split("*")
        # user_response = text_array[len(text_array) - 1]

        # This is data from Africastalking API
        session_id = request.json['sessionId']
        serviceCode = request.json['sessionId']
        phone_number = request.json['phone_number']
        text = request.json['text']
        text_array = text.split("*")
        user_response = text_array[len(text_array) - 1]

        # We are supporsed to have only one occurrence of the phone_number
        # In both the User table and the Session_level table
        # Each user is identified by their phone_numbers
        # Phone number is unique to every user

        user = User.query.filter_by(phone_number=phone_number).first()

        if user:
            # We are not going to consider session_id for the entire registeration

            # check for the level of the user
            session_level = SessionLevel.query.filter_by(
                phone_number=phone_number).first()

            # Handling user registration

            if not user.pin or not user.is_pin_confirmed:
                # user does not have pin set or if pin is not confirmed

                # There is no worries. Level is always available once the phone_number is registered
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

            # User is fully registered. And is ready for business transactions
            # Prompt the user to enter pin to continue
            # NOTE Level = 10

            session = SessionLevel.query.filter_by(
                phone_number=phone_number).first()

            if session.session_id != session_id:

                # This is the 1st time encouter under this section
                # We don't expect the session_id to match becauxe the last operation
                # killed the session | Here  we start with a new session_id
                session.session_id = session_id
                # Also promote to level 11
                session.promote_level(11)
                db.session.add(session)
                db.session.commit()

                # Now tell the user to enter their pin to continue
                response = "CON Please enter your pin to verify it is you"
                return respond(response)

            if session.level == 11:
                # Start by verifying that the pin is right
                if user.pin != user_response:
                    response = "CON Please enter correct PIN"
                    return respond(response)

                # Now that the user has provided the right pin lets
                # Promote the user to level 12 plus the response
                session.promote_level(12)
                db.session.add(session)
                db.session.commit()

                response = "CON 1. Deposit \n"
                response += "2. Withdraw \n"
                response += "3. Balance \n"
                response += "4. Debt \n"
                response += "5. Get loan \n"
                response += "6. Pay loan \n"
                response += "7. Account information"

                return respond(response)

            if session.level == 12:
                response = "CON Congz You are on level 12"
                return respond(response)

        # Register new user
        menu = RegisterUser(phone_number, session_id)
        return menu.get_phone()  # enter name

        # # if user does not exist create one
        # if user:
        #     # check for the level of the user
        #     session_level = SessionLevel.query.filter_by(
        #         session_id=session_id).first()

        #     # Handling user registration

        #     if not user.pin or not user.is_pin_confirmed:
        #         # user does not have pin set or if pin is not confirmed

        #         # check if session_id exists in sessionLevel table
        #         if session_level:

        #             level = session_level.level

        #             if level < 10:
        #                 menu = RegisterUser(
        #                     phone_number, session_id, user_response)
        #                 if level == 0:
        #                     return menu.get_name()  # enter city
        #                 if level == 1:
        #                     return menu.get_city()  # enter pin
        #                 if level == 2:
        #                     return menu.get_pin()  # promoted to level 3
        #                 if level == 3:
        #                     # confirm pin
        #                     return menu.confirm_pin()  # promoted to level 10
        #         else:
        #             # After promoting user registration | is done in the if statement above
        #             # This is because a new the session will be the same

        #             # check if user does not have name
        #             if not user.name:
        #                 response = "CON Please enter your name"

        #                 # demote user to level 0

        #                 # also insert phone number and session_id to the sessionLevel table
        #                 # Lets update the session_level table with the new session_id

        #                 session_level = SessionLevel.query.filter_by(
        #                     phone_number=phone_number).first()
        #                 # now update the session_id field
        #                 session_level.session_id = session_id
        #                 # session_level = SessionLevel(
        #                 #     phone_number=phone_number, session_id=session_id)

        #                 db.session.add(session_level)
        #                 db.session.commit()

        #                 return respond(response)

        #             # check if user does not have city
        #             if not user.city:
        #                 response = "CON You  can now enter your city"

        #                 # promote user to level 1

        #                 # Lets update the session_level table with the new session_id

        #                 session_level = SessionLevel.query.filter_by(
        #                     phone_number=phone_number).first()
        #                 # now update the session_id field
        #                 session_level.session_id = session_id
        #                 session_level.level = 1
        #                 # session_level = SessionLevel(
        #                 #     phone_number=phone_number, session_id=session_id, level=1)

        #                 db.session.add(session_level)
        #                 db.session.commit()

        #                 return respond(response)

        #             # check if user does not have pin
        #             if not user.pin:

        #                 # promote user to level 2

        #                 # Lets update the session_level table with the new session_id

        #                 session_level = SessionLevel.query.filter_by(
        #                     phone_number=phone_number).first()
        #                 # now update the session_id field
        #                 session_level.session_id = session_id

        #                 # session_level = SessionLevel(
        #                 #     phone_number=phone_number, session_id=session_id, level=2)

        #                 db.session.add(session_level)
        #                 db.session.commit()

        #                 # respond to user
        #                 response = "CON Please create a Pin number \n"
        #                 response += "Pin should be 4 integers long \n"
        #                 response += "You will use this pin whenever \n"
        #                 response += "you're trasacting"

        #                 return respond(response)

        #             # if user has pin but is not confirmed
        #             if not user.is_pin_confirmed:
        #                 # Lets update the session_level table with the new session_id

        #                 session_level = SessionLevel.query.filter_by(
        #                     phone_number=phone_number).first()
        #                 # now update the session_id field
        #                 session_level.session_id = session_id
        #                 session_level.level = 3
        #                 # session_level = SessionLevel(
        #                 #     phone_number=phone_number, session_id=session_id, level=3)

        #                 db.session.add(session_level)
        #                 db.session.commit()

        #                 response = "CON Please re-enter your Pin \n"
        #                 response += "to confirm it"
        #                 return respond(response)

        #     else:
        #         # Under this section. The user is fully register under our app

        #         # User should present their pin to proceed
        #         # All operations will be done under one session
        #         # This means we are not going to have session continuation
        #         # At this level, when user kills the session, operations will be started
        #         # from the start

        #         # Initially the incomming session_id will be different fro that we already have

        #         # 1. Enter pin (level 10)
        #         session = SessionLevel.query.filter_by(
        #             phone_number=phone_number).first()
        #         if session.session_id != session_id:

        #             # This is the 1st time encouter under this section
        #             # Also promote to level 11
        #             # new_session = SessionLevel(session_id=session_id, phone_number=phone_number, level=11)
        #             session.session_id = session_id
        #             session.promote_level(11)
        #             db.session.add(session)
        #             db.session.commit()

        #             # Now tell the user to enter their pin to continue

        #             response = "CON Please enter your pin to verify it is you"
        #             return respond(response)

        #         # Process depending on levels
        #         if session.level == 11:
        #             # 2. Verify that it is right
        #             user = User.query.filter_by(
        #                 phone_number=phone_number).first()
        #             if user.pin == user_response:

        #                 # Now that the user has provided the right pin lets
        #                 # Promote the user tolevel 12
        #                 response = "CON 1. Deposit \n"
        #                 response += "2. Withdraw \n"
        #                 response += "3. Balance \n"
        #                 response += "4. Debt \n"
        #                 response += "5. Get loan \n"
        #                 response += "6. Pay loan \n"
        #                 response += "7. Account information"

        #                 return respond(response)

        #             response = "CON Enter correct pin"
        #             return respond(response)
        # else:
        #     menu = RegisterUser(phone_number, session_id)
        #     return menu.get_phone()  # enter name
