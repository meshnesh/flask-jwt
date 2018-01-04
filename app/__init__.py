# app/__init__.py
import json
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy

from flask import request, jsonify, abort, make_response, flash

# local import

from instance.config import app_config

# For password hashing
from flask_bcrypt import Bcrypt

# initialize db
db = SQLAlchemy()


def create_app(config_name):

    from app.models import Events, User

    app = FlaskAPI(__name__, instance_relative_config=True)
    # overriding Werkzeugs built-in password hashing utilities using Bcrypt.
    bcrypt = Bcrypt(app)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/eventlist/', methods=['POST', 'GET'])
    def event():
        # get the access token
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authed
                if request.method == "POST":
                    title = str(request.data.get('title', ''))
                    location = str(request.data.get('location', ''))
                    time = str(request.data.get('time', ''))
                    date = str(request.data.get('date', ''))
                    description = str(request.data.get('description', ''))
                    if title:
                        event = Events(title=title, location=location,
                                       time=time, date=date,
                                       description=description, created_by=user_id)
                        event.save()
                        response = jsonify({
                            'id': event.id,
                            'title': event.title,
                            'location': event.location,
                            'time': event.time,
                            'date': event.date,
                            'description': event.description,
                            'created_by': user_id
                        })

                        return make_response(response), 201

                else:
                    # GET
                    # get all the events for this user
                    events = Events.get_all_user(user_id)
                    results = []

                    for event in events:
                        obj = {
                            'id': event.id,
                            'title': event.title,
                            'location': event.location,
                            'time': event.time,
                            'date': event.date,
                            'description': event.description,
                            'created_by': user_id
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/eventlist/all', methods=['GET'])
    def get_event():
        # GET all the events for this user
        events = Events.query

        title = request.args.get('title')
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=2, type=int)
        location = request.args.get('location')
        # category = request.args.get('category')

        if title:
            events = Events.query.filter_by(title=title)

        if location:
            events = Events.query.filter_by(location=location)

        # if category:
        #     all_events = Event.query.filter_by(category=category)

        eventPage = events.paginate(page, limit, False).items

        results = []

        for event in eventPage:
            obj = {
                'id': event.id,
                'title': event.title,
                'location': event.location,
                'time': event.time,
                'date': event.date,
                'description': event.description
            }
            results.append(obj)

        if not results:
            response = {
                'message': "No events found"
            }
            return make_response(jsonify(response)), 404

        return make_response(jsonify(results)), 200

    @app.route('/events/all/<int:id>', methods=['GET'])
    def get_single_event(id, **kwargs):
        event = Events.query.filter_by(id=id).first()
        if not event:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        else:    
            # GET
            response = jsonify({
                'id': event.id,
                'title': event.title,
                'location': event.location,
                'time': event.time,
                'date': event.date,
                'description': event.description,
                'created_by': event.created_by
            })
            return make_response(response), 200

    @app.route('/eventlist/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def event_manipulation(id, **kwargs):

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                event = Events.query.filter_by(id=id).first()
                if not event:
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == "DELETE":
                    event.delete()
                    return {
                        "message": "bucketlist {} deleted".format(event.id)
                    }, 200
                elif request.method == 'PUT':
                    title = str(request.data.get('title', ''))
                    location = str(request.data.get('location', ''))
                    time = str(request.data.get('time', ''))
                    date = str(request.data.get('date', ''))
                    description = str(request.data.get('description', ''))
                    event.title = title
                    event.location = location
                    event.time = time
                    event.date = date
                    event.description = description
                    event.save()
                    response = {
                        'id': event.id,
                        'title': event.title,
                        'location': event.location,
                        'time': event.time,
                        'date': event.date,
                        'description': event.description,
                        'created_by': event.created_by
                    }
                    return make_response(jsonify(response)), 200
                else:
                    # GET
                    response = jsonify({
                        'id': event.id,
                        'title': event.title,
                        'location': event.location,
                        'time': event.time,
                        'date': event.date,
                        'description': event.description,
                        'created_by': event.created_by
                    })
                    return make_response(response), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401


    @app.route('/eventlist/<int:id>/rsvp/', methods=['POST'])
    def create_rsvp(id, **kwargs):

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                event = Events.query.filter_by(id=id).first_or_404()

                # POST User to the RSVP
                user = User.query.filter_by(id=user_id).first_or_404()
                has_prev_rsvpd = event.add_rsvp(user)
                if has_prev_rsvpd:
                    response = {
                        'message': 'You have already reserved a seat'
                    }
                    return make_response(jsonify(response)), 202

                response = {
                    'message': 'You have Reserved a seat'
                }
                return make_response(jsonify(response)), 200

            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401



    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
