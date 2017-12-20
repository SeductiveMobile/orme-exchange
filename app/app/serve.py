# from eth_client import c
# from btc_client import BitcoinClient
from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # bc = BitcoinClient()
    # bitcoin_info = bc.info()
    #
    # ethereum_info = {
    #     "net_version": c.net_version(),
    #     "web3_client_version": c.web3_clientVersion(),
    #     "gas_price": c.eth_gasPrice(),
    #     "block_number": c.eth_blockNumber()
    # }
    #
    # resp = {"bitcoin": bitcoin_info, "ethereum": ethereum_info}
    # resp["bitcoin"]["balance"] = bc.balance()
    resp = {"bitcoin": "blah-blah", "ethereum": "blah-blah"}
    return jsonify(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
