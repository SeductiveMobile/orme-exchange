#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '.'))

# Custom migration script
#
# Runs before database migrations
# May be used for setting up initial Bitcoin/Ethereum data, e.g. creating some wallets, etc

# Creating database if does not exist. Creating automatically on importing orme.db
import orme.db