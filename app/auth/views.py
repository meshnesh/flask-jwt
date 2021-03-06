from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify, Flask
from app.models import User
from flask_bcrypt import Bcrypt

from flasgger import Swagger

# app = Flask(__name__)

# Flasgger is initialized like a standard flask extension.
# You can also use .init_app() with the "app factory" pattern.
# swag = Swagger(app)


class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """
        This example tests decorator package
        Should not break in Python 2.7+
        ---
        responses:
        200:
            description: Yeah it works
        """

        # Query to see if the user already exists
        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            # There is no user so we'll try to register them
            try:
                post_data = request.data
                # Register the user
                name = post_data['name']
                email = post_data['email']
                password = post_data['password']
                user = User(name=name, email=email, password=password)
                user.save()

                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                # return a response notifying the user that they registered successfully
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202

class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/login"""
        try:
            # Get the user object using their email (unique to every user)
            user = User.query.filter_by(email=request.data['email']).first()

            # Try to authenticate the found user using their password
            if user and user.password_is_valid(request.data['password']):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500


class RestEmailView(MethodView):
    """This class resets a users password."""

    def post(self):
        """Handle PUT request for this view. Url ---> /auth/register"""

        # Query to see if the user email exists
        user = User.query.filter_by(email=request.data['email']).first()
        if user:
            access_token = user.generate_token(user.id)
            if access_token:
                response = {
                    'message': 'Email confirmed you can reset your password.',
                    'access_token': access_token.decode()
                }
                return make_response(jsonify(response)), 200

        response = {
            'message': 'Wrong Email or user email does not exist.'
        }
        return make_response(jsonify(response)), 401

class RestPasswordView(MethodView):
    """This class validates a user email the generates a token for resets a users password."""

    def put(self):
        """This Handles PUT request for handling the reset password for the user 
        ---> /auth/reset-password
        """

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # get_user = User.get_all_users()
                # print(get_user)
                try:
                    reset_password = User.query.filter_by(id=user_id).first_or_404()

                    post_data = request.data
                    name = reset_password.name
                    email = reset_password.email
                    reset_password.password = Bcrypt().generate_password_hash(post_data['password']).decode()
                    user = User(name=name, email=email, password=reset_password.password)
                    user.resetPassword()

                    response = {
                        'message': 'Password rest successfully. Please log in.'
                    }
                    # return a response notifying the user that password was reset successfully
                    return make_response(jsonify(response)), 201
                except Exception as e:
                    # An error occured, therefore return a string message containing the error
                    response = {
                        'message': str(e)
                    }
                    return make_response(jsonify(response)), 401
        message = user_id
        response = {
            'message': message
        }
        
        return make_response(jsonify(response)), 401


# Define the API resource
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
reset_view = RestEmailView.as_view('rest_view')
reset_password_view = RestPasswordView.as_view('rest_password_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

# Define the rule for the registration url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)

# Define the rule for the rest(to validate the email) url --->  /auth/rest
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/reset',
    view_func=reset_view,
    methods=['POST']
)

# Define the rule for the rest_password url --->  /auth/rest-password
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/reset-password/',
    view_func=reset_password_view,
    methods=['PUT']
)
