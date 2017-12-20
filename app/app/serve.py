from eth_client import EthereumClient
from btc_client import BitcoinClient
from flask import Flask
from flask import jsonify

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
