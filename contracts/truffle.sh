#!/bin/sh
echo "Waiting Ethereum to start..."
while ! nc -z $RPC_HOST $RPC_PORT; do
  sleep 0.1
done

echo "Ethereum started, running truffle"
truffle install zeppelin
truffle test
