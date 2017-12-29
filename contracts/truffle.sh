#!/bin/sh
echo "Waiting Ethereum to start..."
while ! nc -z $ETHEREUM_RPC_HOST $ETHEREUM_RPC_PORT; do
  sleep 0.1
done

echo "Ethereum started, running truffle on network: development"
echo "Installing dependencies..."

truffle install zeppelin

echo "Unlocking account for tests"
/usr/bin/python3 unlock.py

# Test on private net
echo "Testing on network: development"
truffle test --network $ETHEREUM_NETWORK

# Deploy to private net
echo "Unlocking account for migrations"
/usr/bin/python3 unlock.py
echo "Deployment on network: development"
truffle migrate --network $ETHEREUM_NETWORK

# Truffle console on private net for tests
#truffle console --network development
