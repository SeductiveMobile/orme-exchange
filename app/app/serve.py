from eth_client import c
from btc_client import btc_conn, btc_info
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    status = "<pre>"
    status += "Ethereum net version: %s\n" % c.net_version()
    status += "Ethereum web3 client version: %s\n" % c.web3_clientVersion()
    status += "Ethereum gas price: %s\n" % c.eth_gasPrice()
    status += "Ethereum block number: %s\n" % c.eth_blockNumber()
    status += "\n"
    status += "Bitcoin blocks: %s\n" % btc_info.blocks
    status += "Bitcoin connections: %s\n" % btc_info.connections
    status += "Bitcoin difficulty: %s\n" % btc_info.difficulty
    status += "Bitcoin ballance: %s\n" % btc_conn.getbalance()
    status += "</pre>"

    return status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
