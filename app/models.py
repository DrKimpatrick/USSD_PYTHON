from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from run import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    phone_number = db.Column(db.String(64), unique=True, index=True, nullable=False)

    city = db.Column(db.String(64))
    registration_date = db.Column(db.DateTime(), default=datetime.utcnow)
    pin = db.Column(db.String(128))
    account = db.Column(db.Integer, default=10)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.pip = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pip, password)

    def __repr__(self):
        return "User {}".format(self.name)

    def deposit(self, amount):
        self.account += amount

    def withdraw(self, amount):
        self.account -= amount


class SessionLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(128), unique=True)
    phone_number = db.Column(db.String(25))
    level = db.Column(db.Integer, default=0)

    def promote_level(self, level=1):
        self.level = level

    def demote_level(self):
        self.level = 0


