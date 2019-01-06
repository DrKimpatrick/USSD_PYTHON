from flask import make_response
from run import db
from .models import User, SessionLevel

def respond(menu_text):
    response = make_response(menu_text, 200)
    response.headers['Content-Type'] = "text/plain"
    return response


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
        user = SessionLevel(phone_number=self.phone_number,
                            session_id=self.session_id)

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
        session_level = SessionLevel.query.filter_by(
            session_id=self.session_id).first()
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
        session_level = SessionLevel.query.filter_by(
            session_id=self.session_id).first()
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

        # promote user to level 3
        session_level = SessionLevel.query.filter_by(
            session_id=self.session_id).first()
        session_level.promote_level(3)
        db.session.add(session_level)
        db.session.commit()

        response = "CON Please re-enter your Pin \n"
        response += "to confirm it"
        return respond(response)
    
    def confirm_pin(self):
        # insert in and then request for >>>>>>>>>
        user = User.query.filter_by(phone_number=self.phone_number).first()
        
        # compare the old pin and current
        if user.pin != self.optional_param:
            response = "CON Pin does not match \n"
            response += "the existing Pin \n"
            response += "Consider resetting it if \n"
            response += "if you don't rember it. \n"
            response += "Try again"

            return respond(response)

        # if Pins really match
        session_level.is_pin_confirmed = True
        db.session.add(session_level)
        db.session.commit()

        # promote user to level 10
        session_level = SessionLevel.query.filter_by(
            session_id=self.session_id).first()
        session_level.promote_level(10)
        db.session.add(session_level)
        db.session.commit()

        response = "END Promoted to level 10"
        return respond(response)
