#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

BANNER = """
Google Play Unofficial API Interactive Shell
Successfully logged in using your Google account. The variable 'api' holds the API object.
Feel free to use help(api).
"""

from googleplay import GooglePlayAPI
from google.protobuf import text_format
from config import *
from pprint import pprint
import sys
import urlparse
import code

api = GooglePlayAPI()
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
code.interact(BANNER, local=locals())
