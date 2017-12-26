from __future__ import absolute_import, unicode_literals
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',)))

from orme.eth_client import EthereumClient
from orme.btc_client import BitcoinClient
from orme.services import UserService
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
    pass


@app.route('/api/users/<id>', methods=['GET'])
def show_user():
    pass


@app.route('/api/users', methods=['POST'])
def create_user():
    content = request.get_json(silent=True)
    if 'email' in content and 'password' in content:
        user = UserService.register_user(content['email'], content['password'])
        response = {
            'id': user.id,
            'email': user.email,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'addresses': [],
        }
        for address in user.addresses:
            addr = {
                'address': address.address,
                'balance': address.balance
            }
            response['addresses'].append(addr)
        return jsonify(response)
    else:
        errors = [{'user': 'cannot create user for unknown reason'}]
        response = jsonify(errors)
        response.status_code = 422
        return response


@app.route('/api/users/<id>', methods=['PUT'])
def update_user():
    pass


@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
