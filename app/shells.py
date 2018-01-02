from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models import *

# app = Flask(__name__)
# db = SQLAlchemy(app)


rsvps = db.Table('rsvps',
                 db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	                db.Column('event_id', db.Integer, db.ForeignKey('eventlists.id'))
                )


class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    eventlists = db.relationship(
        'Events', order_by='Events.id', cascade="all, delete-orphan")
    myrsvps = db.relationship('Events', secondary=rsvps,
                              backref=db.backref('rsvpList', lazy='dynamic'))


class Channel(db.Model):
    
    __tablename__ = 'eventlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    location = db.Column(db.String(255))
    time = db.Column(db.String(255))
    date = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))


db.create_all()

user1 = User(name='Anthony', email='tonny@gmail.com', password='qwerty1234')
user2 = User(name='Stacy', email='statcy', password='qwerty1234')
user3 = User(name='George', email='george@gmail.com', password='qwerty1234')
user4 = User(name='Amber', email='amber@gmail.com', password='qwerty1234')

db.session.add(user1, user2, user3, user4)

event1 = Events(title='Mango Harvest', location='Kitui', time='12:00pm', date='1st Jan 2018', description='qwerty asdadamfnsdf, adaqwrwknfvd')
event2 = Events(title='Tattoo Fest', location='Nai', time='18:00pm', date='31st Jan 2018', description='qwerty adaqwrwknfvd')

db.session.add(event1, event2)

event2.rsvpList.append(user1, user3, user4)
event2.rsvpList.append(user2, user4)

db.session.commit()

event1.rsvpList
for user in event1.rsvpList:
    print(user.name)