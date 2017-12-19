from eth_client import c
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    status = "<pre>"
    status += "Ethereum net version: %s\n" % c.net_version()
    status += "Ethereum web3 client version: %s\n" % c.web3_clientVersion()
    status += "Ethereum gas price: %s\n" % c.eth_gasPrice()
    status += "Ethereum block number: %s\n" % c.eth_blockNumber()
    status += "</pre>"

    return status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
