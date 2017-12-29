#!/bin/sh
echo "Waiting Ethereum to start..."
while ! nc -z $RPC_HOST $RPC_PORT; do
  sleep 0.1
done

echo "Ethereum started, running truffle on network: development"
echo "Installing dependencies..."

truffle install zeppelin

echo "Unlocking account for tests"
/usr/bin/python3 unlock.py

# Test on private net
echo "Testing on network: development"
truffle test --network $NETWORK_NAME

# Deploy to private net
echo "Unlocking account for migrations"
/usr/bin/python3 unlock.py
echo "Deployment on network: development"
truffle migrate --network $NETWORK_NAME

# Truffle console on private net for tests
#truffle console --network development
