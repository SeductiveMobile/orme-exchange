import os
from web3 import Web3, HTTPProvider, IPCProvider


class EthereumClient(object):
    """Ethereum client class"""

    # Handler for Ethereum connection via Web3 HTTP
    connection = None

    info = None

    def __init__(self):
        self.host = os.environ["ETHEREUM_HOST"]
        self.port = int(os.environ["ETHEREUM_PORT"])

        self.connection = Web3(HTTPProvider("http://%s:%i" % (self.host, self.port)))

    def info(self):
        self.info = self.connection.eth

        # Use reference: https://github.com/ethereum/wiki/wiki/JavaScript-API
        data_hash = {
            "block_number": self.info.blockNumber,
            "gas_price": self.info.gasPrice,
            "accounts": self.info.accounts,
        }
        return data_hash
