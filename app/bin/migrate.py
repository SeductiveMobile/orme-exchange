#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.abspath(os.path.join('..', 'app')))

import app.db
import app.models

# Custom migration script
#
# Steps to do withing migrate script
# 1. Create SQL database if not exist;
# 2. Migrate SQL database;
# 3. Seed initial data in Ethereum and Bitcoin nodes;
# 4. Seed initial data in SQL database;