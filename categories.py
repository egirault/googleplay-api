#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

from config import *
from pprint import pprint
from googleplay import GooglePlayAPI
from google.protobuf import text_format
import sys
import urlparse

api = GooglePlayAPI()
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
response = api.browse()

print SEPARATOR.join(["ID", "Name"])
for c in response.category:
  print SEPARATOR.join(i.encode('utf8') for i in [urlparse.parse_qs(c.dataUrl)['cat'][0], c.name])


