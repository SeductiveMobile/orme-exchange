from ethjsonrpc import EthJsonRpc  # to use Parity-specific methods, import ParityEthJsonRpc
c = EthJsonRpc('ethnode', 8545)
# print("Ethereum net version: %s" % c.net_version())
# print("Ethereum web3 client version: %s" % c.web3_clientVersion())
# print("Ethereum gas price: %s" % c.eth_gasPrice())
# print("Ethereum block number: %s" % c.eth_blockNumber())



