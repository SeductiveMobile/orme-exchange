import os

import requests
from bitcoinrpc.authproxy import AuthServiceProxy

SATOSHI = 100000000


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

        # valid_bitcoin_address = '134dV6U7gQ6wCFbfHUz2CMh6Dth72oGpgH'
        # addr = Address(self, valid_bitcoin_address)

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
            # "valid_address_balance": addr.balance(),
        }
        return data_hash

    def balance(self):
        """Overall balance of current wallet

        Returns:
            (int) balance in satoshis

        """
        balance = float(self.connection.getbalance())
        # return balance
        return int(balance * SATOSHI)

    def new_address(self):
        """Generate new address"""
        return self.connection.getnewaddress()

    def get_private_key(self, address):
        """Fetch private key of specific address owned by you.

        Keyword arguments:
        address -- address (public key) to fetch from
        """
        return self.connection.dumpprivkey(address)

    def validate_address(self, address):
        """Check that address is valid on Blockchain.

        Keyword arguments:
        address -- address (public key) to validate
        """
        result = self.connection.validateaddress(address)
        if "isvalid" in result:
            return result["isvalid"]
        return False

    def new_account(self, name):
        """Generate new account and address.

        Keyword arguments:
        name -- name of the account, not stored in the blockchain
        """
        return self.connection.getnewaddress(name)

    def generate_blocks(self, amount):
        """Generate some blocks. Availabe only in Regtest mode.

        Keyword arguments:
        amount -- number of blocks to generate
        """
        return self.connection.generate(amount)

    def lock_wallet(self):
        """Lock current wallet."""
        return self.connection.walletlock()

    def unlock_wallet(self, passphrase=None, seconds=60):
        """Unlock current wallet with a passphase.

        Keyword arguments:
        passphrase -- the passphrase that unlocks the wallet
        seconds -- the number of seconds after which the decryption key will be automatically deleted from memory
        """
        if not passphrase:
            passphrase = os.environ["BITCOIN_WALLET_PASSPHRASE"]
        return self.connection.walletlock(passphrase, seconds)

    def change_wallet_passphrase(self, old_passphrase=None, new_passphrase=None):
        """Set passphrase for current wallet.

        Keyword arguments:
        old_passphrase -- old passphrase that unlocks the wallet
        new_passphrase -- new passphrase that unlocks the wallet
        """
        if not old_passphrase:
            old_passphrase = ''
        if not new_passphrase:
            new_passphrase = os.environ["BITCOIN_WALLET_PASSPHRASE"]
        return self.connection.walletpassphrasechange(old_passphrase, new_passphrase)

    def send(self, from_addr, to_addr, amount):
        """Send funds from address to address. Returns transaction ID.

        Keyword arguments:
        from_addr -- address (public key) we're sending funds from
        to_addr -- address (public key) we're sending funds to
        amount -- (float) amount of bitcoins to send
        """
        return self.connection.sendfrom(from_addr, to_addr, amount)


class Address(object):
    # BTC client handler
    client = None

    #  Public key AKA address
    public_key = None

    # Address private key
    private_key = None

    def __init__(self, client, address=None):
        """Address class constructor.

        Keyword arguments:
        client -- bitcoin client handler
        address -- (optional) actual address we're working on
        """
        self.public_key = address
        self.client = client

    def register(self):
        """Register new address in the blockchain and fetch its private key. Returns false if failed."""
        if self.public_key is None:
            self.public_key = self.client.new_address()
            self.private_key = self.client.get_private_key(self.public_key)
            return True
        return False

    def is_valid(self):
        """Returns validity of current address in the blockchain"""
        return self.client.validate_address(self.public_key)

    def __str__(self):
        return self.public_key

    def balance(self, method="blockexplorer"):
        """Check address balanace.

        Args:
            method (string): check method - internal "bitcoind" or "blockexplorer" for external blockexplorer API. Only blockexplorer is implemented for now.
        Returns:
            (int) balance in satoshis
        """

        if method == "blockexplorer":
            return self._blockexplorer_balance()
        if method == "bitcoind":
            return self._blockexplorer_balance()
        raise RuntimeError('Wrong balance check method')

    # TODO: Implement
    # Solution is https://bitcoin.org/en/developer-reference#importaddress
    # But it requires running full node
    def _bitcoind_balance(self):
        # Return result in satoshis
        raise ValueError('Not implemented yet')

    def _blockexplorer_balance(self):
        """Check address balance via https://blockexplorer.com"""
        endpoint = "https://blockexplorer.com/api/addr/%s" % self.public_key
        headers = {"Content-Type": 'application/json'}
        r = requests.get(endpoint, headers=headers)
        if 200 != r.status_code:
            error_message = "cannot fetch %s address data: %s" \
                            % (self.public_key, r.text)
            raise RuntimeError(error_message)

        address_data = r.json()

        # Balance in BTC, not used now
        # balance = float(address_data['balance'])

        # Return balance in satoshis, not BTC
        balance = int(address_data['balanceSat'])
        return balance

    def send(self, to_address, amount):
        """Send funds to specific address.

        Keyword arguments:
        to_addr -- address (public key) we're sending funds to
        amount -- (float) amount of bitcoins to send
        """
        if self.client.validate_address(to_address):
            pass
        else:
            raise ValueError("cannot transfer funds: address %s is invalid" % to_address)
        # TODO: Check if there are enough funds in current address
        self.client.unlock_wallet()
        self.client.send(self.public_key, to_address, amount)
        self.client.lock_wallet()

        raise ValueError('not implemented yet')
