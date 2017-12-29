#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '.'))

import orme.db
import orme.models

# Database Seed script
# Runs just after database migrations to seed initial data

# Put ORV wallet to the database
orv_address = os.environ['BITCOIN_ORV_WALLET']

orv = orme.models.Address(
    address=orv_address,
    currency='bitcoin',
    wallet_type='orv',
    password=None,
    user=None
)
orme.db.session.add(orv)
orme.db.session.commit()
