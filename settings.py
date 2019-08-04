# -*- coding: utf-8 -*-
import os

API_HOST = os.environ.get('API_HOST', 'localhost')
API_PORT = int(os.environ.get('API_PORT', 8080))
API_URL = '/api/'
