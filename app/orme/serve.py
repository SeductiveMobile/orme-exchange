from __future__ import absolute_import, unicode_literals
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', )))

from orme.eth_client import EthereumClient
from orme.btc_client import BitcoinClient
from orme.services import UserService
from orme.models import User, Address, UserSchema, AddressSchema
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


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
def list_users():
    srv = UserService()
    users = srv.find_all()
    schema = UserSchema(many=True)
    result = schema.dump(users)

    response = jsonify(result.data)
    response.status_code = 200
    return response


@app.route('/api/users/<id>', methods=['GET'])
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
def update_user(id):
    content = request.get_json(silent=True)
    if 'password' in content:
        srv = UserService(int(id))
        user = srv.update_password(content['password'])
        schema = UserSchema()
        result = schema.dump(user)

        response = jsonify(result.data)
        response.status_code = 200
        return response
    else:
        errors = [{'user': 'password for user update not provided'}]
        response = jsonify(errors)
        response.status_code = 422
        return response


@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    srv = UserService(int(id))
    result = srv.delete()

    response = jsonify({})
    response.status_code = 204
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
