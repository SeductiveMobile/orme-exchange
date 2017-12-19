import bitcoinrpc
conn = bitcoinrpc.connect_to_remote('myuser', 'mypassword', host='btcnode', port=18332)
# print "Your balance is %f" % (conn.getbalance(),)
info = conn.getinfo()
print("Blocks: %i" % info.blocks)
print("Connections: %i" % info.connections)
print("Difficulty: %f" % info.difficulty)