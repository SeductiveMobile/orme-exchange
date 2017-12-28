# Business logic here
# Services should manipulate models
# Services should be called from controllers and tasks

from __future__ import absolute_import, unicode_literals

import os
import random
import string

# from orme.celery import app
from celery import Celery
from orme.btc_client import Address as BTCAddress
from orme.btc_client import BitcoinClient
from orme.db import session
from orme.eth_client import Address as ETHAdress
from orme.eth_client import EthereumClient, PricingStrategyContract
from orme.models import Address, User

# from celery import Celery

broker = "redis://%s:%s/0" % (os.environ["REDIS_HOST"], os.environ["REDIS_PORT"])
# app = Celery('orme', broker=broker, include=['orme.services'])
app = Celery('orme', broker=broker)


@app.task
def check_orv_wallets():
    return ORVService.check_for_updates()


@app.task
def check_user_wallets():
    return UserWalletsService.check_for_updates()


@app.task
def sync_orv_wallet(address):
    service = ORVService(address)
    return service.sync()


@app.task
def sync_user_wallet(address):
    service = UserWalletsService(address)
    return service.sync()


@app.task
def say_hello_to(name):
    txt = "Hello, %s" % name
    print(txt)
    return txt


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """ Periodic tasks via Celery Beat
    See examples at http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html

    Args:
        sender: internally used param
        kwargs: not used
    Returns:
        None
    """
    # Calls check_orv_wallets() every 600 seconds.
    sender.add_periodic_task(600.0, check_orv_wallets.s(), name='Check ORV wallets every 10 minutes')

    # Calls check_user_wallets() every 600 seconds.
    sender.add_periodic_task(599.0, check_user_wallets.s(), name='Check User wallets every 10 minutes')


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
            bclient = BitcoinClient()
            blockchain_address = BTCAddress(bclient, self.address)
            if not blockchain_address.is_valid():
                raise ValueError("bitcoin address %s is not valid in the blockchain" % self.address)

            balance = blockchain_address.balance()
            if balance != addr.balance:
                eclient = EthereumClient()
                contract_address = os.environ['PRICING_STRATEGY_CONTRACT_ADDRESS']
                contract = PricingStrategyContract(eclient, contract_address)
                contract.set_available_satoshi(balance)

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
            result = sync_orv_wallet.delay(item.address)
            results.append(result)
        return results


class UserWalletsService(object):

    def __init__(self, address):
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
            result = sync_user_wallet.delay(item.address)
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
            bclient = BitcoinClient()
            blockchain_address = BTCAddress(bclient, self.address)
            if not blockchain_address.is_valid():
                raise ValueError("bitcoin address %s is not valid in the blockchain" % self.address)

            try:
                balance = blockchain_address.balance()
                if balance > 0:
                    to_address = os.environ['ORV_WALLET_ADDRESS']
                    # Send all money to ORV wallet
                    blockchain_address.send(to_address, balance)

                    # Step 1: get user of the address
                    # Step 2: get ethereum wallet of the user
                    # Step 3: Run contract transfer_to
                    user = addr.user
                    for user_address in user.addresses:
                        # Assuming user could have just one ethereum wallet
                        if user_address.currency == 'ethereum':
                            eclient = EthereumClient()
                            contract_address = os.environ['PRICING_STRATEGY_CONTRACT_ADDRESS']
                            contract = PricingStrategyContract(eclient, contract_address)
                            contract.transfer_to(user_address.address, balance)

                    # Update wallet status
                    addr.balance = 0
                    session.commit()
            except RuntimeError:
                # This issue should not happen in production,
                # just in dev/test where we create local accounts, but verify them on mainnet using blockexporer
                print("bitcoin address %s does not exist, doing nothing" % blockchain_address.public_key)
        else:
            raise ValueError("bitcoin address %s not found in the database" % self.address)


class UserService(object):
    def __init__(self, id=None):
        self.id = id

    @classmethod
    def create(cls, email, password):
        """Register user

        Args
            email (str): user email
            password (str): user password
        Returns
            User: created user model object
        Raises
            ValueError: if was not able to register bitcoin wallet for new user
        """
        user = User(
            email=email,
            password_hash=User.encode_password(password),
            # created_at=datetime.datetime.utcnow(),
            # updated_at=datetime.datetime.utcnow(),
        )
        session.add(user)

        # Create wallets for user

        # Create bitcoin wallet
        btc_client = BitcoinClient()
        btc_addr = BTCAddress(btc_client)
        if btc_addr.register():
            address = Address(
                address=btc_addr.public_key,
                currency='bitcoin',
                wallet_type='user',
                password=btc_addr.private_key,
                user=user
            )
            session.add(address)
        else:
            raise ValueError("cannot register bitcoin wallet for user %s" % email)

        # Create Ethereum Wallet
        eclient = EthereumClient()
        num_chars = 8
        random_passphrase = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num_chars))
        eth_addr = ETHAdress(eclient, passphrase=random_passphrase)
        if eth_addr.register():
            address = Address(
                address=eth_addr.address,
                currency='ethereum',
                wallet_type='user',
                password=eth_addr.passphrase,
                user=user
            )
            session.add(address)
        else:
            raise ValueError("cannot register ethereum wallet for user %s" % email)

        session.commit()
        return user

    @staticmethod
    def find_all():
        query = session.query(User)
        users = query.all()
        return users

    def find(self):
        user = session.query(User).get(self.id)
        return user

    # def find_by_email(self, email):
    #     pass

    def delete(self):
        user = session.query(User).get(self.id)
        session.delete(user)
        session.commit()

    def update_password(self, password):
        user = session.query(User).get(self.id)
        user.password_hash = User.encode_password(password)
        session.commit()
        return user


class SessionsService(object):
    def __init__(self):
        pass

    @staticmethod
    def email_login(email, password):
        query = session.query(User).filter(User.email == email)
        user = query.one_or_none()
        if not user:
            # Probably we could raise error here: e-mail not found
            return None
        hashed_password = User.encode_password(password)
        if hashed_password == user.password_hash:
            return user

        return None


if __name__ == '__main__':
    app.start()
