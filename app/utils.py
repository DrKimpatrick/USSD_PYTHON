from flask import make_response
from run import db
from .models import User, SessionLevel


def respond(menu_text):
    response = make_response(menu_text, 200)
    response.headers['Content-Type'] = "text/plain"
    return response


def check_pin(pin):
    # check if pin matches the required specifications
    # pin should be 4 integer characters long
    response = "CON Invalid Pin. \n"
    response += "Pin should be 4 interger characters long"
    if len(pin) == 4:
        try:
            pin = int(pin)
        except:
            return respond(response)
    else:
        return respond(response)


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
        user = User.query.filter_by(phone_number=self.phone_number).first()

        if not user:
            new_user = User(phone_number=self.phone_number)
            db.session.add(new_user)

            # also insert phone number and session_id to the sessionLevel table
            session = SessionLevel(phone_number=self.phone_number,
                                session_id=self.session_id)

            db.session.add(session)
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
            phone_number=self.phone_number).first()
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
            phone_number=self.phone_number).first()
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
        # insert in and then request a confirmatory in

        # check if pin matches the required specifications
        pin = self.optional_param

        if check_pin(pin):
            return check_pin(pin)

        user = User.query.filter_by(phone_number=self.phone_number).first()
        user.pin = self.optional_param

        db.session.add(user)
        db.session.commit()

        # promote user to level 3
        session_level = SessionLevel.query.filter_by(
            phone_number=self.phone_number).first()
        session_level.promote_level(3)
        db.session.add(session_level)
        db.session.commit()

        response = "CON Please re-enter your Pin \n"
        response += "to confirm it"
        return respond(response)

    def confirm_pin(self):
        # insert in and then promote user to level 10
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
        user.is_pin_confirmed = True
        db.session.add(user)
        db.session.commit()

        # promote user to level 10
        session_level = SessionLevel.query.filter_by(
            phone_number=self.phone_number).first()

        session_level.promote_level(10)
        db.session.add(session_level)
        db.session.commit()

        response = "END Your account has been \n"
        response += "successfully setup. You can \n"
        response += "now save with us and even \n"
        response += "get an instant loan"
        return respond(response)
