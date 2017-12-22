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

        # New address is "0x1ebd93ff2fc90b873a68e16b931a7c66e2237e31"
        # addr = Address(client=self, passphrase="nopassphrase")
        # result = addr.register()
        # Address on testnet: '0xd9fea4ca882344050f4c6d64bc74a973087a5947'

        # Use reference: https://github.com/ethereum/wiki/wiki/JavaScript-API
        total_balance = 0
        for acc in self.info.accounts:
            total_balance += self.address_balance(acc)

        data_hash = {
            "block_number": self.info.blockNumber,
            "gas_price": self.info.gasPrice,
            "addresses": self.info.accounts,
            "total_balance": total_balance,
            # "last_address_balance": self.address_balance(self.info.accounts[-1])
            # "newly_created_address": addr.address,
            # "rinkeby_balance": self.address_balance('0xd9fea4ca882344050f4c6d64bc74a973087a5947')
        }
        return data_hash

    def new_address(self, passphrase):
        """Generate new Ethereum address with specified password and return the address

        Keyword arguments:
        passphrase -- passphrase to be used for new address (account)
        """
        return self.connection.personal.newAccount(passphrase)

    def lock_address(self, address):
        """Lock specific address

        Keyword arguments:
        address -- address public key
        """
        return self.connection.personal.lockAccount(address)

    def unlock_address(self, address, passphrase, duration=60):
        """Unlock specific address with passphrase for number of seconds. Returns boolean.

        Keyword arguments:
        address -- address public key
        passphrase -- address unlock passphrase
        duration -- unlock duration in seconds, default is 60
        """
        return self.connection.personal.unlockAccount(address, passphrase, duration)

    def fetch_contract(self, address):
        return self.connection.eth.contract(address=address)

    def address_balance(self, address):
        """Check balance fore specific address

        Keyword arguments:
        address -- address public key
        """
        return self.connection.eth.getBalance(address)


class Address(object):
    # ETH client handler
    client = None

    # Public key AKA address
    address = None

    # Address passphrase for signing
    passphrase = None

    def __init__(self, client, address=None, passphrase=None):
        """Address class constructor.

        Keyword arguments:
        client -- ethereum client handler
        address -- (optional) actual address we're working on
        """
        self.address = address
        self.client = client
        self.passphrase = passphrase

    def register(self):
        """Register new address in the blockchain and fetch its private key. Returns false if failed."""
        if self.address is None and self.passphrase is not None:
            self.address = self.client.new_address(self.passphrase)
            return True
        return False

class Contract(object):

    client = None

    # Public key AKA address
    address = None

    # Contract handler
    # See http://web3py.readthedocs.io/en/stable/contracts.html for handler methods
    handler = None

    def __init__(self, client, address):
        """Contract class constructor.

        Keyword arguments:
        client -- ethereum client handler
        address -- contract actual address we're working on
        """
        self.address = address
        self.client = client
        self.handler = self.__contract_handler()

    def __contract_handler(self):
        return self.client.fetch_contract(self.address)