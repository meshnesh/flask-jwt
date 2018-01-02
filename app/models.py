# app/models.py

from app import db
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta
from flask import current_app, Flask

# app = Flask(__name__)
# db = SQLAlchemy(app)

rsvps = db.Table('rsvps',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('eventlists.id'))
)


class User(db.Model):
    """This class defines the users table """

    __tablename__ = 'users'

    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256))
    eventlists = db.relationship(
        'Events', order_by='Events.id', cascade="all, delete-orphan")
    myrsvps = db.relationship('Events', secondary=rsvps,
                              backref=db.backref('rsvpList', lazy='dynamic'), lazy='dynamic')

    def __init__(self, name, email, password):
        """Initialize the user with a name, an email and a password."""
        self.name = name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)


    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        """This method gets all the events for a given user."""
        return User.query.all()

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=1440),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as error:
            # return an error in string format if an exception occurs
            return str(error)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def __str__(self):
        return """User(id={}, name={}, email={}, events={})""".format(self.id, self.name, self.email, self.myrsvps.all())

    __repr__ = __str__

class Events(db.Model):
    """This class represents the eventlist table."""

    __tablename__ = 'eventlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    location = db.Column(db.String(255))
    time = db.Column(db.String(255))
    date = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, title, location, time, date, description, created_by):
        """initialize an event with its creator."""
        self.title = title
        self.location = location
        self.time = time
        self.date = date
        self.description = description
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    def add_rsvp(self, user):
        # print(user)
        """ This method adds a user to the list of rsvps"""       
        self.rsvpList.append(user)
        db.session.add(user)
        print(user)
        db.session.commit()
        for user in self.rsvpList:
            print(user.name, "Has rsvp")

    def get__all_rsvp(self):
        """This method gets all the events for a given user."""
        # return Events.query.filter_by(created_by=user_id)
        return self.rsvpList.all()

    @staticmethod
    def get_all_user(user_id):
        """This method gets all the events for a given user."""
        return Events.query.filter_by(created_by=user_id)

    @staticmethod
    def get__all_events():
        """This method gets all the events for a given user."""
        # return Events.query.filter_by(created_by=user_id)
        return Events.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __str__(self):
        return "<Events: {}>".format(self.title) # check on this later

    __repr__ = __str__
