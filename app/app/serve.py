from eth_client import EthereumClient
from btc_client import BitcoinClient
from services import UserService
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
        return jsonify(user)
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
