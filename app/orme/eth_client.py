import os

from web3 import Web3, HTTPProvider


class EthereumClient(object):
    """Ethereum client class"""

    # Handler for Ethereum connection via Web3 HTTP
    connection = None

    info = None

    def __init__(self, network='geth'):
        self.network = network
        if network == 'geth':
            self.host = os.environ["ETHEREUM_HOST"]
            self.port = int(os.environ["ETHEREUM_PORT"])
        if network == 'testrpc':
            self.host = os.environ["ETHEREUM_TESTRPC_HOST"]
            self.port = int(os.environ["ETHEREUM_TESTRPC_PORT"])

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

        last_block = self.get_block('latest')
        gas_limit = last_block.gasLimit

        data_hash = {
            "block_number": self.info.blockNumber,
            "gas_price": self.info.gasPrice,
            "addresses": self.info.accounts,
            "total_balance": total_balance,
            "gas_limit": gas_limit,
            # "last_address_balance": self.address_balance(self.info.accounts[-1])
            # "newly_created_address": addr.address,
            # "rinkeby_balance": self.address_balance('0xd9fea4ca882344050f4c6d64bc74a973087a5947')
        }

        return data_hash

    def new_address(self, passphrase):
        """Generate new Ethereum address with specified password and return the address

        Args:
            passphrase (str): passphrase to be used for new address (account)

        Returns:
            Address (public key) string

        """
        return self.connection.personal.newAccount(passphrase)

    def lock_address(self, address):
        """Lock specific address

        Args:
            address (str): address public key

        """
        return self.connection.personal.lockAccount(address)

    def unlock_address(self, address, passphrase, duration=60):
        """Unlock specific address with passphrase for number of seconds. Returns boolean.

        Args:
            address (str): address public key
            passphrase (str): address unlock passphrase
            duration (Optional[int]) unlock duration in seconds, default is 60

        """
        # TODO: remove this hack when we'll stop using testrpc
        if self.network == 'testrpc':
            return True

        return self.connection.personal.unlockAccount(address, passphrase, duration)

    def fetch_contract(self, abi, address):
        return self.connection.eth.contract(abi=abi, address=address)

    def address_balance(self, address):
        """Check balance fore specific address

        Args:
            address (str): address public key
        Returns:
            balance (int) in Wei

        """
        balance = self.connection.eth.getBalance(address)
        return balance

    def get_block(self, block_number='latest'):
        """Get block data

        Args:
            block_number (Optional[int]): block number, uses latest if not specified

        """
        return self.connection.eth.getBlock(block_number)

    def send(self, from_addr, to_addr, amount):
        """Send funds from one address to another

        Args:
            from_addr: sender address
            to_addr: receiver address
            amount: amount to send (in Wei)

        Returns:
            transaction id

        """
        tx = {
            'to': to_addr,
            'from': from_addr,
            'value': amount
        }
        return self.connection.eth.sendTransaction(tx)

    def seed(self, amount=10000000000000000000):
        """Seed initial data. Note, this method is used only for development purposes and won't work in production.

        Args:
            amount: amount to send (in Wei)

        Returns:
            transaction id

        """

        # Send initial funds from coinbase to last address
        from_addr = self.info.accounts[0]
        to_addr = self.info.accounts[-1]
        self.unlock_address(from_addr, "")
        tx = self.send(from_addr, to_addr, amount)
        return tx


class Address(object):
    # ETH client handler
    client = None

    # Public key AKA address
    address = None

    # Address passphrase for signing
    passphrase = None

    def __init__(self, client, address=None, passphrase=None):
        """Address class constructor.

        Args:
            client (EthereumClient): ethereum client handler
            address (Optional[str]): actual address we're working on

        """
        self.address = address
        self.client = client
        self.passphrase = passphrase

    def register(self):
        """Register new address in the blockchain and fetch its private key. Returns false if failed.

        Returns:
            The return value. True for success, False otherwise.

        """
        if self.address is None and self.passphrase is not None:
            self.address = self.client.new_address(self.passphrase)
            return True
        return False


class Contract(object):
    """Ethereum Smart Contract representation class

        It is assumed you'll subclass this class for each of your contracts
        and implement appropriate .transact(), .call(), .estimateGas() methods there.
        See http://web3py.readthedocs.io/en/stable/contracts.html for details

    """

    client = None

    # Public key AKA address
    address = None

    # Contract handler
    # See http://web3py.readthedocs.io/en/stable/contracts.html for handler methods
    handler = None

    def __init__(self, client, abi, address):
        """Contract class constructor.

        Args:
            client (EthereumClient): ethereum client handler
            abi (str): serialized json code of the contract
            address (str): contract actual address we're working on

        """
        self.abi = abi
        self.address = address
        self.client = client
        self.handler = self._contract_handler()

    def _contract_handler(self):
        return self.client.fetch_contract(self.abi, self.address)


class PricingStrategyContract(Contract):
    """Programmatic representation of pricing strategy contract"""

    def __init__(self, client, abi, address):
        super().__init__(client, abi, address)

    def set_available_satoshi(self, amount, from_address=None):
        """Pass ORME wallet balace (in satoshis)

        Args:
            amount (int): balance in satoshis
            from_address (string): address of contract executor, web3.eth.defaultAccount would be used if not set

        Returns:
            transaction ID or None
        """

        if not from_address:
            result = self.handler.transact().setAvailableSatoshi(amount)
        else:
            result = self.handler.transact({'from': from_address}).setAvailableSatoshi(amount)

        return result

    def transfer_to(self, address, amount, from_address=None):
        """Transfer amount of ORME tokens to buyer

        Args:
            address (string) - buyer address
            amount (int) - amount (in Satoshi)
            from_address (string): address of contract executor, web3.eth.defaultAccount would be used if not set

        Returns:
            transaction ID or None
        """
        if not from_address:
            result = self.handler.transact().transferTo(address, amount)
        else:
            result = self.handler.transact({'from': from_address}).transferTo(address, amount)
        return result

    def set_available_orme_in_gwei(self, amount, from_address=None):
        """Set available ORME (in gwei)
        This method is temporal and would be later removed in favor of launching directly from within smart contracts

        Args:
            amount (int) - amount (in GWei)
            from_address (string): address of contract executor, web3.eth.defaultAccount would be used if not set

        Returns:
            transaction ID or None
        """
        if not from_address:
            result = self.handler.transact().setAvailableORMEInGwei(amount)
        else:
            result = self.handler.transact({'from': from_address}).setAvailableORMEInGwei(amount)

        return result
