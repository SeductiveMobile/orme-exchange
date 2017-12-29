#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '.'))

import orme.db
import orme.models
import orme.services

# Doing some test things
orv_address = os.environ['BITCOIN_ORV_WALLET']
serv = orme.services.ORVService(orv_address)
serv.sync()
