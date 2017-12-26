#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.abspath(os.path.join('..', 'app')))

import app.db
import app.models


# Custom migration script
#
# Runs before database migrations
# May be used for setting up initial Bitcoin/Ethereum data, e.g. creating some wallets, etc