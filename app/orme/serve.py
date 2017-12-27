from __future__ import absolute_import, unicode_literals

import os
import sys
from datetime import timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', )))

from orme.eth_client import EthereumClient
from orme.btc_client import BitcoinClient
from orme.services import UserService, SessionsService
from orme.models import UserSchema
from flask import Flask
from flask import jsonify
from flask import request
from flask_jwt import JWT, jwt_required, current_identity


# JWT Auth handler
def authenticate(email, password):
    user = SessionsService.email_login(email, password)
    return user


# JWT identity handler
def identity(payload):
    user_id = payload['identity']
    srv = UserService(int(user_id))
    user = srv.find()
    return user


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
# Default username key is just 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
# Default prefix is JWT which is not standard for JWT
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
# Default time delta is just 5 minutes, setting it to 1 hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=60 * 60)

jwt = JWT(app, authenticate, identity)


@app.route('/')
def home():
    bc = BitcoinClient()
    bitcoin_info = bc.info()

    ec = EthereumClient()
    ethereum_info = ec.info()

    resp = {"bitcoin": bitcoin_info, "ethereum": ethereum_info}
    resp["bitcoin"]["balance"] = bc.balance()
    return jsonify(resp)


# Users resource

@app.route('/api/users', methods=['GET'])
@jwt_required()
def list_users():
    srv = UserService()
    users = srv.find_all()
    schema = UserSchema(many=True)
    result = schema.dump(users)

    response = jsonify(result.data)
    response.status_code = 200
    return response


@app.route('/api/users/<id>', methods=['GET'])
@jwt_required()
def show_user(id):
    srv = UserService(int(id))
    user = srv.find()
    schema = UserSchema()
    result = schema.dump(user)

    response = jsonify(result.data)
    response.status_code = 200
    return response


@app.route('/api/users', methods=['POST'])
def create_user():
    content = request.get_json(silent=True)
    if 'email' in content and 'password' in content:
        user = UserService.create(content['email'], content['password'])
        schema = UserSchema()
        result = schema.dump(user)

        response = jsonify(result.data)
        response.status_code = 200
        return response
    else:
        errors = [{'user': 'cannot create user for unknown reason'}]
        response = jsonify(errors)
        response.status_code = 422
        return response


@app.route('/api/users/<id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    content = request.get_json(silent=True)
    if 'password' in content:
        srv = UserService(int(id))
        user = srv.find()
        if user.id == current_identity.id:
            user = srv.update_password(content['password'])
            schema = UserSchema()
            result = schema.dump(user)

            response = jsonify(result.data)
            response.status_code = 200
            return response
        else:
            errors = [{'authorization': 'only owner could update user'}]
            response = jsonify(errors)
            response.status_code = 401
            return response
    else:
        errors = [{'user': 'password for user update not provided'}]
        response = jsonify(errors)
        response.status_code = 422
        return response


@app.route('/api/users/<id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user_id = int(id)
    srv = UserService(user_id)
    user = srv.find()
    if user.id == current_identity.id:
        result = srv.delete()
        response = jsonify({})
        response.status_code = 204
        return response
    else:
        errors = [{'authorization': 'only owner could delete user'}]
        response = jsonify(errors)
        response.status_code = 401
        return response


# Sessions endpoint
@app.route('/api/sessions', methods=['POST'])
def create_session():
    errors = []
    content = request.get_json(silent=True)
    if 'email' in content and 'password' in content:
        logged_in = SessionsService.email_login(content['email'], content['password'])
        if logged_in:
            # TODO: JWT logic here
            response = jsonify({})
            response.status_code = 200
            return response
        else:
            errors.append({'password': 'wrong password'})
    else:
        errors.append({'user': 'cannot log in without e-mail/password'})

    response = jsonify(errors)
    response.status_code = 422
    return response


# @app.route('/api/sessions', methods=['DELETE'])
# @jwt_required()
# def delete_session():
#     # TODO: Log out logic here
#
#     response = jsonify({})
#     response.status_code = 204
#     return response


# send CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
