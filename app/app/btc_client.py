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

        accounts = []
        for acc in self.connection.listaccounts(0):
            if len(acc) > 0:
                accounts.append(acc)

        # new_address = self.new_address()
        # new_address_valid = self.validate_address(new_address)
        # new_address_pk = self.get_private_key(new_address)

        # New address: "miC9oPat2xrtDstticmrw2YM7UUN9A6jcn"
        # New address private key: "cNci511KkyyU8GqMdZVxv1NxMbUMKqjo75PAQNdBFGgzbD7W8gZm"

        data_hash = {
            "blocks": int(self.blockchain_info["blocks"]),
            "headers": int(self.blockchain_info["headers"]),
            "bestblockhash": self.blockchain_info["bestblockhash"],
            "difficulty": float(self.blockchain_info["difficulty"]),
            "accounts": accounts,
            "account_addresses": self.connection.getaddressesbyaccount(""),
            # "new_address": str(self.new_account('Trololo')),
            # "new_address": new_address,
            # "new_address_valid": new_address_valid,
            # "new_address_pk": new_address_pk,
        }
        return data_hash

    def balance(self):
        return float(self.connection.getbalance())

    def new_address(self):
        """Generate new address"""
        return self.connection.getnewaddress()

    def get_private_key(self, address):
        """Fetch private key of specific address owned by you"""
        return self.connection.dumpprivkey(address)

    def validate_address(self, address):
        """Check that address is valid on Blockchain"""
        result = self.connection.validateaddress(address)
        if "isvalid" in result:
            return result["isvalid"]
        return False

    def new_account(self, name):
        """Generate new account and address"""
        return self.connection.getnewaddress(name)

    def generate_blocks(self, amount):
        """Generate some blocks. Availabe only in Regtest mode"""
        return self.connection.generate(amount)


class Address(object):
    # BTC client handler
    client = None

    #  Public key AKA address
    public_key = None

    # Address private key
    private_key = None

    def __init__(self, client, address=None):
        self.public_key = address
        self.client = client

    def register(self):
        if self.public_key is not None:
            self.public_key = self.client.new_address()
            self.private_key = self.client.get_private_key(self.public_key)
            return True
        return False

    def is_valid(self):
        return self.client.validate_address(self.public_key)

    def __str__(self):
        return self.public_key

    # TODO: Implement
    def balance(self):
        raise ValueError('Not implemented yet')
