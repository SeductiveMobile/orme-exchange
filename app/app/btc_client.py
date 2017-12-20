import os
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


class BitcoinClient(object):
    """Bitcoin client class"""

    # Handler for Bitcoin connection
    connection = None

    network_info = None
    blockchain_info = None
    wallet_info = None

    def __init__(self):
        self.user = os.environ["BITCOIN_USER"]
        self.password = os.environ["BITCOIN_PASSWORD"]
        self.host = os.environ["BITCOIN_HOST"]
        self.port = int(os.environ["BITCOIN_PORT"])

        self.connection = AuthServiceProxy("http://%s:%s@%s:%i" % (self.user, self.password, self.host, self.port))

    def info(self):
        # Use following links for reference:
        # https://chainquery.com/bitcoin-api/getblockchaininfo
        # https://chainquery.com/bitcoin-api/getnetworkinfo
        # https://chainquery.com/bitcoin-api/getwalletinfo
        self.blockchain_info = self.connection.getblockchaininfo()
        self.network_info = self.connection.getnetworkinfo()
        self.wallet_info = self.connection.getwalletinfo()

        data_hash = {
            "blocks": int(self.blockchain_info["blocks"]),
            "headers": int(self.blockchain_info["headers"]),
            "bestblockhash": self.blockchain_info["bestblockhash"],
            "difficulty": float(self.blockchain_info["difficulty"]),
        }
        return data_hash

    def balance(self):
        return float(self.connection.getbalance())
