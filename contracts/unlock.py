import os
from web3 import Web3, HTTPProvider, IPCProvider

host = os.environ["RPC_HOST"]
port = int(os.environ["RPC_PORT"])
address = os.environ["DEPLOYER_ADDRESS"]
passphrase = os.environ["DEPLOYER_PASSPHRASE"]
duration = int(os.environ["UNLOCK_DURATION"])
network_name = os.environ["NETWORK_NAME"]

# We do not need unlocks on TESTRPC
if network_name != "testrpc":
    connection = Web3(HTTPProvider("http://%s:%i" % (host, port)))
    unlock = connection.personal.unlockAccount(address, passphrase, duration)
