#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '.'))

import orme.db
import orme.models


# Database Seed script
# Runs just after database migrations to seed initial data

def pricing_strategy_params():
    # We're taking contract address from a file
    # This file is always available since mapped through docker-compose
    json_path = os.path.abspath('PricingStrategy.json')
    fp = open(json_path, 'r')
    abi_string = fp.read().strip()
    fp.close()
    json_data = json.loads(abi_string)
    contract_abi = json_data['abi']
    networks = list(json_data['networks'].values())
    contract_address = networks[-1]['address']

    return {'address': contract_address, 'abi': json.dumps(contract_abi, sort_keys=True, indent=4, separators=(',', ': '))}


# Put ORV wallet to the database
orv_address = os.environ['BITCOIN_ORV_WALLET']
aquery = orme.db.session.query(orme.models.Address).filter(orme.models.Address.address == orv_address)
orv = aquery.one_or_none()
if orv is None:
    orv = orme.models.Address(
        address=orv_address,
        currency='bitcoin',
        wallet_type='orv',
        password=None,
        user=None
    )
    orme.db.session.add(orv)

# Adding/updating pricing strategy contract
ps_contract = pricing_strategy_params()
cquery = orme.db.session.query(orme.models.Contract).filter(orme.models.Contract.name == 'PricingStrategy')
contract = cquery.one_or_none()
if contract is None:
    contract = orme.models.Contract(
        name='PricingStrategy',
        address=ps_contract['address'],
        abi=ps_contract['abi'],
    )
    orme.db.session.add(contract)
else:
    contract.address = ps_contract['address']
    contract.abi = ps_contract['abi']

orme.db.session.commit()
