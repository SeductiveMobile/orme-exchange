# Business logic here
# Services should manipulate models
# Services should be called from controllers and tasks

import os

from .btc_client import Address as BTCAddress
from .db import session
from .models import Address
from .tasks import app


class ORVService(object):

    def __init__(self, address):
        """ORV Service constructor

        Args
            address (str): address (public key) to make operations on

        """
        self.address = address

    def sync(self):
        """Synchronize ORV address(wallet) on bitcoin blockchain with local database.
            Normally runs be scheduler.
            Step 1: Get wallet by address from database
            Step 2: Check wallet balance via bitcoin client
            Step 3: if balance changed - update it locally (otherwise just update updated_at field)
            Step 4: if balance changed - trigger appropriate smart contract via ETH client

        """
        addr = session.query(Address).filter_by(address=self.address).first()
        if addr:
            blockchain_address = BTCAddress(self.address)
            if not blockchain_address.is_valid():
                raise ValueError("bitcoin address %s is not valid in the blockchain" % self.address)

            balance = blockchain_address.balance()
            # TODO: Prpperly compare blockchain and database balance
            if balance != addr.balance:
                # TODO: trigger appropriate smart contract via ETH client
                pass

            addr.balance = balance
            session.commit()
        else:
            raise ValueError("bitcoin address %s not found in the database" % self.address)

    @classmethod
    def check_for_updates(cls):
        """Spawn synchronization of each ORV bitcoin wallet

            Runs periodically:
                Step 1: Get all ORV wallets from database
                Step 2: Spawn sync_orv() job for each wallet

        """
        query = session.query(Address).filter(Address.wallet_type == 'orv').order_by(Address.id)
        addresses = query.all()
        results = []
        for item in addresses:
            result = app.sync_orv_wallet(item.address)
            results.append(result)
        return results


class UserWalletsService(object):

    def __ini__(self, address):
        """User Wallets Service constructor

        Args
            address (str): address (public key) to make operations on

        """
        self.address = address

    @classmethod
    def check_for_updates(cls):
        """Spawn synchronization of each user bitcoin wallet

            Runs periodically:
                Step 1: Get all users bitcoin wallets
                Step 2: Spawn sync_user_bitcoins() job for each wallet

        """
        query = session.query(Address). \
            filter(Address.wallet_type == 'user'). \
            filter(Address.currency == 'bitcoin'). \
            order_by(Address.id)

        addresses = query.all()
        results = []
        for item in addresses:
            result = app.sync_user_wallet(item.address)
            results.append(result)
        return results


def sync(self):
    """Synchronize user address(wallet) on bitcoin blockchain with local database.
        Normally runs by scheduler.
        Step 1: Step 1: get wallet by address from database
        Step 2: Check wallet balance via bitcoin client
        Step 3: if balance > 0 - transfer all funds to ORV wallet
        Step 4: if balance > 0 - trigger appropriate smart contract via ETH client

    """
    addr = session.query(Address).filter_by(address=self.address).first()
    if addr:
        blockchain_address = BTCAddress(self.address)
        if not blockchain_address.is_valid():
            raise ValueError("bitcoin address %s is not valid in the blockchain" % self.address)

        balance = blockchain_address.balance()
        if balance > 0:
            to_address = os.environ['ORV_WALLET_ADDRESS']
            # Send all money to ORV wallet
            blockchain_address.send(to_address, balance)

            # TODO: trigger appropriate smart contract via ETH client

            # Update wallet status
            addr.balance = 0
            session.commit()
    else:
        raise ValueError("bitcoin address %s not found in the database" % self.address)
