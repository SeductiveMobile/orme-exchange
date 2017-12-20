import os
import bitcoinrpc

class BitcoinClient(object):
    """Bitcoin client class"""

    # Handler for Bitcoin connection
    connection = None

    # Bitcoin node info
    info = None

    def __init__(self):
        self.user = os.environ["BITCOIN_USER"]
        self.password = os.environ["BITCOIN_PASSWORD"]
        self.host = os.environ["BITCOIN_HOST"]
        self.port = int(os.environ["BITCOIN_PORT"])

        self.connection = bitcoinrpc.connect_to_remote(
            self.user,
            self.password,
            self.host,
            self.port
        )

    def info(self):
        self.info = self.connection.getinfo()
        data_hash = {
            "blocks": int(self.info.blocks),
            "connections": int(self.info.connections),
            "difficulty": float(self.info.difficulty),
        }
        return data_hash

    def balance(self):
        return float(self.connection.getbalance())