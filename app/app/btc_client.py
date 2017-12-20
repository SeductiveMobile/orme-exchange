import bitcoinrpc
btc_conn = bitcoinrpc.connect_to_remote('myuser', 'mypassword', host='btcnode', port=18332)
# print "Your balance is %f" % (conn.getbalance(),)
btc_info = btc_conn.getinfo()
# print("Blocks: %i" % btc_info.blocks)
# print("Connections: %i" % btc_info.connections)
# print("Difficulty: %f" % btc_info.difficulty)