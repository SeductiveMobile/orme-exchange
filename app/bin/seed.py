#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.abspath(os.path.join('..', 'app')))

import app.db
import app.models


# Database Seed script
# Runs just after database migrations to seed initial data
